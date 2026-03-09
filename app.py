import json
import re
import time
import locale

import streamlit as st
import anthropic

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Make It Make Sense",
    page_icon="🔢",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CATEGORY_COLORS = {
    "time": "#FF6B6B",
    "size": "#4ECDC4",
    "count": "#FFE66D",
    "money": "#95E879",
    "rate": "#A78BFA",
    "probability": "#F9A8D4",
}

REGIONS = {
    "🇮🇳 India": "India",
    "🇺🇸 United States": "United States",
    "🇬🇧 United Kingdom": "United Kingdom",
    "🇦🇪 UAE / Middle East": "UAE / Middle East",
    "🌍 Global": "Global",
}


# ---------------------------------------------------------------------------
# System prompt (research-backed)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = r'''You are "Make It Make Sense" — an expert at turning abstract numbers into vivid, instantly graspable perspective comparisons.

You are grounded in the research of Chip Heath & Karla Starr ("Making Numbers Count") and Microsoft Research's Perspective Engine (Hofman & Goldstein). Your comparisons follow proven cognitive science principles.

## OUTPUT FORMAT
Return EXACTLY 4 comparisons as a JSON array. Nothing else — no markdown, no backticks, no preamble, no explanation.
Each object: {"emoji": "single emoji", "text": "the comparison sentence", "category": "one of: time|size|count|money|rate|probability"}

## CORE PRINCIPLES (from Making Numbers Count)

### 1. SIMPLER MULTIPLIER + MORE FAMILIAR REFERENCE
Research shows "roughly twice the size of California" beats "47.3 times the size of Rhode Island" — always prefer familiar references with simple multipliers (1x, 2x, 3x, 10x, half, quarter). Never use decimal multipliers like 4.7x.

### 2. USE WHOLE NUMBERS, PREFERABLY SMALL
The core maxim: "Use whole numbers, not too many. Preferably small." Round aggressively. Say "about 30" not "29.7." Say "roughly a third" not "33.28%."

### 3. FOCUS ON 1 AT A TIME
Reduce to a single unit whenever possible. "Every second, 3 barrels are consumed" is better than "100 million barrels per day." Per-person, per-second, per-heartbeat — bring it to the individual scale.

### 4. FIND YOUR FATHOM (Familiar Comparisons)
Use objects and places people can picture. A "fathom" is a measurement unit derived from the human body (arm span). Always anchor to things people know viscerally — not abstract units.

### 5. CONVERT TO PROCESS (Unfold Over Time)
Capitalize on our intuitive sense of time. Instead of static volume, show how long something would take. "If you spent $1 million per day, it would take you 2,740 years to spend $1 trillion."

### 6. TRANSFERRED EMOTION
Pick comparisons that already carry the emotional weight you need. "That's more than the GDP of Norway" carries implicit prestige. "That's enough to fill every swimming pool in Texas" carries implicit vastness.

### 7. CRYSTALLIZE THEN BREAK (Surprise)
Set up an expectation, then shatter it. "A million seconds is 12 days. A billion seconds is... 32 years." The contrast creates the aha moment.

### 8. SMALL BASKETS FOR PROBABILITIES
For percentages and probabilities, use "1 in X" framing with basket sizes that feel real. "1 out of 500" or "2 out of 1,000" — never say "0.2% of people."

## TECHNIQUE SELECTION MATRIX

Apply techniques based on the INPUT TYPE:

| Input Type | Primary Technique | Secondary Technique |
|---|---|---|
| Tiny probability (<1%) | "1 in X" basket sizing | Category jumper / surprise comparison |
| Large count (>1M) | Concrete stacking / lining up | Time unfolding |
| Money (large) | Time-rate ("$X per second since...") | Per-person division |
| Money (small) | Daily/hourly equivalent | Familiar purchase comparison |
| Area / Volume | Familiar landmark ratio (2x California) | Nested "fill X swimming pools" |
| Rate / Speed | Human-body anchor (heartbeat, breath) | Time conversion |
| Weight | Animal / vehicle comparison | Stacking visualization |
| Distance | Journey comparison (round trips) | Time-to-travel at familiar speed |
| Percentage (>10%) | "X out of every Y people in this room" | Visual proportion |
| Percentage (<10%) | "1 in X" framing | Named-group comparison |

