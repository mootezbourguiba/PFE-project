# Intelligent Avionics Health Monitoring and Predictive Maintenance Platform

## Project Overview

This Final Year Project develops a predictive maintenance platform for UAV propulsion systems, specifically focusing on bearing wear detection in brushless DC motors using machine learning anomaly detection.

**Host Company:** AVIONAV  
**University:** ESPRIM — Private Higher School of Engineering of Monastir  
**Academic Year:** 2025/2026  
**Student:** Mootez Bourguiba  

## Technology Stack

### Backend
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (JSON Web Tokens)

### Machine Learning
- **Library:** Scikit-learn
- **Algorithm:** Isolation Forest
- **Data Processing:** Pandas, NumPy

### Frontend
- **Framework:** Streamlit
- **Visualization:** Plotly

## Project Structure

```
pfe/
├── backend/              # FastAPI backend application
│   ├── api/             # API endpoints
│   ├── core/            # Core configuration and security
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic schemas for validation
│   ├── crud/            # Database CRUD operations
│   ├── services/        # Business logic layer
│   └── tests/           # Unit and integration tests
├── alembic/             # Database migrations
├── report/              # LaTeX report source files
├── chapters/            # Report chapters
├── sections/            # Report front matter
├── annexes/             # Report annexes
└── requirements.txt     # Python dependencies
```

## Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pfe
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

6. **Run backend server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access API documentation**
   ```
   http://localhost:8000/docs
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/` - List all users (Admin only)
- `POST /api/v1/users/` - Create new user (Admin only)
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user (Admin only)

### Flights
- `GET /api/v1/flights/` - List all flights
- `POST /api/v1/flights/` - Create new flight
- `GET /api/v1/flights/{flight_id}` - Get flight details
- `GET /api/v1/flights/{flight_id}/telemetry` - Get flight telemetry

### Telemetry
- `POST /api/v1/telemetry/` - Ingest telemetry data
- `GET /api/v1/anomalies/` - List detected anomalies

## User Roles

### Administrator
- Full system access
- User management
- Flight management
- Anomaly review

### Maintenance Engineer
- View monitoring data
- Access historical telemetry
- Analyze anomalies
- Generate reports

### Drone Operator
- View real-time alerts
- Basic status information
- No historical data access

## Database Schema

### Tables
- **User** - User accounts and authentication
- **FlightSession** - Flight metadata
- **TelemetryReading** - Time-series telemetry data
- **AnomalyEvent** - Detected anomalies

### Relationships
```
User 1 ---- N FlightSession
FlightSession 1 ---- N TelemetryReading
FlightSession 1 ---- N AnomalyEvent
```

## Development

### Running Tests
```bash
cd backend
pytest tests/
```

### Code Quality
```bash
# Format code
black .

# Type checking
mypy backend/

# Linting
flake8 backend/
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Report Compilation

The project report is written in LaTeX. To compile:

1. Install TeX distribution (TeX Live or MiKTeX)
2. Navigate to project root
3. Compile with pdfLaTeX:
   ```bash
   pdflatex main.tex
   pdflatex main.tex  # Run twice for references
   ```

## Architecture Documentation

Detailed architecture documentation is available in:
- Chapter 4: Design and Architecture
- Chapter 5: Telemetry Simulation
- Chapter 6: Anomaly Detection Engine
- Chapter 7: Dashboard and Integration
- Chapter 8: Testing, Validation, and Discussion

## License

This project is developed as part of a Final Year Project at ESPRIM.

## Contact

- **Student:** Mootez Bourguiba
- **Academic Supervisor:** Mr. Aymen Charrada
- **Industrial Supervisor:** Mr. Foued El Kamel
