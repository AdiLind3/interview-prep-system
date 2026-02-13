# -*- coding: utf-8 -*-
"""Searchable cheatsheet utility for interview prep system.

Searches through SQL and Python cheatsheet markdown files,
finds sections matching search terms, and displays results
with syntax highlighting using the rich library.

Usage:
    python utils/search_cheatsheet.py "window function"
    python utils/search_cheatsheet.py "JOIN" "CTE"
    python utils/search_cheatsheet.py --list-sections
"""

import argparse
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.logging import RichHandler

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logger = logging.getLogger("search_cheatsheet")
logger.setLevel(logging.DEBUG)

_handler = RichHandler(show_time=True, show_path=False, markup=True)
_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_handler)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

CHEATSHEET_PATHS: dict[str, Path] = {
    "SQL": ROOT_DIR / "sql" / "cheatsheet.md",
    "Python": ROOT_DIR / "python" / "cheatsheet.md",
}

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Section:
    """Represents a single heading-level section from a cheatsheet."""

    source: str          # e.g. "SQL" or "Python"
    heading: str         # full heading text (without leading #)
    level: int           # heading depth (2 = ##, 3 = ###, etc.)
    body: str            # raw markdown body under the heading
    line_number: int     # 1-based line number in the source file


@dataclass
class SearchResult:
    """A section that matched a search query."""

    section: Section
    matched_terms: list[str] = field(default_factory=list)

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_cheatsheet(source_name: str, path: Path) -> list[Section]:
    """Parse a markdown cheatsheet into a list of Section objects.

    Each section starts at a heading line (##, ###, etc.) and ends
    just before the next heading of equal or higher level.

    Args:
        source_name: Human-readable label for the cheatsheet (e.g. "SQL").
        path: Path to the markdown file.

    Returns:
        List of parsed Section objects.
    """
    if not path.exists():
        logger.warning("Cheatsheet not found: %s", path)
        return []

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    heading_re = re.compile(r"^(#{2,6})\s+(.*)")

    sections: list[Section] = []
    current_heading: Optional[str] = None
    current_level: int = 0
    current_body_lines: list[str] = []
    current_line: int = 0

    def _flush() -> None:
        if current_heading is not None:
            body = "\n".join(current_body_lines).strip()
            sections.append(
                Section(
                    source=source_name,
                    heading=current_heading,
                    level=current_level,
                    body=body,
                    line_number=current_line,
                )
            )

    for idx, line in enumerate(lines, start=1):
        match = heading_re.match(line)
        if match:
            _flush()
            current_level = len(match.group(1))
            current_heading = match.group(2).strip()
            current_body_lines = []
            current_line = idx
        else:
            current_body_lines.append(line)

    _flush()

    logger.debug("Parsed %d sections from %s (%s)", len(sections), source_name, path)
    return sections


def load_all_sections() -> list[Section]:
    """Load sections from every registered cheatsheet.

    Returns:
        Combined list of Section objects from all cheatsheets.
    """
    all_sections: list[Section] = []
    for name, path in CHEATSHEET_PATHS.items():
        all_sections.extend(parse_cheatsheet(name, path))
    logger.info("Loaded %d total sections from %d cheatsheets", len(all_sections), len(CHEATSHEET_PATHS))
    return all_sections

# ---------------------------------------------------------------------------
# Searching
# ---------------------------------------------------------------------------


def search_sections(sections: list[Section], terms: list[str]) -> list[SearchResult]:
    """Search sections for one or more terms (case-insensitive).

    A section matches if *any* of the given terms appear in the
    heading or body text.

    Args:
        sections: List of Section objects to search.
        terms: One or more search strings.

    Returns:
        List of SearchResult objects sorted by relevance (number of
        matched terms descending, then by source file order).
    """
    results: list[SearchResult] = []

    for section in sections:
        haystack = (section.heading + "\n" + section.body).lower()
        matched: list[str] = []
        for term in terms:
            if term.lower() in haystack:
                matched.append(term)
        if matched:
            results.append(SearchResult(section=section, matched_terms=matched))

    # Sort: more matched terms first, then preserve file order.
    results.sort(key=lambda r: -len(r.matched_terms))

    logger.info("Found %d matching sections for terms: %s", len(results), terms)
    return results

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def _highlight_terms(text: str, terms: list[str]) -> Text:
    """Build a rich Text object with search terms highlighted.

    Args:
        text: The plain text to render.
        terms: Terms to highlight.

    Returns:
        A rich Text object with highlighted matches.
    """
    rich_text = Text(text)
    for term in terms:
        # Case-insensitive highlight
        start = 0
        lower_text = text.lower()
        lower_term = term.lower()
        while True:
            idx = lower_text.find(lower_term, start)
            if idx == -1:
                break
            rich_text.stylize("bold yellow", idx, idx + len(term))
            start = idx + len(term)
    return rich_text


