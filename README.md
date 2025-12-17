# PFFL AI Commissioner

A complete, production-ready Streamlit web app that perfectly replicates the Phoenix Performance Flag Football League (PFFL) mobile app with AI-powered commissioner capabilities using Google Gemini.

## 🎯 Features

### Exact Visual Match
- **Dark navy blue theme** (#0f172a background, #1e293b cards, #1e40af buttons)
- **Phoenix shield logo** with football at top
- **Bottom navigation bar** with 5 tabs (Home, Leagues, Games, Users, Settings)
- **Floating microphone button** for voice commands
- **Pixel-perfect modals** matching the real app

### Complete Screens
1. **Home Dashboard**
   - Stats cards (Total Leagues, Active Games, Registered Users, Pending Payments)
   - Quick Actions (Create League, Schedule Game)
   - Upcoming Games list with team logos and details

2. **Games Tab**
   - Filter buttons for different leagues
   - Complete games list with scores, times, venues
   - Edit game functionality

3. **Create Game**
   - Team selection dropdowns
   - Date/time pickers
   - Venue and referee assignment
   - Duplicate game detection
   - Success/Error modals

4. **Create League Wizard**
   - 12-step progressive wizard
   - Format selection (5v5 / 7v7)
   - League details, logo upload, dates
   - Entry fee configuration
   - Progress dots indicator

5. **AI Chatbot**
   - Powered by Google Gemini (gemini-2.0-flash-exp)
   - Conversational 12-step league creation
   - Natural language game scheduling
   - Chat history with progress tracking
   - Automatic data structuring and validation

### AI Capabilities
The AI Chatbot can:
- ✅ Create leagues through conversational 12-step process
- ✅ Guide users through each step (format, name, dates, teams, etc.)
- ✅ Schedule games via natural language prompts
- ✅ Validate all data (duplicates, dates, team names)
- ✅ Automatically save leagues and games to database
- ✅ Display created leagues on home page
- ✅ Support both manual and AI-powered workflows
- ✅ Maintain conversation state across interactions

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.streamlit` folder and add your Gemini API key:

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

**Get your API key:** https://makersuite.google.com/app/apikey

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📱 Navigation

- **🏠 Home** - Dashboard with stats and upcoming games
- **🏆 Leagues** - View and create leagues
- **🏈 Games** - All games list with filters
- **👥 Users** - User management (coming soon)
- **🤖 AI Chatbot** - Conversational assistant for league & game management

## 🤖 AI Chatbot Usage

Go to **AI Chatbot** tab and try these commands:

### Create a League (Conversational):
```
"I want to create a new league"
```
The AI will guide you through:
1. League format (5v5 or 7v7)
2. League name
3. Logo selection
4. Start date
5. End date
6. Entry fee type
7. Entry fee amount
8. Number of teams
9. Team names
10. Venue/location
11. Schedule preferences
12. Final confirmation

### Schedule a Game:
```
"Schedule a game between Firebirds and Storm on Sunday at 10am"
"I want to schedule a game for next Friday"
```

### Query Information:
```
"Show me all leagues"
"What games are scheduled this week?"
"List all teams in Phoenix Winter 2025"
```

## 🎨 Design System

### Colors
- **Background:** #0f172a (dark navy)
- **Cards:** #1e293b (slate)
- **Primary:** #1e40af → #3b82f6 (blue gradient)
- **Text:** #ffffff (white)
- **Secondary:** #94a3b8 (gray)

### Components
- **Stat Cards** - Gradient backgrounds with hover effects
- **Game Cards** - Team logos, scores, times, venues
- **Modals** - Success (✅) and Error (⚠️) with custom buttons
- **Progress Dots** - 12-step wizard indicator
- **Filter Buttons** - Pill-shaped with active states

## 📊 Mock Data

The app includes pre-populated data:
- **2 Leagues** (Phoenix Winter 2025, Phoenix Summer League)
- **6 Teams** (Firebirds, Desert Storm, Valley Vipers, etc.)
- **3 Scheduled Games**
- **4 Referees** (John Carter, Anthony Brooks, etc.)
- **2,847 Users**
- **$12,540 Pending Payments**

## 🔧 Technical Stack

- **Frontend:** Streamlit with custom CSS
- **AI:** Google Gemini API (gemini-1.5-flash)
- **State Management:** Streamlit session_state
- **Data:** Mock in-memory database
- **Response Format:** JSON with forced mime type

## 🎯 Business Rules

The AI enforces these rules:
- ✅ League names must be unique
- ✅ End date must be after start date
- ✅ Team A cannot equal Team B
- ✅ No duplicate games between same teams
- ✅ Only Commissioners can create/edit
- ✅ Games can only be edited when status = Scheduled

## 📝 System Prompt

The AI uses a strict system prompt that:
- Forces JSON-only responses
- Implements duplicate detection
- Enforces all business rules
- Uses confident, fast tone
- Returns structured modals

## 🚀 Production Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add `GEMINI_API_KEY` to secrets
4. Deploy!

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 🎨 Screenshots

The app matches these exact screens:
- ✅ Home Dashboard with stats
- ✅ Games list with filters
- ✅ Create Game form
- ✅ Success modal ("Game Created Successfully")
- ✅ Error modal ("Game Already Scheduled")
- ✅ Create League 12-step wizard
- ✅ Bottom navigation bar
- ✅ Floating mic button

## 🔮 Future Enhancements

- [ ] Voice input via mic button
- [ ] Real-time score updates
- [ ] Push notifications
- [ ] Player statistics
- [ ] Payment processing
- [ ] Team management
- [ ] Bracket generation
- [ ] Live game tracking

## 📄 License

MIT License - Built for Phoenix Performance Flag Football League

## 🙏 Credits

Built with ❤️ using:
- Streamlit
- Google Gemini AI
- Custom CSS animations
- Modern web design principles

---

**Ready to run!** Just add your Gemini API key and execute `streamlit run app.py`
