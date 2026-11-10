<div align="center">

# ⚡ PYTHON QUEST

### Level Up Your Python Skills. One Challenge at a Time.

**Python Quest** is a gamified Python learning platform that transforms the traditional process of learning programming into an interactive adventure. Inspired by Duolingo, it combines bite-sized coding challenges with XP rewards, levels, achievement badges, and daily streaks to make learning Python more engaging and rewarding. Starting as a terminal-based game, the project is designed to evolve into a full-stack web application with interactive coding challenges and leaderboards.

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Rich](https://img.shields.io/badge/Rich-FF5DA2?style=for-the-badge&logo=terminal&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-00BFA6?style=for-the-badge&logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

**Planned Tech Stack**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

<br/>

![Challenges](https://img.shields.io/badge/Challenges-27-FF5DA2?style=flat-square)
![Topics](https://img.shields.io/badge/Topics-7-8A2BE2?style=flat-square)
![Badges](https://img.shields.io/badge/Badges-9-FFD700?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-7CFF6B?style=flat-square)

</div>

---

## ✨ What is Python Quest?

Learning Python doesn't have to feel like reading endless documentation or solving random exercises.

**Python Quest turns learning into a game.**

Start your journey as a beginner, complete programming challenges, earn experience points, unlock achievements, and build daily learning streaks.

Every challenge brings you closer to mastering Python.

Whether you're learning variables for the first time or exploring functions and data structures, Python Quest makes every small improvement count.

**Your mission:** Learn. Code. Earn XP. Level Up.

---

## 🎮 Features

| Feature | Description |
|:---|:---|
| 🎯 **27 Interactive Challenges** | Learn through 7 core Python topics and 3 challenge types. |
| ⚡ **XP & Level System** | Earn experience points and progress through 10 levels. |
| 🏆 **9 Achievement Badges** | Unlock achievements by completing milestones. |
| 🔥 **Daily Streaks** | Maintain your learning consistency with persistent streak tracking. |
| 🎨 **Synthwave Terminal UI** | Beautiful terminal interface powered by Rich. |
| 💾 **Persistent Progress** | Automatically save your progress using JSON. |
| 🧩 **Multiple Challenge Types** | MCQs, output prediction, and fill-in-the-blank exercises. |
| 🚀 **Expandable Architecture** | Designed for future FastAPI and web integration. |

---

## 🚀 Getting Started

Get your quest running in just a few steps.

### 1. Clone the Repository

```bash
git clone https://github.com/20vaidehiv-lgtm/Python-Quest.git
```

### 2. Navigate to the Project

```bash
cd Python-Quest
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Your Quest!

```bash
python main.py start --new
```

Enter your username and begin your Python journey!

**Requirements:**
- Python 3.10+
- Rich
- Typer

No database configuration or complicated setup required.

---

## 🕹️ Available Commands

| Command | Description |
|:---|:---|
| `python main.py start --new` | Start a fresh quest. |
| `python main.py start` | Resume your existing quest. |
| `python main.py play 1` | Play a specific challenge. |
| `python main.py stats` | View your player statistics. |
| `python main.py challenges` | Browse all available challenges. |
| `python main.py challenges --topic loops` | Filter challenges by topic. |
| `python main.py leaderboard` | View the leaderboard. |

---

## 🧠 Challenge System

Python Quest currently supports three different challenge formats.

| Type | Description | Example |
|:---|:---|:---|
| ◉ Multiple Choice | Choose the correct answer. | What does `5 != 5` return? |
| ▶ Predict Output | Predict the output of a Python program. | `for i in range(3): print(i)` |
| ␣ Fill in the Blank | Complete missing parts of code. | `age_next_year = ______ + 1` |

**Current learning topics:**

| Topic | Challenges | Concepts Covered |
|:---|:---:|:---|
| Variables | 4 | Variables, data types, assignments |
| Conditionals | 4 | If, elif, else, comparisons |
| Loops | 5 | For loops, while loops, range |
| Functions | 4 | Parameters, return values, functions |
| Lists | 4 | Indexing, modification, list operations |
| Dictionaries | 3 | Keys, values, dictionary operations |
| Strings | 3 | String operations and manipulation |
| **Total** | **27** | **7 Core Topics** |

---

## 🏆 Gamification System

### ⚡ XP & Level Progression

Every completed challenge rewards XP depending on its difficulty.

| Difficulty | XP Reward |
|:---|:---:|
| 🟢 Easy | 10–20 XP |
| 🟠 Medium | 20–25 XP |
| 🔴 Hard | 35 XP |

Your total XP determines your level.

```text
LEVEL PROGRESSION

Level 1       0 XP
Level 2       100 XP
Level 3       300 XP
Level 4       650 XP
Level 5       1200 XP
...
Level 10      9200 XP
```

The progression system uses a mathematical XP curve to make higher levels progressively more challenging.

### 🥇 Achievement Badges

There are currently 9 unique achievements to unlock.

| Badge | Requirement |
|:---|:---|
| 🩸 First Blood | Complete your first challenge. |
| ➕ Getting Started | Complete 5 challenges. |
| 🔥 Week Warrior | Maintain a 7-day streak. |
| 📅 Month Master | Maintain a 30-day streak. |
| 🔁 Loop Master | Complete all loop challenges. |
| ⚙️ Function Fanatic | Complete all function challenges. |
| 📚 Data Dabbler | Complete all list and dictionary challenges. |
| ⚡ Speed Runner | Complete 10 challenges within an hour. |
| 💯 Perfectionist | Complete 20+ challenges with a 100% pass rate. |

### 🔥 Daily Streaks

Consistency matters!

- Play daily to maintain your streak.
- Miss a day and your streak resets.
- Your streak is automatically saved.
- Progress persists even after closing the application.

---

## 🖥️ Demo

Here's what your terminal adventure looks like:

```text
+==================================================+
|                                                  |
|   PYTHON QUEST                                   |
|   Learn Python. Earn XP. Level Up.               |
|                                                  |
|   ✨ LEVEL 1                 🔥 STREAK: 1 DAY    |
|   XP: 0 / 100                                  |
|                                                  |
+==================================================+

  CHALLENGE #01

  ◉ HELLO, VARIABLES!

  Difficulty: EASY
  Reward: +15 XP

  What will be the value of x after this runs?

      x = 10
      x = x + 5
      x = x * 2

      A) 15
      B) 20
      C) 30
      D) 25

  Your answer [A/B/C/D]: C

  🎉 CORRECT!

  +15 XP
  🏆 BADGE UNLOCKED: FIRST BLOOD

