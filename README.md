# 🎓 Career Counselor Bot

> An AI-powered career counseling chatbot built in Python — helping students explore 208 careers with roadmaps, salary info, top colleges, and personalized recommendations.

**Built at IIT Patna | BS in Artificial Intelligence & Cybersecurity**

---

## 📸 Preview

```
╔══════════════════════════════════════════════════════╗
║         🎓  CAREER COUNSELOR BOT  🎓                ║
║         Your Personal Career Guide                  ║
╚══════════════════════════════════════════════════════╝

You: I want to become a pilot
Bot: ═══════════════════════════════════════════════════
     🎯  COMMERCIAL PILOT
     ═══════════════════════════════════════════════════
     📌 What is it?
        Fly commercial aircraft for airlines or cargo companies.
     🗺️  Roadmap: 9 steps from 12th PCM to IndiGo/Air India
     💰 Salary: ₹1.5–2.5 LPA (fresher) → ₹40–80 LPA (captain)
     ...
```

---

## ✨ Features

- 🔍 **208 careers** across 23 sectors — fully Indian context (DGCA, NEET, JEE, UPSC, IPL, ISRO)
- 🗺️ **Step-by-step roadmaps** for every career
- 💰 **Salary data** — fresher to senior level, Indian market
- 🏛️ **Top institutes & entrance exams** for each career
- 🔄 **Backup options** if primary career doesn't work out
- 📚 **Free online course recommendations** (Coursera, YouTube, etc.)
- 🧩 **Interest assessment quiz** — 3 questions → personalized career suggestions
- 💬 **Context memory** — follow up questions work naturally 
- 🌐 **Two interfaces** — terminal (pure python) + web Ui streamlit 
- ⚡ **Smart detection** — 4-step keyword matching with tiebreaker logic

---

## 📁 Folder Structure

```
career_counselor_bot/
│
├── app.py                   ← Web UI (Streamlit) — run this for browser interface
├── main.py                  ← Terminal version — run this for command line
│
├── core/
│   └── engine.py            ← Brain of the bot
│                              (keyword detection, intent detection, response formatting)
│
├── data/
│   ├── careers.json         ← 208 career profiles with full details
│   ├── courses.json         ← Free online courses mapped to careers
│   └── aptitude_map.json    ← Interest → Career mapping for the quiz
│
└── README.md                ← This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows / Mac / Linux

Check your Python version:
```bash
python --version
```

---

### Option 1 — Terminal Version (No installation needed)

```bash
# Step 1: Go into the project folder
cd career_counselor_bot

# Step 2: Run the bot
python main.py
```

Zero external libraries required. Pure Python only. ✅

---

### Option 2 — Web UI (Streamlit)

```bash
# Step 1: Install Streamlit (one time only)
pip install streamlit

# Step 2: Go into the project folder
cd career_counselor_bot

# Step 3: Launch the web app
streamlit run app.py
```

Opens automatically at **http://localhost:8501** in your browser.

---

## 💬 How to Use

### Terminal — What to Type

| You Type | What Happens |
|----------|-------------|
| `pilot` | Full career overview — description, roadmap, salary, colleges, pros/cons |
| `esports` | Esports professional career details |
| `i want to become a doctor` | Same as above — natural language works |
| `salary of software engineer` | Fresher → Senior salary breakdown |
| `roadmap of ias officer` | Step-by-step path to becoming IAS |
| `colleges for ca` | Top institutes + entrance exams |
| `alternatives to pilot` | Backup careers if pilot doesn't work |
| `courses for data science` | Free Coursera/YouTube recommendations |
| `suggest` | 3-question quiz → personalized career picks |
| `list` | All 208 careers grouped by sector |
| `exit` or `quit` | Close the bot |

### Web UI — Additional Features

- **Find My Career Path** button → guided 3-step assessment in sidebar
- **Quick Action buttons** → one-click salary, roadmap, career queries
- **Live search bar** → type 2+ letters to find any career instantly
- **Context chips** → after any career, quick buttons appear for salary/roadmap/colleges/alternatives

---

## 🗂️ Career Database — 208 Careers Across 23 Sectors

| Sector | Count | Examples |
|--------|-------|---------|
| Technology | 27 | Software Engineer, ML Engineer, DevOps, Ethical Hacker, Blockchain Dev |
| Finance | 20 | CA, Investment Banker, Actuary, VC, Hedge Fund Manager |
| Engineering | 17 | Aerospace, Civil, VLSI, Nuclear, Petroleum, Renewable Energy |
| Creative | 16 | Actor, Musician, Animator, Photographer, Screenwriter |
| Medical | 15 | Doctor, Nurse, Dentist, Physiotherapist, Radiologist |
| Research | 11 | ISRO Scientist, Space Scientist, Wildlife Biologist, Oceanographer |
| Government | 9 | IAS, IPS, RBI Officer, SEBI Officer, Forest Officer |
| Sports | 9 | Pro Athlete, Sports Analyst, Esports Coach, Sports Psychologist |
| Business | 8 | Product Manager, Management Consultant, HR Manager, Supply Chain |
| Media | 8 | Journalist, Content Writer, Digital Marketer, PR Professional |
| Science | 8 | Geologist, Astronomer, Biotechnologist, Environmental Scientist |
| Graphic Design | 8 | Brand Designer, Motion Designer, UX Researcher, Concept Artist |
| Law | 7 | Lawyer, Patent Attorney, Mediator, Legal Tech Professional |
| Social Science | 8 | Economist, Psychologist, Sociologist, Political Scientist |
| Education | 6 | Professor, Special Educator, EdTech Creator, Academic Counselor |
| Wellness | 6 | Yoga Therapist, Life Coach, Meditation Teacher, Art Therapist |
| Esports | 6 | Pro Gamer, Esports Coach, Gaming Content Creator, Esports Manager |
| Aviation | 5 | Pilot, ATC, Merchant Navy, Marine Engineer, Drone Pilot |
| Hospitality | 4 | Hotel Manager, Chef, Event Manager, Travel Agent |
| Social Impact | 4 | NGO Manager, Sustainability Consultant, Policy Analyst, Agritech |
| Design | 3 | Architect, Urban Planner, Interior Designer |
| Specialised | 2 | Gemologist, Ethical Fashion Designer |
| Defense | 1 | Defense Officer |

---

## 🧠 How the Bot Works

### Detection Logic (4-step system)

```
User types: "I want to be a data engineer"
                    ↓
