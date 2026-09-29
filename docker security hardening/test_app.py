import subprocess
import sys


def test_example_pass():
    """Simple dummy test to verify test setup works."""
    assert 1 + 1 == 2


def test_default_greeting(monkeypatch):
    """Test default greeting when NAME is not set."""
    monkeypatch.delenv("NAME", raising=False)

    result = subprocess.run(
        [sys.executable, "app.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "Hello, Docker!"
    assert result.returncode == 0


def test_custom_name_greeting(monkeypatch):
    """Test custom greeting when NAME environment variable is set."""
    monkeypatch.setenv("NAME", "Russel")

    result = subprocess.run(
        [sys.executable, "app.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "Hello, Russel!"
    assert result.returncode == 0