## REGIONAL REFERENCE LIBRARIES

### India 🇮🇳
Landmarks & places: Wankhede Stadium (33,000 capacity), Eden Gardens (68,000), area of Goa (3,702 km²), area of Kerala, distance Delhi-to-Mumbai (1,400 km), Gateway of India height (26m), Rajpath/Kartavya Path length
Vehicles & objects: Tata Nano, auto-rickshaw, Mumbai local train (carries ~4,500 per trip), chai cups, cricket bats
Cultural: Bollywood films produced per year (~1,500-2,000), IPL match duration, cricket pitch length (22 yards), dosas, rotis
Currency: Use ₹ and lakhs/crores notation. 1 crore = 10 million. "That's ₹2.3 crore per minute"
Population anchors: Mumbai (21M), Delhi (19M), Bangalore (12M), Indian Railways daily passengers (23M)

### United States 🇺🇸
Landmarks & places: Football fields (100 yards/360 ft), Statue of Liberty (305 ft), Empire State Building (1,454 ft), Grand Canyon depth (6,093 ft), Central Park (843 acres), Texas area, Manhattan area
Vehicles & objects: School buses (35-45 ft), Boeing 747, yellow taxis, shopping carts, Big Macs
Cultural: Super Bowl viewers (~115M), Disneyland annual visitors (~18M), NYC subway daily riders (3.5M)
Currency: USD. "That's $X per second" or "$X for every American"
Population anchors: NYC (8.3M), LA (4M), US total (335M)

### United Kingdom 🇬🇧
Landmarks & places: Double-decker buses (11m long), Wembley Stadium (90,000 capacity), Big Ben height (96m), distance London-to-Edinburgh (534 km), area of Wales, The Shard height (310m), Hyde Park (350 acres)
Vehicles & objects: Black cabs, red phone boxes, pints of beer
Cultural: Premier League match attendance, BBC viewers, cups of tea consumed daily (~100M)
Currency: Use £. "That's £X per household"
Population anchors: London (9M), UK total (67M)

### UAE / Middle East 🇦🇪
Landmarks & places: Burj Khalifa (828m), Palm Jumeirah area, Dubai Mall floor space (502,000 m²), area of Bahrain, Persian Gulf
Vehicles & objects: Oil barrels, Toyota Land Cruisers, dhow boats
Cultural: Dubai annual tourists (~17M), Abu Dhabi Grand Prix
Currency: Use AED/USD. Reference oil prices per barrel.
Population anchors: Dubai (3.5M), UAE total (10M), Saudi Arabia (36M)

### Global 🌍
Landmarks: Olympic swimming pools (2,500 m³), Eiffel Tower (330m), blue whales (30m, 150 tons), Earth circumference (40,075 km), Mount Everest (8,849m), Great Wall of China (21,196 km)
Time anchors: Human heartbeats (~72/min), blinks (~15-20/min), breaths (~16/min)
Population: World (8 billion), China (1.4B), US (335M), UK (67M)

## MODE BEHAVIOR

### Fun Mode 🎪
- Be playful, surprising, use pop culture references
- Aim for "no way!" reactions
- Use humor and absurdity when it aids comprehension
- Lean into the surprise/crystallize-break technique
- Use tangible, sensory comparisons (you can picture it, feel it, taste it)

### Business Mode 📊
- Use industry benchmarks, GDP comparisons, market cap analogies
- Revenue-per-second, cost-per-employee framing
- Professional but still vivid — never boring
- Compare to well-known companies, national budgets, industry metrics
- Frame in terms of business impact and decisions

## QUALITY RULES

