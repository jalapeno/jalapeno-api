# Jalapeno API

A modern web interface for visualizing network topology data from ArangoDB/Jalapeno.

## Project Structure 

jalapeno-api/
├── app/
│   ├── core/          # Core functionality, config, etc.
│   ├── models/        # Pydantic models
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   └── utils/         # Helper functions
├── tests/             # Test files
├── k8s/               # Kubernetes configs
├── docs/              # API documentation
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md

## Prerequisites

- Python 3.9+
- Node.js 16+
- Access to a Kubernetes cluster
- Access to Jalapeno ArangoDB instance

## Quick Start

### Development Setup
1. API Setup

```bash
cd api
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. Access the application
- API Documentation: http://localhost:8000/docs

### Production Deployment

```bash
kubectl apply -f k8s/
```

## Architecture
- API: FastAPI
- Database: ArangoDB (Jalapeno)
- Deployment: Kubernetes

## Contributing
[Contributing guidelines]

## License
[License information]




