"""
Career Counselor Bot - Streamlit Frontend
Run: streamlit run app.py
"""

import streamlit as st
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import (
    detect_career, detect_intent,
    format_career_overview, format_alternatives, format_courses,
    CAREERS_DB, APTITUDE_MAP,
)

st.set_page_config(
    page_title="CareerBot • IIT Patna",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Sora', sans-serif !important; }

.stApp { background-color: #1a1612; color: #f0ebe3; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }

[data-testid="stSidebar"] {
    background-color: #120f0c !important;
    border-right: 1px solid #2e2620 !important;
}
[data-testid="stSidebar"] * { color: #c9bcaa !important; }

.stTextInput > div > div > input {
    background-color: #241e18 !important;
    border: 1.5px solid #3d3228 !important;
    border-radius: 14px !important;
    color: #f0ebe3 !important;
    padding: 13px 18px !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 15px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c17f3b !important;
    box-shadow: 0 0 0 3px rgba(193,127,59,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #6b5e4e !important; }

.stButton > button {
    background: #c17f3b !important;
    color: #1a1612 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 18px !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: #d4913f !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(193,127,59,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stRadio > div { gap: 6px !important; }
.stRadio > div > label {
    background: #241e18 !important;
    border: 1px solid #3d3228 !important;
    border-radius: 10px !important;
    padding: 9px 14px !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    color: #c9bcaa !important;
    font-size: 13px !important;
}
.stRadio > div > label:hover {
    border-color: #c17f3b !important;
    color: #f0ebe3 !important;
}

hr { border-color: #2e2620 !important; margin: 12px 0 !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #1a1612; }
::-webkit-scrollbar-thumb { background: #3d3228; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c17f3b; }

.msg-row-user {
    display: flex; justify-content: flex-end;
    margin: 8px 0; padding: 0 4px;
    animation: fadeUp 0.25s ease;
}
.msg-row-bot {
    display: flex; justify-content: flex-start;
    margin: 8px 0; padding: 0 4px;
    animation: fadeUp 0.25s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.bubble-user {
    background: #c17f3b;
    color: #1a1612;
    padding: 11px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 68%;
    font-size: 14px;
    line-height: 1.55;
    font-weight: 500;
}
.bubble-bot {
    background: #241e18;
    border: 1px solid #3d3228;
    color: #e8dfd4;
    padding: 13px 17px;
    border-radius: 18px 18px 18px 4px;
    max-width: 82%;
    font-size: 13.5px;
    line-height: 1.75;
    font-family: 'IBM Plex Mono', monospace;
    white-space: pre-wrap;
    word-break: break-word;
}

.main-header {
    text-align: center;
    padding: 24px 0 16px;
    border-bottom: 1px solid #2e2620;
    margin-bottom: 20px;
}
.main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f0ebe3;
    letter-spacing: -0.5px;
}
.main-title span { color: #c17f3b; }
.main-subtitle { font-size: 13px; color: #6b5e4e; margin-top: 5px; }

.sidebar-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #5a4f42 !important;
    font-weight: 600;
    margin: 16px 0 8px;
}
.step-label {
    font-size: 11px; color: #5a4f42;
    text-align: center; margin-bottom: 14px;
}
.assessment-q {
    font-size: 13px; font-weight: 600;
    color: #c17f3b; margin-bottom: 12px;
}
.progress-dots {
    display: flex; gap: 6px;
    justify-content: center; margin: 10px 0 14px;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: #3d3228; }
.dot.on { background: #c17f3b; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
for key, val in [
    ("messages", []), ("last_career", None), ("user_name", ""),
    ("show_assessment", False), ("assessment_step", 0),
    ("assessment_answers", {}), ("greeted", False),
]:
    if key not in st.session_state:
        st.session_state[key] = val


# ── Response logic ────────────────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    text = user_input.strip().lower()
    intent = detect_intent(text)

    if intent == "greeting":
        name_match = None
        for phrase in ["i am", "i'm", "my name is"]:
            if phrase in text:
                parts = text.split(phrase)
                if len(parts) > 1:
                    name_match = parts[1].strip().split()[0].capitalize()
        if name_match:
            st.session_state.user_name = name_match
            return f"Hey {name_match}! Great to meet you.\nAsk me about any career, or use 'Find My Career' on the left!"
        name = st.session_state.user_name
        return (f"Hey {name}! " if name else "Hello! ") + "How can I help? Ask about any career or type 'list'!"

    if intent == "exit":
        return "Goodbye! All the best for your future!"

    if intent == "thanks":
        return "Happy to help! Ask about any other career anytime."

    if intent == "dont_know" or text in ["suggest", "help"]:
        st.session_state.show_assessment = True
        st.session_state.assessment_step = 0
        st.session_state.assessment_answers = {}
        return "Opening the Career Assessment in the sidebar! Answer 3 quick questions."

    if text in ["list", "careers", "all careers", "show careers"]:
        by_cat = {}
        for key, val in CAREERS_DB.items():
            cat = val.get("category", "other").replace("_", " ").title()
            by_cat.setdefault(cat, []).append(val["title"])
        lines = ["ALL 208 CAREERS:\n"]
        for cat, titles in sorted(by_cat.items()):
            lines.append(f"[ {cat} ]")
            for t in sorted(titles):
                lines.append(f"  • {t}")
            lines.append("")
        lines.append("Type any career name for full details!")
        return "\n".join(lines)

    career_key = detect_career(text)

    if career_key:
        st.session_state.last_career = career_key
        if intent == "alternatives": return format_alternatives(career_key)
        if intent == "courses":      return format_courses(career_key)
        if intent == "salary":
            c = CAREERS_DB[career_key]; s = c["salary"]
            return (
                f"SALARY — {c['title'].upper()}\n\n"
                f"  Fresher   (0-2 yrs) : {s['fresher']}\n"
                f"  Mid-level (3-7 yrs) : {s['mid_level']}\n"
                f"  Senior    (8+ yrs)  : {s['senior']}\n\n"
                f"  Abroad salaries are typically 3-5x higher."
            )
        if intent == "colleges":
            c = CAREERS_DB[career_key]
            lines = [f"TOP INSTITUTES — {c['title'].upper()}\n"]
            for inst in c["top_institutes"]: lines.append(f"  • {inst}")
            if c.get("entrance_exams"):
                lines.append("\nENTRANCE EXAMS:")
                for e in c["entrance_exams"]: lines.append(f"  • {e}")
            return "\n".join(lines)
        if intent == "roadmap":
            c = CAREERS_DB[career_key]
            lines = [f"ROADMAP — {c['title'].upper()}\n"]
            for i, step in enumerate(c["roadmap"], 1):
                lines.append(f"  {i:02d}. {step}")
            lines.append(f"\n  Duration : {c['duration']}")
            lines.append(f"  Cost     : {c['cost_estimate']}")
            return "\n".join(lines)
        return format_career_overview(career_key)

    if st.session_state.last_career:
        last = st.session_state.last_career
        if intent == "alternatives": return format_alternatives(last)
        if intent == "courses":      return format_courses(last)
        if intent == "salary":
            c = CAREERS_DB[last]; s = c["salary"]
            return f"SALARY — {c['title'].upper()}\n\n  Fresher  : {s['fresher']}\n  Mid-level: {s['mid_level']}\n  Senior   : {s['senior']}"
        if intent == "colleges":
            c = CAREERS_DB[last]
            return "TOP INSTITUTES:\n" + "\n".join(f"  • {i}" for i in c["top_institutes"])
        if intent == "roadmap":
            c = CAREERS_DB[last]
            return f"ROADMAP — {c['title'].upper()}\n\n" + "\n".join(f"  {i:02d}. {s}" for i, s in enumerate(c["roadmap"], 1))

    return (
        "Didn't catch that. Try:\n\n"
        "  • Career name  →  pilot, nurse, esports, chef\n"
        "  • salary / roadmap / colleges  →  after a career\n"
        "  • 'suggest'    →  personalised quiz\n"
        "  • 'list'       →  all 208 careers by category"
    )


def run_assessment_result(answers: dict) -> str:
    stream_map   = {"12th PCM": "PCM", "12th PCB": "PCB", "12th Commerce": "Commerce", "12th Arts": "Arts", "Graduate": "Graduation"}
    interest_map = {"Maths & Science": "maths_science", "Art & Creativity": "arts_creativity",
                    "People & Speaking": "people_communication", "Business & Finance": "business_money",
                    "Helping Others": "helping_others", "Tech & Computers": "technology_gadgets"}
    stream       = stream_map.get(answers.get("stream", "Graduate"), "Graduation")
    interest_key = interest_map.get(answers.get("interest", "Tech & Computers"), "technology_gadgets")
    interest_data = APTITUDE_MAP["interest_to_career_map"].get(interest_key, {})
    stream_data   = APTITUDE_MAP["stream_to_career_map"].get(stream, {})
    common = list(set(interest_data.get("careers", [])) & set(stream_data.get("best_careers", []))) or list(interest_data.get("careers", []))[:3]
    lines = ["YOUR TOP CAREER MATCHES\n", interest_data.get("message", "") + "\n"]
    for i, ck in enumerate(common[:3], 1):
        if ck in CAREERS_DB:
            c = CAREERS_DB[ck]; s = c["salary"]
            lines += [f"{i}. {c['title']}", f"   Starting : {s['fresher']}", f"   Senior   : {s['senior']}", f"   Duration : {c['duration']}\n"]
    if stream_data.get("entrance_exams"):
        lines.append(f"Key exams for {stream}:")
        for e in stream_data["entrance_exams"]: lines.append(f"  • {e}")
    lines.append("\nType any career name above for the full roadmap!")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎓 CareerBot")
    st.markdown("<div style='font-size:12px;color:#5a4f42;margin-top:-8px;margin-bottom:12px'>IIT Patna • 208 Careers</div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div class='sidebar-label'>Career Assessment</div>", unsafe_allow_html=True)

    if st.button("✦ Find My Career Path", use_container_width=True):
        st.session_state.show_assessment = True
        st.session_state.assessment_step = 0
        st.session_state.assessment_answers = {}

    if st.session_state.show_assessment:
        step = st.session_state.assessment_step
        dots = "".join(f"<div class='dot {'on' if i <= step else ''}'></div>" for i in range(3))
        st.markdown(f"<div class='progress-dots'>{dots}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='step-label'>Step {step+1} of 3</div>", unsafe_allow_html=True)

        if step == 0:
            st.markdown("<div class='assessment-q'>Your current stream?</div>", unsafe_allow_html=True)
            stream = st.radio("s", ["12th PCM","12th PCB","12th Commerce","12th Arts","Graduate"], label_visibility="collapsed", key="qs")
            if st.button("Continue →", key="n0", use_container_width=True):
                st.session_state.assessment_answers["stream"] = stream
                st.session_state.assessment_step = 1
                st.rerun()

        elif step == 1:
            st.markdown("<div class='assessment-q'>What excites you most?</div>", unsafe_allow_html=True)
            interest = st.radio("i", ["Maths & Science","Art & Creativity","People & Speaking","Business & Finance","Helping Others","Tech & Computers"], label_visibility="collapsed", key="qi")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", key="b1", use_container_width=True):
                    st.session_state.assessment_step = 0; st.rerun()
            with c2:
                if st.button("Continue →", key="n1", use_container_width=True):
                    st.session_state.assessment_answers["interest"] = interest
                    st.session_state.assessment_step = 2; st.rerun()

        elif step == 2:
            st.markdown("<div class='assessment-q'>What matters most?</div>", unsafe_allow_html=True)
            priority = st.radio("p", ["High salary","Stable govt job","Creative freedom","Social impact"], label_visibility="collapsed", key="qp")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", key="b2", use_container_width=True):
                    st.session_state.assessment_step = 1; st.rerun()
            with c2:
                if st.button("Get Results", key="sub", use_container_width=True):
                    st.session_state.assessment_answers["priority"] = priority
                    result = run_assessment_result(st.session_state.assessment_answers)
                    st.session_state.messages.append({"role": "user", "text": "Show my career recommendations"})
                    st.session_state.messages.append({"role": "bot",  "text": result})
                    st.session_state.show_assessment = False; st.rerun()

    st.divider()
    st.markdown("<div class='sidebar-label'>Quick Actions</div>", unsafe_allow_html=True)

    for label, query in [
        ("All 208 Careers",   "list"),
        ("Salary — Pilot",    "salary of pilot"),
        ("Roadmap — Doctor",  "roadmap of doctor"),
        ("Esports Career",    "esports"),
        ("Software Engineer", "software engineer"),
        ("IAS Officer",       "ias officer"),
        ("Data Scientist",    "data scientist"),
        ("CA Career",         "chartered accountant"),
    ]:
        if st.button(label, key=f"qa_{query}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "text": query})
            st.session_state.messages.append({"role": "bot",  "text": get_response(query)})
            st.rerun()

    st.divider()
    st.markdown("<div class='sidebar-label'>Search Careers</div>", unsafe_allow_html=True)
    q = st.text_input("", placeholder="e.g. design, nurse, law...", key="sb", label_visibility="collapsed")
    if q and len(q) >= 2:
        hits = [(k, v["title"]) for k, v in CAREERS_DB.items()
                if q.lower() in v["title"].lower() or q.lower() in k.replace("_"," ")][:7]
        if hits:
            for k, title in hits:
                if st.button(f"→ {title}", key=f"sh_{k}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "text": title})
                    st.session_state.messages.append({"role": "bot",  "text": get_response(title)})
                    st.rerun()
        else:
            st.markdown("<div style='font-size:12px;color:#5a4f42;padding:6px'>No match found</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size:11px;color:#3d3228;text-align:center;padding:4px'>Built at IIT Patna • BS AI & Cybersecurity</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN CHAT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
    <div class="main-title">Career <span>Counselor</span> Bot</div>
    <div class="main-subtitle">208 careers • Indian context • IIT Patna</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.greeted:
    st.session_state.messages.append({"role": "bot", "text": (
        "Hello! I'm your Career Counselor.\n\n"
        "  • Type any career  →  pilot, nurse, esports, chef, vlsi\n"
        "  • salary / roadmap / colleges  →  after a career name\n"
        "  • alternatives / courses  →  also work after a career\n"
        "  • 'suggest'        →  3-question personalised quiz\n"
        "  • 'list'           →  all 208 careers by category\n\n"
        "What career are you curious about?"
    )})
    st.session_state.greeted = True

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-row-user"><div class="bubble-user">{msg["text"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-row-bot"><div class="bubble-bot">{msg["text"]}</div></div>', unsafe_allow_html=True)

# Context-aware quick chips
if st.session_state.last_career:
    title = CAREERS_DB[st.session_state.last_career]["title"]
    st.markdown("<div style='margin:12px 0 4px;font-size:11px;color:#5a4f42;letter-spacing:0.5px'>QUICK ACTIONS</div>", unsafe_allow_html=True)
    cols = st.columns(5)
    for col, (label, query) in zip(cols, [
        ("💰 Salary",       f"salary of {title}"),
        ("🗺 Roadmap",      f"roadmap of {title}"),
        ("🏛 Colleges",     f"colleges for {title}"),
        ("🔄 Alternatives", f"alternatives to {title}"),
        ("📚 Courses",      f"courses for {title}"),
    ]):
        with col:
            if st.button(label, key=f"ch_{query}"):
                st.session_state.messages.append({"role": "user", "text": query})
                st.session_state.messages.append({"role": "bot",  "text": get_response(query)})
                st.rerun()

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
st.divider()

col_in, col_btn = st.columns([5, 1])
with col_in:
    user_input = st.text_input("msg", placeholder="Type a career or ask anything...", label_visibility="collapsed", key="mi")
with col_btn:
    send = st.button("Send", use_container_width=True)

if send and user_input.strip():
    t = user_input.strip()
    st.session_state.messages.append({"role": "user", "text": t})
    st.session_state.messages.append({"role": "bot",  "text": get_response(t)})
    st.rerun()

if len(st.session_state.messages) > 1:
    if st.button("Clear chat", key="clr"):
        st.session_state.messages = []
        st.session_state.last_career = None
        st.session_state.greeted = False
        st.rerun()
