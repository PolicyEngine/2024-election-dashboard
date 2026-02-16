# 2024 Election Dashboard

Household impact calculator comparing Baseline, Harris, and Trump tax plans using PolicyEngine US microsimulation.

## Architecture

- **Frontend**: `frontend/` - React + TypeScript + Mantine v8 + Recharts, built with Vite
- **API**: `api/modal_app.py` - Modal serverless backend running PolicyEngine US simulations
- **Legacy**: Python Streamlit files in root (kept for reference)

## Commands

```bash
cd frontend && npm install    # Install dependencies
cd frontend && npm run dev    # Dev server
cd frontend && npm run build  # Production build
cd frontend && npm test       # Run vitest tests
```

## API deployment

```bash
unset MODAL_TOKEN_ID MODAL_TOKEN_SECRET && modal deploy api/modal_app.py
```

API URL: `https://policyengine--election-dashboard-calculate.modal.run`

## Design tokens

- Primary teal: #319795
- Harris blue: #3378b2
- Trump red: #f45959
- Baseline grey: #868686
- Font: Inter

## Key files

- `frontend/src/App.tsx` - Main application component
- `frontend/src/components/NetIncomeChart.tsx` - Recharts horizontal bar chart
- `frontend/src/components/MetricsTable.tsx` - Main breakdown table
- `frontend/src/components/CreditsTable.tsx` - Refundable credits table
- `frontend/src/types/index.ts` - TypeScript types, state codes, defaults
- `api/modal_app.py` - All simulation logic (reforms, situation builder, calculation)
