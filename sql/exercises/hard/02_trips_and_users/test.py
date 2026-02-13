"""Test for Trips and Users exercise."""
import sys
import os
import json
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
from utils.database import SQLiteHelper


def test_solution():
    """Test the trips and users solution."""
    exercise_dir = Path(__file__).parent

    db = SQLiteHelper()
    db.connect()

    db.execute_file(str(exercise_dir / "schema.sql"))
    db.execute_file(str(exercise_dir / "sample_data.sql"))

    with open(exercise_dir / "expected_output.json", "r", encoding="utf-8") as f:
        expected = json.load(f)

    solution_file = exercise_dir / "template.sql"
    if not solution_file.exists() or os.path.getsize(solution_file) < 50:
        print("Solution file is empty or too short. Please write your solution in template.sql")
        return False

    with open(solution_file, "r", encoding="utf-8") as f:
        solution_query = f.read()

    try:
        actual = db.execute_query(solution_query)
    except Exception as e:
        print(f"Query execution failed: {e}")
        return False

    if len(actual) != len(expected):
        print(f"Wrong number of rows. Expected {len(expected)}, got {len(actual)}")
        print(f"\nExpected:\n{expected}")
        print(f"\nActual:\n{actual}")
        return False

    for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
        # Allow small floating point differences
        for key in exp_row:
            if isinstance(exp_row[key], float):
                if abs(act_row.get(key, 0) - exp_row[key]) > 0.01:
                    print(f"Row {i+1} does not match")
                    print(f"Expected: {exp_row}")
                    print(f"Actual: {act_row}")
                    return False
            elif act_row.get(key) != exp_row[key]:
                print(f"Row {i+1} does not match")
                print(f"Expected: {exp_row}")
                print(f"Actual: {act_row}")
                return False

    print("All tests passed!")
    print(f"Correct! Calculated cancellation rates for {len(actual)} days.")
    db.close()
    return True


if __name__ == "__main__":
    success = test_solution()
    sys.exit(0 if success else 1)
