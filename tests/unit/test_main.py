"""Unit tests for main module."""

from main import sum_two_numbers


def test_sum_two_numbers_with_positive_integers_returns_sum() -> None:
    # Arrange
    a, b = 2, 3

    # Act
    result = sum_two_numbers(a, b)

    # Assert
    assert result == 5
