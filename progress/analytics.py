#!/usr/bin/env python3
"""Progress tracking and analytics for interview prep."""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, BarColumn, TextColumn

logger = logging.getLogger(__name__)
console = Console()


class ProgressTracker:
    """Track and analyze interview prep progress."""

    def __init__(self, tracker_file: str):
        """Initialize progress tracker.

        Args:
            tracker_file: Path to tracker JSON file
        """
        self.tracker_file = Path(tracker_file)
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load progress data from JSON."""
        if not self.tracker_file.exists():
            console.print(f"[red]Error: Tracker file not found: {self.tracker_file}[/red]")
            sys.exit(1)

        with open(self.tracker_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_data(self):
        """Save progress data to JSON."""
        with open(self.tracker_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def get_days_until_interview(self) -> int:
        """Get number of days until interview."""
        interview_date = datetime.fromisoformat(self.data['interview_date']).date()
        today = datetime.now().date()
        return (interview_date - today).days

    def get_overall_progress(self) -> float:
        """Calculate overall progress percentage."""
        sql_completed = self.data['sql_exercises']['completed']
        sql_total = self.data['sql_exercises']['total']
        python_completed = self.data['python_exercises']['completed']
        python_total = self.data['python_exercises']['total']

        total_completed = sql_completed + python_completed
        total_exercises = sql_total + python_total

        return (total_completed / total_exercises * 100) if total_exercises > 0 else 0

    def display_summary(self):
        """Display comprehensive progress summary."""
        console.clear()

        days_left = self.get_days_until_interview()
        overall = self.get_overall_progress()

        # Header
        title = f"[bold cyan]Interview Prep Progress Report[/bold cyan]\n"
        if days_left > 0:
            title += f"[dim]Interview in {days_left} days[/dim]"
        elif days_left == 0:
            title += f"[yellow]Interview is TODAY![/yellow]"
        else:
            title += f"[green]Interview was {abs(days_left)} days ago[/green]"

        console.print(Panel.fit(title, border_style="cyan"))
        console.print()

        # Overall Progress
        console.print(f"[bold]Overall Progress:[/bold] {overall:.1f}%")
        self._print_progress_bar(overall)
        console.print()

        # SQL Exercises
        sql = self.data['sql_exercises']
        console.print("[bold cyan]SQL Exercises[/bold cyan]")
        console.print(f"   Progress: {sql['completed']}/{sql['total']} "
                     f"({sql['completed']/sql['total']*100:.0f}%)")

        for diff, stats in sql['by_difficulty'].items():
            pct = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "[green]DONE[/green]" if pct == 100 else "[yellow]WIP[/yellow]" if pct >= 50 else "[red]TODO[/red]"
            console.print(f"   {status} {diff.capitalize()}: {stats['completed']}/{stats['total']} ({pct:.0f}%)")

        console.print()

        # Python Exercises
        python = self.data['python_exercises']
        console.print("[bold cyan]Python Exercises[/bold cyan]")
        console.print(f"   Progress: {python['completed']}/{python['total']} "
                     f"({python['completed']/python['total']*100:.0f}%)")

        for category, stats in python['by_category'].items():
            pct = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            status = "[green]DONE[/green]" if pct == 100 else "[yellow]WIP[/yellow]" if pct >= 50 else "[red]TODO[/red]"
            console.print(f"   {status} {category.capitalize()}: {stats['completed']}/{stats['total']} ({pct:.0f}%)")

        console.print()

        # Flashcards
        fc = self.data['flashcards']
        console.print("[bold cyan]Flashcards[/bold cyan]")
        console.print(f"   Total Cards: {fc.get('total_cards', 'N/A')}")
        console.print(f"   Total Reviews: {fc['total_reviews']}")
        console.print(f"   Cards Mastered: {fc['cards_mastered']}")
        console.print(f"   Avg Confidence: {fc['average_confidence']:.1f}/5")

        console.print()

        # System Design
        if 'system_design' in self.data:
            sd = self.data['system_design']
            console.print("[bold cyan]System Design[/bold cyan]")
            console.print(f"   Reviewed: {sd['scenarios_reviewed']}/{sd['total_scenarios']}")
            console.print()

        # Mock Interviews
        console.print("[bold cyan]Mock Interviews[/bold cyan]")
        console.print(f"   Completed: {len(self.data['mock_interviews'])}")

        console.print()

        # Time Investment
        console.print("[bold cyan]Time Investment[/bold cyan]")
        hours = self.data['time_spent_minutes'] / 60
        console.print(f"   Total: {hours:.1f} hours ({self.data['time_spent_minutes']} minutes)")

        console.print()

        # Recommendations
        self._display_recommendations()

    def _print_progress_bar(self, percentage: float):
        """Print a visual progress bar."""
        filled = int(percentage / 10)
        empty = 10 - filled
        bar = "=" * filled + "-" * empty
        console.print(f"   [{bar}] {percentage:.1f}%")

    def _display_recommendations(self):
        """Display personalized recommendations."""
        console.print("[bold yellow]Next Steps:[/bold yellow]")

        recommendations = []

        # Check SQL progress
        sql = self.data['sql_exercises']
        sql_pct = (sql['completed'] / sql['total'] * 100) if sql['total'] > 0 else 0
        if sql_pct < 80:
            recommendations.append(f"Complete {sql['total'] - sql['completed']} more SQL exercises")

        # Check Python progress
        python = self.data['python_exercises']
        python_pct = (python['completed'] / python['total'] * 100) if python['total'] > 0 else 0
        if python_pct < 80:
            recommendations.append(f"Complete {python['total'] - python['completed']} more Python exercises")

        # Check flashcards
        if self.data['flashcards']['total_reviews'] < 50:
            recommendations.append("Review more flashcards (target: 50+ reviews)")

        # Check mock interviews
        if len(self.data['mock_interviews']) < 2:
            recommendations.append("Do at least 2 mock interviews")

        # Check system design
        if 'system_design' in self.data:
            if self.data['system_design']['scenarios_reviewed'] < 3:
                recommendations.append("Review at least 3 system design scenarios")

        if not recommendations:
            console.print("   [green]Great progress! Keep refining your skills![/green]")
        else:
            for i, rec in enumerate(recommendations, 1):
                console.print(f"   {i}. {rec}")

        console.print()

        # Days until interview
        days_left = self.get_days_until_interview()
        if days_left > 0:
            console.print(f"[bold]You have {days_left} days to prepare. Stay focused![/bold]")
        elif days_left == 0:
            console.print(f"[bold green]Today is the day! You have got this![/bold green]")

    def display_detailed_stats(self):
        """Display detailed statistics in table format."""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]Detailed Statistics[/bold cyan]",
            border_style="cyan"
        ))
        console.print()

        # SQL Topics Table
        sql_table = Table(title="SQL Topics Progress", box=box.ROUNDED)
        sql_table.add_column("Topic", style="cyan")
        sql_table.add_column("Completed", justify="center")

        for topic, count in self.data['sql_exercises']['by_topic'].items():
            sql_table.add_row(topic.replace('_', ' ').title(), str(count))

        console.print(sql_table)
        console.print()

        # Python Categories Table
        py_table = Table(title="Python Exercise Progress", box=box.ROUNDED)
        py_table.add_column("Category", style="cyan")
        py_table.add_column("Completed", justify="center")
        py_table.add_column("Total", justify="center")
        py_table.add_column("Percentage", justify="center")

        for category, stats in self.data['python_exercises']['by_category'].items():
            pct = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            py_table.add_row(
                category.replace('_', ' ').title(),
                str(stats['completed']),
                str(stats['total']),
                f"{pct:.0f}%"
            )

        console.print(py_table)
        console.print()

        # Flashcard Categories Table
        fc_table = Table(title="Flashcard Progress by Category", box=box.ROUNDED)
        fc_table.add_column("Category", style="cyan")
        fc_table.add_column("Reviews", justify="center")

        for category, count in self.data['flashcards']['by_category'].items():
            fc_table.add_row(category, str(count))

        console.print(fc_table)
        console.print()

        # Daily Logs
        if self.data['daily_logs']:
            log_table = Table(title="Recent Study Sessions", box=box.ROUNDED)
            log_table.add_column("Date", style="cyan")
            log_table.add_column("Type", justify="center")
            log_table.add_column("Duration (min)", justify="center")
            log_table.add_column("Details")

            for log in self.data['daily_logs'][-10:]:
                log_table.add_row(
                    log['date'][:16],
                    log['type'],
                    str(log['duration_minutes']),
                    log.get('details', '')
                )

            console.print(log_table)

    def log_study_session(self, session_type: str, duration_minutes: int, details: str = ""):
        """Log a study session.

        Args:
            session_type: Type of session (sql, python, flashcards, mock_interview)
            duration_minutes: Duration in minutes
            details: Additional details
        """
        log_entry = {
            "date": datetime.now().isoformat(),
            "type": session_type,
            "duration_minutes": duration_minutes,
            "details": details
        }

        self.data['daily_logs'].append(log_entry)
        self.data['time_spent_minutes'] += duration_minutes
        self.save_data()

        console.print(f"[green]Logged {duration_minutes} minute {session_type} session[/green]")
        logger.info("Logged %d minute %s session", duration_minutes, session_type)


def main():
    """Main entry point."""
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Interview Prep Progress Tracker")
    parser.add_argument(
        "--report",
        choices=["summary", "detailed"],
        default="summary",
        help="Type of report to generate"
    )
    parser.add_argument(
        "--log-session",
        help="Log a study session (format: type,duration,details)"
    )

    args = parser.parse_args()

    # Determine tracker file path
    script_dir = Path(__file__).parent
    tracker_file = script_dir / "tracker.json"

    # Initialize tracker
    tracker = ProgressTracker(str(tracker_file))

    if args.log_session:
        parts = args.log_session.split(',')
        if len(parts) >= 2:
            session_type = parts[0]
            duration = int(parts[1])
            details = parts[2] if len(parts) > 2 else ""
            tracker.log_study_session(session_type, duration, details)
        else:
            console.print("[red]Error: Invalid log format. Use: type,duration,details[/red]")
            sys.exit(1)
    elif args.report == "summary":
        tracker.display_summary()
    elif args.report == "detailed":
        tracker.display_detailed_stats()


if __name__ == "__main__":
    main()
