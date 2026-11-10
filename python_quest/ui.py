"""Rich-based UI components with synthwave theme for Python Quest."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from rich.columns import Columns
from rich.align import Align
from rich.rule import Rule
from rich.prompt import Prompt, Confirm
from rich import box
from typing import Optional

from python_quest.models import User, Challenge, Difficulty, ChallengeType, GameState


# ─── Synthwave Color Palette ───
SYNTH = {
    "bg": "#2B193D",        # Deep purple background
    "fg": "#FDF0D5",        # Warm cream for text
    "pink": "#FF5DA2",      # Hot pink - primary accent
    "cyan": "#00E5FF",      # Electric cyan - secondary accent
    "lime": "#7CFF6B",      # Neon lime - highlights/success
    "purple": "#2B193D",    # Base purple
    "dark_purple": "#1A0D2B", # Darker for panels
    "muted": "#6B5B8A",     # Muted purple for secondary text
}

console = Console()


def synth_gradient(text: str, start: str = SYNTH["pink"], end: str = SYNTH["cyan"]) -> Text:
    """Create a gradient text effect."""
    t = Text(text)
    t.stylize(f"gradient({start},{end})")
    return t


def style_xp(amount: int) -> Text:
    return Text(f"+{amount} XP", style=f"bold {SYNTH['lime']}")


def style_level(level: int) -> Text:
    return Text(f"LVL {level}", style=f"bold {SYNTH['cyan']} on {SYNTH['bg']}")


def difficulty_badge(difficulty: Difficulty) -> Text:
    colors = {
        Difficulty.EASY: SYNTH["lime"],
        Difficulty.MEDIUM: SYNTH["pink"],
        Difficulty.HARD: SYNTH["cyan"],
    }
    return Text(f" {difficulty.value.upper()} ", style=f"bold {SYNTH['bg']} on {colors[difficulty]}")


def challenge_type_icon(ctype: ChallengeType) -> str:
    icons = {
        ChallengeType.MCQ: "◉",
        ChallengeType.PREDICT_OUTPUT: "▶",
        ChallengeType.FILL_BLANK: "␣",
    }
    return icons.get(ctype, "?")


def render_header(title: str, subtitle: str = "") -> Panel:
    header_text = Text()
    header_text.append("╭─ ", style=SYNTH["muted"])
    header_text.append("PYTHON QUEST", style=f"bold {SYNTH['pink']}")
    header_text.append(" ─╮", style=SYNTH["muted"])
    if subtitle:
        header_text.append("\n")
        header_text.append("│ ", style=SYNTH["muted"])
        header_text.append(subtitle, style=SYNTH["cyan"])
        header_text.append(" │", style=SYNTH["muted"])
    header_text.append("\n╰", style=SYNTH["muted"])
    header_text.append("─" * (len(title) + 10), style=SYNTH["muted"])
    header_text.append("╯", style=SYNTH["muted"])

    return Panel(
        Align.center(header_text),
        border_style=SYNTH["pink"],
        padding=(0, 2),
        style=f"on {SYNTH['bg']}",
    )


def render_user_bar(user: User) -> Panel:
    # XP Bar
    progress_text = Text()
    progress_text.append(f"XP: {user.xp_progress_in_level}/{user.xp_needed_for_level} ", style=SYNTH["fg"])
    progress_text.append(f"({user.progress_percent:.0f}%)", style=SYNTH["muted"])

    # Build visual bar
    bar_width = 30
    filled = int(bar_width * user.progress_percent / 100)
    bar = "█" * filled + "░" * (bar_width - filled)
    bar_text = Text(bar, style=SYNTH["pink"])

    # Streak
    streak_text = Text()
    streak_text.append("🔥 ", style=SYNTH["pink"])
    streak_text.append(f"Streak: {user.streak} days", style=SYNTH["fg"])

    # Level
    level_text = Text()
    level_text.append("✨ ", style=SYNTH["cyan"])
    level_text.append(f"Level {user.level}", style=f"bold {SYNTH['cyan']}")

    content = Columns([level_text, progress_text, streak_text], equal=True, expand=True)

    return Panel(
        content,
        title=synth_gradient(" ◆ PLAYER STATS ◆ "),
        border_style=SYNTH["cyan"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def render_challenge_card(challenge: Challenge, show_answer: bool = False) -> Panel:
    # Header with ID, type, difficulty
    header = Text()
    header.append(f"#{challenge.id:02d} ", style=SYNTH["muted"])
    header.append(f"{challenge_type_icon(challenge.type)} ", style=f"bold {SYNTH['cyan']}")
    header.append(challenge.title, style=f"bold {SYNTH['fg']}")
    header.append(" ")
    header.append(difficulty_badge(challenge.difficulty))
    header.append(f"  {challenge.xp_reward} XP", style=SYNTH["lime"])

    # Description
    desc = Text(challenge.description, style=SYNTH["muted"])

    # Challenge content based on type
    content_parts = [header, Text(""), desc, Text("")]

    if challenge.type == ChallengeType.MCQ:
        content_parts.append(Text(challenge.question, style=f"bold {SYNTH['fg']}"))
        content_parts.append(Text(""))
        for i, opt in enumerate(challenge.options):
            letter = chr(65 + i)
            prefix = "▸ " if show_answer and letter == challenge.correct_answer else "  "
            style = SYNTH["lime"] if show_answer and letter == challenge.correct_answer else SYNTH["fg"]
            content_parts.append(Text(f"{prefix}{letter}) {opt}", style=style))

    elif challenge.type == ChallengeType.PREDICT_OUTPUT:
        content_parts.append(Text("What does this code print?", style=f"bold {SYNTH['cyan']}"))
        content_parts.append(Text(""))
        # Code block
        code_lines = challenge.code_snippet.split("\n")
        for line in code_lines:
            content_parts.append(Text(f"  {line}", style=SYNTH["cyan"]))
        content_parts.append(Text(""))
        if show_answer:
            content_parts.append(Text("Expected Output:", style=f"bold {SYNTH['lime']}"))
            content_parts.append(Text(""))
            for line in challenge.expected_output.split("\n"):
                content_parts.append(Text(f"  {line}", style=SYNTH["lime"]))

    elif challenge.type == ChallengeType.FILL_BLANK:
        content_parts.append(Text("Fill in the blank:", style=f"bold {SYNTH['cyan']}"))
        content_parts.append(Text(""))
        code_lines = challenge.blank_code.split("\n")
        for line in code_lines:
            if "______" in line:
                if show_answer:
                    line = line.replace("______", f"[{challenge.blank_answer}]")
                    content_parts.append(Text(f"  {line}", style=SYNTH["lime"]))
                else:
                    content_parts.append(Text(f"  {line}", style=SYNTH["pink"]))
            else:
                content_parts.append(Text(f"  {line}", style=SYNTH["cyan"]))
        content_parts.append(Text(""))
        if show_answer:
            content_parts.append(Text(f"Answer: {challenge.blank_answer}", style=f"bold {SYNTH['lime']}"))

    return Panel(
        Align.left(Text.assemble(*content_parts)),
        border_style=SYNTH["pink"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def render_challenge_list(challenges: list[Challenge], user: User, current_topic: Optional[str] = None) -> Table:
    table = Table(
        box=box.ROUNDED,
        border_style=SYNTH["pink"],
        header_style=f"bold {SYNTH['cyan']}",
        style=f"on {SYNTH['dark_purple']}",
        show_lines=False,
    )
    table.add_column("#", width=4, style=SYNTH["muted"])
    table.add_column("Challenge", style=SYNTH["fg"])
    table.add_column("Type", width=12, justify="center")
    table.add_column("Diff", width=8, justify="center")
    table.add_column("XP", width=6, justify="right", style=SYNTH["lime"])
    table.add_column("Status", width=10, justify="center")

    for c in challenges:
        if current_topic and c.topic != current_topic:
            continue

        completed = c.id in user.completed_challenges
        status = "✓ DONE" if completed else "○ TODO"
        status_style = SYNTH["lime"] if completed else SYNTH["muted"]

        type_label = c.type.value.replace("_", " ").title()

        row_style = SYNTH["muted"] if completed else None
        table.add_row(
            str(c.id),
            c.title,
            Text(type_label, style=SYNTH["cyan"]),
            difficulty_badge(c.difficulty),
            str(c.xp_reward),
            Text(status, style=status_style),
            style=row_style,
        )

    return table


def render_topic_selector(topics: list[str], current: Optional[str] = None) -> Panel:
    buttons = []
    for t in topics:
        label = t.replace("_", " ").title()
        if t == current:
            btn = Text(f"[{label}]", style=f"bold {SYNTH['bg']} on {SYNTH['pink']}")
        else:
            btn = Text(f" {label} ", style=f"{SYNTH['fg']} on {SYNTH['dark_purple']}")
        buttons.append(btn)

    return Panel(
        Columns(buttons, equal=True, expand=True),
        title=synth_gradient(" ◆ TOPICS ◆ "),
        border_style=SYNTH["cyan"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def render_badge_grid(badges: list[dict], earned: set[str]) -> Panel:
    """Render badges in a grid."""
    rows = []
    for i, badge in enumerate(badges):
        is_earned = badge["id"] in earned
        icon = badge["icon"]
        name = badge["name"]
        if is_earned:
            badge_text = Text(f"{icon} {name}", style=f"bold {SYNTH['lime']}")
        else:
            badge_text = Text(f"{icon} {name}", style=SYNTH["muted"])
        rows.append(badge_text)

    return Panel(
        Columns(rows, equal=True, expand=True),
        title=synth_gradient(" ◆ BADGES ◆ "),
        border_style=SYNTH["pink"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def render_leaderboard(entries: list[dict]) -> Table:
    table = Table(
        box=box.ROUNDED,
        border_style=SYNTH["pink"],
        header_style=f"bold {SYNTH['cyan']}",
        style=f"on {SYNTH['dark_purple']}",
    )
    table.add_column("Rank", width=6, justify="right", style=SYNTH["pink"])
    table.add_column("Username", style=SYNTH["fg"])
    table.add_column("Level", width=8, justify="center", style=SYNTH["cyan"])
    table.add_column("XP", width=10, justify="right", style=SYNTH["lime"])

    for i, entry in enumerate(entries, 1):
        rank_style = SYNTH["pink"] if i <= 3 else SYNTH["fg"]
        table.add_row(
            f"#{i}",
            entry["username"],
            str(entry["level"]),
            str(entry["xp"]),
            style=rank_style,
        )

    return table


def render_celebration(message: str, xp_earned: int, leveled_up: bool, new_level: int) -> Panel:
    content = Text()
    content.append("🎉 ", style=SYNTH["pink"])
    content.append(message, style=f"bold {SYNTH['fg']}")
    content.append("\n\n")
    content.append(style_xp(xp_earned))
    if leveled_up:
        content.append("\n\n")
        content.append("⬆ LEVEL UP! ", style=f"bold {SYNTH['cyan']} on {SYNTH['bg']}")
        content.append(style_level(new_level))

    return Panel(
        Align.center(content),
        border_style=SYNTH["lime"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(2, 4),
    )


def render_error(message: str) -> Panel:
    return Panel(
        Text(message, style=f"bold {SYNTH['pink']}"),
        border_style=SYNTH["pink"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def render_success(message: str) -> Panel:
    return Panel(
        Text(message, style=f"bold {SYNTH['lime']}"),
        border_style=SYNTH["lime"],
        style=f"on {SYNTH['dark_purple']}",
        padding=(1, 2),
    )


def clear_screen():
    console.clear()


def print_header(title: str, subtitle: str = ""):
    console.print(render_header(title, subtitle))
    console.print()


def print_user_bar(user: User):
    console.print(render_user_bar(user))
    console.print()


def print_challenge(challenge: Challenge, show_answer: bool = False):
    console.print(render_challenge_card(challenge, show_answer))
    console.print()


def print_challenge_list(challenges: list[Challenge], user: User, topic: Optional[str] = None):
    console.print(render_challenge_list(challenges, user, topic))
    console.print()


def print_topics(topics: list[str], current: Optional[str] = None):
    console.print(render_topic_selector(topics, current))
    console.print()


def print_badges(badges: list[dict], earned: set[str]):
    console.print(render_badge_grid(badges, earned))
    console.print()


def print_leaderboard(entries: list[dict]):
    console.print(render_leaderboard(entries))
    console.print()


def print_celebration(message: str, xp_earned: int, leveled_up: bool, new_level: int):
    console.print(render_celebration(message, xp_earned, leveled_up, new_level))
    console.print()


def print_error(message: str):
    console.print(render_error(message))
    console.print()


def print_success(message: str):
    console.print(render_success(message))
    console.print()


def prompt_choice(prompt: str, choices: list[str], default: str = "") -> str:
    return Prompt.ask(
        f"[{SYNTH['cyan']}]{prompt}[/{SYNTH['cyan']}]",
        choices=choices,
        default=default,
        console=console,
    )


def prompt_text(prompt: str, default: str = "") -> str:
    return Prompt.ask(
        f"[{SYNTH['cyan']}]{prompt}[/{SYNTH['cyan']}]",
        default=default,
        console=console,
    )


def prompt_confirm(prompt: str, default: bool = True) -> bool:
    return Confirm.ask(
        f"[{SYNTH['cyan']}]{prompt}[/{SYNTH['cyan']}]",
        default=default,
        console=console,
    )


def pause():
    console.print(f"[{SYNTH['muted']}]Press Enter to continue...[/{SYNTH['muted']}]")
    console.input()