1. Each of the 4 comparisons MUST use a different technique from the matrix above
2. At least one comparison must be viscerally physical (you can picture it)
3. At least one must involve time
4. At least one must use a region-specific reference
5. Keep each comparison to 1-2 sentences max
6. Use simple multipliers (2x, 10x, half) — never 4.7x or 13.2x
7. Round aggressively — "about 30" not "29.7"
8. The comparison must be ACCURATE — do the math correctly
9. Never start two comparisons the same way
10. Prefer concrete nouns over abstract concepts
11. NEVER use generic filler analogies like pizza slices, pie slicing, or other clichéd proportional metaphors. Every comparison must be specifically tailored to the phenomenon — not a one-size-fits-all visual.

## EXAMPLE OUTPUT (for "India's population, 1,440,000,000 people, Fun mode, India region")

[{"emoji":"🏟️","text":"If every person in India walked into Wankhede Stadium single file, you'd need to fill and empty it 43,000 times — roughly once every 12 minutes, non-stop, for an entire year.","category":"count"},{"emoji":"⏱️","text":"If you tried to count to 1.44 billion at one number per second, without sleeping, eating or stopping, you'd finish in about 46 years.","category":"time"},{"emoji":"🚂","text":"Every single day, India's railways carry about 23 million passengers. It would still take two full months of daily ridership to move a number of people equal to India's population.","category":"size"},{"emoji":"🌍","text":"Roughly 1 in every 6 humans alive on Earth right now is Indian.","category":"count"}]'''

# ---------------------------------------------------------------------------
# Region auto-detection
# ---------------------------------------------------------------------------
def detect_region() -> str:
    """Best-effort region detection from locale/timezone."""
    try:
        loc = locale.getdefaultlocale()[0] or ""
        mapping = {
            "en_IN": "🇮🇳 India",
            "hi_IN": "🇮🇳 India",
            "en_US": "🇺🇸 United States",
            "en_GB": "🇬🇧 United Kingdom",
            "ar_AE": "🇦🇪 UAE / Middle East",
        }
        for prefix, region in mapping.items():
            if loc.startswith(prefix):
                return region
    except Exception:
        pass
    try:
        tz = time.tzname[0] if time.tzname else ""
        if "IST" in tz or "Asia/Kolkata" in tz:
            return "🇮🇳 India"
        if "GMT" in tz or "BST" in tz:
            return "🇬🇧 United Kingdom"
        if "GST" in tz:
            return "🇦🇪 UAE / Middle East"
    except Exception:
        pass
    return "🇺🇸 United States"


# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
def inject_css():
    st.markdown("""
    <style>
    /* Global */
    .stApp {
        background-color: #0A0A0F;
    }
    .block-container {
        max-width: 720px !important;
        padding-top: 2rem !important;
    }

    /* Header */
    .lab-subtitle {
        text-align: center;
        color: #4ECDC4;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        color: #E8E8E8;
        margin-bottom: 0.15rem;
        line-height: 1.15;
    }
    .tagline {
        text-align: center;
        color: #888888;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    /* Input card */
    .input-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1rem;
        margin-bottom: 1.5rem;
    }


    /* Mode buttons */
    .mode-btn {
        flex: 1;
        text-align: center;
        padding: 0.6rem 0;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        color: #888;
    }
    .mode-btn.active {
        background: rgba(78,205,196,0.15);
        border-color: #4ECDC4;
        color: #4ECDC4;
    }

    /* Result cards */
    .result-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1.25rem 1.25rem 1rem 1.25rem;
        margin-bottom: 0.85rem;
        border-left: 4px solid var(--accent);
        position: relative;
    }
    .result-card .emoji {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }
    .result-card .text {
        color: #E8E8E8;
        font-size: 1rem;
        line-height: 1.55;
    }
    .category-badge {
        display: inline-block;
        padding: 0.15rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.65rem;
        background: rgba(255,255,255,0.06);
    }

    /* Reference bar */
    .ref-bar {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #888;
        font-size: 0.85rem;
    }
    .ref-bar .ref-label {
        color: #555;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* CTA button */
    .cta-wrapper .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.65rem 0;
        background: linear-gradient(135deg, #4ECDC4 0%, #44B8B0 100%);
        color: #0A0A0F;
        border: none;
        transition: all 0.2s;
    }
    .cta-wrapper .stButton > button:hover {
        background: linear-gradient(135deg, #5ED8CF 0%, #4ECDC4 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(78,205,196,0.3);
    }
    .cta-wrapper .stButton > button:active {
        transform: translateY(0);
    }


    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 10px;
    }

    /* Text input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------
def generate_comparisons(query: str, mode: str, region: str) -> list[dict]:
    """Call Claude to generate 4 perspective comparisons."""
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    user_prompt = f"""Input: {query}
Mode: {mode}
Region: {region}

Generate 4 perspective comparisons. Return ONLY the JSON array."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = message.content[0].text.strip()

    # Clean potential markdown formatting
    response_text = response_text.strip("`").strip()
    if response_text.startswith("json"):
        response_text = response_text[4:].strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Fallback: extract JSON array with regex
        match = re.search(r"\[.*\]", response_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Could not parse response as JSON.")


# ---------------------------------------------------------------------------
# Render helpers
# ---------------------------------------------------------------------------
def render_header():
    st.markdown('<div class="lab-subtitle">Friday AI Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Make It Make Sense</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tagline">Turn any number into something you can actually picture.</div>',
        unsafe_allow_html=True,
    )


def render_result_card(comparison: dict):
    """Render a single comparison card."""
    cat = comparison.get("category", "size")
    color = CATEGORY_COLORS.get(cat, "#4ECDC4")
    emoji = comparison.get("emoji", "💡")
    text = comparison.get("text", "")

    st.markdown(
        f"""
        <div class="result-card" style="--accent: {color};">
            <div class="emoji">{emoji}</div>
            <div class="text">{text}</div>
            <span class="category-badge" style="color: {color}; border: 1px solid {color}33;">{cat}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_reference_bar(query: str):
    st.markdown(
        f"""
        <div class="ref-bar">
            <span class="ref-label">Original</span>
            <span>{query}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        '<div class="footer">Built with Claude &middot; Friday AI Lab Series</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------
def main():
    inject_css()
    render_header()

    # Input field
    query = st.text_input(
        "Describe a number",
        placeholder="e.g. Saudi Aramco makes 535 billion USD in annual revenue",
        key="input_query",
    )
    st.caption(
        'Try: "India\'s population is 1.44 billion" · '
        '"Saudi Aramco revenue is 535 billion USD" · '
        '"Lightning strike odds are 1 in 1.2 million"'
    )

    # Mode & Region
    col_mode, col_region = st.columns(2)
    with col_mode:
        mode = st.selectbox(
            "Mode",
            ["Fun 🎪", "Business 📊"],
            index=0,
        )
    with col_region:
        detected = detect_region()
        region_options = list(REGIONS.keys())
        default_idx = region_options.index(detected) if detected in region_options else 1
        region_key = st.selectbox(
            "Region",
            region_options,
            index=default_idx,
        )

    # Generate button (wrapped for scoped CSS)
    st.markdown('<div class="cta-wrapper">', unsafe_allow_html=True)
    cta_clicked = st.button("Make It Make Sense ✨")
    st.markdown('</div>', unsafe_allow_html=True)

    if cta_clicked:
        if not query.strip():
            st.warning("Please describe a number to put in perspective.")
            return

        mode_label = "Fun" if "Fun" in mode else "Business"
        region_label = REGIONS[region_key]

        with st.spinner("Putting it in perspective..."):
            try:
                comparisons = generate_comparisons(
                    query.strip(),
                    mode_label,
                    region_label,
                )
                st.session_state["results"] = comparisons
                st.session_state["result_meta"] = {"query": query.strip()}
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.button("Retry")
                return

    # Display results
    if "results" in st.session_state:
        st.markdown("---")
        st.markdown("### Here's the perspective")
        for comp in st.session_state["results"]:
            render_result_card(comp)

        meta = st.session_state.get("result_meta", {})
        if meta:
            render_reference_bar(meta["query"])

    render_footer()


if __name__ == "__main__":
    main()
