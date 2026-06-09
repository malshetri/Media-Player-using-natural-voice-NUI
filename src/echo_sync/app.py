"""
Echo-Sync main application loop.

Orchestrates the complete interaction cycle:
earcon → record → transcribe → classify → execute → log → repeat.

Supports two modes:
- Voice mode: uses microphone for speech input
- Keyboard demo mode: uses typed input (--demo-keyboard flag)
"""

import logging
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from echo_sync.ai.context_mapper import ContextMapper
from echo_sync.ai.intent_classifier import IntentClassifier
from echo_sync.audio.ducking import SmartDucker
from echo_sync.audio.earcons import EarconManager
from echo_sync.audio.recorder import MicrophoneRecorder
from echo_sync.config.prompts import WELCOME_MESSAGE, GOODBYE_MESSAGE
from echo_sync.config.settings import Settings
from echo_sync.interaction.dialog_manager import DialogManager
from echo_sync.interaction.state_machine import AppState, StateMachine
from echo_sync.logging_utils.interaction_logger import InteractionLogger
from echo_sync.media.playlist_manager import PlaylistManager
from echo_sync.media.player_base import PlayerBase
from echo_sync.speech.stt_base import STTBase

logger = logging.getLogger(__name__)
console = Console()


class EchoSyncApp:
    """
    Main Echo-Sync application.

    Manages the interaction loop and coordinates all components.
    """

    def __init__(
        self,
        settings: Settings,
        demo_keyboard: bool = False,
    ) -> None:
        self.settings = settings
        self.demo_keyboard = demo_keyboard
        self.state_machine = StateMachine()
        self.running = False

        # ── Initialize components ───────────────────────────────────
        console.print("[dim]Initializing Echo-Sync...[/dim]")

        # Media player
        self.player = self._create_player(settings)
        self.playlist_manager = PlaylistManager(settings.music_path)

        # Audio
        self.earcons = EarconManager(settings)
        self.ducker = SmartDucker(
            ducking_volume=settings.ducking_volume,
        )
        self.ducker.attach_player(self.player)

        if not demo_keyboard:
            self.recorder = MicrophoneRecorder()
        else:
            self.recorder = None

        # Speech-to-text
        self.stt = self._create_stt(settings)

        # AI
        self.classifier = IntentClassifier(settings)
        self.context_mapper = ContextMapper(settings)

        # Interaction
        self.dialog_manager = DialogManager(
            settings=settings,
            player=self.player,
            playlist_manager=self.playlist_manager,
            context_mapper=self.context_mapper,
            earcon_manager=self.earcons,
            ducker=self.ducker,
        )

        # Logging
        self.interaction_logger = InteractionLogger(settings)

        console.print("[green]✓ Echo-Sync initialized[/green]")

    @staticmethod
    def _create_player(settings: Settings) -> PlayerBase:
        """Create the appropriate media player based on settings."""
        if settings.player == "vlc":
            try:
                from echo_sync.media.vlc_player import VLCPlayer
                return VLCPlayer(default_volume=settings.default_volume)
            except Exception as e:
                logger.warning("VLC player failed, trying pygame: %s", e)

        from echo_sync.media.pygame_player import PygamePlayer
        return PygamePlayer(default_volume=settings.default_volume)

    @staticmethod
    def _create_stt(settings: Settings) -> STTBase:
        """Create the appropriate STT provider based on settings."""
        if settings.stt_mode == "openai":
            from echo_sync.speech.openai_stt import OpenAISTT
            stt = OpenAISTT(settings)
            if stt.is_available():
                return stt
            logger.warning("OpenAI STT not available, trying offline")

        from echo_sync.speech.offline_stt import OfflineSTT
        return OfflineSTT()

    def run(self) -> None:
        """Start the main interaction loop."""
        self.running = True
        self.interaction_logger.log_system_event("System started")

        # Welcome the user
        console.print()
        console.print(
            Panel(
                Text(WELCOME_MESSAGE, style="bold cyan"),
                title="🎵 Echo-Sync",
                border_style="cyan",
            )
        )
        console.print()

        self.earcons.play_listening()

        try:
            while self.running:
                self._interaction_cycle()
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
        finally:
            self._shutdown()

    def _interaction_cycle(self) -> None:
        """Execute one full interaction cycle."""
        # ── Step 1: Get user input ──────────────────────────────────
        self.state_machine.transition(AppState.LISTENING)

        if self.demo_keyboard:
            transcript = self._get_keyboard_input()
        else:
            transcript = self._get_voice_input()

        if transcript is None:
            # User wants to quit
            self.running = False
            return

        # ── Step 2: Handle empty input (silence) ───────────────────
        if not transcript.strip():
            self.state_machine.transition(AppState.HELPING)
            response = self.dialog_manager.handle_silence()
            self._respond(response)
            self.interaction_logger.log_interaction(
                transcript="[silence]",
                system_response=response,
                notes="silence_timeout",
            )
            return

        # ── Step 3: Classify intent ─────────────────────────────────
        self.state_machine.transition(AppState.PROCESSING)
        self.ducker.duck()

        console.print(f"[dim]You said: \"{transcript}\"[/dim]")

        intent = self.classifier.classify(transcript)

        # ── Step 4: Execute action ──────────────────────────────────
        self.state_machine.transition(AppState.EXECUTING)
        response = self.dialog_manager.handle_intent(intent)

        # ── Step 5: Respond to user ─────────────────────────────────
        self._respond(response)

        # ── Step 6: Unduck and log ──────────────────────────────────
        self.ducker.unduck()

        self.interaction_logger.log_interaction(
            transcript=transcript,
            intent_result=intent,
            system_response=response,
        )

        # Update state based on result
        if intent.is_music_command() or intent.needs_playlist():
            self.state_machine.force_state(AppState.PLAYING)
        else:
            self.state_machine.force_state(AppState.IDLE)

    def _get_keyboard_input(self) -> str | None:
        """Get input from keyboard (demo mode)."""
        try:
            console.print()
            user_input = console.input(
                "[bold green]🎤 You:[/bold green] "
            ).strip()

            if user_input.lower() in ("quit", "exit", "q"):
                return None

            return user_input

        except EOFError:
            return None

    def _get_voice_input(self) -> str | None:
        """Get input from microphone."""
        if self.recorder is None:
            return self._get_keyboard_input()

        self.earcons.play_listening()
        console.print("[dim]🎤 Listening...[/dim]")

        audio_path = self.recorder.record()
        if audio_path is None:
            return ""

        # Transcribe
        transcript = self.stt.transcribe(audio_path)

        # Clean up temp file
        try:
            audio_path.unlink(missing_ok=True)
        except Exception:
            pass

        return transcript

    def _respond(self, text: str) -> None:
        """Output the system response."""
        console.print(
            Panel(
                Text(text, style="bold white"),
                title="🔊 Echo-Sync",
                border_style="blue",
            )
        )

    def _shutdown(self) -> None:
        """Clean shutdown of all components."""
        self.state_machine.force_state(AppState.SHUTTING_DOWN)
        self.running = False

        console.print()
        console.print(f"[cyan]{GOODBYE_MESSAGE}[/cyan]")

        # Clean up player
        if hasattr(self.player, "cleanup"):
            self.player.cleanup()

        self.interaction_logger.log_system_event("System shutdown")
        logger.info("Echo-Sync shut down cleanly")
