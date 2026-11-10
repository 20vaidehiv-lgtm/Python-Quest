# Python Quest - Product Requirements Document

## 1. Executive Summary

**Python Quest** is a gamified, web-based learning platform that teaches Python programming through interactive challenges. Users progress through levels, earn XP, unlock badges, and compete on leaderboards — all while learning Python fundamentals in a safe, engaging environment.

**Target Audience**: Beginners learning Python (students, self-learners, coding bootcamp prep)

**Core Value Proposition**: Learn Python by doing — with instant feedback, gamification, and zero setup required.

---

## 2. Product Vision

> "Duolingo for Python" — bite-sized challenges, streak tracking, XP/levels, and a sense of progress that keeps learners coming back daily.

---

## 3. User Personas

| Persona | Goals | Pain Points |
|---------|-------|-------------|
| **Absolute Beginner** | Learn syntax, build confidence | Overwhelmed by setup, afraid of breaking things |
| **Student** | Supplement coursework, practice for exams | Needs structured progression, instant feedback |
| **Career Switcher** | Build portfolio-ready fundamentals | Wants visible progress, real-world relevance |

---

## 4. Core Features (MVP)

### 4.1 Challenge System
- **Challenge Types** (phased rollout):
  1. **Phase 1 (MVP)**: Multiple choice, "What does this code print?", Fill-in-the-blank
  2. **Phase 2**: Write-your-own-code challenges (using external execution API)
- Each challenge has: title, description, difficulty (Easy/Medium/Hard), XP reward, expected output
- Challenges organized by topic: Variables, Control Flow, Functions, Data Structures, OOP, etc.

### 4.2 Gamification
- **XP System**: Earn XP per challenge; harder challenges = more XP
- **Levels**: XP thresholds define levels (e.g., 0–99 XP = Level 1, 100–249 = Level 2, etc.)
- **Streaks**: Daily login/completion streak counter
- **Badges**: Achievements for milestones (e.g., "First Blood", "Week Warrior", "Loop Master", "Streak 7")
- **Leaderboard**: Global + weekly rankings by XP

### 4.3 Progress Tracking
- User dashboard showing: current level, XP, streak, badges earned, challenges completed
- Challenge history with pass/fail status and timestamps
- Topic-wise progress visualization

### 4.4 Authentication
- Simple username/password (Phase 1)
- GitHub OAuth (Phase 2 — optional)

---

## 5. Technical Architecture

### 5.1 Tech Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend API** | FastAPI | Auto `/docs`, type safety, async, great for learning REST |
| **Database** | SQLite + SQLAlchemy | Zero-setup file DB, ORM for Pythonic queries |
| **Templating** | Jinja2 | Server-rendered pages, easy dynamic content |
| **Frontend** | HTML + Tailwind CSS (CDN) + Vanilla JS | No build step, minimal JS (just `fetch`), modern styling |
| **Code Execution** | Judge0 or Piston API | Safe sandboxed execution, free tiers available |
| **Auth** | JWT tokens (FastAPI `python-jose`) | Stateless, scalable |

### 5.2 Database Schema

```sql
-- users
id INTEGER PK, username TEXT UNIQUE, password_hash TEXT, 
xp INTEGER DEFAULT 0, level INTEGER DEFAULT 1, 
streak INTEGER DEFAULT 0, last_active DATE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

-- challenges
id INTEGER PK, title TEXT, description TEXT, 
difficulty TEXT, -- 'easy' | 'medium' | 'hard'
topic TEXT, -- 'variables', 'loops', 'functions', etc.
type TEXT, -- 'mcq' | 'predict_output' | 'fill_blank' | 'code'
expected_output TEXT, -- for validation
xp_reward INTEGER,
starter_code TEXT NULL, -- for code challenges
test_cases JSON NULL, -- for code challenges
order_index INTEGER, -- for sequencing

-- submissions
id INTEGER PK, user_id INTEGER FK, challenge_id INTEGER FK,
passed BOOLEAN, submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
answer TEXT, -- user's answer
execution_output TEXT NULL -- for code challenges

-- badges
id INTEGER PK, name TEXT, description TEXT, icon TEXT,
criteria_type TEXT, -- 'xp' | 'streak' | 'topic_complete' | 'challenge_count'
criteria_value INTEGER

-- user_badges
id INTEGER PK, user_id INTEGER FK, badge_id INTEGER FK, earned_at TIMESTAMP
```

