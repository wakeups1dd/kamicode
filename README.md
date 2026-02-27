# KamiCode

> **AI-Native Competitive Programming Platform**
> Depth + Speed → Verifiable On-Chain Credentials

KamiCode is a competitive programming platform that combines daily algorithmic challenges, AI-powered code analysis, a Glicko-2 rating system, league-based rankings, and on-chain NFT credentials — all in one seamless experience.

## Architecture

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS, Framer Motion |
| Backend API | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Task Queue | Celery + Redis |
| Code Sandbox | Docker containers (per-submission isolation) |
| AI Engine | OpenAI GPT-4o / Claude |
| Blockchain | Ethereum L2 (Base) |
| Smart Contracts | Solidity + Hardhat |
| NFT Metadata | IPFS via Pinata |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/your-org/kamicode.git
cd kamicode

# Copy environment variables
cp .env.example .env

# Start all services
docker compose -f infra/docker-compose.yml up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Project Structure

```
kamicode/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
│   ├── app/
│   │   ├── api/       # Route handlers
│   │   ├── core/      # Config, security, deps
│   │   ├── engines/   # Engine modules
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   └── services/  # Business logic
│   ├── sandbox/       # Docker sandbox runner
│   └── tests/
├── contracts/         # Solidity smart contracts
├── infra/             # Docker, Terraform
└── docs/              # Documentation
```

## License

MIT
