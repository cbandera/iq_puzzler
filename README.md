# IQ Puzzler Pro Solver

A 3D puzzle solver for the "IQ Puzzler Pro" game, featuring both a Python backend solver and a Next.js visualization frontend.

## Project Structure

- `src/` - Python solver core implementation
- `tests/` - Test suite for the Python solver
- `puzzle_vis/` - Next.js frontend for visualization
- `api/` - Flask API server for hosting the Python solver

## Deployment Options

This project has been structured to support multiple deployment options. The recommended approach is to use Render.com, which offers free hosting for both the frontend and backend components.

### Option 1: Render.com (Recommended)

#### 1. Create a GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/iq-puzzler.git
git push -u origin main
```

#### 2. Deploy the Python Backend

1. Log in to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `iq-puzzler-api`
   - **Root Directory**: `api`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt && pip install -e ..`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`
   - **Environment Variables**:
     - `PORT`: `8080`
     - `PYTHONPATH`: `/app`

#### 3. Deploy the Next.js Frontend

1. Create a new Web Service on Render
2. Configure the service:
   - **Name**: `iq-puzzler-frontend`
   - **Root Directory**: `puzzle_vis`
   - **Runtime**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Environment Variables**:
     - `NEXT_PUBLIC_API_URL`: URL of your Python backend (e.g., `https://iq-puzzler-api.onrender.com`)

### Option 2: Railway.app

Railway.app offers a similar deployment experience to Render.com with a free tier:

1. Create a Railway account and connect your GitHub repository
2. Create two services:
   - Python backend (using the `api/Dockerfile`)
   - Next.js frontend (using the `puzzle_vis` directory)
3. Configure environment variables similar to the Render.com setup

### Option 3: Replit

Replit is great for demonstrations and sharing with others:

1. Create a new Repl from your GitHub repository
2. Configure as a full-stack application
3. Use the `.replit` file to run both the frontend and backend

## Local Development

### Backend

```bash
cd api
pip install -r requirements.txt
pip install -e ..
python app.py
```

### Frontend

```bash
cd puzzle_vis
npm install
npm run dev
```

The frontend will be available at http://localhost:3000 and will connect to the backend at http://localhost:8080.

## Environment Variables

### Frontend (puzzle_vis)

- `NEXT_PUBLIC_API_URL`: URL of the Python backend API

### Backend (api)

- `PORT`: Port to run the API server (default: 8080)
