import streamlit as st
import random
from statistics import pstdev   # only needed later for scoring

st.set_page_config(page_title="PressureMap", layout="centered")

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

LENSES = ["Interpersonal", "Financial", "Big Picture"]

SCALE_LABELS = {
    0: "0 — Not at all / Never",
    1: "1 — Rarely",
    2: "2 — Sometimes",
    3: "3 — Often",
    4: "4 — Almost always",
}

# Your real question bank goes here (start small if you want)
QUESTION_BANK = {
    "Financial": [
        {"id": "f01", "text": "How often do you know your exact cash position without guessing?", "variable": "Clarity", "weight": 1.3, "reverse": False},
        {"id": "f02", "text": "How often do bills/fees surprise you?", "variable": "Clarity", "weight": 1.2, "reverse": True},
        # ← Add your other fXX questions here
    ],
    "Interpersonal": [],   # fill later
    "Big Picture": [],     # fill later
}

# ──────────────────────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────────────────────

defaults = {
    "stage": "setup",
    "lens": "Financial",
    "active_questions": [],
    "answers": {},
    "idx": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_app():
    for key, value in defaults.items():
        st.session_state[key] = value
    st.rerun()


# ──────────────────────────────────────────────────────────────
# UI Header + Sidebar
# ──────────────────────────────────────────────────────────────

st.title("PressureMap")
st.caption("Find where the pressure is building")

with st.sidebar:
    st.header("Controls")
    if st.button("Reset Everything"):
        reset_app()


# ──────────────────────────────────────────────────────────────
# Setup Screen
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "setup":
    st.subheader("Choose your focus area")

    st.session_state.lens = st.radio(
        "Which lens feels most pressurized?",
        LENSES,
        horizontal=True,
    )

    if st.button("Start 25 Questions", type="primary"):
        bank = QUESTION_BANK.get(st.session_state.lens, [])
        if not bank:
            st.error("No questions available for this lens yet.")
            st.stop()

        k = min(25, len(bank))
        st.session_state.active_questions = random.sample(bank, k=k)
        st.session_state.answers = {}
        st.session_state.idx = 0
        st.session_state.stage = "questions"
        st.rerun()


# ──────────────────────────────────────────────────────────────
# Questions Screen (basic version - expand later)
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "questions":
    qs = st.session_state.active_questions
    total = len(qs)
    idx = st.session_state.idx

    if idx >= total:
        st.session_state.stage = "results"
        st.rerun()

    st.subheader(f"Question {idx + 1} of {total}")
    st.progress(idx / total)

    q = qs[idx]
    st.write(f"**{q['text']}**")

    choice = st.radio(
        "Your answer:",
        options=list(SCALE_LABELS.keys()),
        format_func=lambda x: SCALE_LABELS[x],
        index=2,  # default to "Sometimes"
        horizontal=True,
        key=f"q_{q['id']}",
    )

    st.session_state.answers[q["id"]] = choice

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Back", disabled=(idx == 0)):
            st.session_state.idx = max(0, idx - 1)
            st.rerun()
    with col2:
        if st.button("Next", disabled=(idx >= total - 1)):
            st.session_state.idx = min(total - 1, idx + 1)
            st.rerun()
    with col3:
        if st.button("Finish & Score", type="primary"):
            st.session_state.stage = "results"
            st.rerun()


# ──────────────────────────────────────────────────────────────
# Results Screen (placeholder - expand with real scoring later)
# ──────────────────────────────────────────────────────────────

if st.session_state.stage == "results":
    st.subheader("Your Results")
    st.write("Scoring logic coming soon...")
    st.metric("Demo Overall Score", "64 / 100", delta="Needs attention")

    st.write("Main pressure area: Execution (demo)")

    if st.button("Run Again"):
        reset_app()
