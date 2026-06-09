"""
Echo-Sync speech-to-text base class.

Defines the abstract interface that all STT providers must implement.
"""

import abc
from pathlib import Path


class STTBase(abc.ABC):
    """
    Abstract base class for speech-to-text providers.

    All STT implementations (OpenAI, offline/Vosk, etc.) must
    implement this interface for consistent usage in the app.
    """

    @abc.abstractmethod
    def transcribe(self, audio_path: Path) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the WAV audio file.

        Returns:
            The transcribed text string.
            Returns empty string if transcription fails.
        """
        ...

    @abc.abstractmethod
    def is_available(self) -> bool:
        """
        Check if this STT provider is available and configured.

        Returns:
            True if the provider is ready to transcribe.
        """
        ...
