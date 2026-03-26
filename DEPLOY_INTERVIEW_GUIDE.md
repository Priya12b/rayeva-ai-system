# Rayeva AI System - Interview Deployment Guide

This guide is optimized for a quick and clean demo deployment.

## What was prepared in code

- Frontend now reads backend URL from environment variable.
- Backend now reads database URL from environment variable.
- Seed data now includes realistic public-facing Rayeva-style products.

## 1) Local final check (10 minutes)

### Backend

1. Open terminal in project root.
2. Run:

   cd backend
   pip install -r requirements.txt
   python seed_db.py
   uvicorn app.main:app --host 0.0.0.0 --port 8000

3. Verify:
   - http://127.0.0.1:8000/
   - http://127.0.0.1:8000/docs

### Frontend

1. Open a new terminal:

   cd frontend
   npm install
   npm start

2. Open:
   - http://localhost:3000

## 2) Deploy backend on Render (easy)

1. Push this repo to GitHub.
2. Go to Render dashboard.
3. Create New Web Service from the repo.
4. Configure:
   - Root Directory: backend
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
5. Add environment variable:
   - DATABASE_URL = sqlite:///./rayeva.db
6. Deploy.
7. After first deploy, open service shell and run once:

   python seed_db.py

8. Confirm backend is live:
   - https://YOUR-BACKEND.onrender.com/
   - https://YOUR-BACKEND.onrender.com/docs

## 3) Deploy frontend on Netlify (easy)

1. Go to Netlify dashboard.
2. Import project from GitHub.
3. Configure:
   - Base directory: frontend
   - Build command: npm run build
   - Publish directory: frontend/build
4. Add environment variable:
   - REACT_APP_API_BASE_URL = https://YOUR-BACKEND.onrender.com
5. Deploy.
6. Open live frontend URL and test both forms.

## 4) Interview-ready test script

Use these demo steps in order:

1. Open frontend deployed URL.
2. Run Module 1 with:
   - Name: Rayeva Wooden Water Bottle
   - Description: Premium handcrafted wooden bottle with bamboo exterior
   - Material: bamboo
   - Base Price: 799
3. Show generated categories and sustainability filters.
4. Run Module 2 with:
   - Client Type: corporate
   - Budget: 5000
   - Sustainability Priority: High
5. Show recommended products and budget optimization.
6. Open backend /docs and show API design.
7. Mention AI logs in database for audit trail.

## 5) Public data used for realistic seeding

These are based on publicly visible site content:

- Rayeva Wooden Water Bottle (₹799)
- Beeswax Food Wraps (₹449)
- Organic Hemp Seed Body Oil (₹599)
- Coconut Shell Bowls Set (₹699)
- Recycled Glass Tumblers (₹799)
- Rayeva Starter Kit (₹499)

## 6) Important note for transparency

Use this line in interview if asked:

"I used publicly visible product examples and built deterministic mock AI logic for reliable demos; this can be switched to a live LLM in production without changing API contracts."

## 7) If something breaks in live demo

1. Backend not responding:
   - Check Render logs
   - Redeploy service
2. Frontend calling localhost:
   - Verify Netlify env var REACT_APP_API_BASE_URL
   - Trigger redeploy
3. Empty proposals:
   - Run python seed_db.py again on backend
