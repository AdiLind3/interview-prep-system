#!/usr/bin/env python3
"""Universal SQL Test Runner for all SQL exercises."""
import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.database import SQLiteHelper

console = Console()


class SQLTestRunner:
    """Test runner for SQL exercises."""

    def __init__(self, exercise_path: str):
        """Initialize test runner.

        Args:
            exercise_path: Path to exercise directory
        """
        self.exercise_path = Path(exercise_path)
        self.exercise_name = self.exercise_path.name

    def run_test(self, solution_file: Optional[str] = None) -> bool:
        """Run test for the exercise.

        Args:
            solution_file: Path to solution file (default: template.sql)

        Returns:
            True if test passes, False otherwise
        """
        console.print(f"\n[bold cyan]Testing: {self.exercise_name}[/bold cyan]\n")

        # Check required files exist
        required_files = ["schema.sql", "sample_data.sql"]
        for file in required_files:
            if not (self.exercise_path / file).exists():
                console.print(f"[red]❌ Missing required file: {file}[/red]")
                return False

        # Set up database
        db = SQLiteHelper()
        db.connect()

        try:
            # Load schema and data
            console.print("[dim]Loading schema...[/dim]")
            db.execute_file(str(self.exercise_path / "schema.sql"))

            console.print("[dim]Loading sample data...[/dim]")
            db.execute_file(str(self.exercise_path / "sample_data.sql"))

            # Determine which solution to test
            if solution_file is None:
                solution_file = self.exercise_path / "template.sql"
            else:
                solution_file = Path(solution_file)

            if not solution_file.exists():
                console.print(f"[red]❌ Solution file not found: {solution_file}[/red]")
                return False

            # Check if solution has content
            with open(solution_file, 'r') as f:
                solution_query = f.read().strip()

            if not solution_query or len(solution_query) < 20:
                console.print("[yellow]⚠️  Solution file is empty or too short.[/yellow]")
                console.print("[yellow]   Please write your solution first![/yellow]")
                return False

            # Execute solution
            console.print("[dim]Executing your solution...[/dim]")
            try:
                actual = db.execute_query(solution_query)
            except Exception as e:
                console.print(f"[red]❌ Query execution failed:[/red]")
                console.print(f"[red]   {e}[/red]")
                return False

            # Check if expected output exists
            expected_file = self.exercise_path / "expected_output.json"
            if expected_file.exists():
                with open(expected_file, 'r') as f:
                    expected = json.load(f)

                # Compare results
                if self._compare_results(actual, expected):
                    console.print(f"[green]✅ All tests passed![/green]")
                    console.print(f"[green]   Returned {len(actual)} rows correctly.[/green]")
                    self._display_results(actual)
                    return True
                else:
                    self._display_comparison(expected, actual)
                    return False
            else:
                # No expected output, just display results
                console.print("[yellow]ℹ️  No expected output file found.[/yellow]")
                console.print("[yellow]   Displaying query results:[/yellow]")
                self._display_results(actual)
                return True

        except Exception as e:
            console.print(f"[red]❌ Test error: {e}[/red]")
            return False
        finally:
            db.close()

    def _compare_results(self, actual: List[Dict[str, Any]],
                        expected: List[Dict[str, Any]]) -> bool:
        """Compare actual and expected results.

        Args:
            actual: Actual query results
            expected: Expected query results

        Returns:
            True if results match, False otherwise
        """
        if len(actual) != len(expected):
            console.print(f"[red]❌ Wrong number of rows![/red]")
            console.print(f"[red]   Expected: {len(expected)}, Got: {len(actual)}[/red]")
            return False

        # Compare each row
        for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
            # Check if all expected columns are present
            for key in exp_row:
                if key not in act_row:
                    console.print(f"[red]❌ Missing column in row {i+1}: {key}[/red]")
                    return False

                # Compare values (handle floats with tolerance)
                exp_val = exp_row[key]
                act_val = act_row[key]

                if isinstance(exp_val, float) and isinstance(act_val, (int, float)):
                    if abs(exp_val - act_val) > 0.01:
                        console.print(f"[red]❌ Row {i+1}, column '{key}': values don't match[/red]")
                        console.print(f"[red]   Expected: {exp_val}, Got: {act_val}[/red]")
                        return False
                else:
                    if exp_val != act_val:
                        console.print(f"[red]❌ Row {i+1}, column '{key}': values don't match[/red]")
                        console.print(f"[red]   Expected: {exp_val}, Got: {act_val}[/red]")
                        return False

        return True

    def _display_results(self, results: List[Dict[str, Any]], title: str = "Query Results"):
        """Display results in a table.

        Args:
            results: Query results
            title: Table title
        """
        if not results:
            console.print("[yellow]Query returned no rows.[/yellow]")
            return

        # Create table
        table = Table(title=title, box=box.ROUNDED)

        # Add columns
        for column in results[0].keys():
            table.add_column(column, style="cyan")

        # Add rows (limit to 10 for display)
        display_count = min(10, len(results))
        for row in results[:display_count]:
            table.add_row(*[str(v) for v in row.values()])

        if len(results) > display_count:
            console.print(f"\n[dim]Showing first {display_count} of {len(results)} rows[/dim]")

        console.print(table)

    def _display_comparison(self, expected: List[Dict[str, Any]],
                           actual: List[Dict[str, Any]]):
        """Display expected vs actual results.

        Args:
            expected: Expected results
            actual: Actual results
        """
        console.print("\n[bold red]❌ Test Failed![/bold red]\n")
        console.print("[bold]Expected Output:[/bold]")
        self._display_results(expected, "Expected")
        console.print("\n[bold]Your Output:[/bold]")
        self._display_results(actual, "Actual")


