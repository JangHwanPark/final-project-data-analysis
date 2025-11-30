# Frontend (Next.js Dashboard)
This Next.js (App Router) dashboard renders the analysis artifacts produced by the Python backend. The UI is organized with a feature-sliced structure (`app/`, `entities/`, `features/`, `widgets/`, `shared/`, `view/`).

## Data Source
Generated JSON files live in `src/shared/data/` (e.g., `summary-full.json`, `overview.json`, `difficulty.json`, `tags.json`, `structure.json`).
They are produced by the backend pipeline (`python -m backend.app.main` inside `back`) and copied into this folder so the app can import them statically.

## Key Routes
- `/` — Main analytics dashboard backed by real summary data.
- `/dashboard` — Management overview using mock activity/stat cards.(Test)

## Getting Started
```bash
cd front
npm install
npm run dev
# http://localhost:3000
```

## Scripts
- `npm run dev` — Start the development server.
- `npm run build` — Build the production bundle.
- `npm run start` — Run the production server.
- `npm run lint` — Lint with ESLint.
- `npm run format` — Format with Prettier.

## Tech Stack
- Next.js 16 (App Router), React 19
- Tailwind CSS 4
- Recharts, TanStack Table, Mantine components
- Zustand for client-side state
- date-fns, framer-motion, lucide-react for UX polish