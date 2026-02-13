#!/usr/bin/env python3
"""
Flask web application for Interview Prep System
Mobile-friendly interface for studying on the go
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import os

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from concepts.flashcards.cli import FlashcardManager, SpacedRepetition
from utils.config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interview-prep-2026'

# Initialize paths
BASE_DIR = Path(__file__).parent.parent
FLASHCARDS_FILE = BASE_DIR / "concepts" / "flashcards" / "cards.json"
PROGRESS_FILE = BASE_DIR / "progress" / "tracker.json"
SQL_EXERCISES_DIR = BASE_DIR / "sql" / "exercises"
PYTHON_EXERCISES_DIR = BASE_DIR / "python" / "exercises"


# ============ Helper Functions ============

def load_flashcards():
    """Load flashcards from JSON."""
    with open(FLASHCARDS_FILE, 'r') as f:
        return json.load(f)


def save_flashcards(data):
    """Save flashcards to JSON."""
    with open(FLASHCARDS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_progress():
    """Load progress tracker."""
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)


def save_progress(data):
    """Save progress tracker."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_due_flashcards():
    """Get flashcards due for review."""
    data = load_flashcards()
    today = datetime.now().date()

    due_cards = []
    for card in data['cards']:
        if card['next_review'] is None:
            due_cards.append(card)
        else:
            next_review = datetime.fromisoformat(card['next_review']).date()
            if next_review <= today:
                due_cards.append(card)

    return due_cards


def get_sql_exercises():
    """Get all SQL exercises."""
    exercises = []
    for difficulty in ['easy', 'medium', 'hard']:
        diff_path = SQL_EXERCISES_DIR / difficulty
        if diff_path.exists():
            for exercise_dir in sorted(diff_path.iterdir()):
                if exercise_dir.is_dir():
                    problem_file = exercise_dir / 'problem_statement.md'
                    if problem_file.exists():
                        exercises.append({
                            'id': f"{difficulty}/{exercise_dir.name}",
                            'name': exercise_dir.name.replace('_', ' ').title(),
                            'difficulty': difficulty,
                            'path': str(exercise_dir)
                        })
    return exercises


def get_python_exercises():
    """Get all Python exercises."""
    exercises = []
    for category_dir in PYTHON_EXERCISES_DIR.iterdir():
        if category_dir.is_dir() and category_dir.name != '__pycache__':
            for exercise_file in sorted(category_dir.glob('*.py')):
                exercises.append({
                    'id': f"{category_dir.name}/{exercise_file.name}",
                    'name': exercise_file.stem.replace('_', ' ').title(),
                    'category': category_dir.name.replace('_', ' ').title(),
                    'path': str(exercise_file)
                })
    return exercises


# ============ Routes ============

@app.route('/')
def index():
    """Home page with navigation."""
    progress = load_progress()

    # Calculate stats
    sql_pct = (progress['sql_exercises']['completed'] / progress['sql_exercises']['total'] * 100) if progress['sql_exercises']['total'] > 0 else 0
    python_pct = (progress['python_exercises']['completed'] / progress['python_exercises']['total'] * 100) if progress['python_exercises']['total'] > 0 else 0

    due_count = len(get_due_flashcards())

    days_until = (datetime.fromisoformat(progress['interview_date']).date() - datetime.now().date()).days

    stats = {
        'sql_progress': sql_pct,
        'python_progress': python_pct,
        'flashcards_due': due_count,
        'days_until_interview': days_until,
        'total_time_hours': progress['time_spent_minutes'] / 60
    }

    return render_template('index.html', stats=stats)


@app.route('/flashcards')
def flashcards():
    """Flashcard study interface."""
    data = load_flashcards()
    categories = list(set(card['category'] for card in data['cards']))

    return render_template('flashcards.html', categories=sorted(categories))


@app.route('/api/flashcards/due')
def api_flashcards_due():
    """Get flashcards due for review."""
    category = request.args.get('category', None)

    due_cards = get_due_flashcards()

    if category:
        due_cards = [c for c in due_cards if c['category'] == category]

    # Shuffle for variety
    random.shuffle(due_cards)

    return jsonify({
        'cards': due_cards,
        'count': len(due_cards)
    })


@app.route('/api/flashcards/review', methods=['POST'])
def api_flashcard_review():
    """Update flashcard after review."""
    data = request.json
    card_id = data['card_id']
    quality = data['quality']

    flashcards_data = load_flashcards()

    # Find and update card
    for card in flashcards_data['cards']:
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

            save_flashcards(flashcards_data)

            # Update progress
            progress = load_progress()
            progress['flashcards']['total_reviews'] += 1
            if quality >= 4:
                progress['flashcards']['cards_mastered'] = sum(1 for c in flashcards_data['cards'] if c['confidence'] >= 4)

            # Update average confidence
            total_confidence = sum(c['confidence'] for c in flashcards_data['cards'])
            progress['flashcards']['average_confidence'] = total_confidence / len(flashcards_data['cards'])

            # Update category stats
            progress['flashcards']['by_category'][card['category']] = progress['flashcards']['by_category'].get(card['category'], 0) + 1

            save_progress(progress)

            return jsonify({
                'success': True,
                'next_review': card['next_review']
            })

    return jsonify({'success': False, 'error': 'Card not found'}), 404


