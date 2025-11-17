import os
import json
import textwrap
import streamlit as st
from openai import OpenAI

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="AI Creative Builder", page_icon="🎨", layout="wide")

st.title("🎨 AI Creative Builder")
st.write("Generate multiple AI-powered ad creatives with scoring, brand presets, and image prompts.")

# -------------------------
# Brand presets (C)
# -------------------------
BRAND_PRESETS = {
    "None / Custom": {
        "description": "Use only the tone you select below.",
        "voice": "",
        "tone_override": None,
    },
    "Apple-style (minimal, premium)": {
        "description": "Clean, minimalist, aspirational, focus on experience over features.",
        "voice": (
            "Write in a calm, minimal, premium voice. Short sentences. "
            "Avoid exclamation marks. Focus on experience, not specs."
        ),
        "tone_override": "Minimalist, premium, aspirational",
    },
    "Nike-style (bold, motivational)": {
        "description": "Energetic, bold, movement-focused, emotional motivation.",
        "voice": (
            "Write in a bold, high-energy, movement-driven voice. "
            "Use active verbs, emotional phrases, and a slightly edgy tone."
        ),
        "tone_override": "Energetic, bold, motivational",
    },
    "Sephora-style (beauty, expert yet friendly)": {
        "description": "Beauty-focused, expert-backed but still warm and friendly.",
        "voice": (
            "Write in a modern beauty brand voice: expert but accessible, "
            "benefit-focused, inclusive, and friendly."
        ),
        "tone_override": "Modern beauty, expert yet friendly",
    },
    "Duolingo-style (chaotic, cheeky)": {
        "description": "Playful, chaotic, slightly unhinged, internet-native.",
        "voice": (
            "Write in a chaotic, cheeky, meme-aware voice. "
            "Use internet-native language and playful threats, but keep it brand-safe."
        ),
        "tone_override": "Chaotic, cheeky, playful",
    },
}

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("⚙️ Settings")

preset_name = st.sidebar.selectbox(
    "Brand preset",
    list(BRAND_PRESETS.keys()),
    index=0,
)

preset = BRAND_PRESETS[preset_name]
st.sidebar.write(preset["description"])

st.sidebar.markdown("---")
st.sidebar.write("This app uses OpenAI's `gpt-4o-mini` model to generate creatives.")

# -------------------------
# Main input controls
# -------------------------
product_name = st.text_input("Product name", placeholder="Hydrating Vitamin C Serum")

brand_tone = st.selectbox(
    "Brand tone (used if no preset override)",
    ["Playful", "Luxury", "Professional", "Edgy", "Friendly", "Minimalist"],
)

channel = st.selectbox(
    "Channel",
    ["Facebook", "Instagram", "TikTok", "Google Search", "LinkedIn", "Display Banner"],
)

extra_context = st.text_area(
    "Anything else the AI should know?",
    placeholder="Target audience, benefits, key claims, offer, etc.",
)

num_variations = 3  # fixed for now – could be made configurable

# -------------------------
# OpenAI client setup
# -------------------------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.warning(
        "OPENAI_API_KEY is not set. "
        "Set it in your shell (e.g., ~/.bash_profile) and restart your terminal.\n\n"
        'Example:\n\nexport OPENAI_API_KEY="your-real-key-here"'
    )
    client = None
else:
    client = OpenAI(api_key=api_key)


# -------------------------
# Helpers
# -------------------------
def wrap_text_for_display(s: str, width: int = 80) -> str:
    """Wrap long lines so blocks don't force horizontal scrolling."""
    if not s:
        return ""
    paragraphs = s.split("\n")
    wrapped = []
    for p in paragraphs:
        if not p.strip():
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(p, width=width))
    return "\n".join(wrapped)


def render_score_row(label: str, value):
    """Render one score row as label + progress bar + numeric value."""
    try:
        v = int(value)
    except (TypeError, ValueError):
        v = None

    if v is None:
        pct = 0
        display = "—"
    else:
        v = max(0, min(10, v))
        pct = v * 10
        display = f"{v}/10"

    col_label, col_bar, col_val = st.columns([1.4, 5, 1])
    with col_label:
        st.write(label)
    with col_bar:
        st.progress(pct)
    with col_val:
        st.write(display)


