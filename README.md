# CareerFluence Backend

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /api/streams` - Get all streams
- `GET /api/streams/{id}` - Get specific stream details
- `GET /api/streams/{id}/courses` - Get courses for a stream
- `GET /api/streams/{id}/jobs` - Get jobs and exams for a stream
- `GET /api/gov-jobs` - Get government jobs
- `GET /api/analytics` - Get analytics data
- `GET /api/charts/{chart_name}` - Serve chart images
- `GET /health` - Health check

## Chart Generation

The server automatically generates the following charts:
- Stream popularity pie chart
- Emerging trends bar chart
- Salary trends line chart  
- In-demand skills horizontal bar chart

Charts are saved in the `charts/` directory and served via the API.