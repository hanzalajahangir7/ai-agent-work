import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta
import base64
from io import BytesIO
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="PFFL AI Chatbot",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for exact PFFL styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header */
    .pffl-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .pffl-logo {
        font-size: 48px;
        margin-bottom: 10px;
    }
    
    .pffl-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .pffl-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 5px;
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #1e3a5f 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #334155;
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(30, 64, 175, 0.4);
    }
    
    .stat-value {
        font-size: 36px;
        font-weight: 700;
        color: #3b82f6;
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 14px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        box-shadow: 0 6px 12px rgba(30, 64, 175, 0.5);
        transform: translateY(-2px);
    }
    
    /* Game Cards */
    .game-card {
        background: #1e293b;
        padding: 16px;
        border-radius: 12px;
        margin: 10px 0;
        border: 1px solid #334155;
        transition: all 0.3s;
    }
    
    .game-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }
    
    .team-name {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
    }
    
    .game-time {
        font-size: 12px;
        color: #94a3b8;
    }
    
    .game-score {
        font-size: 24px;
        font-weight: 700;
        color: #3b82f6;
    }
    
    /* Navigation */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1e293b;
        padding: 12px 0;
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #334155;
        z-index: 1000;
        box-shadow: 0 -4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .nav-item {
        text-align: center;
        color: #94a3b8;
        cursor: pointer;
        padding: 8px 16px;
        transition: all 0.3s;
        border-radius: 8px;
    }
    
    .nav-item:hover {
        color: #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .nav-item.active {
        color: #3b82f6;
        background: rgba(59, 130, 246, 0.2);
    }
    
    .nav-icon {
        font-size: 24px;
        display: block;
        margin-bottom: 4px;
    }
    
    .nav-label {
        font-size: 11px;
        font-weight: 500;
    }
    
    /* Floating Mic Button */
    .mic-button {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.5);
        cursor: pointer;
        transition: all 0.3s;
        z-index: 999;
    }
    
    .mic-button:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 25px rgba(30, 64, 175, 0.7);
    }
    
    .mic-icon {
        font-size: 28px;
        color: white;
    }
    
    /* Modals */
    .modal-overlay {
        background: rgba(15, 23, 42, 0.95);
        padding: 20px;
        border-radius: 16px;
        border: 2px solid #334155;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    .modal-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }
    
    .modal-body {
        font-size: 16px;
        color: #94a3b8;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    
    .modal-icon {
        font-size: 64px;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Form Inputs */
    .stSelectbox, .stTextInput, .stDateInput, .stTimeInput {
        background: #1e293b;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div, .stTextInput > div > div > input {
        background: #1e293b;
        color: #ffffff;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    /* Progress Dots */
    .progress-dots {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin: 20px 0;
    }
    
    .progress-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #334155;
        transition: all 0.3s;
    }
    
    .progress-dot.active {
        background: #3b82f6;
        transform: scale(1.3);
    }
    
    /* Filter Buttons */
    .filter-button {
        display: inline-block;
        padding: 8px 16px;
        margin: 4px;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 20px;
        color: #94a3b8;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .filter-button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
    }
    
    .filter-button.active {
        background: #1e40af;
        border-color: #3b82f6;
        color: #ffffff;
    }
    
    /* Quick Actions */
    .quick-action {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(30, 64, 175, 0.3);
    }
    
    .quick-action:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(30, 64, 175, 0.5);
    }
    
    .quick-action-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }
    
    .quick-action-label {
        font-size: 14px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'leagues' not in st.session_state:
    st.session_state.leagues = [
        {
            'id': 1,
            'name': 'Phoenix Winter 2025',
            'format': '7v7',
            'start_date': '2025-01-15',
            'end_date': '2025-03-30',
            'teams': [
                {'id': 1, 'name': 'Phoenix Firebirds', 'logo': '🔥'},
                {'id': 2, 'name': 'Desert Storm', 'logo': '⛈️'},
                {'id': 3, 'name': 'Valley Vipers', 'logo': '🐍'},
                {'id': 4, 'name': 'Cactus Kings', 'logo': '🌵'},
                {'id': 5, 'name': 'Sun Devils', 'logo': '😈'},
                {'id': 6, 'name': 'Red Rocks', 'logo': '🪨'},
            ]
        },
        {
            'id': 2,
            'name': 'Phoenix Summer League',
            'format': '5v5',
            'start_date': '2025-06-01',
            'end_date': '2025-08-15',
            'teams': []
        }
    ]
if 'games' not in st.session_state:
    st.session_state.games = [
        {
            'id': 1,
            'league_id': 1,
            'league_name': 'Phoenix Winter 2025',
            'team_a': 'Phoenix Firebirds',
            'team_a_logo': '🔥',
            'team_b': 'Desert Storm',
            'team_b_logo': '⛈️',
            'date': '2025-01-20',
            'time': '10:00',
            'venue': 'Phoenix Sports Complex',
            'referee': 'John Carter',
            'status': 'Scheduled',
            'score_a': None,
            'score_b': None
        },
        {
            'id': 2,
            'league_id': 1,
            'league_name': 'Phoenix Winter 2025',
            'team_a': 'Valley Vipers',
            'team_a_logo': '🐍',
            'team_b': 'Cactus Kings',
            'team_b_logo': '🌵',
            'date': '2025-01-20',
            'time': '14:00',
            'venue': 'Desert Field',
            'referee': 'Anthony Brooks',
            'status': 'Scheduled',
            'score_a': None,
            'score_b': None
        },
        {
            'id': 3,
            'league_id': 1,
            'league_name': 'Phoenix Winter 2025',
            'team_a': 'Sun Devils',
            'team_a_logo': '😈',
            'team_b': 'Red Rocks',
            'team_b_logo': '🪨',
            'date': '2025-01-21',
            'time': '11:00',
            'venue': 'Valley Stadium',
            'referee': 'John Carter',
            'status': 'Scheduled',
            'score_a': None,
            'score_b': None
        }
    ]
if 'users' not in st.session_state:
    st.session_state.users = 2847
if 'pending_payments' not in st.session_state:
    st.session_state.pending_payments = 12540
if 'referees' not in st.session_state:
    st.session_state.referees = ['John Carter', 'Anthony Brooks', 'Sarah Williams', 'Mike Johnson']
if 'create_league_step' not in st.session_state:
    st.session_state.create_league_step = 1
if 'league_data' not in st.session_state:
    st.session_state.league_data = {}
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = None
if 'ai_response' not in st.session_state:
    st.session_state.ai_response = None
if 'chatbot_state' not in st.session_state:
    st.session_state.chatbot_state = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# System prompt for AI Chatbot
SYSTEM_PROMPT = """You are the PFFL AI Chatbot - a helpful assistant for the Phoenix Performance Flag Football League.

AVAILABLE LEAGUES: {leagues}
AVAILABLE REFEREES: {referees}

YOUR JOB:
1. Help users CREATE LEAGUES through a 12-step conversation
2. Help users SCHEDULE GAMES through conversation
3. Answer questions about leagues and games

LEAGUE CREATION - 12 STEPS:
When user wants to create a league, collect these in order:
1. format (5v5 or 7v7)
2. name (must be unique)
3. logo (emoji like 🏆)
4. start_date (YYYY-MM-DD format)
5. end_date (YYYY-MM-DD, must be after start_date)
6. fee_type (captain or player)
7. fee_amount (number)
8. num_teams (number)
9. teams (comma-separated team names)
10. venue (location name)
11. schedule_preferences (like "Weekends" or "Weekday evenings")
12. confirmation (yes/no)

GAME SCHEDULING:
When user wants to schedule a game, collect:
- league_name (which league)
- team_a (first team name)
- team_b (second team name)
- date (YYYY-MM-DD)
- time (HH:MM format like 14:30)
- venue (location)
- referee (from available referees)

RESPONSE RULES:
- Ask ONE question at a time
- Be friendly and conversational
- Remember previous answers
- When all info collected, create the league/game

RESPONSE FORMAT - Always return valid JSON:

For asking next question:
{{
  "action": "ask_question",
  "title": "Step 2: League Name",
  "body": "Great! You chose 7v7. What should we call your league?",
  "speak": "What name would you like for your league?",
  "current_step": 2,
  "total_steps": 12,
  "conversation_state": {{"format": "7v7", "name": null}}
}}

When league is complete:
{{
  "action": "create_league",
  "title": "League Created! 🎉",
  "body": "Your league 'Spring Championship' is ready with 6 teams!",
  "speak": "All done! Your league is created.",
  "data": {{
    "name": "Spring Championship",
    "format": "7v7",
    "start_date": "2025-01-15",
    "end_date": "2025-03-30",
    "teams": ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F"],
    "fee_type": "captain",
    "fee_amount": 50,
    "venue": "Phoenix Stadium",
    "schedule_preferences": "Weekends"
  }}
}}

When game is complete:
{{
  "action": "create_game",
  "title": "Game Scheduled! ⚡",
  "body": "Game between Firebirds and Storm is set for Sunday!",
  "speak": "Game scheduled successfully!",
  "data": {{
    "league_name": "Phoenix Winter 2025",
    "team_a": "Phoenix Firebirds",
    "team_b": "Desert Storm",
    "date": "2025-01-20",
    "time": "10:00",
    "venue": "Phoenix Sports Complex",
    "referee": "John Carter"
  }}
}}

For showing info:
{{
  "action": "show_info",
  "title": "Current Leagues",
  "body": "You have 2 active leagues: Phoenix Winter 2025 (7v7) and Phoenix Summer League (5v5).",
  "speak": "Here are your leagues"
}}

For errors:
{{
  "action": "error",
  "title": "Oops!",
  "body": "That league name already exists. Please choose a different name.",
  "speak": "Please try a different name"
}}

Remember: Return ONLY the JSON object. No extra text before or after."""

def get_ai_response(user_message, context=None):
    """Get AI response from Gemini with conversation state management"""
    if not GEMINI_API_KEY:
        return {
            "action": "error",
            "title": "API Key Missing",
            "body": "Please add your GEMINI_API_KEY to the .env file.",
            "buttons": [{"text": "Close"}]
        }
    
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
            }
        )
        
        # Build dynamic context
        leagues_list = [{"name": l['name'], "format": l['format'], "teams": len(l['teams'])} for l in st.session_state.leagues]
        
        context_data = {
            "leagues": leagues_list,
            "referees": st.session_state.referees,
            "total_games": len(st.session_state.games),
            "conversation_state": st.session_state.get('chatbot_state', {}),
            "chat_history": st.session_state.get('chat_history', [])[-3:] if st.session_state.get('chat_history') else []
        }
        
        if context:
            context_data.update(context)
        
        # Format system prompt with context
        formatted_prompt = SYSTEM_PROMPT.format(
            leagues=json.dumps(leagues_list),
            referees=', '.join(st.session_state.referees)
        )
        
        full_prompt = f"""{formatted_prompt}

CONTEXT DATA:
{json.dumps(context_data, indent=2)}

USER MESSAGE: {user_message}

IMPORTANT: Return ONLY valid JSON. No markdown, no code blocks, no extra text. Just pure JSON starting with {{ and ending with }}."""
        
        # Call Gemini API
        response = model.generate_content(full_prompt)
        response_text = response.text.strip()
        
        # Debug: Print raw response
        print(f"RAW AI RESPONSE: {response_text[:200]}...")
        
        # Clean up response text - remove markdown code blocks if present
        if response_text.startswith('```'):
            # Remove markdown code blocks
            lines = response_text.split('\n')
            # Find the first line that starts with { and last line that ends with }
            start_idx = 0
            end_idx = len(lines) - 1
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    start_idx = i
                    break
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().endswith('}'):
                    end_idx = i
                    break
            response_text = '\n'.join(lines[start_idx:end_idx + 1])
        
        # Try to find JSON in the response if it's not pure JSON
        if not response_text.startswith('{'):
            # Look for JSON object in the text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            else:
                # No JSON found, return error
                return {
                    "action": "error",
                    "title": "Response Format Issue",
                    "body": "I'm having trouble formatting my response. Let me try again.",
                    "speak": "Sorry, let me rephrase that."
                }
        
        # Parse JSON
        ai_response = json.loads(response_text)
        
        # Validate response has required fields
        if 'action' not in ai_response:
            ai_response['action'] = 'show_info'
        if 'title' not in ai_response:
            ai_response['title'] = 'AI Response'
        if 'body' not in ai_response:
            ai_response['body'] = 'Processing your request...'
        
        print(f"PARSED RESPONSE: {json.dumps(ai_response, indent=2)}")
        
        # Update conversation state if provided
        if 'conversation_state' in ai_response:
            st.session_state.chatbot_state = ai_response['conversation_state']
        
        return ai_response
        
    except json.JSONDecodeError as e:
        return {
            "action": "error",
            "title": "Response Format Error",
            "body": f"I had trouble understanding that. Could you try rephrasing your request?",
            "speak": "Sorry, I didn't quite get that. Can you try again?",
            "buttons": [{"text": "Close"}]
        }
    except Exception as e:
        return {
            "action": "error",
            "title": "Error",
            "body": f"Something went wrong: {str(e)[:100]}",
            "speak": "Oops, something went wrong. Please try again.",
            "buttons": [{"text": "Close"}]
        }

