import os
import streamlit as st
from openai import OpenAI

# Set up the page
st.set_page_config(page_title="AI Creative Builder", page_icon="🎨")

st.title("🎨 AI Creative Builder")
st.write("Generate ad copy ideas with the help of AI.")

# --- 1. Inputs ---

product_name = st.text_input("Product name", placeholder="Hydrating Vitamin C Serum")

brand_tone = st.selectbox(
    "Brand tone",
    ["Playful", "Luxury", "Professional", "Edgy", "Friendly", "Minimalist"],
)

channel = st.selectbox(
    "Channel",
    ["Facebook", "Instagram", "TikTok", "Google Search", "LinkedIn", "Display Banner"],
)

extra_context = st.text_area(
    "Anything else the AI should know?",
    placeholder="Target audience, benefits, offers, etc.",
)

# --- 2. Set up OpenAI client ---

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning(
        "OPENAI_API_KEY is not set. "
        "In your terminal, run:\n\n"
        'export OPENAI_API_KEY="your-real-key-here"\n'
        "Then restart this app."
    )
else:
    client = OpenAI(api_key=api_key)

    def generate_creatives(product_name, brand_tone, channel, extra_context):
        prompt = f"""
You are an expert performance marketing copywriter.

Create ad creative for this product:

Product: {product_name}
Brand tone: {brand_tone}
Channel: {channel}
Extra context: {extra_context or "N/A"}

Return three sections, clearly labeled:

HEADLINE:
(one short, punchy headline)

PRIMARY_TEXT:
(1–3 sentences of ad copy, optimized for the channel)

IMAGE_CONCEPT:
(a visual concept that could be used by a designer or AI image model)
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write high-converting, on-brand ad creatives.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content

    # --- 3. Button + output ---

    if st.button("Generate creatives"):
        if not product_name:
            st.error("Please enter a product name first.")
        else:
            with st.spinner("Asking the AI for ideas..."):
                try:
                    result = generate_creatives(
                        product_name, brand_tone, channel, extra_context
                    )
                except Exception as e:
                    st.error(f"Something went wrong talking to OpenAI: {e}")
                else:
                    st.subheader("✨ AI-generated creative")
                    st.markdown(result)
                    st.caption("Powered by OpenAI – model: gpt-4o-mini")
