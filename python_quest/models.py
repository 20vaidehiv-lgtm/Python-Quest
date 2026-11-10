"""Data models for Python Quest terminal prototype."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
import json
from pathlib import Path


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ChallengeType(str, Enum):
    MCQ = "mcq"                    # Multiple choice
    PREDICT_OUTPUT = "predict"     # What does this code print?
    FILL_BLANK = "fill_blank"      # Fill in the missing code


@dataclass
class Challenge:
    id: int
    title: str
    description: str
    difficulty: Difficulty
    type: ChallengeType
    topic: str
    xp_reward: int
    # Type-specific fields
    question: str = ""                    # For MCQ: the question
    options: list[str] = field(default_factory=list)  # For MCQ: options
    correct_answer: str = ""              # For MCQ: correct option letter (A/B/C/D)
    code_snippet: str = ""                # For PREDICT/FILL: code to show
    expected_output: str = ""             # For PREDICT: expected output
    blank_code: str = ""                  # For FILL: code with _____ blanks
    blank_answer: str = ""                # For FILL: what goes in the blank
    order_index: int = 0

    @property
    def difficulty_label(self) -> str:
        return self.difficulty.value.capitalize()

    @property
    def xp_color(self) -> str:
        if self.difficulty == Difficulty.EASY:
            return "#7CFF6B"   # lime
        elif self.difficulty == Difficulty.MEDIUM:
            return "#FF5DA2"   # pink
        return "#00E5FF"       # cyan


@dataclass
class User:
    username: str
    xp: int = 0
    level: int = 1
    streak: int = 0
    completed_challenges: list[int] = field(default_factory=list)
    last_active: str = ""  # ISO date string

    # Level thresholds: level -> min XP required
    LEVEL_THRESHOLDS = {
        1: 0, 2: 100, 3: 300, 4: 650, 5: 1200,
        6: 2000, 7: 3100, 8: 4600, 9: 6600, 10: 9200,
    }

    @property
    def xp_for_next_level(self) -> int:
        next_level = self.level + 1
        return self.LEVEL_THRESHOLDS.get(next_level, 999999)

    @property
    def xp_progress_in_level(self) -> int:
        current_threshold = self.LEVEL_THRESHOLDS.get(self.level, 0)
        return self.xp - current_threshold

    @property
    def xp_needed_for_level(self) -> int:
        current_threshold = self.LEVEL_THRESHOLDS.get(self.level, 0)
        next_threshold = self.LEVEL_THRESHOLDS.get(self.level + 1, 999999)
        return next_threshold - current_threshold

    @property
    def progress_percent(self) -> float:
        if self.xp_needed_for_level == 0:
            return 100.0
        return min(100.0, (self.xp_progress_in_level / self.xp_needed_for_level) * 100)

    def add_xp(self, amount: int) -> tuple[int, bool]:
        """Add XP and return (new_level, leveled_up)."""
        old_level = self.level
        self.xp += amount
        # Recalculate level
        for lvl in range(old_level + 1, 11):
            if self.xp >= self.LEVEL_THRESHOLDS[lvl]:
                self.level = lvl
            else:
                break
        return self.level, self.level > old_level


@dataclass
class GameState:
    user: User
    challenges: list[Challenge]
    data_file: Path = Path("quest_data.json")

    def save(self) -> None:
        data = {
            "user": {
                "username": self.user.username,
                "xp": self.user.xp,
                "level": self.user.level,
                "streak": self.user.streak,
                "completed_challenges": self.user.completed_challenges,
                "last_active": self.user.last_active,
            }
        }
        self.data_file.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, challenges: list[Challenge], data_file: Path = Path("quest_data.json")) -> "GameState":
        if data_file.exists():
            data = json.loads(data_file.read_text())
            user_data = data.get("user", {})
            user = User(
                username=user_data.get("username", "Player"),
                xp=user_data.get("xp", 0),
                level=user_data.get("level", 1),
                streak=user_data.get("streak", 0),
                completed_challenges=user_data.get("completed_challenges", []),
                last_active=user_data.get("last_active", ""),
            )
        else:
            user = User(username="Player")
        return cls(user=user, challenges=challenges, data_file=data_file)

    def get_challenge(self, challenge_id: int) -> Optional[Challenge]:
        for c in self.challenges:
            if c.id == challenge_id:
                return c
        return None

    def get_next_challenge(self) -> Optional[Challenge]:
        for c in sorted(self.challenges, key=lambda x: x.order_index):
            if c.id not in self.user.completed_challenges:
                return c
        return None

    def get_challenges_by_topic(self, topic: str) -> list[Challenge]:
        return [c for c in self.challenges if c.topic == topic]

    def get_available_topics(self) -> list[str]:
        return sorted(set(c.topic for c in self.challenges))