def generate_creatives(product_name, brand_tone, channel, extra_context, preset, num_variations=3):
    effective_tone = preset["tone_override"] or brand_tone
    preset_voice = preset["voice"]

    system_msg = (
        "You are an expert performance marketing creative strategist. "
        "You generate multiple ad creatives and score them."
    )

    user_prompt = f"""
Create {num_variations} distinct ad creative variations for this product.

Product: {product_name}
Effective brand tone: {effective_tone}
Channel: {channel}
Extra context: {extra_context or "N/A"}

Brand preset voice guidelines:
{preset_voice or "None. Use only the effective brand tone."}

For EACH variation, generate:
- A short, punchy HEADLINE
- 1–3 sentence PRIMARY_TEXT optimized for the channel
- An IMAGE_CONCEPT: a clear visual idea for a designer or an image model
- A DALLE_PROMPT: a text prompt suitable for DALL·E-style image generation
- SCORES: integers from 1 to 10 for:
  - clarity
  - brand_fit
  - channel_fit
  - scroll_stopping
  - overall

Return ONLY valid JSON in this exact structure:

{{
  "variations": [
    {{
      "id": "A",
      "headline": "...",
      "primary_text": "...",
      "image_concept": "...",
      "dalle_prompt": "...",
      "scores": {{
        "clarity": 0,
        "brand_fit": 0,
        "channel_fit": 0,
        "scroll_stopping": 0,
        "overall": 0
      }}
    }},
    {{
      "id": "B",
      ...
    }},
    {{
      "id": "C",
      ...
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw_content = response.choices[0].message.content

    # Try to parse JSON; if it fails, return raw string for display
    try:
        start = raw_content.find("{")
        end = raw_content.rfind("}") + 1
        json_str = raw_content[start:end]
        data = json.loads(json_str)
        return data, raw_content, None
    except Exception as e:
        return None, raw_content, e


# -------------------------
# UI: Generate button & results
# -------------------------
if st.button("🚀 Generate creatives"):
    if not product_name:
        st.error("Please enter a product name first.")
    elif not client:
        st.error("OpenAI client is not configured.")
    else:
        with st.spinner("Asking the AI for multiple variations..."):
            data, raw_output, parse_error = generate_creatives(
                product_name,
                brand_tone,
                channel,
                extra_context,
                preset,
                num_variations=num_variations,
            )

        if parse_error or not data:
            st.error("I had trouble parsing the AI response as JSON. Showing raw output instead.")
            st.code(raw_output)
        else:
            variations = data.get("variations", [])
            if not variations:
                st.warning("No variations came back from the model.")
            else:
                st.subheader("✨ AI-generated creatives")

                for var in variations:
                    var_id = var.get("id", "?")
                    headline = var.get("headline", "").strip()
                    primary_text = var.get("primary_text", "").strip()
                    image_concept = var.get("image_concept", "").strip()
                    dalle_prompt = var.get("dalle_prompt", "").strip()
                    scores = var.get("scores", {})

                    st.markdown(f"## Variation {var_id}")

                    # Wrap long texts so they’re fully visible
                    wrapped_headline = wrap_text_for_display(headline, width=80)
                    wrapped_primary = wrap_text_for_display(primary_text, width=80)
                    wrapped_image = wrap_text_for_display(image_concept, width=80)
                    wrapped_dalle = wrap_text_for_display(dalle_prompt, width=80)

                    # Headline – full-width, super readable
                    st.markdown("**Headline**")
                    st.markdown(wrapped_headline or "—")

                    # Primary Text – full-width
                    st.markdown("**Primary Text**")
                    st.markdown(wrapped_primary or "—")

                    # Image Concept – readable + copyable
                    st.markdown("**Image Concept**")
                    st.markdown(wrapped_image or "—")
                    with st.expander("Copy Image Concept"):
                        st.code(wrapped_image or "—")

                    # DALL·E Prompt – readable + copyable
                    st.markdown("**DALL·E Prompt**")
                    st.markdown(wrapped_dalle or "—")
                    with st.expander("Copy DALL·E Prompt"):
                        st.code(wrapped_dalle or "—")

                    # Creative scores as progress bars
                    st.markdown("**Creative Scores (1–10)**")
                    render_score_row("Clarity", scores.get("clarity"))
                    render_score_row("Brand fit", scores.get("brand_fit"))
                    render_score_row("Channel fit", scores.get("channel_fit"))
                    render_score_row("Scroll-stopping", scores.get("scroll_stopping"))
                    render_score_row("Overall", scores.get("overall"))

                    st.markdown("---")

                st.caption(
                    "Model: gpt-4o-mini"
                )
