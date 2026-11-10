# Python Quest 🐍

> **Learn Python through gamified challenges in your terminal.**  
> Earn XP • Level Up • Unlock Badges • Build Streaks  
> *Duolingo for Python — zero setup, pure terminal.*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **27 Challenges** | Across 7 Python topics, 3 challenge types |
| ⚡ **XP & Levels** | Mathematical progression curve (Lv 1→10) |
| 🏆 **9 Badges** | Unique unlocks: First Blood, Loop Master, Perfectionist... |
| 🔥 **Daily Streaks** | Persistent streak tracking across sessions |
| 🎨 **Synthwave UI** | Rich-powered gradients, panels, tables in terminal |
| 💾 **Zero Setup** | Single JSON save file — no database needed |
| 🏗️ **Extensible** | Clean architecture ready for FastAPI + Web |

---

## 🎮 Quick Start

```bash
# 1. Clone & enter
git clone https://github.com/20vaidehiv-lgtm/Python-Quest.git
cd Python-Quest

# 2. Install deps (Rich + Typer only — no Rust, no build)
pip install -r requirements.txt

# 3. Start your quest!
python main.py start --new
```

> **Windows?** Works out of the box — ASCII-safe rendering, no emoji encoding issues.

---

## 📸 Demo

```
+==================================================+
|                                                  |
|  PYTHON QUEST                                    |
|  Learn Python through interactive challenges     |
|  Earn XP + Level Up + Unlock Badges + Build Streaks|
|                                                  |
+==================================================+

Enter your username (Player): Vaidehi

+==================================================+
| ◆ PLAYER STATS ◆                                 |
| ✨ Level 1                    🔥 Streak: 1 days |
| XP: 0/100 (0%) ██████████████████████████████░░ |
+==================================================+

+==================================================+
| #01 ◉ Hello, Variables!     EASY  15 XP        |
| Learn how to store and use data in variables.   |
|                                                 |
| What will be the value of `x` after this runs?  |
|                                                 |
|   x = 10                                        |
|   x = x + 5                                     |
|   x = x * 2                                     |
|                                                 |
|   A) 15                                         |
|   B) 20                                         |
| ▸ C) 30                                         |
|   D) 25                                         |
+==================================================+

Your answer [A/B/C/D]: C

🎉 Correct!
+15 XP
🏆 Badge Unlocked: [*] First Blood - Complete your first challenge
```

---

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `python main.py start [--user NAME] [--new]` | Launch interactive game |
| `python main.py play [ID] [--user NAME]` | Play specific challenge |
| `python main.py stats [--user NAME]` | View profile, badges, progress |
| `python main.py challenges [--topic NAME] [--user NAME]` | Browse challenges |
| `python main.py leaderboard [--user NAME]` | View mock leaderboard |

---

## 🧩 Challenge Types

| Type | Icon | Description | Example |
|------|------|-------------|---------|
| **Multiple Choice** | `◉` | Pick the correct answer (A/B/C/D) | "What does `5 != 5` evaluate to?" |
| **Predict Output** | `▶` | Read code, predict exact output | `for i in range(3): print(i)` → `0\n1\n2` |
| **Fill in the Blank** | `␣` | Complete the code snippet | `age_next_year = ______ + 1` → `int(age)` |

> **No code execution needed** — all validation is string-based, safe & instant.

---

## 📚 Topics & Progress

| Topic | Challenges | XP Range | Status |
|-------|------------|----------|--------|
| **Variables** | 4 | 10–15 | ████░░░░░░ |
| **Conditionals** | 4 | 10–20 | ░░░░░░░░░░ |
| **Loops** | 5 | 15–25 | ░░░░░░░░░░ |
| **Functions** | 4 | 15–35 | ░░░░░░░░░░ |
| **Lists** | 4 | 15–25 | ░░░░░░░░░░ |
| **Dicts** | 3 | 15–25 | ░░░░░░░░░░ |
| **Strings** | 3 | 15–15 | ░░░░░░░░░░ |

**Total**: 27 challenges • ~400 XP to Level 3

---

## 🏅 Gamification

### XP Curve
```
Level 1:   0 XP     (Start)
Level 2: 100 XP     ████
Level 3: 300 XP     ████████████
Level 4: 650 XP     ████████████████████
Level 5: 1200 XP    ████████████████████████████
... up to Level 10 (9200 XP)
```
*Formula: `100 × (n-1) × 1.2^(n-2)`*

### Challenge Rewards
- **Easy** 🟢 10–20 XP
- **Medium** 🟠 20–25 XP  
- **Hard** 🔴 35 XP

### Badges (9 Total)

| Badge | Trigger | Icon |
|-------|---------|------|
| **First Blood** | Complete 1 challenge | `[*]` |
| **Getting Started** | Complete 5 challenges | `[+]` |
| **Week Warrior** | 7-day streak | `[7]` |
| **Month Master** | 30-day streak | `[30]` |
| **Loop Master** | All loop challenges | `[@]` |
| **Function Fanatic** | All function challenges | `[!]` |
| **Data Dabbler** | All list + dict challenges | `[#]` |
| **Speed Runner** | 10 challenges in 1 hour | `[>]` |
| **Perfectionist** | 20+ challenges, 100% pass | `[100]` |

### Streaks
- Login/play daily → streak increments
- Miss a day → resets to 1
- Persisted in `quest_data.json`

