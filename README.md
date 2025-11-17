# 🎨 AI Creative Builder

An AI-powered tool that generates high-quality advertising creatives — including headlines, primary ad text, and designer-ready image concepts — based on product details, brand tone, and the intended marketing channel.

Built with:
- **Python**
- **Streamlit** (UI)
- **OpenAI API** (model: `gpt-4o-mini`)

---

## 🌟 Features

### ✔ AI-Generated Ad Headlines  
Short, punchy lines optimized for platforms like Instagram, Facebook, TikTok, and Google.

### ✔ AI-Written Primary Text  
1–3 sentence ad copy tailored to the selected brand tone and channel.

### ✔ AI Image Concept Recommendations  
Clear visual ideas a designer or image model (like DALL·E or Midjourney) could use to create creative variations.

### ✔ Clean, Simple UI  
Built with Streamlit for fast iteration and demo-ready presentation.

---

## 🚀 Demo (Run Locally)

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/ai-creative-builder.git
cd ai-creative-builder
````

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Set it in your shell configuration (recommended):

```bash
export OPENAI_API_KEY="your-key-here"
```

Or store it permanently in `~/.bash_profile` or `~/.zshrc`:

```bash
nano ~/.bash_profile
# Add this line:
export OPENAI_API_KEY="your-key-here"
source ~/.bash_profile
```

### 5. Run the app

```bash
streamlit run app.py
```

Open the browser link that appears:

```
http://localhost:8501
```

---

## 🧩 How It Works

* The app collects:

  * Product name
  * Brand tone
  * Channel
  * Additional creative context

* It sends a structured prompt to OpenAI’s `gpt-4o-mini` model.

* The model returns 3 labeled sections:

  * **HEADLINE**
  * **PRIMARY_TEXT**
  * **IMAGE_CONCEPT**

* Streamlit displays everything cleanly.

This mirrors how real creative generation systems work inside ads platforms.

---

## 📄 Example Output

**HEADLINE**

> “Glow All Out: Bright Skin, Zero Effort”

**PRIMARY_TEXT**

> A luxury vitamin C serum crafted for visible radiance.
> Made for Instagram audiences who scroll fast but value instant results.

**IMAGE_CONCEPT**

> Soft-focus close-up of glowing skin beside citrus slices in diffused natural lighting.

---

## 🔮 Future Enhancements (Planned)

These are features I plan to add next — both for portfolio depth and product realism:

* Generate **3–5 variations** of creative
* Add **brand presets** (e.g., Nike, Sephora, Apple-like tones)
* Add “Copy to Clipboard” buttons
* Export creatives as CSV or JSON
* Allow users to generate **matching DALL·E prompts**
* Add “rate this creative” → feed into iteration loop
* Add guardrails (e.g., avoid false claims, sensitive categories)

---

## ⭐ Project Status

**Version 1.0 — Fully working AI-powered creative generator.**
More enhancements coming soon.

```

---
