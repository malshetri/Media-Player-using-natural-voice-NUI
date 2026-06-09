"""
Echo-Sync OpenAI speech-to-text provider.

Uses the OpenAI Transcription API for accurate speech recognition.
"""

import logging
from pathlib import Path

from openai import OpenAI

from echo_sync.config.settings import Settings
from echo_sync.speech.stt_base import STTBase

logger = logging.getLogger(__name__)


class OpenAISTT(STTBase):
    """
    OpenAI-powered speech-to-text transcription.

    Uses the OpenAI API with the configured transcription model
    for accurate, cloud-based speech recognition.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.stt_model

    def transcribe(self, audio_path: Path) -> str:
        """
        Transcribe an audio file using the OpenAI API.

        Args:
            audio_path: Path to the WAV audio file.

        Returns:
            Transcribed text string. Empty string on failure.
        """
        try:
            logger.info("Transcribing with OpenAI: %s", audio_path)

            with open(audio_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language="en",
                )

            transcript = response.text.strip()
            logger.info("Transcription result: '%s'", transcript)
            return transcript

        except Exception as e:
            logger.error("OpenAI transcription failed: %s", e)
            return ""

    def is_available(self) -> bool:
        """Check if the OpenAI API key is configured."""
        return (
            self.settings.openai_api_key != "your_api_key_here"
            and len(self.settings.openai_api_key) > 10
        )