### 5.3 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/challenges` | List all challenges (with filters: topic, difficulty) |
| GET | `/api/challenges/{id}` | Get single challenge detail |
| POST | `/api/submit` | Submit answer, return `{ passed, xp_earned, feedback }` |
| GET | `/api/leaderboard` | Top 50 users by XP (params: `period=week|all`) |
| GET | `/api/user/me` | Current user profile + progress |
| GET | `/api/user/me/badges` | User's earned badges |
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, return JWT |
| GET | `/api/auth/me` | Validate token, return user |

### 5.4 Frontend Pages

| Route | Page | Components |
|-------|------|------------|
| `/` | Landing | Hero, features, CTA to register/login |
| `/login` | Login/Register | Forms, validation |
| `/dashboard` | User Dashboard | Level/XP bar, streak, badges, recent activity, continue button |
| `/challenges` | Challenge List | Filterable grid, topic tabs, difficulty badges |
| `/challenge/{id}` | Challenge Detail | Description, answer input (type-specific), submit button, feedback modal |
| `/leaderboard` | Leaderboard | Table with rank, username, level, XP, period toggle |
| `/profile` | Profile | Stats, all badges, challenge history |

---

## 6. User Flows

### 6.1 First-Time User
1. Lands on `/` → clicks "Start Free"
2. Registers → redirected to `/dashboard`
3. Sees "Welcome! Start with Variables" → clicks first challenge
4. Completes challenge → sees XP animation, badge check
5. Dashboard updates → streak = 1, level may increase

### 6.2 Returning User
1. Login → `/dashboard`
2. Sees streak, next recommended challenge
3. Clicks challenge → solves → submits
4. Instant feedback → XP animation → next challenge suggestion

### 6.3 Code Challenge Flow (Phase 2)
1. User opens code challenge → sees Monaco/CodeMirror editor
2. Writes code → clicks "Run" → hits Piston/Judge0 API
3. Sees output/errors in panel → iterates
4. Clicks "Submit" → backend validates against test cases
5. Returns pass/fail with detailed feedback

---

## 7. Gamification Design

### 7.1 XP Curve
| Level | XP Required | Total XP |
|-------|-------------|----------|
| 1 | 0 | 0 |
| 2 | 100 | 100 |
| 3 | 200 | 300 |
| 4 | 350 | 650 |
| 5 | 550 | 1,200 |
| 6 | 800 | 2,000 |
| 7 | 1,100 | 3,100 |
| 8 | 1,500 | 4,600 |
| 9 | 2,000 | 6,600 |
| 10 | 2,600 | 9,200 |

*Formula: `xp_for_level_n = 100 * (n-1) * 1.2^(n-2)` (rounded)*

### 7.2 Challenge XP Rewards
- Easy: 10–20 XP
- Medium: 25–40 XP
- Hard: 50–75 XP
- Code challenges (Phase 2): +50% bonus

### 7.3 Badge Catalog (MVP)
| Badge | Criteria | Icon |
|-------|----------|------|
| First Blood | Complete 1 challenge | 🩸 |
| Getting Started | Complete 5 challenges | 🌱 |
| Week Warrior | 7-day streak | 📅 |
| Month Master | 30-day streak | 🗓️ |
| Loop Master | Complete all loop challenges | 🔄 |
| Function Fanatic | Complete all function challenges | ⚡ |
| Data Dabbler | Complete all data structure challenges | 📊 |
| Speed Runner | Complete 10 challenges in 1 hour | ⚡ |
| Perfectionist | 100% pass rate (min 20 challenges) | 💯 |

---

## 8. Development Phases

### Phase 1: Terminal Prototype (Week 1)
- [ ] Python CLI app with hardcoded challenges (list of dicts)
- [ ] Loop: show challenge → get input → check → award XP
- [ ] JSON file persistence for user progress
- [ ] Basic streak tracking

