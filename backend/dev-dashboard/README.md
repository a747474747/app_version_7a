# Four-Engine Dev Dashboard

A comprehensive development dashboard for testing and monitoring the Four-Engine Architecture system, with special focus on User Story 1 - Consumer Fact Check functionality.

## Features

### 🔧 System Monitoring
- **System Status**: Real-time health checks for backend, database, and rule loader
- **Engine States**: Live view of all four engine states (Calculation, Projection, Strategy, LLM)
- **Trace Logs**: Visual display of calculation trace logs with CAL-* IDs
- **Rule Sets**: JSON view of loaded calculation rules and parameters

### 💬 Fact-Check Chat Tester (NEW - User Story 1)
Test the complete Consumer Fact Check workflow with real-time backend processing visualization.

#### How to Use the Chat Tester

1. **Enter a Question**: Type a financial question in the text area, such as:
   - "What is my tax liability?"
   - "What is my net wealth?"
   - "How much super do I have?"

2. **Optional Scenario**: Select a scenario file to provide financial data, or leave empty to let the LLM hydrate the state from your question.

3. **Click "Ask Question"**: Watch the real-time processing flow as the system:
   - 🔍 **Intent Recognition**: Analyzes your question to determine intent
   - 💧 **State Hydration**: Converts natural language to structured financial data
   - 🚀 **API Call**: Makes the actual fact-check API request
   - 🧮 **Calculation Engine**: Runs deterministic tax/wealth calculations
   - 📝 **Narrative Generation**: Creates human-readable explanations
   - 🔒 **Privacy Filtering**: Removes PII before displaying response
   - 📋 **Trace Logging**: Records all calculation steps

4. **View Results**: See the final AI response and processing metadata.

#### Example Questions to Try

```
"What is my tax liability this year?"
"How much is my net wealth?"
"What superannuation balance do I have?"
"How much tax will I pay on my income?"
```

### 🤖 LLM Engine Monitoring
- Connection health and usage metrics
- Model performance and cost tracking
- Operation type counters (Intent Recognition, State Hydration, etc.)
- Privacy filtering statistics
- Prompt management and caching

### 🧮 Calculation Testing
- Interactive calculation runner with scenario selection
- Calculation domain browser with detailed function information

### ⚙️ Additional Features
- **Auto-refresh**: Optional 5-second auto-refresh for live debugging
- **Keyboard shortcuts**: Ctrl+R (refresh), Ctrl+C (clear logs)
- **LLM Tier Candidates**: View validated models by intelligence tier

## Usage

### Quick Start

1. **Start the Backend Server**:
   ```bash
   cd backend
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the Dashboard**:
   Open `backend/dev-dashboard/index.html` in your web browser.

3. **Test User Story 1**:
   - Use the "Fact-Check Chat Tester" section
   - Ask questions like "What is my tax liability?"
   - Watch the real-time processing flow
   - View calculation results and AI responses

### Alternative Access

If you prefer serving the dashboard:

```bash
# From backend/dev-dashboard/
python -m http.server 8080
# Then visit http://localhost:8080
```

Or simply open `index.html` directly in your browser (CORS restrictions may apply).

## API Endpoints Needed

For full functionality, the backend should provide these endpoints:

- `GET /health` - System health check
- `GET /debug/trace-logs` - Recent trace log entries
- `GET /debug/engine-states` - Current engine states
- `GET /debug/rules` - Loaded rule configurations
- `DELETE /debug/trace-logs` - Clear trace logs

## Development Notes

- The dashboard uses vanilla JavaScript with no external dependencies
- It's designed to work with CORS enabled on the backend
- Currently shows placeholder data - implement the debug endpoints for full functionality
- Auto-refresh can be intensive - use during debugging only
