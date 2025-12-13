"""Tests for helper functions."""

import pytest

from bot.utils.helpers import format_duration


class TestFormatDuration:
    """Tests for the format_duration function."""

    def test_seconds_only(self) -> None:
        """Test formatting seconds less than a minute."""
        assert format_duration(45) == "45s"
        assert format_duration(0) == "0s"

    def test_minutes_and_seconds(self) -> None:
        """Test formatting minutes and seconds."""
        assert format_duration(90) == "1m 30s"
        assert format_duration(120) == "2m 0s"

    def test_hours_minutes_seconds(self) -> None:
        """Test formatting hours, minutes, and seconds."""
        assert format_duration(3661) == "1h 1m 1s"
        assert format_duration(7200) == "2h 0m 0s"

    def test_large_duration(self) -> None:
        """Test formatting large durations."""
        assert format_duration(86400) == "24h 0m 0s"
