"""
Echo-Sync offline speech-to-text fallback.

Provides a stub for offline STT (Vosk/faster-whisper) that can be
used when internet/API is unavailable during a demo.

This is a placeholder — install faster-whisper or vosk to enable.
"""

import logging
from pathlib import Path

from echo_sync.speech.stt_base import STTBase

logger = logging.getLogger(__name__)


class OfflineSTT(STTBase):
    """
    Offline speech-to-text fallback.

    Uses faster-whisper if available, otherwise returns empty results.
    Useful as a fallback when the OpenAI API is unavailable.
    """

    def __init__(self) -> None:
        self._model = None
        self._available = False
        self._try_load()

    def _try_load(self) -> None:
        """Attempt to load the offline STT model."""
        try:
            from faster_whisper import WhisperModel

            logger.info("Loading offline whisper model (tiny)...")
            self._model = WhisperModel("tiny", device="cpu", compute_type="int8")
            self._available = True
            logger.info("Offline STT model loaded successfully")
        except ImportError:
            logger.info(
                "faster-whisper not installed — offline STT unavailable. "
                "Install with: pip install faster-whisper"
            )
        except Exception as e:
            logger.warning("Failed to load offline STT model: %s", e)

    def transcribe(self, audio_path: Path) -> str:
        """
        Transcribe audio using the offline model.

        Args:
            audio_path: Path to the WAV audio file.

        Returns:
            Transcribed text. Empty string if unavailable or fails.
        """
        if not self._available or self._model is None:
            logger.warning("Offline STT not available")
            return ""

        try:
            segments, info = self._model.transcribe(
                str(audio_path),
                language="en",
                beam_size=5,
            )
            text = " ".join(segment.text.strip() for segment in segments)
            logger.info("Offline transcription: '%s'", text)
            return text.strip()

        except Exception as e:
            logger.error("Offline transcription failed: %s", e)
            return ""

    def is_available(self) -> bool:
        """Check if the offline model is loaded."""
        return self._available