+==================================================+
|             QUEST PROGRESS UPDATED              |
+==================================================+
```

---

## 🏗️ Project Architecture

The project follows a modular architecture with a clear separation of responsibilities.

```text
Python-Quest/
│
├── main.py
├── requirements.txt
├── PRD.md
├── PROJECT_TECH_STACK.md
├── quest_data.json
│
└── python_quest/
    │
    ├── __init__.py
    ├── models.py
    ├── challenges.py
    ├── engine.py
    ├── ui.py
    └── cli.py
```

### Architecture Overview

| Module | Responsibility |
|:---|:---|
| `main.py` | Application entry point. |
| `models.py` | Data structures using Python dataclasses. |
| `challenges.py` | Contains all 27 challenge definitions. |
| `engine.py` | Handles XP, levels, badges, streaks and answer validation. |
| `ui.py` | Terminal interface using Rich. |
| `cli.py` | Command-line interface using Typer. |
| `quest_data.json` | Stores player progress and game data. |

### Design Principles

- **Modularity:** Each module has a specific responsibility.
- **Maintainability:** Easy to update and extend individual components.
- **Persistence:** Player progress is saved between sessions.
- **Scalability:** Architecture designed to support future backend integration.

---

## 🛠️ Tech Stack

### Phase 1 — Terminal Application (Implemented)

| Technology | Purpose |
|:---|:---|
| Python | Core programming language and game logic. |
| Rich | Terminal styling, panels, tables and progress bars. |
| Typer | Command-line interface and command routing. |
| JSON | Local player data and progress storage. |

### Phase 2+ — Full-Stack Web Application (Planned)

| Technology | Purpose |
|:---|:---|
| FastAPI | Backend REST API. |
| SQLAlchemy | Database ORM. |
| SQLite | Database storage. |
| Alembic | Database migrations. |
| HTML5 | Frontend structure. |
| Tailwind CSS | Responsive UI styling. |
| JavaScript | Frontend interactions and API integration. |
| Piston / Judge0 | Code execution and validation. |
| CodeMirror / Monaco | Interactive code editor. |

---

## 🗺️ Development Roadmap

Python Quest is being developed in multiple phases.

- [x] **Phase 1 — Terminal MVP**
  - Rich-powered terminal interface.
  - 27 challenges across 7 topics.
  - XP, levels, badges and streaks.
  - JSON-based persistence.
  - Typer CLI commands.

- [ ] **Phase 2 — Backend Development**
  - FastAPI integration.
  - SQLAlchemy and SQLite.
  - User authentication.
  - Challenge and submission APIs.
  - Swagger documentation.

- [ ] **Phase 3 — Web Frontend**
  - HTML + Tailwind CSS.
  - Interactive dashboard.
  - Challenge interface.
  - Leaderboard.
  - JavaScript API integration.

- [ ] **Phase 4 — Gamification Improvements**
  - XP and level-up animations.
  - Streak calendar.
  - Challenge recommendations.
  - Weekly leaderboards.

- [ ] **Phase 5 — Interactive Coding Challenges**
  - Piston / Judge0 integration.
  - CodeMirror / Monaco editor.
  - Test case validation.
  - Secure code execution.

- [ ] **Phase 6 — Social Features**
  - GitHub OAuth.
  - Public player profiles.
  - Friend challenges.

- [ ] **Phase 7 — Deployment**
  - Docker integration.
  - GitHub Actions CI/CD.
  - Cloud deployment.
  - Screenshots and demo GIF.

---

## 🤝 Contributing

Want to add a new challenge?

1. Open `python_quest/challenges.py`.
2. Add a new `Challenge` object to the `CHALLENGES` list.
3. Assign the next available ID and order index.
4. Run the application and verify your challenge.

Contributions, suggestions and bug reports are welcome!

---

## 🎯 Project Vision

Python Quest started as a terminal-based Python learning game, but the long-term goal is much bigger.

The vision is to build a complete interactive learning platform where beginners can:

- Learn programming through structured challenges.
- Practice writing and understanding code.
- Track their learning progress.
- Compete with friends through leaderboards.
- Build consistent coding habits.
- Gradually move from beginner exercises to real coding problems.

**From a simple terminal game to a complete coding-learning platform.**

---

## 👩‍💻 Developer

<div align="center">

### Vaidehi Vaidya

Computer Science & Engineering Student

Building projects, exploring new technologies, and learning by creating.

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/20vaidehiv-lgtm)

</div>

---

<div align="center">

### 💜 Made with Python, curiosity & a little synthwave magic.

**LEARN • PLAY • LEVEL UP**

⭐ If you like this project, consider giving it a star!

</div>
