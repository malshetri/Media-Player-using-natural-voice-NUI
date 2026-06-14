"""
Tests for the Echo-Sync demo routing.

Integration-style tests that simulate the full demo script
through the intent classifier, verifying correct routing for
all expected demo inputs.
"""

import pytest

from echo_sync.ai.intent_classifier import try_rule_based
from echo_sync.ai.intent_schema import IntentResult


class TestDemoRouting:
    """
    Simulate the demo script and verify each input routes correctly.

    These map to the expected demo flow:
        play → volume up → I am tired → I need energy →
        What can I say? → What is the weather? → [empty] → pause
    """

    def test_demo_play(self):
        """'play' should start music."""
        result = try_rule_based("play")
        assert result is not None
        assert result.intent_type == "direct_command"
        assert result.action == "play"

    def test_demo_volume_up(self):
        """'volume up' should increase volume."""
        result = try_rule_based("volume up")
        assert result is not None
        assert result.intent_type == "direct_command"
        assert result.action == "volume_up"

    def test_demo_i_am_tired(self):
        """'I am tired' should select calm playlist."""
        result = try_rule_based("I am tired")
        assert result is not None
        assert result.intent_type == "context_request"
        assert result.action == "select_playlist"
        assert result.interpreted_context == "calm"

    def test_demo_i_need_energy(self):
        """'I need energy' should select energy playlist."""
        result = try_rule_based("I need energy")
        assert result is not None
        assert result.intent_type == "context_request"
        assert result.action == "select_playlist"
        assert result.interpreted_context == "energy"

    def test_demo_what_can_i_say(self):
        """'What can I say?' should give help."""
        result = try_rule_based("What can I say?")
        assert result is not None
        assert result.intent_type == "help_request"
        assert result.action == "help"

    def test_demo_weather(self):
        """'What is the weather?' should be rejected as off-topic."""
        result = try_rule_based("What is the weather?")
        assert result is not None
        assert result.intent_type == "off_topic"
        assert result.action == "reject"
        assert "music" in result.user_feedback.lower()

    def test_demo_empty_input(self):
        """Empty input should trigger clarification."""
        result = try_rule_based("")
        assert result is not None
        assert result.intent_type == "unclear"
        assert result.action == "clarify"

    def test_demo_pause(self):
        """'pause' should pause music."""
        result = try_rule_based("pause")
        assert result is not None
        assert result.intent_type == "direct_command"
        assert result.action == "pause"


class TestPlaylistCommands:
    """Test rule-based playlist command matching."""

    @pytest.mark.parametrize(
        "phrase,expected_context",
        [
            ("play calm music", "calm"),
            ("play relaxing music", "calm"),
            ("play energetic music", "energy"),
            ("play energy music", "energy"),
            ("play focus music", "focus"),
            ("play study music", "focus"),
            ("play happy music", "happy"),
            ("play sad music", "sad"),
            ("play chill music", "calm"),
            ("play upbeat music", "energy"),
            ("play ambient music", "focus"),
            ("play cheerful music", "happy"),
            ("play melancholic music", "sad"),
        ],
    )
    def test_play_keyword_music(self, phrase, expected_context):
        """'play <keyword> music' should select the right playlist."""
        result = try_rule_based(phrase)
        assert result is not None, f"Failed for '{phrase}'"
        assert result.intent_type == "context_request"
        assert result.action == "select_playlist"
        assert result.interpreted_context == expected_context

    def test_play_keyword_without_music_suffix(self):
        """'play calm' (without 'music') should also match."""
        result = try_rule_based("play calm")
        assert result is not None
        assert result.intent_type == "context_request"
        assert result.action == "select_playlist"
        assert result.interpreted_context == "calm"

    def test_play_unknown_genre_is_direct(self):
        """'play jazz' (unknown keyword) stays as direct play command."""
        result = try_rule_based("play jazz")
        assert result is not None
        assert result.intent_type == "direct_command"
        assert result.action == "play"


class TestContextStatements:
    """Test rule-based context statement matching."""

    @pytest.mark.parametrize(
        "phrase,expected_context",
        [
            ("I am tired", "calm"),
            ("I'm exhausted", "calm"),
            ("I feel stressed", "calm"),
            ("I need energy", "energy"),
            ("I want motivation", "energy"),
            ("I need to focus", "focus"),
            ("I want to study", "focus"),
            ("I need to concentrate", "focus"),
            ("I am happy", "happy"),
            ("I feel excited", "happy"),
            ("I feel sad", "sad"),
            ("I am lonely", "sad"),
            ("feeling down", "sad"),
        ],
    )
    def test_context_statement(self, phrase, expected_context):
        """Context statements should map to the correct playlist."""
        result = try_rule_based(phrase)
        assert result is not None, f"Failed for '{phrase}'"
        assert result.intent_type == "context_request"
        assert result.action == "select_playlist"
        assert result.interpreted_context == expected_context


class TestOffTopicDetection:
    """Test rule-based off-topic rejection."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "What is the weather?",
            "What is 2+2?",
            "Who is the president?",
            "Tell me about dogs",
            "Where is Berlin?",
            "How can I cook pasta?",
        ],
    )
    def test_off_topic_rejected(self, phrase):
        """Off-topic questions should be rejected."""
        result = try_rule_based(phrase)
        assert result is not None, f"Failed for '{phrase}'"
        assert result.intent_type == "off_topic"
        assert result.action == "reject"
        assert "music" in result.user_feedback.lower()


class TestExpandedHelp:
    """Test expanded help recognition patterns."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "help",
            "help me",
            "What can I say?",
            "What can I do?",
            "I don't know",
            "What should I say?",
            "Hey Eko",
            "Hi Echo",
            "hello iko",
            "ico",
            "hey acou",
        ],
    )
    def test_help_recognized(self, phrase):
        """Help-like phrases should be classified as help requests."""
        result = try_rule_based(phrase)
        assert result is not None, f"Failed for '{phrase}'"
        assert result.intent_type == "help_request"
        assert result.action == "help"
