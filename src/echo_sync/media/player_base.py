"""
Echo-Sync media player base class.

Defines the abstract interface that all player backends must implement.
"""

import abc
from pathlib import Path


class PlayerBase(abc.ABC):
    """
    Abstract base class for media player backends.

    All player implementations (VLC, Pygame) must implement
    this interface for consistent usage in the app.
    """

    @abc.abstractmethod
    def play(self, file_path: Path) -> bool:
        """
        Start playing an audio file.

        Args:
            file_path: Path to the audio file.

        Returns:
            True if playback started successfully.
        """
        ...

    @abc.abstractmethod
    def pause(self) -> None:
        """Pause the current playback."""
        ...

    @abc.abstractmethod
    def resume(self) -> None:
        """Resume paused playback."""
        ...

    @abc.abstractmethod
    def stop(self) -> None:
        """Stop playback completely."""
        ...

    @abc.abstractmethod
    def next_track(self) -> bool:
        """
        Skip to the next track in the playlist.

        Returns:
            True if there is a next track and it started playing.
        """
        ...

    @abc.abstractmethod
    def previous_track(self) -> bool:
        """
        Go back to the previous track.

        Returns:
            True if there is a previous track and it started playing.
        """
        ...

    @abc.abstractmethod
    def set_volume(self, volume: int) -> None:
        """
        Set the playback volume.

        Args:
            volume: Volume level 0-100.
        """
        ...

    @abc.abstractmethod
    def get_volume(self) -> int:
        """
        Get the current volume level.

        Returns:
            Current volume 0-100.
        """
        ...

    @abc.abstractmethod
    def is_playing(self) -> bool:
        """Check if audio is currently playing."""
        ...

    @abc.abstractmethod
    def get_current_track(self) -> str:
        """Get the name of the currently playing track."""
        ...

    def volume_up(self, step: int = 10) -> int:
        """Increase volume by step. Returns new volume."""
        new_vol = min(100, self.get_volume() + step)
        self.set_volume(new_vol)
        return new_vol

    def volume_down(self, step: int = 10) -> int:
        """Decrease volume by step. Returns new volume."""
        new_vol = max(0, self.get_volume() - step)
        self.set_volume(new_vol)
        return new_vol