def _render_code_blocks(body: str, terms: list[str], console: Console) -> None:
    """Render the section body, using Syntax for code blocks and
    highlighted Text for prose.

    Args:
        body: Raw markdown body text.
        terms: Search terms for highlighting.
        console: Rich Console to print to.
    """
    code_block_re = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)
    last_end = 0

    for match in code_block_re.finditer(body):
        # Print prose before this code block
        prose = body[last_end:match.start()].strip()
        if prose:
            console.print(_highlight_terms(prose, terms))

        lang = match.group(1) or "text"
        code = match.group(2).rstrip()
        try:
            syntax = Syntax(code, lang, theme="monokai", line_numbers=False, word_wrap=True)
            console.print(syntax)
        except Exception:
            # Fallback if the language is not recognized
            console.print(_highlight_terms(code, terms))

        last_end = match.end()

    # Print any remaining prose after the last code block
    remaining = body[last_end:].strip()
    if remaining:
        console.print(_highlight_terms(remaining, terms))


def display_results(results: list[SearchResult], console: Console) -> None:
    """Display search results as styled panels in the terminal.

    Args:
        results: List of SearchResult objects.
        console: Rich Console instance.
    """
    if not results:
        console.print("[bold red]No matching sections found.[/bold red]")
        return

    console.print(
        f"\n[bold green]Found {len(results)} matching section(s).[/bold green]\n"
    )

    for idx, result in enumerate(results, start=1):
        sec = result.section
        tag = f"[{sec.source} cheatsheet, line {sec.line_number}]"
        title = f"{idx}. {sec.heading}  {tag}"
        matched_label = ", ".join(result.matched_terms)

        header_text = Text()
        header_text.append("Source: ", style="dim")
        header_text.append(sec.source, style="bold cyan")
        header_text.append("  |  Matched: ", style="dim")
        header_text.append(matched_label, style="bold yellow")

        console.print(
            Panel(
                header_text,
                title=escape(title),
                title_align="left",
                border_style="blue",
                expand=True,
            )
        )

        _render_code_blocks(sec.body, result.matched_terms, console)
        console.print()  # blank line between results


def list_all_sections(sections: list[Section], console: Console) -> None:
    """Print all section headings grouped by cheatsheet source.

    Args:
        sections: All parsed sections.
        console: Rich Console instance.
    """
    from collections import defaultdict

    grouped: dict[str, list[Section]] = defaultdict(list)
    for sec in sections:
        grouped[sec.source].append(sec)

    for source, secs in grouped.items():
        console.print(f"\n[bold cyan]{source} Cheatsheet[/bold cyan]")
        console.print("-" * 40)
        for sec in secs:
            indent = "  " * (sec.level - 2)
            console.print(f"  {indent}{sec.heading}")

# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        description="Search the SQL and Python cheatsheets for quick reference.",
        epilog="Examples:\n"
               '  python utils/search_cheatsheet.py "window function"\n'
               '  python utils/search_cheatsheet.py "JOIN" "CTE"\n'
               "  python utils/search_cheatsheet.py --list-sections\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "terms",
        nargs="*",
        help="One or more search terms (case-insensitive).",
    )
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List all available section headings and exit.",
    )
    parser.add_argument(
        "--source",
        choices=["sql", "python", "all"],
        default="all",
        help="Limit search to a specific cheatsheet (default: all).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output.",
    )
    return parser


def main() -> None:
    """Main entry point for the search_cheatsheet CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.verbose:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.DEBUG)

    console = Console()

    # Load sections
    all_sections = load_all_sections()

    # Optionally filter by source
    if args.source != "all":
        source_label = args.source.capitalize()
        if args.source == "sql":
            source_label = "SQL"
        all_sections = [s for s in all_sections if s.source == source_label]

    # List mode
    if args.list_sections:
        list_all_sections(all_sections, console)
        return

    # Search mode -- require at least one term
    if not args.terms:
        parser.print_help()
        sys.exit(1)

    results = search_sections(all_sections, args.terms)
    display_results(results, console)


if __name__ == "__main__":
    main()
