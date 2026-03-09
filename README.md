# 🔢 Make It Make Sense

**Turn any number into something you can actually picture.**

Ever read a stat like *"Saudi Aramco earns $535 billion annually"* and think... cool, but what does that even *mean*? This app takes abstract numbers and transforms them into vivid, instantly graspable comparisons — backed by real cognitive science research.

> 🧠 Grounded in Chip Heath's *Making Numbers Count* and Microsoft Research's *Perspective Engine*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude-blueviolet?style=flat&logo=anthropic)](https://anthropic.com)

---

## ✨ What It Does

You give it a number. It gives you **4 vivid perspective comparisons** that make it click.

**Example — India's population (1.44 billion people):**

| | Comparison |
|---|---|
| 🏟️ | Fill and empty Wankhede Stadium 43,000 times — once every 12 minutes for a year |
| ⏱️ | Counting at 1 per second, non-stop, you'd finish in about 46 years |
| 🚂 | India's railways carry 23M daily — it'd still take 2 months to move everyone |
| 🌍 | Roughly 1 in every 6 humans alive right now is Indian |

---

## 🎮 Features

- **Two modes** — Fun 🎪 (playful, surprising) or Business 📊 (benchmarks, industry framing)
- **Regional awareness** — Comparisons use landmarks and references from 🇮🇳 India, 🇺🇸 US, 🇬🇧 UK, 🇦🇪 UAE, or 🌍 Global
- **Pre-loaded examples** — One-click demos to try instantly
- **Research-backed** — Uses 8 proven techniques from cognitive science (simpler multipliers, time unfolding, small baskets, and more)
- **Dark themed UI** — Clean, modern, LinkedIn-showcase-ready

---

## 🚀 Quick Start

### 1. Clone

```bash
git clone https://github.com/Pushpesh-31/make-it-make-sense.git
cd make-it-make-sense
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

### 4. Run

```bash
streamlit run app.py
```

---

## 🧪 Pre-loaded Examples

| Phenomenon | Number | Unit |
|---|---|---|
| Annual revenue of Saudi Aramco | 535,000,000,000 | USD |
| Daily oil production worldwide | 100,000,000 | barrels |
| Chance of lightning strike in a year | 0.0000008 | probability |
| Deepwater Horizon oil spill volume | 210,000,000 | gallons |
| India's population | 1,440,000,000 | people |
| Distance to Mars (closest) | 55,000,000 | kilometers |

---

## 🛠️ Tech Stack

- **Frontend** — Streamlit with custom dark-themed CSS
- **AI** — Anthropic Claude (claude-sonnet-4-20250514)
- **Language** — Python 3.11+

---

## 📁 Project Structure

```
make-it-make-sense/
├── app.py                  # The entire app
├── requirements.txt        # Dependencies
├── .streamlit/
│   ├── config.toml         # Theme config
│   └── secrets.toml        # API key (gitignored)
└── .gitignore
```

---

## 🧠 The Science Behind It

The system prompt encodes 8 research-backed principles:

1. **Simpler Multiplier** — "2x California" beats "47.3x Rhode Island"
2. **Whole Numbers** — Round aggressively, keep it small
3. **Focus on 1** — Per-person, per-second, per-heartbeat
4. **Find Your Fathom** — Anchor to things people know viscerally
5. **Convert to Process** — Unfold over time for intuitive grasp
6. **Transferred Emotion** — Pick references that carry emotional weight
7. **Crystallize & Break** — Set expectation, then shatter it
8. **Small Baskets** — "1 in 500" not "0.2%"

---

## 📄 License

MIT — do whatever you want with it.

---

<p align="center">
  <strong>Built with Claude · Friday AI Lab Series</strong><br>
  <sub>Making numbers make sense, one comparison at a time.</sub>
</p>
