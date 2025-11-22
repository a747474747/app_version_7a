# Four-Engine Dev Dashboard

A simple HTML/JavaScript dashboard for visualizing real-time TraceLogs, Engine States, and Rule Sets during development and debugging.

## Features

- **System Status**: Real-time health checks for backend, database, and rule loader
- **Engine States**: Live view of all four engine states (Calculation, Projection, Strategy, LLM)
- **Trace Logs**: Visual display of calculation trace logs with CAL-* IDs
- **Rule Sets**: JSON view of loaded calculation rules and parameters
- **Auto-refresh**: Optional 5-second auto-refresh for live debugging
- **Keyboard shortcuts**: Ctrl+R (refresh), Ctrl+C (clear logs)

## Usage

1. Start the backend server:
   ```bash
   cd backend && python -m uvicorn src.main:app --reload
   ```

2. Open the dashboard in your browser:
   ```bash
   # From backend/dev-dashboard/
   python -m http.server 8080
   # Then visit http://localhost:8080
   ```

   Or simply open `index.html` directly in your browser.

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
