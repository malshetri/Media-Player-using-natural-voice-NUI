"""
Tests for the Echo-Sync context mapper.

Tests the mapping from interpreted context to music folder paths.
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from echo_sync.ai.context_mapper import ContextMapper, CONTEXT_TO_FOLDER


@pytest.fixture
def music_dir(tmp_path):
    """Create actual music directories for testing."""
    for folder in ["calm", "energy", "focus", "happy", "sad", "fallback"]:
        (tmp_path / folder).mkdir()
    return tmp_path


@pytest.fixture
def mock_settings(music_dir):
    """Create mock settings with a real temporary music path."""
    settings = MagicMock()
    settings.music_path = music_dir
    return settings


@pytest.fixture
def mapper(mock_settings):
    """Create a ContextMapper with mock settings."""
    return ContextMapper(mock_settings)


class TestContextMapper:
    """Test context-to-playlist mapping."""

    def test_calm_maps_to_calm_folder(self, mapper):
        path = mapper.get_playlist_path("calm")
        assert path.name == "calm"

    def test_energy_maps_to_energy_folder(self, mapper):
        path = mapper.get_playlist_path("energy")
        assert path.name == "energy"

    def test_focus_maps_to_focus_folder(self, mapper):
        path = mapper.get_playlist_path("focus")
        assert path.name == "focus"

    def test_happy_maps_to_happy_folder(self, mapper):
        path = mapper.get_playlist_path("happy")
        assert path.name == "happy"

    def test_sad_maps_to_sad_folder(self, mapper):
        path = mapper.get_playlist_path("sad")
        assert path.name == "sad"

    def test_unknown_maps_to_fallback(self, mapper):
        path = mapper.get_playlist_path("unknown")
        assert path.name == "fallback"

    def test_none_maps_to_fallback(self, mapper):
        path = mapper.get_playlist_path("none")
        assert path.name == "fallback"

    def test_invalid_context_maps_to_fallback(self, mapper):
        path = mapper.get_playlist_path("nonexistent")
        assert path.name == "fallback"

    def test_all_contexts_mapped(self):
        """Ensure all expected contexts have mappings."""
        expected = {"calm", "energy", "focus", "happy", "sad", "unknown", "none"}
        assert set(CONTEXT_TO_FOLDER.keys()) == expected

    def test_context_description(self):
        """Test user-friendly context descriptions."""
        assert "calm" in ContextMapper.get_context_description("calm")
        assert "energetic" in ContextMapper.get_context_description("energy")
        assert "focused" in ContextMapper.get_context_description("focus")
        assert "happy" in ContextMapper.get_context_description("happy")
        assert "soft" in ContextMapper.get_context_description("sad")

    def test_get_all_music_folders(self, mapper):
        """Test that all folders are returned."""
        folders = mapper.get_all_music_folders()
        assert len(folders) == len(CONTEXT_TO_FOLDER)
        for ctx in CONTEXT_TO_FOLDER:
            assert ctx in folders
