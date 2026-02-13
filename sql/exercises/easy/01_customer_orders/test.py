"""Test for Customer Orders exercise."""
import sys
import os
import json
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
from utils.database import SQLiteHelper


def test_solution():
    """Test the customer orders solution."""
    exercise_dir = Path(__file__).parent

    # Set up database
    db = SQLiteHelper()
    db.connect()

    # Load schema and data
    db.execute_file(str(exercise_dir / "schema.sql"))
    db.execute_file(str(exercise_dir / "sample_data.sql"))

    # Load expected output
    with open(exercise_dir / "expected_output.json", 'r') as f:
        expected = json.load(f)

    # Load and execute student solution
    solution_file = exercise_dir / "template.sql"
    if not solution_file.exists() or os.path.getsize(solution_file) < 50:
        print("❌ Solution file is empty or too short. Please write your solution in template.sql")
        return False

    with open(solution_file, 'r') as f:
        solution_query = f.read()

    try:
        actual = db.execute_query(solution_query)
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        return False

    # Compare results (order-independent for ties)
    if len(actual) != len(expected):
        print(f"❌ Wrong number of rows. Expected {len(expected)}, got {len(actual)}")
        print(f"\nExpected:\n{expected}")
        print(f"\nActual:\n{actual}")
        return False

    # Check if results match (allowing different order for same count)
    for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
        if act_row != exp_row:
            # Allow same count with different order
            if i < len(expected) - 1:
                if exp_row['order_count'] == expected[i+1]['order_count']:
                    continue
            print(f"❌ Row {i+1} doesn't match")
            print(f"Expected: {exp_row}")
            print(f"Actual: {act_row}")
            return False

    print("✅ All tests passed!")
    print(f"✅ Correct! Found {len(actual)} customers with orders.")
    db.close()
    return True


if __name__ == "__main__":
    success = test_solution()
    sys.exit(0 if success else 1)
