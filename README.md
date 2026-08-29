# StratPlan AI

**Multi-Agent Business Planning System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Node](https://img.shields.io/badge/Node-18+-green.svg)](https://nodejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-teal.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)

Generate comprehensive monthly, quarterly, and yearly business plans with AI agents. 100% free, open-source, and self-hostable.

---

## Overview

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

## Architecture

```
+-----------------------------------------------------------------------+
|                          STRATPLAN AI                                  |
+-----------------------------------------------------------------------+
|                                                                       |
|   Next.js 14 Frontend  <-->  FastAPI Backend  <-->  SQLite/Postgres   |
|         |                       |                    |                |
|         |              +--------+--------+            |                |
|         |              |   LangGraph     |            |                |
|         |              |   Orchestrator  |            |                |
|         |              +--------+--------+            |                |
|         |                       |                     |                |
|         v                       v                     v                |
|   +----------+  +-----------+  +-----------+  +-----------+            |
|   |   Plan   |  | Financial |  |  Market   |  | Competitor |           |
|   |Generator |  |   Agent   |  | Research  |  |   Agent   |            |
|   +----+-----+  +-----+-----+  +-----+-----+  +-----+-----+          |
|        |              |             |             |                    |
|        +--------------+-------------+-------------+                    |
|                              |                                         |
|                    +---------+---------+                               |
|                    |   Strategy Agent  |                               |
|                    |   Execution Agent |                               |
|                    +---------+---------+                               |
|                              |                                         |
|                    +---------+---------+                               |
|                    |  Ollama (Phi-3)   |                               |
|                    |  Local LLM Engine |                               |
|                    +-------------------+                               |
|                                                                       |
|   Data Sources: Alpha Vantage | Finnhub | FRED | yfinance             |
|                 Apify | BeautifulSoup | pytrends                      |
|                                                                       |
+-----------------------------------------------------------------------+
```

---

## Tech Stack

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Framework | FastAPI | Async REST API with auto-generated OpenAPI docs |
| Agent Orchestration | LangGraph + LangChain | Multi-agent workflows with shared state |
| LLM Engine | Ollama (Phi-3 Mini) | Local inference, zero API costs |
| Database | SQLAlchemy + SQLite | Lightweight local storage |
| Data Collection | httpx, BeautifulSoup, yfinance | Async market data fetching |
| Financial Modeling | Custom engine | 3-statement P&L, Cash Flow, Balance Sheet |
| Export | WeasyPrint, python-docx, openpyxl | PDF, DOCX, XLSX generation |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | Next.js 14 | React SSR/SSG with App Router |
| Styling | Tailwind CSS | Utility-first CSS |
| UI Components | Custom (shadcn/ui-style) | Buttons, Tabs, Cards |
| Charts | Recharts | Financial visualizations |
| State Management | React Query | Server state caching |
| HTTP Client | Axios | API communication |
| Live Demo | Streamlit | Rapid prototyping interface |

### Data Sources (All Free)

| API | Free Tier | Purpose |
|-----|-----------|---------|
| Alpha Vantage | 25 req/day | Industry benchmarks, stock data |
| Finnhub | 60 req/min | Market news, earnings, sentiment |
| FRED API | Unlimited | GDP, CPI, interest rates |
| yfinance | Unlimited | Historical sector performance |
| Apify | $5 credit/mo | Competitor website scraping |
| pytrends | Unlimited | Google search demand validation |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Ollama (for local LLM inference)

### 1. Clone and Setup

```bash
git clone https://github.com/shamiquekhan/stratplan-ai.git
cd stratplan-ai
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment (optional - works without API keys)
cp .env.example .env
# Edit .env with your API keys for enhanced data quality

# Pull Ollama model
ollama pull phi3:mini

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Or Use Streamlit Demo

```bash
cd frontend

# Install Streamlit dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run streamlit_app.py --server.port 8501
```

### Access Points

| Service | URL |
|---------|-----|
| Next.js Frontend | http://localhost:3000 |
| Streamlit Demo | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

---

## Project Structure

```
stratplan-ai/
|
+-- backend/
|   +-- app/
|   |   +-- agents/              # 6 specialized AI agents
|   |   |   +-- base.py              # Abstract base agent class
|   |   |   +-- plan_generator.py    # Executive summary generation
|   |   |   +-- financial_agent.py   # 3-statement financial modeling
|   |   |   +-- market_research.py   # TAM/SAM/SOM analysis
|   |   |   +-- competitor_agent.py  # Competitive intelligence
|   |   |   +-- strategy_agent.py    # SWOT, PESTLE, GTM, OKRs
|   |   |   +-- execution_agent.py   # Tracking and versioning
|   |   |
|   |   +-- orchestrator/        # LangGraph workflow
|   |   |   +-- graph.py            # State machine definition
|   |   |
|   |   +-- services/            # Business logic
|   |   |   +-- financial_engine.py  # Projection calculations
|   |   |   +-- data_collectors.py   # Market data collection
|   |   |   +-- export_service.py    # PDF/DOCX/XLSX export
|   |   |   +-- templates/           # Jinja2 templates
|   |   |
|   |   +-- routers/             # API endpoints
|   |   |   +-- plans.py            # CRUD + generate + export
|   |   |
|   |   +-- tools/               # External data sources
|   |   |   +-- data_sources.py     # Alpha Vantage, FRED, Finnhub
|   |   |
|   |   +-- db/                  # Database models
|   |   |   +-- models.py           # SQLAlchemy models
|   |   |
|   |   +-- core/                # Configuration
|   |   |   +-- config.py           # Pydantic settings
|   |   |   +-- database.py         # Engine setup
|   |   |
|   |   +-- api/                 # Pydantic schemas
|   |       +-- schemas.py          # Request/response models
|   |
|   +-- tests/                   # Unit tests
|   +-- Dockerfile               # Backend container
|   +-- docker-compose.yml       # Backend + Ollama
|   +-- requirements.txt         # Python dependencies
|   +-- .env.example             # Environment template
|
+-- frontend/
|   +-- app/                     # Next.js App Router
|   |   +-- page.tsx                 # Landing + plan creation wizard
|   |   +-- dashboard/page.tsx       # Plan management dashboard
|   |   +-- plan/[id]/               # Plan detail with tabs
|   |   |   +-- page.tsx             # Main layout + tabs
|   |   |   +-- OverviewTab.tsx      # Executive summary view
|   |   |   +-- financials/          # P&L, cash flow, balance sheet
|   |   |   +-- competitors/         # Competitor profiles + matrix
|   |   |   +-- strategy/            # SWOT, OKRs, milestones
|   |   |   +-- export/              # Export options
|   |   +-- layout.tsx               # Root layout
|   |   +-- globals.css              # Global styles
|   |
|   +-- components/              # Reusable components
|   |   +-- shared.tsx               # SectionCard
|   |   +-- ui/                      # Button, Tabs
|   |
|   +-- lib/                     # Utilities
|   |   +-- api.ts                   # Axios API client
|   |   +-- utils.ts                 # Formatters
|   |   +-- types.ts                 # TypeScript types
|   |
|   +-- streamlit_app.py         # Streamlit live demo
|   +-- Dockerfile               # Frontend container
|   +-- docker-compose.yml       # Frontend service
|   +-- package.json             # Node dependencies
|   +-- tailwind.config.ts       # Tailwind config
|   +-- tsconfig.json            # TypeScript config
|
+-- .gitignore
+-- README.md
```

---

## The 6 Agents

| Agent | Role | Key Outputs |
|-------|------|-------------|
| **Plan Generator** | Business Strategist | Executive summary, company overview, problem/solution narrative |
| **Financial Agent** | CFO | 3-statement model (P&L, Cash Flow, Balance Sheet), sensitivity analysis, SaaS metrics |
| **Market Research** | Analyst | TAM/SAM/SOM sizing, industry trends, benchmarks, macro indicators |
| **Competitor Agent** | Intelligence Officer | Pricing analysis, feature comparison, tech stack detection, positioning matrix |
| **Strategy Agent** | CSO | SWOT, PESTLE, GTM strategy, OKRs, milestone roadmaps, risk assessment |
| **Execution Agent** | COO | Plan versioning, variance tracking, alert system |

### Agent Workflow

```
User Input (Business Idea)
        |
        v
  [Collect Data] -----> Fetch market data from APIs
        |
        v
  [Plan Generator] ---> Executive summary, company overview
        |
        v
  [Financial Agent] --> Build 3-statement financial model
        |
        v
  [Market Research] --> TAM/SAM/SOM, trends, benchmarks
        |
        v
  [Competitor Agent] -> Scrape and analyze competitors
        |
        v
  [Strategy Agent] ---> SWOT, GTM, OKRs, milestones
        |
        v
  [Execution Agent] --> Version snapshot, execution tracker
        |
        v
  Saved to Database ----> Return complete plan to user
```

---

## Financial Model

The Financial Agent builds a **complete 3-statement model** grounded in real data:

### 1. Assumptions

- Industry benchmarks from Alpha Vantage
- Macroeconomic indicators from FRED (GDP, CPI, Fed Funds, Unemployment)
- Company stage and business model adjustments

### 2. Profit & Loss (36 months)

- Revenue streams with growth rates
- COGS with margin assumptions
- Operating expenses by category (R&D, Sales, G&A)
- EBITDA, depreciation, interest, tax, net income

### 3. Cash Flow

- Operating activities (net income + adjustments)
- Investing activities (capex, investments)
- Financing activities (debt, equity)
- Runway calculation and cash balance tracking

### 4. Balance Sheet

- Current and fixed assets
- Current and long-term liabilities
- Shareholder equity
- Working capital modeling

### 5. SaaS Metrics (when applicable)

- MRR, ARR, churn rate
- LTV, CAC, LTV/CAC ratio
- Payback period

---

## Free API Setup

All APIs have generous free tiers. Add keys to `backend/.env` for enhanced data quality:

| API | Free Tier | Purpose | Sign Up |
|-----|-----------|---------|---------|
| Alpha Vantage | 25 req/day | Industry benchmarks | [Get Key](https://www.alphavantage.co/support/#api-key) |
| Finnhub | 60 req/min | Market news, stock data | [Get Key](https://finnhub.io/register) |
| FRED | Unlimited | GDP, CPI, interest rates | [Get Key](https://fred.stlouisfed.org/docs/api/api_key.html) |
| Apify | $5/mo credit | Competitor scraping | [Get Token](https://apify.com) |
| SerpAPI | 100 searches/mo | Search visibility | [Get Key](https://serpapi.com) |

> No keys required. The system works with Ollama alone, using sensible defaults for financial assumptions.

---

## Deployment

### Docker Compose

```bash
# Start backend + Ollama
cd backend
docker-compose up -d

# Start frontend (separate terminal)
cd frontend
docker-compose up -d
```

### Production Checklist

- Set `DEBUG=false` in backend `.env`
- Use Supabase/PostgreSQL for database (`DATABASE_URL`)
- Configure `BACKEND_CORS_ORIGINS` for your domain
- Set up Ollama on GPU instance for faster inference
- Add API keys for enhanced data quality
- Enable HTTPS (Vercel/Render handle this)

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

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend build check
cd frontend
npm run build
```

---

## Contributing

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

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration
- [Ollama](https://ollama.com/) for local LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) for the async backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Recharts](https://recharts.org/) for financial visualizations
- [Streamlit](https://streamlit.io/) for rapid prototyping