@app.route('/progress')
def progress():
    """Progress dashboard."""
    progress_data = load_progress()
    flashcards_data = load_flashcards()

    # Calculate overall progress
    sql_completed = progress_data['sql_exercises']['completed']
    sql_total = progress_data['sql_exercises']['total']
    python_completed = progress_data['python_exercises']['completed']
    python_total = progress_data['python_exercises']['total']

    overall = ((sql_completed + python_completed) / (sql_total + python_total) * 100) if (sql_total + python_total) > 0 else 0

    stats = {
        'overall_progress': overall,
        'sql': progress_data['sql_exercises'],
        'python': progress_data['python_exercises'],
        'flashcards': progress_data['flashcards'],
        'mock_interviews': len(progress_data['mock_interviews']),
        'time_hours': progress_data['time_spent_minutes'] / 60,
        'days_until': (datetime.fromisoformat(progress_data['interview_date']).date() - datetime.now().date()).days
    }

    return render_template('progress.html', stats=stats)


@app.route('/exercises/sql')
def sql_exercises():
    """SQL exercises browser."""
    exercises = get_sql_exercises()
    return render_template('sql_exercises.html', exercises=exercises)


@app.route('/exercises/sql/<difficulty>/<exercise_name>')
def sql_exercise_detail(difficulty, exercise_name):
    """SQL exercise detail view."""
    exercise_path = SQL_EXERCISES_DIR / difficulty / exercise_name

    # Load problem statement
    problem_file = exercise_path / 'problem_statement.md'
    if problem_file.exists():
        with open(problem_file, 'r') as f:
            problem_text = f.read()
    else:
        problem_text = "Problem statement not found"

    # Load schema
    schema_file = exercise_path / 'schema.sql'
    schema_text = ""
    if schema_file.exists():
        with open(schema_file, 'r') as f:
            schema_text = f.read()

    # Load sample data
    data_file = exercise_path / 'sample_data.sql'
    data_text = ""
    if data_file.exists():
        with open(data_file, 'r') as f:
            data_text = f.read()

    # Load solution (for show/hide)
    solution_file = exercise_path / 'solution.sql'
    solution_text = ""
    if solution_file.exists():
        with open(solution_file, 'r', encoding='utf-8') as f:
            solution_text = f.read()

    exercise = {
        'id': f"{difficulty}/{exercise_name}",
        'name': exercise_name.replace('_', ' ').title(),
        'difficulty': difficulty,
        'problem': problem_text,
        'schema': schema_text,
        'sample_data': data_text,
        'solution': solution_text
    }

    return render_template('sql_exercise_detail.html', exercise=exercise)


@app.route('/api/sql/run', methods=['POST'])
def api_sql_run():
    """Run a SQL query against exercise data and validate it."""
    import sqlite3

    data = request.json
    exercise_id = data.get('exercise_id', '')
    user_query = data.get('query', '').strip()

    if not user_query:
        return jsonify({'success': False, 'error': 'Empty query'})

    parts = exercise_id.split('/')
    if len(parts) != 2:
        return jsonify({'success': False, 'error': 'Invalid exercise ID'})

    difficulty, exercise_name = parts
    exercise_path = SQL_EXERCISES_DIR / difficulty / exercise_name

    schema_file = exercise_path / 'schema.sql'
    data_file = exercise_path / 'sample_data.sql'
    expected_file = exercise_path / 'expected_output.json'

    if not schema_file.exists():
        return jsonify({'success': False, 'error': 'Exercise not found'})

    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()

        with open(schema_file, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        with open(data_file, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        cursor.execute(user_query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        result = [dict(zip(columns, row)) for row in rows]

        conn.close()

        # Compare with expected output
        correct = False
        expected = None
        if expected_file.exists():
            with open(expected_file, 'r', encoding='utf-8') as f:
                expected = json.load(f)
            def normalize(val):
                if isinstance(val, float) and val == int(val):
                    return int(val)
                return val
            norm_result = [{k: normalize(v) for k, v in row.items()} for row in result]
            norm_expected = [{k: normalize(v) for k, v in row.items()} for row in expected]
            correct = norm_result == norm_expected

        return jsonify({
            'success': True,
            'correct': correct,
            'columns': columns,
            'rows': [list(row.values()) for row in result],
            'row_count': len(result),
            'expected_count': len(expected) if expected else None
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/exercises/python')
def python_exercises():
    """Python exercises browser."""
    exercises = get_python_exercises()
    return render_template('python_exercises.html', exercises=exercises)


@app.route('/exercises/python/<category>/<exercise_name>')
def python_exercise_detail(category, exercise_name):
    """Python exercise detail view."""
    exercise_path = PYTHON_EXERCISES_DIR / category / exercise_name

    if exercise_path.exists():
        with open(exercise_path, 'r') as f:
            code_text = f.read()
    else:
        code_text = "Exercise not found"

    exercise = {
        'id': f"{category}/{exercise_name}",
        'name': exercise_name.replace('.py', '').replace('_', ' ').title(),
        'category': category.replace('_', ' ').title(),
        'code': code_text
    }

    return render_template('python_exercise_detail.html', exercise=exercise)


@app.route('/resources')
def resources():
    """Learning resources page."""
    links_file = BASE_DIR / 'resources' / 'links.md'

    if links_file.exists():
        with open(links_file, 'r') as f:
            links_text = f.read()
    else:
        links_text = "Resources not found"

    return render_template('resources.html', content=links_text)


@app.route('/cheatsheet/<topic>')
def cheatsheet(topic):
    """View cheat sheets."""
    if topic == 'sql':
        file_path = BASE_DIR / 'sql' / 'cheatsheet.md'
    elif topic == 'python':
        file_path = BASE_DIR / 'python' / 'cheatsheet.md'
    else:
        return "Cheat sheet not found", 404

    if file_path.exists():
        with open(file_path, 'r') as f:
            content = f.read()
    else:
        content = "Cheat sheet not found"

    return render_template('cheatsheet.html', topic=topic.upper(), content=content)


# ============ Run App ============

if __name__ == '__main__':
    # Use PORT environment variable for Render deployment, default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    # Set debug=True for local development, but it will be ignored in production
    app.run(host='0.0.0.0', port=port)