def check_duplicate_game(team_a, team_b, league_id):
    """Check if game already exists between two teams"""
    for game in st.session_state.games:
        if game['league_id'] == league_id:
            if (game['team_a'] == team_a and game['team_b'] == team_b) or \
               (game['team_a'] == team_b and game['team_b'] == team_a):
                return True
    return False

def create_game(team_a, team_b, date, time, venue, referee, league_id, league_name):
    """Create a new game"""
    # Get team logos
    league = next((l for l in st.session_state.leagues if l['id'] == league_id), None)
    team_a_logo = '🏈'
    team_b_logo = '🏈'
    
    if league:
        for team in league['teams']:
            if team['name'] == team_a:
                team_a_logo = team['logo']
            if team['name'] == team_b:
                team_b_logo = team['logo']
    
    new_game = {
        'id': len(st.session_state.games) + 1,
        'league_id': league_id,
        'league_name': league_name,
        'team_a': team_a,
        'team_a_logo': team_a_logo,
        'team_b': team_b,
        'team_b_logo': team_b_logo,
        'date': date,
        'time': time,
        'venue': venue,
        'referee': referee,
        'status': 'Scheduled',
        'score_a': None,
        'score_b': None
    }
    st.session_state.games.append(new_game)
    return new_game

def show_modal(modal_type, title, body, buttons):
    """Display a modal"""
    if modal_type == "success":
        st.markdown(f"""
        <div class="modal-overlay">
            <div class="modal-icon">✅</div>
            <div class="modal-title">{title}</div>
            <div class="modal-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)
    elif modal_type == "error":
        st.markdown(f"""
        <div class="modal-overlay">
            <div class="modal-icon">⚠️</div>
            <div class="modal-title">{title}</div>
            <div class="modal-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show buttons
    cols = st.columns(len(buttons))
    for idx, button in enumerate(buttons):
        with cols[idx]:
            if st.button(button['text'], key=f"modal_btn_{idx}", use_container_width=True):
                st.session_state.show_modal = None
                if button.get('primary'):
                    st.rerun()

def render_header():
    """Render PFFL header"""
    st.markdown("""
    <div class="pffl-header">
        <div class="pffl-logo">🛡️🏈</div>
        <h1 class="pffl-title">phoenix PFFL</h1>
        <p class="pffl-subtitle">Phoenix Performance Flag Football League</p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Render bottom navigation"""
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-item {'active' if st.session_state.page == 'home' else ''}" onclick="window.location.href='?page=home'">
            <span class="nav-icon">🏠</span>
            <span class="nav-label">Home</span>
        </div>
        <div class="nav-item {'active' if st.session_state.page == 'leagues' else ''}" onclick="window.location.href='?page=leagues'">
            <span class="nav-icon">🏆</span>
            <span class="nav-label">Leagues</span>
        </div>
        <div class="nav-item {'active' if st.session_state.page == 'games' else ''}" onclick="window.location.href='?page=games'">
            <span class="nav-icon">🏈</span>
            <span class="nav-label">Games</span>
        </div>
        <div class="nav-item {'active' if st.session_state.page == 'users' else ''}" onclick="window.location.href='?page=users'">
            <span class="nav-icon">👥</span>
            <span class="nav-label">Users</span>
        </div>
        <div class="nav-item {'active' if st.session_state.page == 'settings' else ''}" onclick="window.location.href='?page=settings'">
            <span class="nav-icon">⚙️</span>
            <span class="nav-label">Settings</span>
        </div>
    </div>
    <div class="mic-button">
        <span class="mic-icon">🎤</span>
    </div>
    """, unsafe_allow_html=True)

def render_home():
    """Render home dashboard"""
    st.markdown("### 📊 Dashboard Overview")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Leagues</div>
            <div class="stat-value">{len(st.session_state.leagues)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Active Games</div>
            <div class="stat-value">{len(st.session_state.games)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Registered Users</div>
            <div class="stat-value">{st.session_state.users:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Pending Payments</div>
            <div class="stat-value">${st.session_state.pending_payments:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Create League", use_container_width=True):
            st.session_state.page = 'create_league'
            st.rerun()
    
    with col2:
        if st.button("📅 Schedule Game", use_container_width=True):
            st.session_state.page = 'create_game'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Upcoming Games
    st.markdown("### 🏈 Upcoming Games")
    upcoming_games = sorted(
        [g for g in st.session_state.games if g['status'] == 'Scheduled'],
        key=lambda x: (x['date'], x['time'])
    )[:5]
    
    for game in upcoming_games:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="game-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="team-name">{game['team_a_logo']} {game['team_a']} vs {game['team_b_logo']} {game['team_b']}</div>
                        <div class="game-time">📅 {game['date']} at {game['time']} • {game['league_name']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='padding-top: 20px; color: #94a3b8;'>📍 {game['venue']}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Edit", key=f"edit_home_{game['id']}", use_container_width=True):
                st.session_state.edit_game_id = game['id']
                st.session_state.page = 'edit_game'
                st.rerun()

def render_games():
    """Render games list"""
    st.markdown("### 🏈 All Games")
    
    # Filter buttons
    filters = ['All Games', 'Phoenix Winter 2025', 'Phoenix Summer League']
    selected_filter = st.radio("", filters, horizontal=True, label_visibility="collapsed")
    
    # Filter games
    if selected_filter == 'All Games':
        filtered_games = st.session_state.games
    else:
        filtered_games = [g for g in st.session_state.games if g['league_name'] == selected_filter]
    
    # Display games
    for game in sorted(filtered_games, key=lambda x: (x['date'], x['time'])):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            score_display = ""
            if game['score_a'] is not None and game['score_b'] is not None:
                score_display = f"<span class='game-score'>{game['score_a']} - {game['score_b']}</span>"
            
            st.markdown(f"""
            <div class="game-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <div class="team-name">{game['team_a_logo']} {game['team_a']} vs {game['team_b_logo']} {game['team_b']}</div>
                        <div class="game-time">📅 {game['date']} at {game['time']} • {game['league_name']}</div>
                        <div class="game-time">📍 {game['venue']} • 👨‍⚖️ {game['referee']}</div>
                    </div>
                    <div style="text-align: center; min-width: 100px;">
                        {score_display}
                        <div style="color: #94a3b8; font-size: 12px; margin-top: 5px;">{game['status']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("Edit →", key=f"edit_game_{game['id']}", use_container_width=True):
                st.session_state.edit_game_id = game['id']
                st.session_state.page = 'edit_game'
                st.rerun()

def render_create_game():
    """Render create game screen"""
    st.markdown("### ➕ Create New Game")
    
    # Select league
    league_names = [l['name'] for l in st.session_state.leagues]
    selected_league_name = st.selectbox("League", league_names)
    selected_league = next(l for l in st.session_state.leagues if l['name'] == selected_league_name)
    
    # Team selection
    team_names = [t['name'] for t in selected_league['teams']]
    
    col1, col2 = st.columns(2)
    with col1:
        team_a = st.selectbox("Team A", team_names, key="team_a")
    with col2:
        team_b_options = [t for t in team_names if t != team_a]
        team_b = st.selectbox("Team B", team_b_options, key="team_b")
    
    # Date and time
    col1, col2 = st.columns(2)
    with col1:
        game_date = st.date_input("Game Date", min_value=datetime.now().date())
    with col2:
        game_time = st.time_input("Game Time")
    
    # Venue and officials
    venue = st.text_input("Venue", placeholder="Enter venue name")
    
    col1, col2 = st.columns(2)
    with col1:
        referee = st.selectbox("Referee", st.session_state.referees)
    with col2:
        stat_keeper = st.text_input("Stat Keeper (Optional)", placeholder="Enter name")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create button
    if st.button("🏈 Create Game", use_container_width=True, type="primary"):
        # Check for duplicate
        if check_duplicate_game(team_a, team_b, selected_league['id']):
            st.session_state.show_modal = {
                'type': 'error',
                'title': 'Game Already Scheduled',
                'body': 'A game between these two teams has already been created.',
                'buttons': [
                    {'text': 'Close'},
                    {'text': 'View Fixture', 'primary': True}
                ]
            }
            st.rerun()
        else:
            # Create game
            create_game(
                team_a, team_b,
                str(game_date), str(game_time),
                venue, referee,
                selected_league['id'], selected_league['name']
            )
            st.session_state.show_modal = {
                'type': 'success',
                'title': 'Game Created Successfully',
                'body': f'Your new Game has been added to the {selected_league["name"]} League.',
                'buttons': [
                    {'text': 'Close'},
                    {'text': 'View Game Details', 'primary': True}
                ]
            }
            st.rerun()
    
    # Back button
    if st.button("← Back to Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

def render_create_league():
    """Render create league wizard"""
    st.markdown(f"### ➕ Create New League - Step {st.session_state.create_league_step}/12")
    
    # Progress dots
    dots_html = '<div class="progress-dots">'
    for i in range(1, 13):
        active_class = 'active' if i == st.session_state.create_league_step else ''
        dots_html += f'<div class="progress-dot {active_class}"></div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step content
    if st.session_state.create_league_step == 1:
        st.markdown("#### Select League Format")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("5v5", use_container_width=True, key="5v5"):
                st.session_state.league_data['format'] = '5v5'
                st.session_state.create_league_step = 2
                st.rerun()
        with col2:
            if st.button("7v7", use_container_width=True, key="7v7"):
                st.session_state.league_data['format'] = '7v7'
                st.session_state.create_league_step = 2
                st.rerun()
    
    elif st.session_state.create_league_step == 2:
        st.markdown("#### League Details")
        league_name = st.text_input("League Name", placeholder="Enter league name")
        
        if st.button("Next →", use_container_width=True, type="primary"):
            if league_name:
                st.session_state.league_data['name'] = league_name
                st.session_state.create_league_step = 3
                st.rerun()
            else:
                st.error("Please enter a league name")
    
    elif st.session_state.create_league_step == 3:
        st.markdown("#### Upload League Logo")
        uploaded_file = st.file_uploader("Choose a logo", type=['png', 'jpg', 'jpeg'])
        
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.league_data['logo'] = '🏆'
            st.session_state.create_league_step = 4
            st.rerun()
    
    elif st.session_state.create_league_step == 4:
        st.markdown("#### League Duration")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min_value=datetime.now().date())
        with col2:
            end_date = st.date_input("End Date", min_value=datetime.now().date())
        
        if st.button("Next →", use_container_width=True, type="primary"):
            if end_date > start_date:
                st.session_state.league_data['start_date'] = str(start_date)
                st.session_state.league_data['end_date'] = str(end_date)
                st.session_state.create_league_step = 5
                st.rerun()
            else:
                st.error("End date must be after start date")
    
    elif st.session_state.create_league_step == 5:
        st.markdown("#### Entry Fee Type")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Per Captain", use_container_width=True):
                st.session_state.league_data['fee_type'] = 'captain'
                st.session_state.create_league_step = 6
                st.rerun()
        with col2:
            if st.button("Per Player", use_container_width=True):
                st.session_state.league_data['fee_type'] = 'player'
                st.session_state.create_league_step = 6
                st.rerun()
    
    else:
        st.markdown("#### Additional Setup")
        st.info("Steps 6-12 would include: Entry fee amount, team registration, referee assignment, schedule preferences, playoff format, rules, and final review.")
        
        if st.button("Complete League Creation", use_container_width=True, type="primary"):
            # Create league
            new_league = {
                'id': len(st.session_state.leagues) + 1,
                'name': st.session_state.league_data.get('name', 'New League'),
                'format': st.session_state.league_data.get('format', '7v7'),
                'start_date': st.session_state.league_data.get('start_date', str(datetime.now().date())),
                'end_date': st.session_state.league_data.get('end_date', str(datetime.now().date() + timedelta(days=90))),
                'teams': []
            }
            st.session_state.leagues.append(new_league)
            st.session_state.create_league_step = 1
            st.session_state.league_data = {}
            st.session_state.page = 'leagues'
            st.success("League created successfully!")
            st.rerun()
    
    # Back button
    if st.session_state.create_league_step > 1:
        if st.button("← Previous", use_container_width=True):
            st.session_state.create_league_step -= 1
            st.rerun()

def render_leagues():
    """Render leagues list"""
    st.markdown("### 🏆 All Leagues")
    
    for league in st.session_state.leagues:
        st.markdown(f"""
        <div class="game-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="team-name">🏆 {league['name']}</div>
                    <div class="game-time">Format: {league['format']} • {league['start_date']} to {league['end_date']}</div>
                    <div class="game-time">Teams: {len(league['teams'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View Details →", key=f"league_{league['id']}", use_container_width=True):
            st.session_state.selected_league_id = league['id']
            st.session_state.page = 'league_detail'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Create New League", use_container_width=True, type="primary"):
        st.session_state.page = 'create_league'
        st.rerun()

def render_ai_chat():
    """Render AI Chatbot interface with conversational league creation"""
    st.markdown("### 🤖 AI Chatbot")
    st.markdown("I can help you create leagues, schedule games, and manage your tournaments through conversation!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        for chat in st.session_state.chat_history[-10:]:  # Show last 10 messages
            # User message
            with st.container():
                st.markdown(f"**👤 You:** {chat['user']}")
            
            # AI response
            if 'ai' in chat:
                response = chat['ai']
                
                # Show progress if in league creation
                progress_html = ""
                if response.get('current_step') and response.get('total_steps'):
                    progress_percent = (response['current_step'] / response['total_steps']) * 100
                    progress_html = f"""
                    <div style="margin: 10px 0;">
                        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 4px;">
                            Step {response['current_step']} of {response['total_steps']}
                        </div>
                        <div style="background: #1e293b; height: 6px; border-radius: 3px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #1e40af, #3b82f6); height: 100%; width: {progress_percent}%; transition: width 0.3s;"></div>
                        </div>
                    </div>
                    """
                
                # Display AI response using Streamlit components
                with st.container():
                    col1, col2 = st.columns([0.1, 0.9])
                    with col1:
                        st.markdown("🤖")
                    with col2:
                        st.markdown(f"**{response.get('title', 'AI Response')}**")
                        
                        # Show progress if in league creation
                        if response.get('current_step') and response.get('total_steps'):
                            progress_percent = response['current_step'] / response['total_steps']
                            st.progress(progress_percent, text=f"Step {response['current_step']} of {response['total_steps']}")
                        
                        st.markdown(response.get('body', ''))
                        
                        if response.get('speak'):
                            st.info(f"💬 {response.get('speak')}")
                
                # Show created item details if available
                if 'created_item' in chat:
                    item = chat['created_item']
                    if item['type'] == 'league':
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #065f46 0%, #047857 100%); padding: 20px; border-radius: 12px; margin: 12px 0; border: 2px solid #10b981;">
                            <div style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">🏆 League Created Successfully!</div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">League Name</div>
                                    <div style="font-size: 16px; color: #ffffff; font-weight: 600;">{item['data']['name']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">Format</div>
                                    <div style="font-size: 16px; color: #ffffff; font-weight: 600;">{item['data']['format']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">Duration</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data']['start_date']} to {item['data']['end_date']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">Teams</div>
                                    <div style="font-size: 16px; color: #ffffff; font-weight: 600;">{len(item['data']['teams'])} Teams</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">Entry Fee</div>
                                    <div style="font-size: 14px; color: #ffffff;">${item['data'].get('fee_amount', 0)} per {item['data'].get('fee_type', 'captain')}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 4px;">Venue</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data'].get('venue', 'TBD')}</div>
                                </div>
                            </div>
                            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.2);">
                                <div style="font-size: 11px; color: #86efac; text-transform: uppercase; margin-bottom: 6px;">Teams</div>
                                <div style="font-size: 13px; color: #ffffff;">{', '.join([t['name'] if isinstance(t, dict) else t for t in item['data']['teams']])}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif item['type'] == 'game':
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); padding: 20px; border-radius: 12px; margin: 12px 0; border: 2px solid #60a5fa;">
                            <div style="font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 12px;">🏈 Game Scheduled Successfully!</div>
                            <div style="text-align: center; margin: 16px 0;">
                                <div style="font-size: 20px; font-weight: 700; color: #ffffff;">
                                    {item['data']['team_a']} <span style="color: #93c5fd;">vs</span> {item['data']['team_b']}
                                </div>
                            </div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                                <div>
                                    <div style="font-size: 11px; color: #bfdbfe; text-transform: uppercase; margin-bottom: 4px;">League</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data']['league_name']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #bfdbfe; text-transform: uppercase; margin-bottom: 4px;">Date & Time</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data']['date']} at {item['data']['time']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #bfdbfe; text-transform: uppercase; margin-bottom: 4px;">Venue</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data']['venue']}</div>
                                </div>
                                <div>
                                    <div style="font-size: 11px; color: #bfdbfe; text-transform: uppercase; margin-bottom: 4px;">Referee</div>
                                    <div style="font-size: 14px; color: #ffffff;">{item['data']['referee']}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Input area
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input(
            "Your message:",
            placeholder="e.g., I want to create a new league",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col2:
        send_button = st.button("Send 📤", use_container_width=True, type="primary")
    
    # Quick action buttons
    st.markdown("##### Quick Actions:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏆 Create League", use_container_width=True):
            user_input = "I want to create a new league"
            send_button = True
    with col2:
        if st.button("📅 Schedule Game", use_container_width=True):
            user_input = "I want to schedule a game"
            send_button = True
    with col3:
        if st.button("🔄 Reset Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chatbot_state = {}
            st.session_state.ai_response = None
            st.rerun()
    
    # Process message
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"user": user_input})
        
        # Get AI response
        response = get_ai_response(user_input)
        
        # Add AI response to history
        st.session_state.chat_history[-1]["ai"] = response
        st.session_state.ai_response = response
        
        # Handle different actions
        if response.get('action') == 'create_league':
            # Extract league data and create league
            league_data = response.get('data', {})
            
            # Parse team names if they're in a string format
            teams = league_data.get('teams', [])
            if isinstance(teams, str):
                teams = [t.strip() for t in teams.split(',')]
            
            # Create team objects with emojis
            team_objects = []
            team_emojis = ['🔥', '⚡', '🌟', '💪', '🏆', '⭐', '🎯', '🚀', '💎', '👑', '🦅', '🐉']
            for idx, team_name in enumerate(teams):
                if isinstance(team_name, dict):
                    team_objects.append(team_name)
                else:
                    team_objects.append({
                        'id': idx + 1,
                        'name': team_name,
                        'logo': team_emojis[idx % len(team_emojis)]
                    })
            
            # Create the league
            new_league = {
                'id': len(st.session_state.leagues) + 1,
                'name': league_data.get('name', 'New League'),
                'format': league_data.get('format', '7v7'),
                'start_date': league_data.get('start_date', str(datetime.now().date())),
                'end_date': league_data.get('end_date', str(datetime.now().date() + timedelta(days=90))),
                'teams': team_objects,
                'fee_type': league_data.get('fee_type', 'captain'),
                'fee_amount': league_data.get('fee_amount', 0),
                'venue': league_data.get('venue', 'TBD'),
                'schedule_preferences': league_data.get('schedule_preferences', 'Weekends')
            }
            
            st.session_state.leagues.append(new_league)
            
            # Add created item to chat history for display
            st.session_state.chat_history[-1]['created_item'] = {
                'type': 'league',
                'data': new_league
            }
            
            # Reset chatbot state
            st.session_state.chatbot_state = {}
            
        elif response.get('action') == 'create_game':
            # Extract game data and create game
            game_data = response.get('data', {})
            
            # Find league
            league_name = game_data.get('league_name')
            league = next((l for l in st.session_state.leagues if l['name'] == league_name), None)
            
            if league:
                # Check for duplicates
                if not check_duplicate_game(game_data['team_a'], game_data['team_b'], league['id']):
                    new_game = create_game(
                        game_data['team_a'],
                        game_data['team_b'],
                        game_data['date'],
                        game_data['time'],
                        game_data.get('venue', 'TBD'),
                        game_data.get('referee', st.session_state.referees[0]),
                        league['id'],
                        league['name']
                    )
                    
                    # Add created item to chat history for display
                    st.session_state.chat_history[-1]['created_item'] = {
                        'type': 'game',
                        'data': game_data
                    }
        
        st.rerun()

# Main app
def main():
    render_header()
    
    # Handle query params for navigation
    query_params = st.query_params
    if 'page' in query_params:
        st.session_state.page = query_params['page']
    
    # Show modal if needed
    if st.session_state.show_modal:
        show_modal(
            st.session_state.show_modal['type'],
            st.session_state.show_modal['title'],
            st.session_state.show_modal['body'],
            st.session_state.show_modal['buttons']
        )
    
    # Route to pages
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'games':
        render_games()
    elif st.session_state.page == 'create_game':
        render_create_game()
    elif st.session_state.page == 'create_league':
        render_create_league()
    elif st.session_state.page == 'leagues':
        render_leagues()
    elif st.session_state.page == 'users':
        st.markdown("### 👥 Users")
        st.info("User management coming soon!")
    elif st.session_state.page == 'settings':
        render_ai_chat()
    
    # Navigation buttons (mobile-friendly)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    with col2:
        if st.button("🏆 Leagues", use_container_width=True):
            st.session_state.page = 'leagues'
            st.rerun()
    with col3:
        if st.button("🏈 Games", use_container_width=True):
            st.session_state.page = 'games'
            st.rerun()
    with col4:
        if st.button("👥 Users", use_container_width=True):
            st.session_state.page = 'users'
            st.rerun()
    with col5:
        if st.button("🤖 AI Chatbot", use_container_width=True):
            st.session_state.page = 'settings'
            st.rerun()

if __name__ == "__main__":
    main()