### Phase 2: SQLite + FastAPI (Week 2)
- [ ] SQLAlchemy models + migrations (Alembic)
- [ ] CRUD endpoints for challenges, submissions
- [ ] JWT auth endpoints
- [ ] `/docs` auto-generated API docs

### Phase 3: Frontend MVP (Week 3)
- [ ] Base HTML layout with Tailwind CDN
- [ ] Dashboard page (level bar, streak, badges)
- [ ] Challenge list with topic filters
- [ ] Challenge detail page (MCQ, predict-output, fill-blank)
- [ ] Submit via `fetch`, show feedback modal
- [ ] Leaderboard page

### Phase 4: Gamification Polish (Week 4)
- [ ] XP/level animations (CSS/JS)
- [ ] Badge earning notifications
- [ ] Streak visualization (calendar heatmap)
- [ ] Challenge recommendations ("Next up for you")
- [ ] Weekly leaderboard reset logic

### Phase 5: Code Challenges (Week 5–6)
- [ ] Integrate Piston/Judge0 API
- [ ] Add CodeMirror/Monaco editor to challenge page
- [ ] Code challenge type in DB + test case runner
- [ ] Sandbox security review

### Phase 6: GitHub Polish (Week 7)
- [ ] README with screenshots, architecture diagram
- [ ] Demo GIF (using terminalizer or screen capture)
- [ ] Dockerfile for easy deployment
- [ ] GitHub Actions: lint, test, build
- [ ] Deploy to Railway/Render/Fly.io (free tier)

---

## 9. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Page load time | < 2s (static assets cached) |
| API response (submit) | < 500ms (excl. code execution) |
| Code execution timeout | 10s max |
| Concurrent users (MVP) | 100+ |
| Data persistence | SQLite file (daily backup) |
| Security | No `exec()`, parameterized queries, JWT with HttpOnly cookies |

---

## 10. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Code execution API rate limits | High | Medium | Cache results, fallback to local validation for simple cases |
| SQLite concurrency | Low | Medium | Use WAL mode, connection pooling; migrate to Postgres if needed |
| XSS in user-submitted code | Medium | High | Sanitize output, CSP headers, sandboxed execution only |
| Auth token theft | Low | High | HttpOnly cookies, short JWT expiry (15min), refresh tokens |
| Scope creep | High | Medium | Strict phase gates, document Phase 2+ items separately |

---

## 11. Success Metrics (Post-Launch)

| Metric | Target (Month 1) |
|--------|------------------|
| Registered users | 100+ |
| Daily active users | 20% of registered |
| Avg. challenges completed/user | 15+ |
| 7-day retention | 30%+ |
| Code challenge pass rate | 60%+ |

---

## 12. Appendix: File Structure (Target)

```
python-quest/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory
│   ├── config.py            # Settings (pydantic-settings)
│   ├── database.py          # SQLAlchemy engine, session
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API routes
│   │   ├── auth.py
│   │   ├── challenges.py
│   │   ├── submissions.py
│   │   ├── leaderboard.py
│   │   └── users.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── challenge_service.py
│   │   ├── execution_service.py  # Piston/Judge0 wrapper
│   │   └── gamification.py   # XP, levels, badges
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── challenge_list.html
│   │   ├── challenge_detail.html
│   │   ├── leaderboard.html
│   │   └── auth/
│   └── static/              # CSS/JS (minimal)
│       ├── style.css
│       └── app.js
├── tests/
├── scripts/
│   └── seed_challenges.py   # Populate DB with challenges
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
└── alembic/                 # Migrations
```

---

## 13. Next Steps

1. **Initialize repo** → `git init`, create `requirements.txt`
2. **Phase 1**: Build terminal prototype to validate challenge logic
3. **Phase 2**: Set up FastAPI + SQLAlchemy + auth
4. **Phase 3**: Build frontend pages iteratively
5. **Deploy early** → get feedback, iterate

---

*Generated for Python Quest project — ready to build! 🚀*