def find_exercises(base_path: Path, difficulty: Optional[str] = None) -> List[Path]:
    """Find all SQL exercises.

    Args:
        base_path: Base exercises directory
        difficulty: Filter by difficulty (easy/medium/hard)

    Returns:
        List of exercise paths
    """
    exercises = []

    if difficulty:
        search_path = base_path / difficulty
        if search_path.exists():
            exercises.extend(sorted(search_path.glob("*/")))
    else:
        for diff in ["easy", "medium", "hard"]:
            diff_path = base_path / diff
            if diff_path.exists():
                exercises.extend(sorted(diff_path.glob("*/")))

    return exercises


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SQL Exercise Test Runner")
    parser.add_argument(
        "exercise",
        nargs="?",
        help="Path to specific exercise directory, or 'all' to test all exercises"
    )
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard"],
        help="Filter exercises by difficulty"
    )
    parser.add_argument(
        "--solution",
        help="Path to solution file (default: template.sql)"
    )
    args = parser.parse_args()

    # Determine base path
    script_dir = Path(__file__).parent.parent
    exercises_dir = script_dir / "exercises"

    if args.exercise and args.exercise.lower() != "all":
        # Test single exercise
        exercise_path = Path(args.exercise)
        if not exercise_path.is_absolute():
            exercise_path = exercises_dir / args.exercise

        if not exercise_path.exists():
            console.print(f"[red]Error: Exercise not found: {exercise_path}[/red]")
            sys.exit(1)

        runner = SQLTestRunner(exercise_path)
        success = runner.run_test(args.solution)
        sys.exit(0 if success else 1)

    else:
        # Test all exercises
        exercises = find_exercises(exercises_dir, args.difficulty)

        if not exercises:
            console.print("[yellow]No exercises found![/yellow]")
            sys.exit(1)

        console.print(f"\n[bold cyan]Running {len(exercises)} SQL exercises...[/bold cyan]\n")

        results = []
        for exercise_path in exercises:
            runner = SQLTestRunner(exercise_path)
            success = runner.run_test()
            results.append((exercise_path.name, success))
            console.print()

        # Summary
        console.print("\n[bold cyan]Summary:[/bold cyan]\n")
        passed = sum(1 for _, success in results if success)
        total = len(results)

        for name, success in results:
            status = "[green]✅ PASSED[/green]" if success else "[red]❌ FAILED[/red]"
            console.print(f"  {status} - {name}")

        console.print(f"\n[bold]Results: {passed}/{total} passed[/bold]")
        sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
