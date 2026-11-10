"""Game engine - core logic for Python Quest terminal prototype."""
from typing import Optional
from datetime import date
from python_quest.models import GameState, User, Challenge, ChallengeType
from python_quest.challenges import CHALLENGES


class QuestEngine:
    def __init__(self, game_state: GameState):
        self.state = game_state
        self.badges = self._load_badges()

    def _load_badges(self) -> list[dict]:
        return [
            {"id": "first_blood", "name": "First Blood", "icon": "[*]", "desc": "Complete your first challenge"},
            {"id": "getting_started", "name": "Getting Started", "icon": "[+]", "desc": "Complete 5 challenges"},
            {"id": "week_warrior", "name": "Week Warrior", "icon": "[7]", "desc": "7-day streak"},
            {"id": "month_master", "name": "Month Master", "icon": "[30]", "desc": "30-day streak"},
            {"id": "loop_master", "name": "Loop Master", "icon": "[@]", "desc": "Complete all loop challenges"},
            {"id": "function_fanatic", "name": "Function Fanatic", "icon": "[!]", "desc": "Complete all function challenges"},
            {"id": "data_dabbler", "name": "Data Dabbler", "icon": "[#]", "desc": "Complete all data structure challenges"},
            {"id": "speed_runner", "name": "Speed Runner", "icon": "[>]", "desc": "Complete 10 challenges in 1 hour"},
            {"id": "perfectionist", "name": "Perfectionist", "icon": "[100]", "desc": "100% pass rate (min 20 challenges)"},
        ]

    def check_answer(self, challenge: Challenge, user_answer: str) -> tuple[bool, str]:
        """Check if user's answer is correct. Returns (is_correct, feedback)."""
        user_answer = user_answer.strip()

        if challenge.type == ChallengeType.MCQ:
            correct = user_answer.upper() == challenge.correct_answer.upper()
            if correct:
                return True, "Correct! [OK]"
            else:
                return False, f"Not quite. The answer was {challenge.correct_answer}) {challenge.options[ord(challenge.correct_answer) - 65]}"

        elif challenge.type == ChallengeType.PREDICT_OUTPUT:
            # Normalize whitespace for comparison
            expected = challenge.expected_output.strip()
            actual = user_answer.strip()
            correct = expected == actual
            if correct:
                return True, "Spot on! The output matches exactly. [OK]"
            else:
                return False, f"Expected:\n{expected}\n\nGot:\n{actual}"

        elif challenge.type == ChallengeType.FILL_BLANK:
            # For fill-in-the-blank, check if answer matches (case-insensitive, flexible whitespace)
            expected = challenge.blank_answer.strip().lower()
            actual = user_answer.strip().lower()
            # Allow some flexibility - remove extra spaces
            expected_norm = " ".join(expected.split())
            actual_norm = " ".join(actual.split())
            correct = expected_norm == actual_norm
            if correct:
                return True, "Perfect! The blank is filled correctly. [OK]"
            else:
                return False, f"The answer was: {challenge.blank_answer}"

        return False, "Unknown challenge type"

    def complete_challenge(self, challenge_id: int, user_answer: str) -> dict:
        """Process a challenge completion. Returns result dict."""
        challenge = self.state.get_challenge(challenge_id)
        if not challenge:
            return {"success": False, "error": "Challenge not found"}

        if challenge_id in self.state.user.completed_challenges:
            return {"success": False, "error": "Already completed", "already_done": True}

        is_correct, feedback = self.check_answer(challenge, user_answer)

        result = {
            "success": True,
            "challenge": challenge,
            "correct": is_correct,
            "feedback": feedback,
            "xp_earned": 0,
            "leveled_up": False,
            "new_level": self.state.user.level,
            "badges_earned": [],
        }

        if is_correct:
            # Award XP
            xp = challenge.xp_reward
            new_level, leveled_up = self.state.user.add_xp(xp)
            result["xp_earned"] = xp
            result["leveled_up"] = leveled_up
            result["new_level"] = new_level

            # Mark completed
            self.state.user.completed_challenges.append(challenge_id)

            # Check for badges
            new_badges = self._check_badges()
            result["badges_earned"] = new_badges

            # Save
            self.state.save()

        return result

    def _check_badges(self) -> list[str]:
        """Check and award any newly earned badges. Returns list of badge IDs."""
        earned = set()  # In a real app, this would be stored per user
        newly_earned = []

        user = self.state.user
        completed_count = len(user.completed_challenges)

        # First Blood
        if completed_count >= 1 and "first_blood" not in earned:
            newly_earned.append("first_blood")

        # Getting Started
        if completed_count >= 5 and "getting_started" not in earned:
            newly_earned.append("getting_started")

        # Week Warrior
        if user.streak >= 7 and "week_warrior" not in earned:
            newly_earned.append("week_warrior")

        # Month Master
        if user.streak >= 30 and "month_master" not in earned:
            newly_earned.append("month_master")

        # Topic completion badges
        topics_completed = {}
        for c in self.state.challenges:
            if c.id in user.completed_challenges:
                topics_completed[c.topic] = topics_completed.get(c.topic, 0) + 1

        topic_totals = {}
        for c in self.state.challenges:
            topic_totals[c.topic] = topic_totals.get(c.topic, 0) + 1

        if topics_completed.get("loops", 0) >= topic_totals.get("loops", 0) and "loop_master" not in earned:
            newly_earned.append("loop_master")

        if topics_completed.get("functions", 0) >= topic_totals.get("functions", 0) and "function_fanatic" not in earned:
            newly_earned.append("function_fanatic")

        # Data dabbler - lists + dicts
        data_challenges = topic_totals.get("lists", 0) + topic_totals.get("dicts", 0)
        data_completed = topics_completed.get("lists", 0) + topics_completed.get("dicts", 0)
        if data_completed >= data_challenges and "data_dabbler" not in earned:
            newly_earned.append("data_dabbler")

        # Perfectionist
        if completed_count >= 20:
            # In a real app, we'd check pass rate from submissions table
            # For now, if they completed 20+, assume they're doing well
            if "perfectionist" not in earned:
                newly_earned.append("perfectionist")

        return newly_earned

    def get_next_challenge(self) -> Optional[Challenge]:
        return self.state.get_next_challenge()

    def get_challenges_by_topic(self, topic: str) -> list[Challenge]:
        return self.state.get_challenges_by_topic(topic)

    def get_available_topics(self) -> list[str]:
        return self.state.get_available_topics()

    def get_user_stats(self) -> dict:
        user = self.state.user
        completed = len(user.completed_challenges)
        total = len(self.state.challenges)
        return {
            "username": user.username,
            "level": user.level,
            "xp": user.xp,
            "xp_progress": user.xp_progress_in_level,
            "xp_needed": user.xp_needed_for_level,
            "progress_percent": user.progress_percent,
            "streak": user.streak,
            "completed": completed,
            "total": total,
            "completion_percent": (completed / total * 100) if total > 0 else 0,
        }

    def update_streak(self):
        """Update streak based on last active date."""
        today = date.today().isoformat()
        if self.state.user.last_active != today:
            # Check if yesterday
            from datetime import datetime, timedelta
            if self.state.user.last_active:
                last = datetime.fromisoformat(self.state.user.last_active).date()
                if last == date.today() - timedelta(days=1):
                    self.state.user.streak += 1
                else:
                    self.state.user.streak = 1
            else:
                self.state.user.streak = 1
            self.state.user.last_active = today
            self.state.save()

    def get_badge_info(self, badge_id: str) -> Optional[dict]:
        for b in self.badges:
            if b["id"] == badge_id:
                return b
        return None

    def get_earned_badge_ids(self) -> set[str]:
        """Get set of badge IDs the user has earned."""
        # In Phase 1, we compute dynamically
        earned = set()
        user = self.state.user
        completed_count = len(user.completed_challenges)

        if completed_count >= 1:
            earned.add("first_blood")
        if completed_count >= 5:
            earned.add("getting_started")
        if user.streak >= 7:
            earned.add("week_warrior")
        if user.streak >= 30:
            earned.add("month_master")

        topics_completed = {}
        for c in self.state.challenges:
            if c.id in user.completed_challenges:
                topics_completed[c.topic] = topics_completed.get(c.topic, 0) + 1

        topic_totals = {}
        for c in self.state.challenges:
            topic_totals[c.topic] = topic_totals.get(c.topic, 0) + 1

        if topics_completed.get("loops", 0) >= topic_totals.get("loops", 0):
            earned.add("loop_master")
        if topics_completed.get("functions", 0) >= topic_totals.get("functions", 0):
            earned.add("function_fanatic")

        data_challenges = topic_totals.get("lists", 0) + topic_totals.get("dicts", 0)
        data_completed = topics_completed.get("lists", 0) + topics_completed.get("dicts", 0)
        if data_completed >= data_challenges:
            earned.add("data_dabbler")

        if completed_count >= 20:
            earned.add("perfectionist")

        return earned


def create_new_game(username: str = "Player") -> GameState:
    """Create a fresh game state for a new user."""
    user = User(username=username)
    return GameState(user=user, challenges=CHALLENGES)


def load_game(username: str = "Player") -> GameState:
    """Load existing game or create new."""
    return GameState.load(CHALLENGES)