"""
Echo-Sync VLC media player backend.

Uses python-vlc to control audio playback. VLC is preferred because
it handles many audio formats reliably (MP3, FLAC, WAV, OGG, etc.).
"""

import logging
from pathlib import Path
from typing import Optional

from echo_sync.media.player_base import PlayerBase

logger = logging.getLogger(__name__)


class VLCPlayer(PlayerBase):
    """
    VLC-based media player.

    Requires VLC media player to be installed on the system.
    Uses python-vlc bindings for control.
    """

    def __init__(self, default_volume: int = 80) -> None:
        self._vlc = None
        self._instance = None
        self._player = None
        self._media_list = None
        self._list_player = None
        self._volume = default_volume
        self._current_track: str = ""
        self._playlist: list[Path] = []
        self._playlist_index: int = -1

        self._init_vlc()

    def _init_vlc(self) -> None:
        """Initialize VLC instance and player."""
        try:
            import vlc

            self._vlc = vlc
            self._instance = vlc.Instance("--no-xlib", "--quiet")
            self._player = self._instance.media_player_new()
            self._player.audio_set_volume(self._volume)
            logger.info("VLC player initialized")
        except (ImportError, Exception) as e:
            logger.error(
                "Failed to initialize VLC: %s. "
                "Make sure VLC is installed on your system.",
                e,
            )

    def load_playlist(self, tracks: list[Path]) -> None:
        """
        Load a list of tracks as the current playlist.

        Args:
            tracks: List of paths to audio files.
        """
        self._playlist = tracks
        self._playlist_index = -1
        logger.info("Loaded playlist with %d tracks", len(tracks))

    def play(self, file_path: Optional[Path] = None) -> bool:
        """
        Start playing an audio file or the first track in the playlist.

        Args:
            file_path: Path to audio file. If None, plays from playlist.

        Returns:
            True if playback started successfully.
        """
        if self._player is None:
            logger.error("VLC player not initialized")
            return False

        try:
            if file_path is not None:
                media = self._instance.media_new(str(file_path))
                self._player.set_media(media)
                self._current_track = file_path.stem
            elif self._playlist:
                self._playlist_index = 0
                media = self._instance.media_new(
                    str(self._playlist[self._playlist_index])
                )
                self._player.set_media(media)
                self._current_track = self._playlist[
                    self._playlist_index
                ].stem
            else:
                logger.warning("No file or playlist to play")
                return False

            self._player.play()
            self._player.audio_set_volume(self._volume)
            logger.info("Playing: %s", self._current_track)
            return True

        except Exception as e:
            logger.error("Failed to play: %s", e)
            return False

    def pause(self) -> None:
        """Pause the current playback."""
        if self._player and self._player.is_playing():
            self._player.pause()
            logger.info("Paused")

    def resume(self) -> None:
        """Resume paused playback."""
        if self._player:
            self._player.play()
            logger.info("Resumed")

    def stop(self) -> None:
        """Stop playback completely."""
        if self._player:
            self._player.stop()
            self._current_track = ""
            logger.info("Stopped")

    def next_track(self) -> bool:
        """Skip to the next track in the playlist."""
        if not self._playlist:
            logger.warning("No playlist loaded")
            return False

        self._playlist_index += 1
        if self._playlist_index >= len(self._playlist):
            self._playlist_index = 0  # Loop to start

        return self.play(self._playlist[self._playlist_index])

    def previous_track(self) -> bool:
        """Go back to the previous track."""
        if not self._playlist:
            logger.warning("No playlist loaded")
            return False

        self._playlist_index -= 1
        if self._playlist_index < 0:
            self._playlist_index = len(self._playlist) - 1  # Loop to end

        return self.play(self._playlist[self._playlist_index])

    def set_volume(self, volume: int) -> None:
        """Set the playback volume (0-100)."""
        self._volume = max(0, min(100, volume))
        if self._player:
            self._player.audio_set_volume(self._volume)
            logger.debug("Volume set to %d%%", self._volume)

    def get_volume(self) -> int:
        """Get the current volume level."""
        return self._volume

    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        if self._player:
            return bool(self._player.is_playing())
        return False

    def get_current_track(self) -> str:
        """Get the name of the currently playing track."""
        return self._current_track

    def cleanup(self) -> None:
        """Release VLC resources."""
        if self._player:
            self._player.stop()
            self._player.release()
        if self._instance:
            self._instance.release()
        logger.info("VLC player cleaned up")
