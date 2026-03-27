"""
Career Counselor Bot - Terminal Version
========================================
Run this file to start the chatbot:
    python main.py
"""

from core.engine import (
    detect_career,
    detect_intent,
    format_career_overview,
    format_alternatives,
    format_courses,
    run_interest_assessment,
    get_greeting,
    CAREERS_DB
)

# ─── Session memory: remember what user told us ───────────────────────────────
session = {
    "last_career": None,
    "user_name": None,
    "stream": None,
    "turn_count": 0
}

# ─── Generate smart response ──────────────────────────────────────────────────
def get_response(user_input: str) -> str:
    global session
    session["turn_count"] += 1
    text = user_input.strip().lower()

    # ── Greetings ──
    intent = detect_intent(text)

    if intent == "greeting":
        name_match = None
        for word in ["i am", "i'm", "my name is", "this is"]:
            if word in text:
                parts = text.split(word)
                if len(parts) > 1:
                    name_match = parts[1].strip().split()[0].capitalize()
        if name_match:
            session["user_name"] = name_match
            return f"\nHey {name_match}! Great to meet you 😊\nWhat career are you curious about? Or type 'suggest' if you need help deciding!\n"
        name = session.get("user_name", "")
        greeting = f"\nHey {name}! " if name else "\nHello! "
        return greeting + "How can I help you today? Ask me about any career or type 'suggest' for personalized recommendations!\n"

    # ── Exit ──
    if intent == "exit":
        return "\n👋 Thanks for using Career Counselor Bot! All the best for your future! 🌟\nType 'exit' to close.\n[EXIT]\n"

    # ── Thanks ──
    if intent == "thanks":
        return "\n😊 Happy to help! Feel free to ask anything else about careers or type 'suggest' for recommendations!\n"

    # ── Don't know / suggest ──
    if intent == "dont_know" or text in ["suggest", "help", "what should i do", "i'm confused"]:
        return run_interest_assessment()

    # ── List all careers ──
    if text in ["list", "careers", "all careers", "what careers", "show careers"]:
        lines = ["\n🌟 Careers I can guide you about:\n"]
        for key, val in CAREERS_DB.items():
            lines.append(f"   • {val['title']}  →  type '{key.replace('_', ' ')}'")
        lines.append("\nJust type the career name to get full details! 🎯\n")
        return "\n".join(lines)

    # ── Detect career ──
    career_key = detect_career(text)

    if career_key:
        session["last_career"] = career_key  # remember it

        # ── Alternatives specifically ──
        if intent == "alternatives":
            return format_alternatives(career_key)

        # ── Courses specifically ──
        if intent == "courses":
            return format_courses(career_key)

        # ── Salary specifically ──
        if intent == "salary":
            c = CAREERS_DB[career_key]
            sal = c["salary"]
            return (
                f"\n💰 Salary for {c['title']} in India:\n"
                f"   • Fresher (0-2 yrs)  : {sal['fresher']}\n"
                f"   • Mid-level (3-7 yrs): {sal['mid_level']}\n"
                f"   • Senior (8+ yrs)    : {sal['senior']}\n\n"
                f"💡 Tip: These are Indian market averages. Abroad can be 3-5x higher.\n"
            )

        # ── College info specifically ──
        if intent == "colleges":
            c = CAREERS_DB[career_key]
            lines = [f"\n🏛️  Top Institutes for {c['title']}:\n"]
            for inst in c["top_institutes"]:
                lines.append(f"   • {inst}")
            if c.get("entrance_exams"):
                lines.append(f"\n📝 Entrance Exams:\n")
                for exam in c["entrance_exams"]:
                    lines.append(f"   • {exam}")
            lines.append("")
            return "\n".join(lines)

        # ── Roadmap specifically ──
        if intent == "roadmap":
            c = CAREERS_DB[career_key]
            lines = [f"\n🗺️  Roadmap to become a {c['title']}:\n"]
            for i, step in enumerate(c["roadmap"], 1):
                lines.append(f"   Step {i}: {step}")
            lines.append(f"\n⏱️  Estimated Time: {c['duration']}")
            lines.append(f"💸 Estimated Cost: {c['cost_estimate']}\n")
            return "\n".join(lines)

        # ── Default: full career overview ──
        return format_career_overview(career_key)

    # ── If no career detected but we have context ──
    if session["last_career"]:
        last = session["last_career"]

        if intent == "alternatives":
            return format_alternatives(last)
        if intent == "courses":
            return format_courses(last)
        if intent == "salary":
            c = CAREERS_DB[last]
            sal = c["salary"]
            return (
                f"\n💰 Salary for {c['title']}:\n"
                f"   Fresher  : {sal['fresher']}\n"
                f"   Mid-level: {sal['mid_level']}\n"
                f"   Senior   : {sal['senior']}\n"
            )
        if intent == "colleges":
            c = CAREERS_DB[last]
            lines = [f"\n🏛️  Top Institutes for {c['title']}:\n"]
            for inst in c["top_institutes"]:
                lines.append(f"   • {inst}")
            return "\n".join(lines)
        if intent == "roadmap":
            c = CAREERS_DB[last]
            lines = [f"\n🗺️  Roadmap to become a {c['title']}:\n"]
            for i, step in enumerate(c["roadmap"], 1):
                lines.append(f"   Step {i}: {step}")
            return "\n".join(lines)

    # ── Fallback ──
    return (
        "\n🤔 Hmm, I didn't quite catch that. Here's what I can help with:\n\n"
        "   • Type a career name  →  e.g., 'pilot', 'software engineer', 'doctor'\n"
        "   • Type 'suggest'      →  get personalized recommendations\n"
        "   • Type 'list'         →  see all careers I know about\n"
        "   • Type 'help'         →  get guided through options\n\n"
        "Try again! 😊\n"
    )


# ─── Main loop ────────────────────────────────────────────────────────────────
def main():
    print(get_greeting())

    # Ask for name upfront
    try:
        name = input("Before we start — what's your name? (Press Enter to skip): ").strip()
        if name:
            session["user_name"] = name.capitalize()
            print(f"\nNice to meet you, {session['user_name']}! 🙌\n")
    except (KeyboardInterrupt, EOFError):
        pass

    print("─" * 55)
    print("Ask me anything about careers! Type 'list' to see all available careers.")
    print("─" * 55 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye! Best of luck with your career journey! 🌟\n")
            break

        if not user_input:
            print("Bot: Please type something! 😊\n")
            continue

        response = get_response(user_input)
        print(f"Bot: {response}")

        if "[EXIT]" in response:
            break


if __name__ == "__main__":
    main()
