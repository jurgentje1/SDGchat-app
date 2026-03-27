import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIG & CONSTANTS
# ============================================================================

st.set_page_config(
    page_title="SDGChat",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

MODELS = {
    # ── Flagship ──
    "GPT-OSS 120B":      "openai/gpt-oss-120b",
    # ── Reasoning ──
    "Qwen QwQ 32B":      "qwen-qwq-32b",
    "DeepSeek R1 70B":   "deepseek-r1-distill-llama-70b",
    # ── Standard ──
    "LLaMA 3.3 70B":     "llama-3.3-70b-versatile",
    "LLaMA 3.1 8B":      "llama-3.1-8b-instant",
    "Qwen3 32B":         "qwen/qwen3-32b",
    # ── Vision ──
    "LLaMA 3.2 11B Vision": "llama-3.2-11b-vision-preview",
    "LLaMA 3.2 90B Vision": "llama-3.2-90b-vision-preview",
}

MODEL_BADGES = {
    "GPT-OSS 120B":         "Flagship",
    "Qwen QwQ 32B":         "Reasoning",
    "DeepSeek R1 70B":      "Reasoning",
    "LLaMA 3.3 70B":        "Versatile",
    "LLaMA 3.1 8B":         "Fast",
    "Qwen3 32B":            "32B",
    "LLaMA 3.2 11B Vision": "Vision",
    "LLaMA 3.2 90B Vision": "Vision",
}

PRESETS = {
    "🌍 Eco Expert": {
        "icon": "🌍",
        "temp": 0.5, 
        "prompt": "Je bent een expert in de Sustainable Development Goals, specifiek SDG 11 (Sustainable Cities and Communities) en SDG 15 (Life on Land). Help de gebruiker met vragen, educatie en plannen over duurzaamheid, groene infrastructuur en natuurbehoud.",
        "title": "SDG 11 & 15 Assistent",
        "subtitle": "Stel vragen over Sustainable Cities en Life on Land",
        "examples": [
            "Hoe zorgen we voor meer 'Sustainable Cities' (SDG 11)?",
            "Wat zijn de grootste uitdagingen voor 'Life on Land' (SDG 15)?",
            "Bedenk een project om biodiversiteit in de stad te verbeteren",
            "Welke concrete stappen kan mijn buurt nemen voor SDG 11?"
        ]
    },
    "🤖 Assistant": {
        "icon": "🤖",
        "temp": 0.7, 
        "prompt": "You are a helpful, friendly, and knowledgeable AI assistant. Respond clearly and concisely.",
        "title": "Hoe kan ik je helpen?",
        "subtitle": "Stel een vraag of start een gesprek",
        "examples": [
            "Leg quantumcomputing uit in eenvoudige termen",
            "Schrijf een Python functie voor Fibonacci",
            "Wat zijn de beste manieren om te leren coderen?",
            "Maak een creatief verhaal over de toekomst"
        ]
    },
    "💻 Coder": {
        "icon": "💻",
        "temp": 0.2, 
        "prompt": "You are an expert programmer and code reviewer. Provide clean, well-commented code solutions.",
        "title": "Codeer Assistent",
        "subtitle": "Vraag om code, debugging of architectuur advies",
        "examples": [
            "Schrijf een React component voor een takenlijst",
            "Hoe werkt async/await in Python?",
            "Vind de bug in deze variabele assignment",
            "Wat zijn de SOLID principes in software design?"
        ]
    },
    "✍️ Writer": {
        "icon": "✍️",
        "temp": 1.2, 
        "prompt": "You are a talented creative writer. Help with storytelling and writing advice using vivid language.",
        "title": "Creatieve Schrijver",
        "subtitle": "Hulp bij verhalen, blogs of creatieve teksten",
        "examples": [
            "Schrijf een spannend kort verhaal over tijdreizen",
            "Bedenk 5 pakkende titels voor mijn tech blog",
            "Verbeter deze alinea zodat hij vlotter leest",
            "Schrijf een haiku over de veranderende seizoenen"
        ]
    },
    "🔍 Analyst": {
        "icon": "🔍",
        "temp": 0.3, 
        "prompt": "You are a data analyst and critical thinker. Analyze information systematically and provide insights.",
        "title": "Data Analist",
        "subtitle": "Voor diepgaande analyses en kritisch denkwerk",
        "examples": [
            "Analyseer de voor- en nadelen van remote werken",
            "Hoe kan ik een dataset het beste visualiseren?",
            "Wat zijn de huidige trends in e-commerce?",
            "Beoordeel deze strategische beslissing kritisch"
        ]
    },
    "💡 Brainstormer": {
        "icon": "💡",
        "temp": 1.5, 
        "prompt": "You are a creative brainstorming partner. Generate innovative ideas and think outside the box.",
        "title": "Brainstorm Partner",
        "subtitle": "Ontdek nieuwe en creatieve ideeën",
        "examples": [
            "Bedenk 10 innovatieve ideeën voor een fitness app",
            "Hoe kan ik een saai onderwerp leuk presenteren?",
            "Originele suggesties voor een verjaardagscadeau",
            "Alternatieve toepassingen voor oude kartonnen dozen"
        ]
    },
    "🤔 Philosopher": {
        "icon": "🤔",
        "temp": 1.1, 
        "prompt": "You are a thoughtful philosopher. Explore ideas deeply and ask meaningful questions.",
        "title": "De Filosoof",
        "subtitle": "Verken diepe vragen en existentiële thema's",
        "examples": [
            "Wat is de ware zin van het leven?",
            "Hoe beïnvloedt moderne technologie onze identiteit?",
            "Bestaan er fundamentele en objectieve waarden?",
            "Vergelijk het stoïcisme met het modernisme"
        ]
    },
    "🎯 Debater": {
        "icon": "🎯",
        "temp": 1.0, 
        "prompt": "You are a skilled debater. Present logical arguments and engage in constructive discourse.",
        "title": "De Debater",
        "subtitle": "Voor scherpe argumenten en constructief debat",
        "examples": [
            "Beargumenteer waarom AI strikter gereguleerd moet worden",
            "Wat zijn de sterkste argumenten vóór een basisinkomen?",
            "Overtuig mij dat we in een simulatie leven",
            "Wat is de optimale rol van de overheid?"
        ]
    },
    "📚 Teacher": {
        "icon": "📚",
        "temp": 0.5, 
        "prompt": "You are an experienced educator. Explain concepts clearly and adapt to different learning styles.",
        "title": "De Docent",
        "subtitle": "Leer iets nieuws, geduldig en duidelijk uitgelegd",
        "examples": [
            "Leg de relativiteitstheorie uit aan een middelbare scholier",
            "Hoe werkte de samenleving in het Romeinse rijk?",
            "Leer me de basis van Franse grammatica",
            "Waarom is de lucht blauw?"
        ]
    },
}

# ============================================================================
# SESSION STATE
# ============================================================================

defaults = {
    "messages": [],
    "current_model": "GPT-OSS 120B",
    "current_preset": "🌍 Eco Expert",
    "temperature": 0.5,
    "system_prompt": PRESETS["🌍 Eco Expert"]["prompt"]
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================================
# CSS
# ============================================================================

def get_theme_css():
    bg_main = "#0f1117"
    text_main = "#e0e0e0"
    bg_card = "rgba(35,35,55,.75)"
    bg_card_hover = "rgba(45,45,70,.95)"
    border_col = "rgba(255,107,53,.35)"
    border_col_card = "rgba(255,107,53,.22)"
    text_muted = "#c8c8d8"
    dialog_bg = "#1a1a2e"
    chat_user = "rgba(255,107,53,.13)"
    chat_bot = "rgba(100,100,160,.18)"
    input_bg = "rgba(30,30,50,.85)"
    input_focus = "rgba(35,35,60,1)"

    return f"""
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
        background: {bg_main} !important;
        color: {text_main};
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    header[data-testid="stHeader"] {{ display: none !important; }}

    [data-testid="stMainBlockContainer"],
    [data-testid="block-container"] {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes chatPop {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* ── Header ── */
    .gc-header-left {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 0 10px 20px;
    }}
    .gc-logo {{
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #ff6b35, #ff5520);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
        flex-shrink: 0;
    }}
    .gc-brand-title {{ font-size: 18px; font-weight: 700; color: {text_main}; line-height: 1.2; }}
    .gc-brand-sub   {{ font-size: 12px; color: #888; }}

    /* ── Model selectbox ── */
    div[data-testid="stSelectbox"] label {{ display: none !important; }}

    div[data-testid="stSelectbox"] > div > div[data-baseweb="select"] > div {{
        background: rgba(255,107,53,.08) !important;
        border: 1px solid {border_col} !important;
        border-radius: 8px !important;
        min-height: 38px !important;
    }}

    /* The visible text value */
    div[data-testid="stSelectbox"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stSelectbox"] span,
    div[data-testid="stSelectbox"] div[class*="ValueContainer"] {{
        color: {text_main} !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
    }}

    /* Caret */
    div[data-testid="stSelectbox"] svg {{ fill: #ff6b35 !important; }}

    /* Dropdown menu */
    [data-baseweb="popover"] ul {{
        background: {dialog_bg} !important;
        border: 1px solid rgba(255,107,53,.3) !important;
        border-radius: 10px !important;
    }}
    [data-baseweb="popover"] li {{
        color: {text_main} !important;
        font-size: 13px !important;
    }}
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] li[aria-selected="true"] {{
        background: rgba(255,107,53,.15) !important;
    }}

    /* ── Header icon buttons ── */
    div[data-testid="stButton"] > button {{
        background: {bg_card} !important;
        border: 1px solid {border_col} !important;
        border-radius: 8px !important;
        color: {text_main} !important;
        font-size: 16px !important;
        padding: 6px 10px !important;
        transition: all .25s ease !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        background: {bg_card_hover} !important;
        border-color: rgba(255,107,53,.55) !important;
    }}

    /* ── Welcome screen ── */
    .gc-welcome {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 72vh;
        text-align: center;
        padding: 40px 20px 120px;
        animation: fadeIn .55s ease-out;
    }}
    .gc-chat-icon {{
        width: 110px; height: 110px;
        background: linear-gradient(135deg, #ff6b35, #ff8555);
        border-radius: 28px;
        display: flex; align-items: center; justify-content: center;
        font-size: 54px;
        margin-bottom: 28px;
        box-shadow: 0 12px 40px rgba(255,107,53,.25);
    }}
    .gc-title    {{ font-size: 40px; font-weight: 700; color: {text_main}; margin-bottom: 10px; }}
    .gc-subtitle {{ font-size: 15px; color: #888; margin-bottom: 38px; }}

    .gc-cards div[data-testid="stButton"] > button {{
        background: {bg_card} !important;
        border: 1px solid {border_col_card} !important;
        border-radius: 14px !important;
        color: {text_muted} !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 18px 20px !important;
        text-align: left !important;
        white-space: normal !important;
        height: auto !important;
        line-height: 1.45 !important;
        transition: all .25s ease !important;
    }}
    .gc-cards div[data-testid="stButton"] > button:hover {{
        background: {bg_card_hover} !important;
        border-color: rgba(255,107,53,.5) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(255,107,53,.12) !important;
        color: {text_main} !important;
    }}

    /* ── Chat messages ── */
    div[data-testid="stChatMessage"] {{
        animation: chatPop .35s ease-out;
        max-width: 860px;
        margin: 0 auto;
    }}
    div[data-testid="stChatMessageUser"] div[data-testid="stChatMessageContent"] {{
        background: {chat_user};
        border-left: 3px solid #ff6b35;
        border-radius: 12px;
        padding: 14px 18px;
    }}
    div[data-testid="stChatMessageAssistant"] div[data-testid="stChatMessageContent"] {{
        background: {chat_bot};
        border-left: 3px solid #7b8bff;
        border-radius: 12px;
        padding: 14px 18px;
    }}
    div[data-testid="stChatMessageContent"] p,
    div[data-testid="stChatMessageContent"] {{ color: {text_main}; }}

    /* ── Chat input ── */
    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] input {{
        background: {input_bg} !important;
        border: 1px solid rgba(255,107,53,.30) !important;
        border-radius: 16px !important;
        color: {text_main} !important;
        font-size: 14px !important;
    }}
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] input:focus {{
        background: {input_focus} !important;
        border-color: rgba(255,107,53,.6) !important;
        box-shadow: 0 0 15px rgba(255,107,53,.18) !important;
    }}
    div[data-testid="stChatInput"] button {{
        background: linear-gradient(135deg, #ff6b35, #ff5520) !important;
        border-radius: 50% !important;
        border: none !important;
        color: #fff !important;
    }}

    /* ── Status bar ── */
    .gc-status {{
        text-align: center;
        font-size: 12px;
        color: #888;
        padding: 6px 0 10px;
    }}
    .gc-status-dot {{
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #ff6b35;
        margin-right: 5px;
        vertical-align: middle;
    }}

    /* ── Settings dialog (st.dialog) ── */
    div[data-testid="stDialog"] > div {{
        background: {dialog_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 18px !important;
        padding: 28px !important;
    }}
    div[data-testid="stDialog"] h2 {{
        color: {text_main} !important;
        font-size: 18px !important;
    }}
    /* Slider */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {{
        background: #ff6b35 !important;
    }}
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[class*="Track"] {{
        background: {border_col} !important;
    }}
    /* Textarea */
    div[data-testid="stTextArea"] textarea {{
        background: {input_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 10px !important;
        color: {text_main} !important;
        font-size: 13px !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 7px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,107,53,.04); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(255,107,53,.28); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,107,53,.5); }}

    .section-label {{
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 10px;
    }}
</style>
"""

st.markdown(get_theme_css(), unsafe_allow_html=True)

# ============================================================================
# GROQ API
# ============================================================================

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ API key niet gevonden. Maak een `.env` bestand met `GROQ_API_KEY=your_key`")
        st.stop()
    return Groq(api_key=api_key)

def stream_groq_response(messages_list, model, temperature, system_prompt):
    try:
        client = get_groq_client()
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages_list)
        stream = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=temperature,
            stream=True,
            max_tokens=2048,
        )
        full_response = ""
        for chunk in stream:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                full_response += content
                yield full_response
    except Exception as e:
        st.error(f"❌ API Fout: {str(e)}")
        return