---

## 🛠 Tech Stack

### Phase 1 (Current — Terminal)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/UI-Rich-FF5DA2?logo=terminal&logoColor=white)
![Typer](https://img.shields.io/badge/CLI-Typer-00E5FF?logo=command-line&logoColor=white)
![JSON](https://img.shields.io/badge/Storage-JSON-7CFF6B?logo=json&logoColor=black)

### Phase 2+ (Planned — Web)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)
![Tailwind](https://img.shields.io/badge/CSS-Tailwind-00E5FF?logo=tailwindcss&logoColor=white)
![Piston](https://img.shields.io/badge/Execution-Piston-FF5DA2?logo=code&logoColor=white)

---

## 🏗 Architecture

```
python-quest/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── PRD.md                     # Product Requirements
├── PROJECT_TECH_STACK.md      # Full tech reference
├── quest_data.json            # Auto-created save file
└── python_quest/
    ├── __init__.py            # Version
    ├── models.py              # User, Challenge, GameState (dataclasses)
    ├── challenges.py          # 27 Challenge definitions
    ├── engine.py              # QuestEngine: logic, XP, badges, streak
    ├── ui.py                  # Rich components: panels, tables, styling
    └── cli.py                 # Typer commands: start, play, stats...
```

### Separation of Concerns
| Layer | Responsibility |
|-------|----------------|
| **Models** | Pure data structures, serialization |
| **Engine** | Game logic: answer checking, XP, badges, streak |
| **UI** | Rich rendering: panels, tables, gradients, prompts |
| **CLI** | Command routing, user interaction flow |

---

## 🗺 Roadmap

### Phase 1: Terminal MVP ✅
- [x] Rich + Typer CLI
- [x] 27 challenges, 3 types, 7 topics
- [x] XP, levels, badges, streaks
- [x] JSON persistence
- [x] Synthwave theme

### Phase 2: Backend API
- [ ] FastAPI + SQLAlchemy + Alembic
- [ ] JWT auth (register/login/me)
- [ ] Challenge/Submission/Leaderboard endpoints
- [ ] Auto `/docs` (Swagger UI)

### Phase 3: Web Frontend
- [ ] HTML + Tailwind CDN + Vanilla JS
- [ ] Dashboard, Challenge pages, Leaderboard
- [ ] `fetch()` API integration
- [ ] Responsive, accessible

### Phase 4: Gamification Polish
- [ ] XP/Level animations
- [ ] Streak calendar heatmap
- [ ] Challenge recommendations
- [ ] Weekly leaderboard reset

### Phase 5: Code Challenges
- [ ] Piston/Judge0 API integration
- [ ] CodeMirror/Monaco editor
- [ ] Sandbox security review
- [ ] Test case validation

### Phase 6: Social & Auth
- [ ] GitHub OAuth
- [ ] Profile pages
- [ ] Friend challenges

### Phase 7: Deploy & Polish
- [ ] Docker + GitHub Actions CI
- [ ] Railway/Render/Fly.io deploy
- [ ] README screenshots + Demo GIF
- [ ] Portfolio writeup

---

## 🤝 Contributing

### Add a Challenge
1. Open `python_quest/challenges.py`
2. Add a new `Challenge` dataclass to `CHALLENGES` list
3. Increment `order_index` sequentially
4. Run `python main.py challenges` to verify

### Challenge Template
```python
Challenge(
    id=28,  # Next available ID
    title="Your Title",
    description="What this teaches",
    difficulty=Difficulty.EASY,  # EASY | MEDIUM | HARD
    type=ChallengeType.MCQ,      # MCQ | PREDICT_OUTPUT | FILL_BLANK
    topic="variables",           # variables | conditionals | loops | functions | lists | dicts | strings
    xp_reward=15,
    order_index=28,
    # Type-specific fields:
    question="Your question?",
    options=["A) Opt1", "B) Opt2", "C) Opt3", "D) Opt4"],
    correct_answer="C",
    # OR for predict:
    code_snippet="print(2+2)",
    expected_output="4",
    # OR for fill blank:
    blank_code="x = ______",
    blank_answer="5",
)
```

### Report Issues
- Bug? → Open issue with steps to reproduce
- Feature? → Open issue with use case
- Typo in challenge? → PR welcome!

---

## 📄 License

MIT License — feel free to use, modify, distribute.

---

## 💼 Portfolio Talking Points

> **Built a complete gamified learning system** from scratch in Python:
> - **Custom synthwave terminal UI** using Rich (gradients, panels, tables, progress bars)
> - **Mathematical XP/leveling curve** with 10 levels, balanced challenge rewards
> - **9 unique badges** with varied unlock conditions (count, streak, topic mastery)
> - **27 educational challenges** across 7 core Python topics, 3 validation types
> - **Clean architecture**: models → engine → UI → CLI separation, fully type-hinted
> - **Phase 2 ready**: models map 1:1 to SQLAlchemy, FastAPI endpoints designed in PRD
> - **Cross-platform**: solved Windows encoding issues, ASCII-safe rendering

---

<div align="center">

**Made with 💜 and synthwave vibes**

[![GitHub](https://img.shields.io/badge/GitHub-20vaidehiv--lgtm/Python--Quest-181717?logo=github)](https://github.com/20vaidehiv-lgtm/Python-Quest)

</div>