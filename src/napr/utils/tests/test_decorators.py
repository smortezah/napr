"""Test for decorators."""

from napr.utils.decorators import info


def test_info():
    """Test the info decorator."""

    @info(message="Test message")
    def test_func():
        """Test function."""
        pass

    test_func()
    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Test function."
    assert test_func.__wrapped__.__name__ == "test_func"
    assert test_func.__wrapped__.__doc__ == "Test function."