# ============================================================================
# SETTINGS DIALOG  (st.dialog = echte popup, sluit met ✕ of Escape)
# ============================================================================

@st.dialog("⚙️ Instellingen", width="large")
def settings_dialog():
    # ── Presets ──
    st.markdown('<div class="section-label">Rol preset</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, (pname, pdata) in enumerate(PRESETS.items()):
        with cols[idx % 2]:
            is_active = pname == st.session_state.current_preset
            icon, role = pdata["icon"], pname.split(" ", 1)[1] if " " in pname else pname
            label = f"{icon} {role}  (temp {pdata['temp']})"
            if is_active:
                st.button(label, disabled=True, use_container_width=True, key=f"pd_{idx}_on")
            else:
                if st.button(label, use_container_width=True, key=f"pd_{idx}"):
                    st.session_state.current_preset = pname
                    st.session_state.temperature    = pdata["temp"]
                    st.session_state.system_prompt  = pdata["prompt"]
                    st.rerun()

    st.divider()

    # ── Temperature ──
    st.markdown(
        f'<div class="section-label">Temperatuur &nbsp;'
        f'<span style="color:#ff6b35;font-weight:700;">{st.session_state.temperature}</span></div>',
        unsafe_allow_html=True,
    )
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0, max_value=2.0,
        value=float(st.session_state.temperature),
        step=0.1,
        label_visibility="collapsed",
    )

    st.divider()

    # ── System prompt ──
    st.markdown('<div class="section-label">Systeemaanwijzing</div>', unsafe_allow_html=True)
    st.session_state.system_prompt = st.text_area(
        "Prompt",
        value=st.session_state.system_prompt,
        height=140,
        label_visibility="collapsed",
    )

    if st.button("💾  Opslaan & sluiten", use_container_width=True, key="save_and_close"):
        st.rerun()   # closes the dialog

