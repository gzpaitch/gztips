Avenca Digital is a digital agency. The name is used primarily as my professional identity - alias. It represents the way I approach clients and publish/share my work and projects: delivering reliable, modern digital solutions with a focus on clarity, performance, and practical outcomes. Currently, the agency concentrates on web development projects built with React/Next.js/Vite, as well as app development using Flutter/Dart. In addition, it supports backend and integration work through APIs developed with FastAPI/Hono, along with other related services that help connect products and streamline workflows. Another key focus is the use and development of Artificial Intelligence, leveraging AI where it genuinely adds value, whether that means improving efficiency, enhancing user experiences, or enabling smarter automation. POI: automation, n8n, nextjs, web, flutter, dart, claude codde, llm, coding, ai coding, vibe coding, product, saas, micro-saas, solid, best practices


---

# Avenca Digital — Internal Reference

**Avenca Digital** is a digital agency and the professional identity/alias of its founder. This document serves as the canonical internal reference for agents, projects, and automations that need context about who Avenca is, how it works, and what it builds.

---

## Identity & Positioning

Avenca Digital represents a deliberate approach to digital product delivery: building reliable, modern solutions with a sharp focus on clarity, performance, and outcomes that actually matter. The agency operates across client projects and internal products, combining web, mobile, backend, infrastructure, and AI in a single, integrated workflow.

The differentiating factor is **AI-first development** — Claude Code and LLMs are embedded at the core of every project, not as add-ons, but as primary tools that shape how fast and how well things get built.

---

## Technical Stack

### Frontend
- **Default:** Next.js (App Router) — used for most web projects, both client-facing and internal
- **Alternative:** Vite + React — for lightweight SPAs that don't require SSR or backend integration
- **Language:** TypeScript throughout; tabs for indentation; functional patterns preferred

### Mobile
- **Stack:** Flutter + Dart — single codebase targeting iOS and Android
- **State management:** GetX (currently active project); planning migration to a more modern approach (Bloc, MVVM, or similar) in future projects
- **Published:** [Corretor News](https://play.google.com) — live on the Play Store, a real-world reference of delivered mobile product

### Backend & APIs
- **FastAPI (Python)** — preferred when the project involves AI/ML integration or Python-heavy workflows
- **Hono (TypeScript)** — preferred for edge/serverless environments or when keeping the full stack in TypeScript
- **Choice is context-driven**, not opinionated — both are active and production-ready options

### Data & Storage
- **Supabase** — Postgres + auth + storage as a managed platform; used across multiple projects
- **Firebase** — Firestore + auth for projects that benefit from real-time or lighter backend needs
- No fixed ORM preference — stack adapts to the platform chosen

### Infrastructure
- **VPS:** Hostinger — self-managed Linux server hosting both personal and client projects
- **Panel:** EasyPanel — manages all services, deployments, and containers on the VPS
- **Hosted services include:** n8n, Paperclip, and various client and internal project deployments
- **Frontend deploys:** Vercel for Next.js projects when not self-hosted

### Automation
- **n8n** — self-hosted instance on the VPS; used for internal workflow automation, webhooks, and data pipelines
- Automation is applied wherever it reliably removes repetition: CI/CD, notifications, integrations, scheduled tasks

---

## AI & LLM Integration

AI is not a product category here — it's infrastructure. The approach:

- **Claude Code** is the primary development environment; AI-assisted coding is the default workflow, not an experiment
- **LLM APIs** (primarily Anthropic/Claude) are consumed directly in products where AI adds real value — chatbots, content generation, document processing, smart automation
- **Integration-focused:** the current posture is building on top of existing model APIs rather than training or fine-tuning models
- **Agents:** experience building agentic workflows, tool-use patterns, and multi-step AI pipelines for both internal and client use

---

## Business & Delivery Model

- Operates across **client projects** and **internal products** (SaaS, micro-SaaS, tools)
- Client work includes web apps, mobile apps, API development, and automation workflows
- Infrastructure (VPS + EasyPanel) supports both internal services and client-hosted projects under the same managed environment
- Product thinking drives every engagement: the goal is always a working, maintainable product — not just code that runs

---

## Approach & Values

- **AI-first by default** — Claude Code and LLMs are primary tools in every project, not auxiliary ones
- **Automation mindset** — if it can be automated reliably, it should be
- **Platform over infrastructure** — Supabase, Firebase, Vercel, EasyPanel reduce ops overhead so more energy goes into the product
- **Solid foundations** — proven patterns, typed code, maintainable structure from day one
- **Speed with quality** — vibe coding as a multiplier, not a shortcut; fast iteration without accumulating tech debt

---

## Keywords & Tags

Next.js · React · Vite · Flutter · Dart · FastAPI · Hono · TypeScript · Python · Supabase · Firebase · n8n · EasyPanel · VPS · Vercel · Claude Code · LLMs · Anthropic · AI Integration · Automation · SaaS · Micro-SaaS · Web · Mobile · Product · Vibe Coding · AI-first
