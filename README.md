# StratPlan AI — Multi-Agent Business Planning System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Node](https://img.shields.io/badge/Node-18+-green.svg)](https://nodejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-teal.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)

> **Generate comprehensive monthly, quarterly, and yearly business plans with AI agents — 100% free, open-source, and self-hostable.**

## 🎯 Overview

StratPlan AI is a multi-agent business planning system that creates investor-ready plans with:
- **Executive summaries** tailored to your business
- **3-statement financial models** (P&L, Cash Flow, Balance Sheet) grounded in real industry benchmarks
- **TAM/SAM/SOM market sizing** with live macroeconomic data
- **Competitor intelligence** — pricing, features, tech stack scraped from live websites
- **SWOT, PESTLE, GTM strategy** with OKRs and milestone roadmaps
- **Execution tracking** with variance alerts and version history
- **Export to PDF, DOCX, XLSX** for professional delivery

All powered by 6 specialized AI agents orchestrated via LangGraph, using **zero paid APIs**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STRATPLAN AI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Next.js 14 Frontend  ←→  FastAPI Backend  ←→  SQLite/Postgres │
│         │                       │                    │           │
│         │              ┌────────┴────────┐            │           │
│         │              │   LangGraph     │            │           │
│         │              │   Orchestrator  │            │           │
│         │              └────────┬────────┘            │           │
│         │                       │                     │           │
│         ▼                       ▼                     ▼           │
│   ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│   │  Plan   │  │Financial │  │ Market   │  │Competitor│          │
│   │Generator│  │  Agent   │  │ Research │  │  Agent   │          │
│   └────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│        │            │             │             │                │
│        └────────────┴─────────────┴─────────────┘                │
│                              │                                    │
│                    ┌─────────┴─────────┐                          │
│                    │   Strategy Agent  │                          │
│                    │   Execution Agent │                          │
│                    └─────────┬─────────┘                          │
│                              │                                    │
│                    ┌─────────┴─────────┐                          │
│                    │  Ollama (Phi-3)   │                          │
│                    │  Local LLM Engine │                          │
│                    └───────────────────┘                          │
│                                                                  │
│   Data Sources: Alpha Vantage • Finnhub • FRED • yfinance        │
│                 Apify • BeautifulSoup • pytrends                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node 18+, Ollama

### Option 1: Docker Compose (Easiest)

```bash
# Clone the repo
git clone https://github.com/yourusername/stratplan-ai.git
cd stratplan-ai

# Start everything (backend + Ollama + frontend)
docker-compose -f backend/docker-compose.yml up -d

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Pull Ollama model
ollama pull phi3:mini

# Set environment variables (optional - all have free tiers)
cp .env.example .env
# Edit .env with your API keys

# Run backend
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔑 Free API Setup (Optional but Recommended)

All APIs have generous free tiers. Add keys to `backend/.env` for enhanced data quality:

| API | Free Tier | Purpose | Sign Up |
|-----|-----------|---------|---------|
| **Alpha Vantage** | 25 req/day | Industry benchmarks | [Get Key](https://www.alphavantage.co/support/#api-key) |
| **Finnhub** | 60 req/min | Market news, stock data | [Get Key](https://finnhub.io/register) |
| **FRED** | Unlimited | GDP, CPI, interest rates | [Get Key](https://fred.stlouisfed.org/docs/api/api_key.html) |
| **Apify** | $5/mo credit | Competitor scraping | [Get Token](https://apify.com) |
| **SerpAPI** | 100 searches/mo | Search visibility | [Get Key](https://serpapi.com) |

> **No keys required** — the system works with Ollama alone, using sensible defaults for financial assumptions.

---

## 📁 Project Structure

```
stratplan-ai/
├── backend/
│   ├── app/
│   │   ├── agents/           # 6 specialized AI agents
│   │   │   ├── plan_generator.py
│   │   │   ├── financial_agent.py
│   │   │   ├── market_research.py
│   │   │   ├── competitor_agent.py
│   │   │   ├── strategy_agent.py
│   │   │   └── execution_agent.py
│   │   ├── orchestrator/     # LangGraph workflow
│   │   ├── services/         # Data collectors, exporters
│   │   ├── routers/          # FastAPI endpoints
│   │   ├── db/models.py      # SQLAlchemy models
│   │   └── core/             # Config, database
│   ├── tests/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # Plan creation wizard
│   │   ├── dashboard/page.tsx    # Plan management
│   │   └── plan/[id]/            # Plan detail with tabs
│   ├── components/
│   │   └── ui/                   # Reusable UI components
│   └── lib/                      # API client, utilities
└── docs/
    ├── ARCHITECTURE.md
    └── FINANCIAL_MODEL.md
```

---

## 🤖 The 6 Agents

| Agent | Role | Key Outputs |
|-------|------|-------------|
| **Plan Generator** | Business strategist | Executive summary, company overview, problem/solution |
| **Financial Agent** | CFO | 3-statement model, sensitivity analysis, SaaS metrics |
| **Market Research** | Analyst | TAM/SAM/SOM, trends, benchmarks, macro indicators |
| **Competitor Agent** | Intelligence | Pricing, features, tech stack, positioning matrix |
| **Strategy Agent** | CSO | SWOT, PESTLE, GTM, OKRs, milestones, risk assessment |
| **Execution Agent** | COO | Version control, variance tracking, alert system |

---

## 📊 Financial Model Details

The Financial Agent builds a **complete 3-statement model**:

1. **Assumptions** grounded in:
   - Industry benchmarks (Alpha Vantage)
   - Macroeconomic data (FRED: GDP, CPI, Fed Funds, Unemployment)
   - Company stage & business model

2. **P&L** — Monthly for 36 months:
   - Revenue streams with growth rates
   - COGS with margin assumptions
   - Operating expenses by category
   - EBITDA, depreciation, interest, tax, net income

3. **Cash Flow** — Operating, investing, financing activities
   - Runway calculation
   - Cash balance tracking

4. **Balance Sheet** — Assets, liabilities, equity
   - Working capital modeling
   - Capex & depreciation schedules

5. **SaaS Metrics** (when applicable):
   - MRR, ARR, churn, LTV, CAC, payback period

---

## 🌐 Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in backend `.env`
- [ ] Use Supabase/PostgreSQL for database (`DATABASE_URL`)
- [ ] Configure `BACKEND_CORS_ORIGINS` for your domain
- [ ] Set up Ollama on GPU instance for faster inference
- [ ] Add API keys for enhanced data quality
- [ ] Enable HTTPS (Vercel/Render handle this)

### Deploy to Render + Vercel

**Backend (Render):**
1. Connect GitHub repo
2. Create Web Service from `backend/Dockerfile`
3. Add environment variables
4. Create persistent disk for SQLite (or use Supabase)

**Frontend (Vercel):**
1. Import GitHub repo
2. Set Root Directory to `frontend`
3. Add `NEXT_PUBLIC_API_URL` = your Render backend URL
4. Deploy

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style (Black for Python, ESLint/Prettier for TypeScript)
- Add tests for new features
- Update documentation for API changes
- Keep agents focused and single-purpose

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **LangGraph** for agent orchestration
- **Ollama** for local LLM inference
- **Alpha Vantage, Finnhub, FRED** for free financial data
- **shadcn/ui** for beautiful UI components
- **Recharts** for financial visualizations

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/stratplan-ai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/stratplan-ai/discussions)
- **Email:** your-email@example.com

---

**Built with ❤️ using 100% free and open-source tools.**  
**Ready for the Suproc AI Agent Marketplace.**