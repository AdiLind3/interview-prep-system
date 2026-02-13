#!/usr/bin/env python3
"""
Interactive Flashcard CLI with Spaced Repetition (SM-2 Algorithm)

The SM-2 (SuperMemo 2) algorithm is a spaced repetition algorithm that
calculates when to review a flashcard based on how well you remember it.

Features:
- Interactive quiz sessions
- Spaced repetition scheduling
- Progress tracking
- Category filtering
- Beautiful terminal UI
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from rich.markdown import Markdown

console = Console()


class SpacedRepetition:
    """SM-2 Spaced Repetition Algorithm."""

    @staticmethod
    def calculate_next_review(
        quality: int,
        repetitions: int,
        ease_factor: float,
        interval: int
    ) -> tuple[int, float, int]:
        """
        Calculate next review date using SM-2 algorithm.

        Args:
            quality: Answer quality (0-5)
                0: Complete blackout
                1: Incorrect, but remembered
                2: Incorrect, but easy to recall
                3: Correct, but difficult
                4: Correct, after some hesitation
                5: Perfect recall
            repetitions: Number of consecutive correct responses
            ease_factor: Ease factor (difficulty multiplier)
            interval: Current interval in days

        Returns:
            (new_interval, new_ease_factor, new_repetitions)
        """
        if quality < 3:
            # Reset on poor performance
            new_repetitions = 0
            new_interval = 1
            new_ease_factor = ease_factor
        else:
            # Good performance
            if repetitions == 0:
                new_interval = 1
            elif repetitions == 1:
                new_interval = 6
            else:
                new_interval = int(interval * ease_factor)

            new_repetitions = repetitions + 1

            # Adjust ease factor
            new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

            # Ease factor should be at least 1.3
            if new_ease_factor < 1.3:
                new_ease_factor = 1.3

        return new_interval, new_ease_factor, new_repetitions


class FlashcardManager:
    """Manage flashcard data and operations."""

    def __init__(self, cards_file: str):
        """Initialize flashcard manager.

        Args:
            cards_file: Path to flashcards JSON file
        """
        self.cards_file = Path(cards_file)
        self.data = self._load_cards()

    def _load_cards(self) -> Dict:
        """Load flashcards from JSON file."""
        if not self.cards_file.exists():
            console.print(f"[red]Error: Flashcard file not found: {self.cards_file}[/red]")
            sys.exit(1)

        with open(self.cards_file, 'r') as f:
            return json.load(f)

    def save_cards(self):
        """Save flashcards to JSON file."""
        with open(self.cards_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get_cards(self, category: Optional[str] = None) -> List[Dict]:
        """Get all cards, optionally filtered by category.

        Args:
            category: Category to filter by (None = all)

        Returns:
            List of flashcard dictionaries
        """
        cards = self.data['cards']
        if category:
            cards = [c for c in cards if c['category'] == category]
        return cards

    def get_due_cards(self, category: Optional[str] = None) -> List[Dict]:
        """Get cards that are due for review.

        Args:
            category: Category to filter by (None = all)

        Returns:
            List of due flashcard dictionaries
        """
        today = datetime.now().date()
        cards = self.get_cards(category)

        due_cards = []
        for card in cards:
            if card['next_review'] is None:
                # Never reviewed
                due_cards.append(card)
            else:
                next_review = datetime.fromisoformat(card['next_review']).date()
                if next_review <= today:
                    due_cards.append(card)

        return due_cards

    def update_card(self, card_id: int, quality: int):
        """Update card after review.

        Args:
            card_id: Card ID
            quality: Answer quality (0-5)
        """
        for card in self.data['cards']:
            if card['id'] == card_id:
                # Calculate new schedule
                new_interval, new_ease_factor, new_repetitions = SpacedRepetition.calculate_next_review(
                    quality=quality,
                    repetitions=card['repetitions'],
                    ease_factor=card['ease_factor'],
                    interval=card['interval']
                )

                # Update card
                card['interval'] = new_interval
                card['ease_factor'] = new_ease_factor
                card['repetitions'] = new_repetitions
                card['last_reviewed'] = datetime.now().isoformat()
                card['next_review'] = (datetime.now() + timedelta(days=new_interval)).isoformat()
                card['confidence'] = min(5, quality)

                self.save_cards()
                break

    def get_categories(self) -> List[str]:
        """Get list of all categories."""
        return list(set(card['category'] for card in self.data['cards']))

    def get_stats(self) -> Dict:
        """Get statistics about flashcards."""
        cards = self.data['cards']
        total = len(cards)
        reviewed = sum(1 for c in cards if c['last_reviewed'] is not None)
        mastered = sum(1 for c in cards if c['confidence'] >= 4)
        due = len(self.get_due_cards())

        return {
            'total': total,
            'reviewed': reviewed,
            'mastered': mastered,
            'due': due,
            'avg_confidence': sum(c['confidence'] for c in cards) / total if total > 0 else 0
        }


class FlashcardCLI:
    """Interactive flashcard CLI."""

    def __init__(self, manager: FlashcardManager):
        """Initialize CLI.

        Args:
            manager: FlashcardManager instance
        """
        self.manager = manager

    def show_main_menu(self):
        """Display main menu."""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]Interview Prep Flashcards[/bold cyan]\n"
            "[dim]Spaced Repetition Learning System[/dim]",
            border_style="cyan"
        ))

        stats = self.manager.get_stats()
        console.print(f"\n[bold]Statistics:[/bold]")
        console.print(f"   Total Cards: {stats['total']}")
        console.print(f"   Reviewed: {stats['reviewed']}")
        console.print(f"   Mastered (confidence ≥4): {stats['mastered']}")
        console.print(f"   Due for Review: [yellow]{stats['due']}[/yellow]")
        console.print(f"   Average Confidence: {stats['avg_confidence']:.1f}/5")

        console.print("\n[bold]Options:[/bold]")
        console.print("  1. Start study session (all due cards)")
        console.print("  2. Study specific category")
        console.print("  3. View all categories")
        console.print("  4. Show statistics")
        console.print("  5. Exit")

    def study_session(self, category: Optional[str] = None):
        """Run a study session.

        Args:
            category: Category to study (None = all)
        """
        due_cards = self.manager.get_due_cards(category)

        if not due_cards:
            console.print("[yellow]No cards due for review! Great job! 🎉[/yellow]")
            Prompt.ask("\nPress Enter to continue")
            return

        console.print(f"\n[cyan]Starting study session with {len(due_cards)} cards...[/cyan]\n")
        Confirm.ask("Ready to start?", default=True)

        correct_count = 0
        total_count = len(due_cards)

        for i, card in enumerate(due_cards, 1):
            console.clear()
            console.print(f"[dim]Card {i}/{total_count}[/dim]\n")

            # Show question
            console.print(Panel(
                f"[bold]{card['question']}[/bold]",
                title=f"📁 {card['category']}",
                border_style="cyan"
            ))

            console.print("\n[dim]Think about your answer...[/dim]")
            Prompt.ask("\nPress Enter when ready to see the answer")

            # Show answer
            console.print("\n" + "=" * 60)
            console.print(Panel(
                Markdown(card['answer']),
                title="Answer",
                border_style="green"
            ))

            # Get self-assessment
            console.print("\n[bold]How well did you know this?[/bold]")
            console.print("  0: Complete blackout (forgot completely)")
            console.print("  1: Incorrect, but remembered something")
            console.print("  2: Incorrect, but close")
            console.print("  3: [yellow]Correct, but difficult[/yellow]")
            console.print("  4: [green]Correct, after hesitation[/green]")
            console.print("  5: [bold green]Perfect recall![/bold green]")

            quality = -1
            while quality < 0 or quality > 5:
                try:
                    quality = int(Prompt.ask("\nYour rating (0-5)", default="3"))
                    if quality < 0 or quality > 5:
                        console.print("[red]Please enter a number between 0 and 5[/red]")
                except ValueError:
                    console.print("[red]Please enter a valid number[/red]")

            # Update card
            self.manager.update_card(card['id'], quality)

            if quality >= 3:
                correct_count += 1
                console.print("[green]Good job![/green]")
            else:
                console.print("[yellow]📝 We'll review this again soon.[/yellow]")

            # Show next review date
            for c in self.manager.data['cards']:
                if c['id'] == card['id']:
                    next_review = datetime.fromisoformat(c['next_review']).strftime('%Y-%m-%d')
                    console.print(f"[dim]Next review: {next_review}[/dim]")
                    break

            if i < total_count:
                Prompt.ask("\nPress Enter for next card")

        # Session summary
        console.clear()
        console.print(Panel.fit(
            f"[bold green]🎉 Session Complete![/bold green]\n\n"
            f"Cards reviewed: {total_count}\n"
            f"Good recalls (≥3): {correct_count}/{total_count} ({correct_count/total_count*100:.0f}%)\n\n"
            f"[dim]Great work! Keep it up! 💪[/dim]",
            border_style="green"
        ))
        Prompt.ask("\nPress Enter to continue")

    def show_categories(self):
        """Display all categories."""
        console.clear()
        categories = self.manager.get_categories()

        table = Table(title="📁 Flashcard Categories", box=box.ROUNDED)
        table.add_column("Category", style="cyan")
        table.add_column("Total Cards", justify="center")
        table.add_column("Due", justify="center", style="yellow")

        for category in sorted(categories):
            cards = self.manager.get_cards(category)
            due = len(self.manager.get_due_cards(category))
            table.add_row(category, str(len(cards)), str(due))

        console.print(table)
        Prompt.ask("\nPress Enter to continue")

    def run(self):
        """Run the main CLI loop."""
        while True:
            self.show_main_menu()

            choice = Prompt.ask("\nChoose an option", choices=["1", "2", "3", "4", "5"], default="1")

            if choice == "1":
                self.study_session()
            elif choice == "2":
                categories = self.manager.get_categories()
                console.print("\n[bold]Categories:[/bold]")
                for i, cat in enumerate(sorted(categories), 1):
                    console.print(f"  {i}. {cat}")

                cat_choice = Prompt.ask("\nChoose category number")
                try:
                    cat_idx = int(cat_choice) - 1
                    if 0 <= cat_idx < len(categories):
                        self.study_session(sorted(categories)[cat_idx])
                except ValueError:
                    console.print("[red]Invalid choice[/red]")
            elif choice == "3":
                self.show_categories()
            elif choice == "4":
                # Stats already shown in main menu
                Prompt.ask("\nPress Enter to continue")
            elif choice == "5":
                console.print("\n[cyan]Happy studying![/cyan]")
                break


def main():
    """Main entry point."""
    # Determine cards file path
    script_dir = Path(__file__).parent
    cards_file = script_dir / "cards.json"

    # Initialize manager and CLI
    manager = FlashcardManager(str(cards_file))
    cli = FlashcardCLI(manager)

    # Run CLI
    cli.run()


if __name__ == "__main__":
    main()
