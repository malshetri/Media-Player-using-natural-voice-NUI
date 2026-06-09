"""
Echo-Sync Pygame media player backend.

Fallback player using pygame.mixer when VLC is not available.
Supports basic playback, volume control, and playlist management.
"""

import logging
from pathlib import Path
from typing import Optional

from echo_sync.media.player_base import PlayerBase

logger = logging.getLogger(__name__)


class PygamePlayer(PlayerBase):
    """
    Pygame-based media player fallback.

    Uses pygame.mixer for audio playback. Less format support than VLC
    but works without external dependencies.
    """

    def __init__(self, default_volume: int = 80) -> None:
        self._volume = default_volume
        self._current_track: str = ""
        self._playlist: list[Path] = []
        self._playlist_index: int = -1
        self._initialized = False
        self._paused = False

        self._init_pygame()

    def _init_pygame(self) -> None:
        """Initialize pygame mixer."""
        try:
            import pygame

            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
            pygame.mixer.music.set_volume(self._volume / 100.0)
            self._initialized = True
            logger.info("Pygame mixer initialized")
        except (ImportError, Exception) as e:
            logger.error("Failed to initialize pygame mixer: %s", e)

    def load_playlist(self, tracks: list[Path]) -> None:
        """Load a list of tracks as the current playlist."""
        self._playlist = tracks
        self._playlist_index = -1
        logger.info("Loaded playlist with %d tracks", len(tracks))

    def play(self, file_path: Optional[Path] = None) -> bool:
        """Start playing an audio file or from playlist."""
        if not self._initialized:
            logger.error("Pygame mixer not initialized")
            return False

        try:
            import pygame

            if file_path is not None:
                target = file_path
                self._current_track = file_path.stem
            elif self._playlist:
                self._playlist_index = 0
                target = self._playlist[self._playlist_index]
                self._current_track = target.stem
            else:
                logger.warning("No file or playlist to play")
                return False

            pygame.mixer.music.load(str(target))
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self._volume / 100.0)
            self._paused = False
            logger.info("Playing: %s", self._current_track)
            return True

        except Exception as e:
            logger.error("Failed to play: %s", e)
            return False

    def pause(self) -> None:
        """Pause the current playback."""
        if self._initialized:
            import pygame

            pygame.mixer.music.pause()
            self._paused = True
            logger.info("Paused")

    def resume(self) -> None:
        """Resume paused playback."""
        if self._initialized:
            import pygame

            pygame.mixer.music.unpause()
            self._paused = False
            logger.info("Resumed")

    def stop(self) -> None:
        """Stop playback completely."""
        if self._initialized:
            import pygame

            pygame.mixer.music.stop()
            self._current_track = ""
            self._paused = False
            logger.info("Stopped")

    def next_track(self) -> bool:
        """Skip to the next track in the playlist."""
        if not self._playlist:
            return False

        self._playlist_index += 1
        if self._playlist_index >= len(self._playlist):
            self._playlist_index = 0

        return self.play(self._playlist[self._playlist_index])

    def previous_track(self) -> bool:
        """Go back to the previous track."""
        if not self._playlist:
            return False

        self._playlist_index -= 1
        if self._playlist_index < 0:
            self._playlist_index = len(self._playlist) - 1

        return self.play(self._playlist[self._playlist_index])

    def set_volume(self, volume: int) -> None:
        """Set the playback volume (0-100)."""
        self._volume = max(0, min(100, volume))
        if self._initialized:
            import pygame

            pygame.mixer.music.set_volume(self._volume / 100.0)
            logger.debug("Volume set to %d%%", self._volume)

    def get_volume(self) -> int:
        """Get the current volume level."""
        return self._volume

    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        if self._initialized:
            import pygame

            return pygame.mixer.music.get_busy() and not self._paused
        return False

    def get_current_track(self) -> str:
        """Get the name of the currently playing track."""
        return self._current_track

    def cleanup(self) -> None:
        """Release pygame resources."""
        if self._initialized:
            import pygame

            pygame.mixer.quit()
            logger.info("Pygame mixer cleaned up")
