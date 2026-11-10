"""Main CLI application for Python Quest terminal prototype."""
import sys
from typing import Optional
import typer
from rich.console import Console

from python_quest.models import GameState
from python_quest.engine import QuestEngine, create_new_game, load_game
from python_quest.ui import (
    console, clear_screen, print_header, print_user_bar, print_challenge,
    print_challenge_list, print_topics, print_badges, print_leaderboard,
    print_celebration, print_error, print_success, prompt_choice,
    prompt_text, prompt_confirm, pause, SYNTH,
)
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from python_quest.challenges import CHALLENGES


app = typer.Typer(
    name="python-quest",
    help="Python Quest - Learn Python through gamified challenges",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


def get_engine(username: Optional[str] = None) -> QuestEngine:
    """Get or create game engine."""
    if username:
        # Try to load existing, or create new
        try:
            state = GameState.load(CHALLENGES)
            if state.user.username != username:
                state = create_new_game(username)
        except Exception:
            state = create_new_game(username)
    else:
        state = load_game()
    return QuestEngine(state)


@app.command()
def start(
    username: str = typer.Option(None, "--user", "-u", help="Username (creates new if not exists)"),
    new: bool = typer.Option(False, "--new", "-n", help="Force new game"),
):
    """Start or continue your Python Quest adventure."""
    clear_screen()

    # Welcome screen - ASCII safe for Windows
    welcome = Text()
    welcome.append("+", style=SYNTH["pink"])
    welcome.append("=" * 50, style=SYNTH["pink"])
    welcome.append("+\n", style=SYNTH["pink"])
    welcome.append("|", style=SYNTH["pink"])
    welcome.append(" " * 50, style=f"on {SYNTH['bg']}")
    welcome.append("|\n", style=SYNTH["pink"])
    welcome.append("|", style=SYNTH["pink"])
    welcome.append("  PYTHON QUEST  ", style=f"bold {SYNTH['pink']} on {SYNTH['bg']}")
    welcome.append(" " * 32, style=f"on {SYNTH['bg']}")
    welcome.append("|\n", style=SYNTH["pink"])
    welcome.append("|", style=SYNTH["pink"])
    welcome.append("  Learn Python through interactive challenges", style=f"{SYNTH['cyan']} on {SYNTH['bg']}")
    welcome.append(" " * 6, style=f"on {SYNTH['bg']}")
    welcome.append("|\n", style=SYNTH["pink"])
    welcome.append("|", style=SYNTH["pink"])
    welcome.append("  Earn XP + Level Up + Unlock Badges + Build Streaks", style=f"{SYNTH['lime']} on {SYNTH['bg']}")
    welcome.append(" " * 3, style=f"on {SYNTH['bg']}")
    welcome.append("|\n", style=SYNTH["pink"])
    welcome.append("|", style=SYNTH["pink"])
    welcome.append(" " * 50, style=f"on {SYNTH['bg']}")
    welcome.append("|\n", style=SYNTH["pink"])
    welcome.append("+", style=SYNTH["pink"])
    welcome.append("=" * 50, style=SYNTH["pink"])
    welcome.append("+", style=SYNTH["pink"])

    console.print(Align.center(welcome))
    console.print()

    # Get username
    if new or username is None:
        username = prompt_text("Enter your username", "Player")

    # Load or create game
    if new:
        state = create_new_game(username)
        print_success(f"New quest started for {username}!")
    else:
        try:
            state = GameState.load(CHALLENGES)
            if state.user.username != username:
                state = create_new_game(username)
                print_success(f"New quest started for {username}!")
            else:
                print_success(f"Welcome back, {username}!")
        except Exception:
            state = create_new_game(username)
            print_success(f"New quest started for {username}!")

    engine = QuestEngine(state)
    engine.update_streak()

    pause()
    main_menu(engine)


@app.command()
def stats(
    username: str = typer.Option(None, "--user", "-u", help="Username"),
):
    """Show your current stats."""
    engine = get_engine(username)
    show_stats(engine)
    pause()


def show_stats(engine: QuestEngine):
    stats = engine.get_user_stats()
    clear_screen()
    print_header("Your Stats", f"Level {stats['level']} • {stats['xp']} XP")
    print_user_bar(engine.state.user)

    # Progress breakdown
    progress_table = Table(box=None, show_header=False, style=f"on {SYNTH['bg']}")
    progress_table.add_column("Metric", style=SYNTH["fg"])
    progress_table.add_column("Value", style=SYNTH["cyan"], justify="right")

    progress_table.add_row("Challenges Completed", f"{stats['completed']} / {stats['total']}")
    progress_table.add_row("Overall Progress", f"{stats['completion_percent']:.1f}%")
    progress_table.add_row("Current Streak", f"{stats['streak']} days")

    console.print(Panel(
        progress_table,
        title=f"[{SYNTH['pink']}]◆ PROGRESS ◆[/{SYNTH['pink']}]",
        border_style=SYNTH["cyan"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    ))

    # Badges
    earned = engine.get_earned_badge_ids()
    print_badges(engine.badges, earned)


@app.command()
def challenges(
    topic: str = typer.Option(None, "--topic", "-t", help="Filter by topic"),
    username: str = typer.Option(None, "--user", "-u", help="Username"),
):
    """List available challenges."""
    engine = get_engine(username)
    show_challenges(engine, topic)
    pause()


def show_challenges(engine: QuestEngine, topic_filter: Optional[str] = None):
    clear_screen()
    topics = engine.get_available_topics()

    if topic_filter and topic_filter in topics:
        current_topic = topic_filter
    else:
        current_topic = None

    print_header("Challenges", f"{len(engine.state.challenges)} total • {len(topics)} topics")
    print_topics(topics, current_topic)

    challenges_to_show = engine.state.challenges
    if current_topic:
        challenges_to_show = engine.get_challenges_by_topic(current_topic)

    print_challenge_list(challenges_to_show, engine.state.user, current_topic)


@app.command()
def play(
    challenge_id: int = typer.Argument(None, help="Challenge ID to play"),
    username: str = typer.Option(None, "--user", "-u", help="Username"),
):
    """Play a specific challenge."""
    engine = get_engine(username)

    if challenge_id is None:
        # Show challenge list and let user pick
        clear_screen()
        show_challenges(engine)
        challenge_id = int(prompt_text("Enter challenge ID", "1"))

    challenge = engine.state.get_challenge(challenge_id)
    if not challenge:
        print_error(f"Challenge #{challenge_id} not found!")
        return

    play_challenge(engine, challenge)


def play_challenge(engine: QuestEngine, challenge: Challenge):
    clear_screen()
    print_header("Challenge", f"#{challenge.id:02d} • {challenge.title}")
    print_user_bar(engine.state.user)
    print_challenge(challenge)

    # Get answer based on type
    if challenge.type.value == "mcq":
        answer = prompt_choice("Your answer", ["A", "B", "C", "D"])
    else:
        answer = prompt_text("Your answer")

    # Submit
    result = engine.complete_challenge(challenge.id, answer)

    clear_screen()
    print_header("Result", f"#{challenge.id:02d} • {challenge.title}")
    print_user_bar(engine.state.user)
    print_challenge(challenge, show_answer=True)

    if result["correct"]:
        msg = "Correct!" if challenge.type.value != "fill_blank" else "Perfect!"
        print_celebration(msg, result["xp_earned"], result["leveled_up"], result["new_level"])

        if result["badges_earned"]:
            console.print()
            for badge_id in result["badges_earned"]:
                badge = engine.get_badge_info(badge_id)
                if badge:
                    print_success(f"🏆 Badge Unlocked: {badge['icon']} {badge['name']} - {badge['desc']}")
    else:
        print_error(f"Incorrect. {result['feedback']}")

    # Next steps
    console.print()
    next_challenge = engine.get_next_challenge()
    if next_challenge:
        if prompt_confirm(f"Continue to Challenge #{next_challenge.id:02d}?", True):
            play_challenge(engine, next_challenge)
    else:
        print_success("🎉 You've completed all available challenges!")
        pause()


@app.command()
def leaderboard(username: str = typer.Option(None, "--user", "-u", help="Username")):
    """Show the leaderboard (mock data for Phase 1)."""
    engine = get_engine(username)
    clear_screen()
    print_header("Leaderboard", "Top Python Questers")

    # Mock leaderboard data for Phase 1
    mock_entries = [
        {"username": engine.state.user.username, "level": engine.state.user.level, "xp": engine.state.user.xp},
        {"username": "CodeMaster", "level": 8, "xp": 4800},
        {"username": "PyNinja", "level": 6, "xp": 2100},
        {"username": "LoopLover", "level": 5, "xp": 1350},
        {"username": "FunctionFan", "level": 4, "xp": 780},
    ]
    # Sort by XP
    mock_entries.sort(key=lambda x: x["xp"], reverse=True)

    print_leaderboard(mock_entries)
    pause()


def main_menu(engine: QuestEngine):
    """Main interactive menu loop."""
    while True:
        clear_screen()
        stats = engine.get_user_stats()
        print_header("Main Menu", f"Level {stats['level']} • {stats['xp']} XP • {stats['streak']}🔥")
        print_user_bar(engine.state.user)

        # Next challenge suggestion
        next_ch = engine.get_next_challenge()
        if next_ch:
            next_panel = Panel(
                Text.assemble(
                    Text("Next Up: ", style=SYNTH["muted"]),
                    Text(f"#{next_ch.id:02d} {next_ch.title}", style=f"bold {SYNTH['cyan']}"),
                    Text(f" ({next_ch.difficulty_label}, {next_ch.xp_reward} XP)", style=SYNTH["lime"]),
                ),
                border_style=SYNTH["cyan"],
                style=f"on {SYNTH['dark_purple']}",
                padding=(1, 2),
            )
            console.print(next_panel)
            console.print()

        # Menu options
        menu_table = Table(box=None, show_header=False, style=f"on {SYNTH['bg']}")
        menu_table.add_column("Key", style=SYNTH["pink"], width=4)
        menu_table.add_column("Action", style=SYNTH["fg"])

        menu_table.add_row("1", "▶ Play Next Challenge")
        menu_table.add_row("2", "📋 Browse All Challenges")
        menu_table.add_row("3", "📊 View Stats & Badges")
        menu_table.add_row("4", "🏆 Leaderboard")
        menu_table.add_row("5", "⚙️  Settings")
        menu_table.add_row("q", "🚪 Quit")

        console.print(Panel(
            menu_table,
            title=f"[{SYNTH['pink']}]◆ MENU ◆[/{SYNTH['pink']}]",
            border_style=SYNTH["cyan"],
            style=f"on {SYNTH['dark_purple']}",
            padding=(1, 2),
        ))

        choice = prompt_choice("Choose an option", ["1", "2", "3", "4", "5", "q"])

        if choice == "1":
            if next_ch:
                play_challenge(engine, next_ch)
            else:
                print_success("All challenges completed! 🎉")
                pause()
        elif choice == "2":
            browse_challenges_menu(engine)
        elif choice == "3":
            show_stats(engine)
            pause()
        elif choice == "4":
            leaderboard(engine.state.user.username)
        elif choice == "5":
            settings_menu(engine)
        elif choice == "q":
            print_success("Thanks for playing Python Quest! 🐍")
            sys.exit(0)


def browse_challenges_menu(engine: QuestEngine):
    """Interactive challenge browser."""
    while True:
        clear_screen()
        topics = engine.get_available_topics()
        print_header("Browse Challenges")
        print_topics(topics)

        topic = prompt_choice("Select topic (or 'back')", topics + ["back"], "back")
        if topic == "back":
            return

        clear_screen()
        challenges = engine.get_challenges_by_topic(topic)
        print_challenge_list(challenges, engine.state.user, topic)

        challenge_id = prompt_text("Enter challenge ID to play (or 'back')", "back")
        if challenge_id.lower() == "back":
            continue

        try:
            cid = int(challenge_id)
            challenge = engine.state.get_challenge(cid)
            if challenge and challenge.topic == topic:
                play_challenge(engine, challenge)
            else:
                print_error("Invalid challenge ID for this topic")
                pause()
        except ValueError:
            print_error("Please enter a valid number")
            pause()


def settings_menu(engine: QuestEngine):
    """Settings menu."""
    while True:
        clear_screen()
        print_header("Settings")

        menu_table = Table(box=None, show_header=False, style=f"on {SYNTH['bg']}")
        menu_table.add_column("Key", style=SYNTH["pink"], width=4)
        menu_table.add_column("Action", style=SYNTH["fg"])

        menu_table.add_row("1", f"Username: {engine.state.user.username}")
        menu_table.add_row("2", "Reset Progress (DANGER)")
        menu_table.add_row("b", "Back to Main Menu")

        console.print(Panel(
            menu_table,
            border_style=SYNTH["cyan"],
            style=f"on {SYNTH['dark_purple']}",
            padding=(1, 2),
        ))

        choice = prompt_choice("Choose", ["1", "2", "b"])

        if choice == "1":
            new_name = prompt_text("New username", engine.state.user.username)
            engine.state.user.username = new_name
            engine.state.save()
            print_success(f"Username changed to {new_name}")
            pause()
        elif choice == "2":
            if prompt_confirm("⚠️  This will DELETE all progress. Are you sure?", False):
                if prompt_confirm("Really really sure? Type 'yes' to confirm", False):
                    engine.state = create_new_game(engine.state.user.username)
                    print_success("Progress reset. Fresh start!")
                    pause()
        elif choice == "b":
            return


if __name__ == "__main__":
    app()