# ============================================================================
# HEADER
# ============================================================================

col_left, col_right = st.columns([3, 2])

active_preset = PRESETS[st.session_state.current_preset]

with col_left:
    role_name = st.session_state.current_preset.split(" ", 1)[1] if " " in st.session_state.current_preset else st.session_state.current_preset
    st.markdown(f"""
    <div class="gc-header-left">
        <div class="gc-logo">{active_preset['icon']}</div>
        <div>
            <div class="gc-brand-title">SDGChat</div>
            <div class="gc-brand-sub">Rol: {role_name}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    model_names = list(MODELS.keys())
    model_index = model_names.index(st.session_state.current_model) if st.session_state.current_model in model_names else 0

    hc1, hc2, hc3 = st.columns([6, 1, 1])
    with hc1:
        selected_model = st.selectbox(
            "Model",
            options=model_names,
            index=model_index,
            label_visibility="collapsed",
            key="model_select",
            format_func=lambda m: f"{m}  ·  {MODEL_BADGES.get(m, '')}",
        )
        st.session_state.current_model = selected_model

    with hc2:
        if st.button("🗑️", key="clear_chat", help="Gesprek wissen"):
            st.session_state.messages = []
            st.rerun()

    with hc3:
        if st.button("⚙️", key="settings_toggle", help="Instellingen"):
            settings_dialog()   # opens the modal popup

st.markdown("<hr style='margin:0; border-color:rgba(255,107,53,.12);'>", unsafe_allow_html=True)

# ============================================================================
# MAIN AREA
# ============================================================================

if not st.session_state.messages:
    st.markdown(f"""
    <div class="gc-welcome">
        <div class="gc-chat-icon">{active_preset['icon']}</div>
        <div class="gc-title">{active_preset['title']}</div>
        <div class="gc-subtitle">{active_preset['subtitle']} aan {st.session_state.current_model}</div>
    </div>
    """, unsafe_allow_html=True)

    _, card_col, _ = st.columns([1, 4, 1])
    with card_col:
        st.markdown('<div class="gc-cards">', unsafe_allow_html=True)
        row1 = st.columns(2)
        row2 = st.columns(2)
        examples = active_preset["examples"]
        for idx, prompt in enumerate(examples):
            if idx >= 4:
                break
            col = row1[idx] if idx < 2 else row2[idx - 2]
            with col:
                if st.button(prompt, use_container_width=True, key=f"example_{idx}"):
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ============================================================================
# CHAT INPUT + STREAMING
# ============================================================================

prompt = st.chat_input("Typ een bericht... (Enter om te sturen, Shift+Enter voor nieuwe regel)")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for partial in stream_groq_response(
            st.session_state.messages,
            MODELS[st.session_state.current_model],
            st.session_state.temperature,
            st.session_state.system_prompt,
        ):
            full_response = partial
            placeholder.markdown(full_response + " ▍")
        placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# ============================================================================
# STATUS BAR
# ============================================================================

preset_icon = active_preset['icon']
preset_name = st.session_state.current_preset.split(" ", 1)[1] if " " in st.session_state.current_preset else st.session_state.current_preset
badge = MODEL_BADGES.get(st.session_state.current_model, "")

st.markdown(f"""
<div class="gc-status">
    <span class="gc-status-dot"></span>
    {st.session_state.current_model}
    {"· <span style='color:#ff6b35;font-weight:700;'>"+badge+"</span>" if badge else ""}
    &nbsp;·&nbsp; {preset_icon} {preset_name}
    &nbsp;·&nbsp; Gebalanceerd ({st.session_state.temperature})
</div>
""", unsafe_allow_html=True)