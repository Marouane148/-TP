"""Unit tests for distance calculation logic."""
import pytest
import math
from app import calculate_distance, parse_coordinates, create_result


@pytest.mark.unit
class TestCalculateDistance:
    """Test the calculate_distance function."""

    def test_basic_calculation(self):
        """Test basic distance calculation between two points."""
        result = calculate_distance(0, 0, 3, 4)
        assert result == 5.0

    def test_same_point(self):
        """Test distance between same point."""
        result = calculate_distance(5, 5, 5, 5)
        assert result == 0.0

    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        result = calculate_distance(-2, -5, 1, 6)
        expected = math.sqrt((1 - (-2)) ** 2 + (6 - (-5)) ** 2)
        assert result == pytest.approx(expected)

    def test_pythagorean_triple_5_12_13(self):
        """Test with 5-12-13 Pythagorean triple."""
        result = calculate_distance(0, 0, 5, 12)
        assert result == 13.0

    def test_single_axis_movement_x(self):
        """Test movement only on X axis."""
        result = calculate_distance(0, 0, 10, 0)
        assert result == 10.0

    def test_single_axis_movement_y(self):
        """Test movement only on Y axis."""
        result = calculate_distance(0, 0, 0, 7)
        assert result == 7.0

    def test_large_coordinates(self):
        """Test with large coordinate values."""
        result = calculate_distance(0, 0, 1000, 1000)
        expected = 1000 * math.sqrt(2)
        assert result == pytest.approx(expected)


@pytest.mark.unit
class TestParseCoordinates:
    """Test the parse_coordinates function."""

    def test_valid_positive_coordinates(self):
        """Test parsing valid positive coordinates."""
        x, y = parse_coordinates("2,5")
        assert x == 2
        assert y == 5

    def test_valid_with_spaces(self):
        """Test parsing coordinates with spaces."""
        x, y = parse_coordinates("  2 , 5  ")
        assert x == 2
        assert y == 5

    def test_negative_coordinates(self):
        """Test parsing negative coordinates."""
        x, y = parse_coordinates("-3,-7")
        assert x == -3
        assert y == -7

    def test_mixed_sign_coordinates(self):
        """Test parsing mixed positive and negative coordinates."""
        x, y = parse_coordinates("10,-20")
        assert x == 10
        assert y == -20

    def test_zero_coordinates(self):
        """Test parsing zero coordinates."""
        x, y = parse_coordinates("0,0")
        assert x == 0
        assert y == 0

    def test_invalid_format_missing_comma(self):
        """Test that missing comma raises ValueError."""
        with pytest.raises(ValueError, match="Invalid coordinate format"):
            parse_coordinates("2 5")

    def test_invalid_format_non_numeric(self):
        """Test that non-numeric values raise ValueError."""
        with pytest.raises(ValueError, match="Invalid coordinate format"):
            parse_coordinates("a,b")

    def test_invalid_format_only_one_value(self):
        """Test that single value raises ValueError."""
        with pytest.raises(ValueError, match="Coordinates must contain"):
            parse_coordinates("5")

    def test_invalid_format_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError):
            parse_coordinates("")

    def test_extra_coordinates_ignored(self):
        """Test that extra coordinates are ignored (only first 2 used)."""
        x, y = parse_coordinates("1,2,3,4")
        assert x == 1
        assert y == 2


@pytest.mark.unit
class TestCreateResult:
    """Test the create_result function."""

    def test_result_structure(self):
        """Test that result has required fields."""
        result = create_result(0, 0, 3, 4)
        assert 'requested_at' in result
        assert 'result_distance' in result
        assert 'start_point' in result
        assert 'end_point' in result

    def test_result_values(self):
        """Test that result contains correct values."""
        result = create_result(1, 2, 4, 6)
        assert result['start_point'] == [1, 2]
        assert result['end_point'] == [4, 6]
        assert result['result_distance'] == 5.0

    def test_result_timestamp_format(self):
        """Test that timestamp is in ISO format."""
        result = create_result(0, 0, 1, 1)
        assert 'T' in result['requested_at']
        assert len(result['requested_at']) > 0
