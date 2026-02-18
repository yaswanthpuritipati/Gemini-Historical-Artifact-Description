Project Demo:https://drive.google.com/file/d/1lIKMKX5XjGW0KfBFTqg4miBHyIP1Wwhz/view?usp=drive_link

# 🏛️ Gemini Historical Artifact Explorer

> **Uncover the stories behind humanity's greatest treasures — powered by Google Gemini AI**

A premium web application built with **Streamlit** and **Google's Gemini 2.5 Flash** AI model that generates rich, scholarly descriptions and analyses of historical artifacts. Users can either type an artifact name or upload an image for AI-powered historical analysis.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [Application Workflow](#-application-workflow)
- [UI/UX Design](#-uiux-design)
- [API Integration](#-api-integration)
- [Configuration](#-configuration)
- [Security Notes](#-security-notes)
- [Troubleshooting](#-troubleshooting)
- [Learning Resources](#-learning-resources)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Overview

The **Gemini Historical Artifact Explorer** is an AI-powered web application designed for historians, museum curators, researchers, and history enthusiasts. It leverages Google's cutting-edge **Gemini 2.5 Flash** large language model to generate detailed, engaging, and scholarly descriptions of historical artifacts.

### What It Does

The application provides two primary modes of interaction:

1. **Text-Based Description (Describe by Name)** — Users type the name of any artifact, monument, or historical period, and the AI generates a comprehensive scholarly description.
2. **Image-Based Analysis (Analyze from Image)** — Users upload a photograph of an artifact (pottery, sculpture, manuscript, weapon, jewelry, architecture, etc.), and the AI identifies, classifies, and analyzes it.

### Who It's For

| Audience | Use Case |
|---|---|
| 🎓 **Historians** | Research assistance, artifact documentation |
| 🏛️ **Museum Curators** | Exhibit descriptions, catalog entries |
| 📚 **Students** | Learning about historical artifacts and periods |
| 🔬 **Researchers** | Quick artifact identification and context |
| 🌍 **History Enthusiasts** | Exploring and discovering artifacts |

---

## 🎯 Features

### Core Features

| Feature | Description |
|---|---|
| **📝 Text-Based Descriptions** | Enter any artifact name or historical period to generate detailed AI descriptions |
| **🖼️ Image Analysis** | Upload artifact photos (JPG, PNG, GIF, WEBP) for AI-powered identification and analysis |
| **🎯 Adjustable Detail Level** | Slider control to set description length from 500 to 2,000 words |
| **📥 Downloadable Reports** | Export generated content as `.txt` or `.md` (Markdown) files |
| **🤖 Gemini 2.5 Flash** | Powered by Google's latest and fastest generative AI model |
| **💡 Historical Facts** | Sidebar displays random curated historical facts for engagement |

### AI-Generated Content Sections

**For text-based descriptions:**
1. **Historical Background** — Origin, time period, cultural context
2. **Physical Characteristics** — Materials, dimensions, notable features
3. **Historical Significance** — Importance and lasting impact
4. **Interesting Facts** — Unique or lesser-known details
5. **Modern Context** — Relevance today and current location

**For image-based analysis:**
1. **Identification** — Artifact classification, type, and likely origin
2. **Historical Background** — Period, culture, and context
3. **Physical Analysis** — Materials, craftsmanship, condition assessment
4. **Significance** — Importance and cultural impact
5. **Interesting Facts** — Unique details and observations

### UI/UX Features

- **Premium Museum Theme** — Dark terracotta & cream color palette inspired by archaeology and museum aesthetics
- **Glassmorphism Cards** — Frosted glass effect UI components
- **Smooth Animations** — Fade-in transitions, floating icons, and subtle hover effects
- **Ornamental Dividers** — Decorative diamond-centered dividers
- **Responsive Layout** — Adapts to different screen sizes
- **Sidebar Panel** — API status indicator, random facts, feature list, and about section
- **Elegant Typography** — Cinzel (serif headings), Cormorant Garamond (quotes), Inter (body text)

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                   USER BROWSER                  │
│          (localhost:8501 — Streamlit UI)         │
└──────────────────────┬──────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────┐
│              STREAMLIT SERVER (app.py)           │
│                                                 │
│  ┌─────────────┐  ┌──────────────────────────┐  │
│  │  Sidebar     │  │   Main Content Area      │  │
│  │  • API Status│  │   ┌──────────────────┐   │  │
│  │  • Facts     │  │   │ Tab 1: Text Mode │   │  │
│  │  • Features  │  │   │ Tab 2: Image Mode│   │  │
│  │  • About     │  │   └──────────────────┘   │  │
│  └─────────────┘  └──────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │         get_gemini_response()            │   │
│  │     (Prompt Engineering + API Call)       │   │
│  └──────────────────┬───────────────────────┘   │
└─────────────────────┼───────────────────────────┘
                      │ HTTPS (API)
┌─────────────────────▼───────────────────────────┐
│          GOOGLE GENERATIVE AI API               │
│          (Gemini 2.5 Flash Model)               │
│                                                 │
│  • Text generation from prompts                 │
│  • Multimodal input (text + image)              │
│  • Markdown-formatted responses                 │
└─────────────────────────────────────────────────┘
```

### Data Flow

```
User Input (text/image)
    │
    ▼
Prompt Engineering (structured prompt with instructions)
    │
    ▼
Google Generative AI API (Gemini 2.5 Flash)
    │
    ▼
AI Response (markdown-formatted text)
    │
    ▼
Streamlit UI Rendering (glass cards, result cards)
    │
    ▼
Optional Download (TXT / Markdown export)
```

---

## 📁 Project Structure

```
Gemini Historical Artifact/
│
├── .streamlit/
│   └── config.toml           # Streamlit theme & server configuration
│
├── .venv/                     # Python virtual environment (not committed)
│
├── app.py                     # Main application (UI + logic + CSS)
├── requirements.txt           # Python package dependencies
├── .env.example               # Example environment variables
├── models.txt                 # Reference list of available Gemini models
└── README.md                  # Project documentation (this file)
```

### File Descriptions

| File | Purpose |
|---|---|
| `app.py` | The single-file Streamlit application containing all UI, CSS, and logic (~885 lines) |
| `requirements.txt` | Python dependencies: `streamlit`, `google-generativeai`, `python-dotenv`, `Pillow` |
| `.streamlit/config.toml` | Streamlit configuration: theme colors, server settings, dev options |
| `.env.example` | Template for environment variables (API key) |
| `models.txt` | Reference file listing available Google Generative AI model names |

---

## 📚 Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Core programming language |
| **Streamlit** | ≥ 1.28.0 | Web application framework for rapid UI development |
| **Google Generative AI SDK** | ≥ 0.8.0 | Python client for Google's Gemini API |
| **Pillow (PIL)** | ≥ 10.0.0 | Image processing and handling |
| **python-dotenv** | ≥ 1.0.0 | Environment variable management |

### AI Model

- **Model**: `gemini-2.5-flash` (Google's latest fast generative model)
- **Capabilities**: Text generation, multimodal analysis (text + image input)
- **API**: Google Generative AI REST API via Python SDK

### Frontend Technologies (within Streamlit)

- **CSS3** — Custom styling with CSS variables, animations, glassmorphism
- **Google Fonts** — Cinzel, Cormorant Garamond, Inter
- **HTML5** — Custom HTML components via `st.markdown(unsafe_allow_html=True)`

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8 or higher** installed on your system
- **Google Generative AI API Key** (free tier available)
- **pip** (Python package manager)

### Step 1: Clone or Download the Project

```bash
git clone <repository-url>
cd "Gemini Historical Artifact"
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Obtain a Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API key"**
4. Copy the generated API key

### Step 5: Configure the API Key

The API key is currently configured directly in `app.py`. For production use, set it as an environment variable:

```bash
# Create .env file
cp .env.example .env
# Edit .env and add your API key
GOOGLE_API_KEY=your_api_key_here
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

### Step 7: Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

---

## 📖 Usage Guide

### Mode 1: Describe by Name (Text Input)

1. Open the app and select the **"✍️ Describe by Name"** tab
2. Type the name of an artifact, monument, or historical period in the text field
   - Examples: *"Tutankhamun's Golden Mask"*, *"Terracotta Army"*, *"Viking Runestone"*
3. Adjust the **Description length** slider (500–2,000 words)
4. Click **"🚀 Generate Description"**
5. Wait for Gemini AI to generate the response
6. Read the formatted result with section headers
7. Download as **Text** or **Markdown** using the buttons below

### Mode 2: Analyze from Image (Image Upload)

1. Select the **"🖼️ Analyze from Image"** tab
2. Upload an artifact image using drag-and-drop or browse
   - Supported formats: **JPG, JPEG, PNG, GIF, WEBP**
3. The image preview will appear centered on the page
4. Adjust the **Analysis length** slider (500–2,000 words)
5. Click **"🔍 Analyze Artifact"**
6. Wait for Gemini AI to examine and analyze the image
7. Read the identification and analysis results
8. Download as **Text** or **Markdown**

### Usage Examples

| Artifact | Mode | Words | Expected Output |
|---|---|---|---|
| Tutankhamun's Golden Mask | Text | 1200 | Egyptian history, gold craftsmanship, 18th dynasty context |
| Leonardo da Vinci's Notebook | Text | 800 | Renaissance context, mirror writing, scientific illustrations |
| The Bayeux Tapestry | Text | 1500 | Norman conquest of 1066, embroidery techniques, narrative art |
| *Upload pottery photo* | Image | 1000 | Classification, period identification, material analysis |
| The Rosetta Stone | Text | 1000 | Ptolemaic dynasty, decipherment history, British Museum |

---

## ⚙️ Application Workflow

### Internal Process Flow

```
1. USER ACTION
   └── Enters text OR uploads image + sets word count

2. INPUT VALIDATION
   ├── Check API key is configured
   ├── Check text field is not empty (Text mode)
   └── Check file is uploaded (Image mode)

3. PROMPT ENGINEERING
   ├── Text Mode: Structured prompt with 5 section headers + word count
   └── Image Mode: Expert persona prompt + image data + 5 section headers

4. API CALL (get_gemini_response)
   ├── Initialize GenerativeModel('gemini-2.5-flash')
   ├── Call generate_content() with prompt (+ optional image)
   └── Return response.text

5. RESPONSE RENDERING
   ├── Calculate word count
   ├── Display result card with title + word badge
   ├── Render markdown-formatted response
   └── Provide download buttons (TXT + MD)

6. ERROR HANDLING
   ├── API key not configured → st.error()
   ├── Empty input → st.warning()
   └── API errors → Display error message
```

### Session State Management

| Key | Type | Purpose |
|---|---|---|
| `api_key_configured` | `bool` | Tracks whether the API key was successfully configured |

---

## 🎨 UI/UX Design

### Design Philosophy

The app is designed with a **museum-quality, archaeological aesthetic** to match the historical artifact theme. The design choices reinforce the feeling of exploring ancient treasures.

### Color Palette — Warm Terracotta & Cream

| Color | Hex Code | CSS Variable | Usage |
|---|---|---|---|
| Terracotta | `#C4693D` | `--terra` | Primary accent, buttons, active states |
| Terracotta Light | `#E8A878` | `--terra-light` | Headings, links, highlights |
| Terracotta Dark | `#9B4A28` | `--terra-dark` | Gradients, dark accents |
| Cream | `#F5ECD7` | `--cream` | Button text, bright accents |
| Background Primary | `#1A1512` | `--bg-primary` | Main page background |
| Card Background | `rgba(38,30,26,0.8)` | `--bg-card` | Glass card backgrounds |
| Text Primary | `#F0E8D8` | `--text-primary` | Main body text |
| Text Muted | `#A89880` | `--text-muted` | Secondary text, labels |

### Typography

| Font | Type | Usage |
|---|---|---|
| **Cinzel** | Serif | Headings, card titles, hero title — evokes ancient inscriptions |
| **Cormorant Garamond** | Serif (Italic) | Subtitle, fact cards — scholarly, elegant quotes |
| **Inter** | Sans-serif | Body text, buttons, labels — modern readability |

### Animations

| Animation | Duration | Usage |
|---|---|---|
| `fadeInUp` | 0.5–0.8s | Cards, results appearing |
| `fadeIn` | 0.5s | Image preview |
| `shimmer` | 3s (infinite) | Hero title brightness pulse |
| `floatIcon` | 3s (infinite) | Hero and sidebar icons floating |
| `pulse-dot` | 2s (infinite) | API status indicator |

### UI Components

| Component | Description |
|---|---|
| **Hero Header** | Centered title with floating icon and italic subtitle |
| **Glass Cards** | Frosted glass containers with top accent lines |
| **Ornamental Dividers** | Gradient lines with centered diamond decoration |
| **Tab Bar** | Pill-style tab selector with gradient active state |
| **Buttons** | Gradient filled with hover lift animation |
| **Status Indicator** | Sidebar pill with pulsing dot (green/red) |
| **Fact Cards** | Left-bordered italic quotes in the sidebar |
| **Word Badges** | Small gradient pills showing word counts |
| **Result Cards** | Special containers for AI output with decorative top bar |

---

## 🔗 API Integration

### Google Generative AI SDK

The application uses the `google-generativeai` Python package to interact with Google's Gemini API.

### Core Function

```python
def get_gemini_response(prompt, image=None):
    """Generate response from Gemini model."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text
```

### Prompt Engineering

**Text Mode Prompt Structure:**
```
Generate a detailed and engaging description of **{artifact_name}**.

Include the following sections:
1. Historical Background — Origin, time period, cultural context
2. Physical Characteristics — Materials, dimensions, notable features
3. Historical Significance — Importance and lasting impact
4. Interesting Facts — Unique or lesser-known details
5. Modern Context — Relevance today and current location

Write approximately {word_count} words in an engaging, informative tone
suitable for historians, museum curators, and history enthusiasts.
Use markdown formatting with headers.
```

**Image Mode Prompt Structure:**
```
You are a world-class historian and artifact expert.
Analyze the artifact shown in this image and provide a detailed description.

Include:
1. Identification — What is this artifact? Classify its type and likely origin.
2. Historical Background — Period, culture, and context.
3. Physical Analysis — Materials, craftsmanship, condition.
4. Significance — Why is it important?
5. Interesting Facts — Unique details.

Write approximately {word_count} words in an engaging, scholarly tone.
Use markdown formatting with headers.
```

### Image Input Format

```python
image_parts = {
    "mime_type": uploaded_file.type,   # e.g., "image/jpeg"
    "data": uploaded_file.getvalue(),  # raw bytes
}
```

---

## 🔧 Configuration

### Streamlit Configuration (`.streamlit/config.toml`)

```toml
[logger]
level = "info"

[client]
showErrorDetails = true

[browser]
gatherUsageStats = false

[server]
headless = true
port = 8501
runOnSave = true          # Auto-reload on file save (development)

[theme]
primaryColor = "#C4693D"              # Terracotta
backgroundColor = "#1A1512"           # Dark warm brown
secondaryBackgroundColor = "#282018"  # Card background
textColor = "#F0E8D8"                # Warm cream text
font = "sans serif"
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | Your Google Generative AI API key |

### Requirements (`requirements.txt`)

```
streamlit>=1.28.0
google-generativeai>=0.8.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

---

## 🔐 Security Notes

- **⚠️ Never commit API keys** to version control. Use environment variables or Streamlit secrets.
- The application does **not** store user data, uploaded images, or generated descriptions persistently.
- API keys are only used during the current browser session.
- Uploaded images are processed in-memory and sent directly to the Gemini API — they are not saved to disk.
- For production deployment, use [Streamlit Secrets Management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) instead of hardcoding the API key.

---

## 🛠️ Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `TypeError: use_container_width` | Streamlit version too old for `st.image()` | Use `use_column_width=True` or upgrade Streamlit: `pip install --upgrade streamlit` |
| `404 models/gemini-pro not found` | Model name deprecated | Use `gemini-2.5-flash` (already configured) |
| `429 Too Many Requests` | API rate limiting | Wait a few seconds and retry; consider API quota limits |
| Title not visible | CSS gradient text not supported in browser | Fixed — now uses solid color with text-shadow |
| API Disconnected (sidebar) | Invalid or missing API key | Verify your API key at [Google AI Studio](https://aistudio.google.com/) |
| Image upload fails | Unsupported format | Use JPG, JPEG, PNG, GIF, or WEBP only |
| Blank response | API timeout or model issue | Retry the request; check internet connection |

---

## 🎓 Learning Resources

### Technologies
- [Streamlit Documentation](https://docs.streamlit.io/) — Official Streamlit reference
- [Google Generative AI Python SDK](https://ai.google.dev/gemini-api/docs) — Gemini API documentation
- [Streamlit Tutorial (DataCamp)](https://www.datacamp.com/tutorial/streamlit) — Beginner-friendly guide

### AI & LLMs
- [Large Language Models (LLM) — GeeksForGeeks](https://www.geeksforgeeks.org/large-language-model-llm/)
- [Google Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/learn-resources)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

### Design
- [Glassmorphism CSS Generator](https://css.glass/)
- [Google Fonts](https://fonts.google.com/)

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is provided as-is for **educational and research purposes**.

---

## 📧 Support

For issues or questions:
- [Google Generative AI Documentation](https://ai.google.dev/)
- [Streamlit Community Forum](https://discuss.streamlit.io/)

---

<div align="center">

**🏛️ Gemini Historical Artifact Explorer**

*Powered by Google Gemini 2.5 Flash · Built for Historical Research*

*Crafted with care for historians & museum curators*

</div>
