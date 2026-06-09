"""
Tests for the Echo-Sync playlist manager.

Tests music folder scanning, playlist building, and track selection.
"""

import pytest
from pathlib import Path
from unittest.mock import patch

from echo_sync.media.playlist_manager import PlaylistManager, SUPPORTED_EXTENSIONS


@pytest.fixture
def music_dir(tmp_path):
    """Create a temporary music directory with test files."""
    # Create category folders with dummy files
    for category in ["calm", "energy", "focus", "happy", "sad", "fallback"]:
        folder = tmp_path / category
        folder.mkdir()
        # Create dummy MP3 files
        for i in range(3):
            (folder / f"track_{i}.mp3").write_text("fake audio")

    # Add a non-audio file to test filtering
    (tmp_path / "calm" / "notes.txt").write_text("not audio")

    return tmp_path


@pytest.fixture
def manager(music_dir):
    """Create a PlaylistManager with the test music directory."""
    return PlaylistManager(music_dir)


class TestPlaylistManager:
    """Test playlist scanning and selection."""

    def test_scan_finds_all_categories(self, manager):
        categories = manager.get_available_categories()
        assert "calm" in categories
        assert "energy" in categories
        assert "focus" in categories
        assert "happy" in categories
        assert "sad" in categories
        assert "fallback" in categories

    def test_scan_finds_correct_count(self, manager):
        # Each folder has 3 MP3 files
        assert manager.get_track_count("calm") == 3
        assert manager.get_track_count("energy") == 3

    def test_scan_ignores_non_audio_files(self, manager):
        # calm/ has 3 MP3s + 1 txt → should only have 3
        assert manager.get_track_count("calm") == 3

    def test_total_track_count(self, manager):
        # 6 categories × 3 tracks each = 18
        assert manager.get_track_count() == 18

    def test_get_playlist_returns_tracks(self, manager):
        playlist = manager.get_playlist("calm", shuffle=False)
        assert len(playlist) == 3
        for track in playlist:
            assert track.suffix == ".mp3"

    def test_get_playlist_shuffles(self, manager):
        """Shuffled playlists should eventually differ from sorted order."""
        sorted_playlist = manager.get_playlist("calm", shuffle=False)
        # Run multiple times — at least one should differ
        found_different = False
        for _ in range(20):
            shuffled = manager.get_playlist("calm", shuffle=True)
            if shuffled != sorted_playlist:
                found_different = True
                break
        # With 3 items, probability of same order is 1/6, so 20 tries should catch it
        assert found_different or len(sorted_playlist) <= 1

    def test_empty_category_falls_back(self, manager, music_dir):
        """Missing category should fall back to 'fallback'."""
        playlist = manager.get_playlist("nonexistent")
        assert len(playlist) == 3  # Fallback has 3 tracks

    def test_get_track_by_name(self, manager):
        """Search for a track by name."""
        track = manager.get_track_by_name("track_0")
        assert track is not None
        assert "track_0" in track.stem

    def test_get_track_by_name_not_found(self, manager):
        """Search for nonexistent track returns None."""
        track = manager.get_track_by_name("doesnotexist")
        assert track is None

    def test_get_all_tracks(self, manager):
        all_tracks = manager.get_all_tracks()
        assert len(all_tracks) == 18

    def test_refresh_rescans(self, manager, music_dir):
        """Refresh should rescan folders."""
        # Add a new file
        (music_dir / "calm" / "new_track.mp3").write_text("new")
        manager.refresh()
        assert manager.get_track_count("calm") == 4

    def test_supported_extensions(self):
        """Check that common audio formats are supported."""
        assert ".mp3" in SUPPORTED_EXTENSIONS
        assert ".wav" in SUPPORTED_EXTENSIONS
        assert ".flac" in SUPPORTED_EXTENSIONS
        assert ".ogg" in SUPPORTED_EXTENSIONS

    def test_nonexistent_root(self, tmp_path):
        """Manager handles missing root gracefully."""
        mgr = PlaylistManager(tmp_path / "does_not_exist")
        assert mgr.get_track_count() == 0
