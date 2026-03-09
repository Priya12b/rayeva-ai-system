# Quick Setup Guide - Rayeva AI System

Get the system running in **5 minutes**!

## Step 1: Backend Setup (2 min)

### A. One-time: Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### B. Every time: Start backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

✅ Backend ready at: `http://localhost:8000`

**See it working:**
- Swagger UI: http://localhost:8000/docs
- Health: `curl http://localhost:8000/`

---

## Step 2: Frontend Setup (2 min)

### A. One-time: Install dependencies

```bash
cd frontend
npm install
```

### B. Every time: Start frontend

```bash
cd frontend
npm start
```

✅ Frontend ready at: `http://localhost:3000`

---

## Step 3: Populate Database (1 min)

With backend running, in a new terminal:

```bash
cd backend
python seed_db.py
```

✅ Database now has 10 sample products!

---

## Testing the API

### Option 1: Use cURL (Quickest)

```bash
# Test Module 1: Category Generator
curl -X POST "http://localhost:8000/ai/generate-category" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bamboo Toothbrush",
    "description": "Eco-friendly toothbrush",
    "material": "bamboo",
    "base_price": 12.99
  }'

# Test Module 2: Proposal Generator
curl -X POST "http://localhost:8000/ai/generate-proposal" \
  -H "Content-Type: application/json" \
  -d '{
    "client_type": "nonprofit",
    "budget": 500,
    "sustainability_priority": "high"
  }'
```

### Option 2: Use Swagger UI

1. Open: http://localhost:8000/docs
2. Click on `/ai/generate-category` endpoint
3. Click "Try it out"
4. Fill in the form
5. Click "Execute"

### Option 3: Use Demo Script

```bash
python demo_api.py
```

---

## Verify Everything Works

✅ Backend running: `curl http://localhost:8000/`
✅ Database created: Check `backend/rayeva.db` exists
✅ Sample products: `python seed_db.py` completed without errors
✅ API responds: Try any of the cURL examples above

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: fastapi` | Run `pip install -r requirements.txt` in backend folder |
| Port 8000 already in use | Change with `--port 8001` or kill process on 8000 |
| CORS error in frontend | Already configured in `main.py`, check backend is running |
| `npm: command not found` | Install Node.js from https://nodejs.org |
| `.db file not found` | Run `python seed_db.py` to create and populate |

---

## Key Files to Explore

- **API Code:** `backend/app/services/ai_service.py` (AI logic + prompts)
- **Database:** `backend/rayeva.db` (SQLite)
- **Models:** `backend/app/models/`
- **Routes:** `backend/app/routers/`
- **Documentation:** `README.md`, `ARCHITECTURE_MODULE_3.md`, `ARCHITECTURE_MODULE_4.md`

---

## Next: Testing Each Module

### Module 1: Category Generator

**What it does:** Takes a product description → generates optimal categories + SEO tags

**Test:**
```bash
curl -X POST "http://localhost:8000/ai/generate-category" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Organic Yoga Mat",
    "description": "Natural rubber mat for yoga and pilates practice",
    "material": "cork",
    "base_price": 45.00
  }'
```

**Check result:** Should categorize as "Fitness & Sports" with sustainability filters like "biodegradable"

### Module 2: Proposal Generator

**What it does:** Takes client need → recommends optimal product mix within budget

**Test:**
```bash
curl -X POST "http://localhost:8000/ai/generate-proposal" \
  -H "Content-Type: application/json" \
  -d '{
    "client_type": "corporate",
    "budget": 1000,
    "sustainability_priority": "high"
  }'
```

**Check result:** Should recommend products that maximize sustainability within budget

### Module 3 & 4: Architect Review

See: 
- `ARCHITECTURE_MODULE_3.md` - Impact Reporting system design
- `ARCHITECTURE_MODULE_4.md` - WhatsApp Support Bot design

---

## Inspect the Database

```bash
# View all products
sqlite3 backend/rayeva.db "SELECT id, name, ai_primary_category FROM products LIMIT 5;"

# View AI logs (shows every AI request)
sqlite3 backend/rayeva.db "SELECT module_name, validated, created_at FROM ai_logs;"

# View proposals generated
sqlite3 backend/rayeva.db "SELECT id, client_type, budget FROM proposals;"
```

---

## Ready for Demo?

1. ✅ Backend running
2. ✅ Frontend running
3. ✅ Database seeded with 10 products
4. ✅ Can access Swagger UI at http://localhost:8000/docs

**You're ready to show:**
- Product categorization (Module 1)
- Proposal generation (Module 2)
- AI logs showing prompts (audit trail)
- Architecture docs (Modules 3 & 4)

---

**Questions?** Check README.md for full documentation.
