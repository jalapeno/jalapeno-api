# Jalapeno API

A modern web interface for visualizing network topology data from ArangoDB/Jalapeno.

## Project Structure 

jalapeno-api/
├── app/
│   ├── config/        # config, etc.
│   ├── routes/        # API endpoints
│   └── utils/         # Helper functions
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
cd app
python3 -m venv venv
source venv/bin/activate 
cd ..
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. Access the application
- API Documentation: http://localhost:8000/docs

3. Local Development

```bash
export LOCAL_DEV=1
uvicorn app.main:app --reload
```

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