Step 1: Keyword scoring
        "data engineer" matches data_engineer keywords → score: 1
        Tiebreak: longest matched keyword wins
                    ↓
Step 2: (if no keyword match)
        Try matching career key directly
        "data engineer" → data_engineer ✓
                    ↓
Step 3: (if still no match)
        Try matching career title from JSON
        "Data Engineer" in title → match ✓
                    ↓
Step 4: (last resort)
        All main words found in text → partial match
```

### Intent Detection

The bot understands WHAT you want, not just WHICH career:

```
"salary of pilot"    → career: pilot  + intent: salary   → shows salary only
"roadmap for doctor" → career: doctor + intent: roadmap  → shows 9-step path
"colleges for CA"    → career: ca     + intent: colleges → shows top institutes
"pilot"              → career: pilot  + intent: general  → shows full overview
```

### Session Memory

```python
session = {
    "last_career": "pilot",   # remembers last discussed career
    "user_name": "Shivam",    # personalizes responses
    "turn_count": 5           # tracks conversation length
}

# So this works naturally:
You: "Tell me about pilot"
Bot: [shows full pilot info]
You: "What is the salary?"      ← no need to say "pilot salary"
Bot: [shows pilot salary]       ← context remembered!
```

---

## 🏗️ Architecture

```
User Input (terminal or web)
        ↓
   main.py / app.py         ← handles input/output loop
        ↓
   detect_intent()          ← what does user want? (salary/roadmap/colleges/general)
        ↓
   detect_career()          ← which career are they asking about?
        ↓
   format_*() functions     ← build the response string
        ↓
   careers.json             ← fetch the actual data
        ↓
   Response to user
```

**Files and their responsibilities:**

| File | Lines | Responsibility |
|------|-------|---------------|
| `core/engine.py` | 660 | All intelligence — detection, formatting, assessment |
| `app.py` | 467 | Streamlit web UI |
| `main.py` | 199 | Terminal chat loop |
| `data/careers.json` | ~6000 | 208 career profiles |
| `data/aptitude_map.json` | ~80 | Interest → career mapping |
| `data/courses.json` | ~60 | Online course recommendations |

---

## 🔧 Common Issues & Fixes

### "python3 is not recognized" (Windows)
Use `python` instead of `python3` on Windows:
```powershell
python main.py
python -m streamlit run app.py
```

### Bot gives wrong/no match for a career
The `__pycache__` folder may be running an old cached version of engine.py. Delete it:
```powershell
# Windows
Remove-Item -Recurse -Force core\__pycache__

# Mac/Linux
rm -rf core/__pycache__
```

### Streamlit not found
```bash
pip install streamlit
# or
pip3 install streamlit
```

### careers.json shows only 10/116 careers instead of 208
You have an old version of `careers.json`. Replace it with the latest file from the project.

---

## 🔮 Roadmap — What's Next

- [x] Terminal chatbot — pure Python, zero dependencies
- [x] 208 careers across 23 sectors — Indian context
- [x] Streamlit web UI with dark warm theme
- [x] 4-step smart career detection with tiebreaker
- [x] Interest-based assessment quiz
- [x] Context memory for follow-up questions
- [ ] Gemini / Groq API integration — replace rule-based with LLM responses
- [ ] User profile saving — remember stream, interests across sessions
- [ ] Entrance exam prep resources per career
- [ ] College ranking comparison tool
- [ ] WhatsApp / Telegram bot integration
- [ ] Mobile-responsive PWA version

---

## 👥 Team Roles

| Person | Role | Responsibility |
|--------|------|---------------|
| Person 1 (Backend Lead) | System Architect | engine.py — all detection logic, response formatting, session memory |
| Person 2 (Frontend & API) | UI Developer | app.py — Streamlit interface, API integration (Phase 2) |
| Person 3 (Datasets) | Data Engineer | careers.json — expand to 500+ careers, validate data accuracy |
| Person 4 (Testing) | QA Engineer | Test all career queries, edge cases, user feedback |
| Person 5 (Docs & Viva) | Technical Writer | Report writing, presentation, viva preparation |

---

## 📦 Dependencies

| Package | Version | Used For | Required? |
|---------|---------|----------|-----------|
| Python | 3.8+ | Core language | ✅ Yes |
| streamlit | Latest | Web UI | Only for `app.py` |
| json | built-in | Data loading | ✅ Yes |
| os | built-in | File paths | ✅ Yes |
| sys | built-in | Path management | ✅ Yes |

**Terminal version: Zero external dependencies.**
**Web UI: Only requires `pip install streamlit`.**

---

## 📄 License

Built for academic purposes at IIT Patna.
BS in Artificial Intelligence & Cybersecurity — Semester Project.

---

## 🙏 Acknowledgements

- Career data curated with Indian context — DGCA, UPSC, ICAI, ISRO, NEET, JEE
- Salary data sourced from AmbitionBox, Glassdoor India, LinkedIn Salary (2024-25)
- Built with ❤️ at IIT Patna

