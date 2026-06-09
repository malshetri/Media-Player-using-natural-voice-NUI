"""
Echo-Sync AI intent classifier.

Calls the OpenAI API with the system prompt and forces structured JSON
output matching the IntentResult schema. Includes rule-based fast-path
for common direct commands before hitting the API.
"""

import json
import logging
import re
from typing import Optional

from openai import OpenAI

from echo_sync.ai.intent_schema import IntentResult
from echo_sync.config.prompts import INTENT_CLASSIFIER_SYSTEM_PROMPT
from echo_sync.config.settings import Settings

logger = logging.getLogger(__name__)


# ── Rule-based fast-path patterns ───────────────────────────────────────────
# These bypass the AI for common, unambiguous direct commands.
# This makes the system faster and more reliable for simple cases.

DIRECT_COMMAND_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    # (compiled regex, action, user_feedback)
    (re.compile(r"^pause$", re.IGNORECASE), "pause", "Music paused."),
    (re.compile(r"^stop$", re.IGNORECASE), "stop", "Music stopped."),
    (re.compile(r"^(resume|continue|unpause)$", re.IGNORECASE), "resume", "Resuming music."),
    (re.compile(r"^next(\s+song)?$", re.IGNORECASE), "next", "Playing next song."),
    (re.compile(r"^(previous|prev)(\s+song)?$", re.IGNORECASE), "previous", "Playing previous song."),
    (re.compile(r"^(volume\s+up|louder|turn\s+it\s+up|make\s+it\s+louder)$", re.IGNORECASE), "volume_up", "Volume increased."),
    (re.compile(r"^(volume\s+down|quieter|turn\s+it\s+down|lower\s+the\s+volume|make\s+it\s+quieter)$", re.IGNORECASE), "volume_down", "Volume decreased."),
    (re.compile(r"^play$", re.IGNORECASE), "play", "Playing music."),
]

HELP_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^(help|help\s+me|what\s+can\s+i\s+say\??)$", re.IGNORECASE), "help"),
]


def try_rule_based(text: str) -> Optional[IntentResult]:
    """
    Attempt to classify the input using simple rule-based patterns.

    Returns an IntentResult if matched, None if the AI should handle it.
    This fast-path is used for common, unambiguous direct commands.
    """
    text = text.strip()

    if not text:
        return IntentResult(
            intent_type="unclear",
            action="clarify",
            interpreted_context="none",
            confidence=0.3,
            user_feedback="I didn't catch that. You can say: play something calm, or ask for help.",
        )

    # Check direct commands
    for pattern, action, feedback in DIRECT_COMMAND_PATTERNS:
        if pattern.match(text):
            return IntentResult(
                intent_type="direct_command",
                action=action,
                interpreted_context="none",
                confidence=0.98,
                user_feedback=feedback,
            )

    # Check help requests
    for pattern, action in HELP_PATTERNS:
        if pattern.match(text):
            return IntentResult(
                intent_type="help_request",
                action="help",
                interpreted_context="none",
                confidence=0.98,
                user_feedback=(
                    "You can say: play, pause, next song, volume up, "
                    "or tell me how you feel and I'll find the right music."
                ),
            )

    # Check for "play <something>" pattern
    play_match = re.match(r"^play\s+(.+)$", text, re.IGNORECASE)
    if play_match:
        target = play_match.group(1).strip()
        return IntentResult(
            intent_type="direct_command",
            action="play",
            interpreted_context="none",
            confidence=0.95,
            user_feedback=f"Playing {target}.",
        )

    return None


class IntentClassifier:
    """
    AI-powered intent classifier for Echo-Sync.

    Uses rule-based fast-path for common commands and falls back
    to OpenAI API for complex/ambiguous inputs.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.ai_model

    def classify(self, transcript: str) -> IntentResult:
        """
        Classify user speech transcript into a structured intent.

        First tries rule-based matching for speed and reliability.
        Falls back to AI classification for complex cases.

        Args:
            transcript: The transcribed user speech text.

        Returns:
            IntentResult with classified intent, action, context, and feedback.
        """
        # Fast-path: rule-based matching
        rule_result = try_rule_based(transcript)
        if rule_result is not None:
            logger.info(
                "Rule-based match: %s → %s",
                transcript,
                rule_result.intent_type,
            )
            return rule_result

        # AI classification
        logger.info("AI classification for: %s", transcript)
        return self._classify_with_ai(transcript)

    def _classify_with_ai(self, transcript: str) -> IntentResult:
        """
        Call the OpenAI API for intent classification.

        Uses structured JSON output format to ensure consistent results.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": INTENT_CLASSIFIER_SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": transcript,
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=200,
            )

            content = response.choices[0].message.content
            if content is None:
                logger.warning("AI returned empty content")
                return self._fallback_unclear(transcript)

            # Parse the JSON response into our schema
            data = json.loads(content)
            result = IntentResult.model_validate(data)
            logger.info(
                "AI classified '%s' as %s (confidence: %.2f)",
                transcript,
                result.intent_type,
                result.confidence,
            )
            return result

        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI JSON response: %s", e)
            return self._fallback_unclear(transcript)

        except Exception as e:
            logger.error("AI classification error: %s", e)
            return self._fallback_unclear(transcript)

    @staticmethod
    def _fallback_unclear(transcript: str) -> IntentResult:
        """Return a safe fallback when AI classification fails."""
        return IntentResult(
            intent_type="unclear",
            action="clarify",
            interpreted_context="none",
            confidence=0.2,
            user_feedback=(
                "I had trouble understanding that. "
                "You can say: play, pause, next song, or tell me how you feel."
            ),
        )
