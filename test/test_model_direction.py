import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.TrafficControl import Direction

def print_green(message):
    """Helper function to print text in green."""
    print(f"\033[92m{message}\033[0m")

def test_direction_enum_values():
    assert Direction.North == 0, "Direction.North should be 0"
    assert Direction.East == 1, "Direction.East should be 1"
    assert Direction.South == 2, "Direction.South should be 2"
    assert Direction.West == 3, "Direction.West should be 3"
    print_green("test_direction_enum_values: Test Passed")

def test_direction_enum_members():
    # Test that the enum members are correctly defined
    assert isinstance(Direction.North, Direction), "Direction.North should be an instance of Direction"
    assert isinstance(Direction.East, Direction), "Direction.East should be an instance of Direction"
    assert isinstance(Direction.South, Direction), "Direction.South should be an instance of Direction"
    assert isinstance(Direction.West, Direction), "Direction.West should be an instance of Direction"
    print_green("test_direction_enum_members: Test Passed")

test_direction_enum_members()
test_direction_enum_values()
