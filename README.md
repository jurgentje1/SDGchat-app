# visit the site

https://sdgchat.streamlit.app/

# SDGChat (Streamlit + Groq)

A modern Streamlit chat app with multiple AI roles, model switching, and real-time streaming responses via the Groq API.

## Features

- Sticky top header for always-visible navigation and controls
- Multiple role presets (Eco Expert, Coder, Writer, Analyst, and more)
- Fast model switcher with badge labels
- Configurable temperature and system prompt in settings dialog
- Streaming assistant responses for smoother UX
- Clean custom dark theme and responsive layout

## Tech Stack

- Python
- Streamlit
- Groq Python SDK
- python-dotenv

## Requirements

- Python 3.10+ recommended
- A Groq API key

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your key:
     ```env
     GROQ_API_KEY=your_api_key_here
     ```

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit (typically `http://localhost:8501`).

## Project Structure

- `app.py` - main Streamlit application
- `requirements.txt` - Python dependencies
- `.env.example` - environment variable template

## Notes

- Keep `.env` private and never commit secrets.
- The header is intentionally fixed/sticky to remain accessible during scrolling.

## License

MIT (or your preferred license).
