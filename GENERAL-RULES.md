# Development Rules Guide — v1.0

---

## Non-Negotiable Principles

### Reuse First

Before creating **new services, utilities, types, interfaces, components, or hooks**, **check** if something existing can be **reused or improved**.

### Plan Before Coding

Always start with **pseudocode** (step-by-step), **define dependencies**, risks, and integration points. **Validate the approach** with the team before coding.

### Code Quality

- Code in **TypeScript First** (when applicable).
- **Correct, functional, bug-free**, following **DRY** and **KISS**.
- **Readability over microperformance**.
- **Names, comments, and docs in English (US)**.
- **No TODOs/PLACEHOLDERs** in merges to `main`.
- **Complete imports**, clear and consistent naming.
- If unsure, **state explicitly** (don’t guess).

### Security & Privacy by Default

Validate inputs, handle errors without leaking details, protect secrets.

### Automation over Manual Rules

Lint, format, test, and type-check **automated** in pre-commit/CI.

---

**Rules**

- **Named exports** by default; **PascalCase** for components; **camelCase** for functions/variables.
- Separate **presentational** vs **container** components when relevant.
- One file per component; **index.ts** only for re-export.
- **Hooks** start with `use*` and have no side effects outside React.

**Styles**

- **Design System**: tokens (colors, typography, spacing) centralized.
- If using utility CSS (e.g., Tailwind), standardize **variants** and reusable **components**.
- Avoid inline styles except rare cases.

---

## Implementation Standards

1. **TypeScript**: `strict` on; forbid implicit `any`; use **narrow types**; domain-based models.
2. **Errors**: create **error types**; user-safe messages; on front-end, **Error Boundaries** + friendly toasts.
3. **Accessibility (A11y)**: visible focus, semantic HTML, keyboard navigation; align with **WCAG 2.2 AA**.
4. **i18n**: stable keys, no HTML interpolation; avoid string concatenation.
5. **Performance**: avoid unnecessary renders; memoize wisely; lazy-loading; set **performance budgets** (e.g., TTI < 3s on 4G).
6. **Security**: input validation, escaping/encoding, CSRF/XSS/SQLi protections; secrets out of repo; **CSP** and secure headers.
7. **Dependencies**: weekly updates (bot + review); **pin versions**; avoid libs with low **bus factor**.
8. **Feature Flags**: for gradual releases; remove stale flags.

---

## Code Style Guide

- **Domain-oriented, clear names** (`CustomerInvoice`, `calculateTax`).
- **Pure functions** where possible; avoid uncontrolled side effects.
- **Early return** to reduce nesting.
- **Prefer composition over inheritance**.
- **Comments** only for context; code should explain itself.
- **Minimal docs** with TSDoc for public functions.
- **Short files** (< 300 LOC) and **short functions** (< 30 LOC) when reasonable.

---

## Refactoring

1. **Break down large components** into smaller, single-responsibility ones.
2. **Suggest new folder structures** by domain/feature.
3. **React Naming**: `PascalCase` for components, `use*` for hooks, typed props.
4. **State**: move shared state to context/store only when necessary.
5. **Boy Scout Rule**: leave the code better than you found it.
6. **Metrics**: reduce cognitive complexity and file size.

---

## Dependency Governance

- Use a **single package manager** (pnpm) standardized in repo.
- **Lockfile** versioned; weekly updates via bot + human review.

---

## Config & Secrets Management

- Variables via **`.env` per environment** (or secret manager).

---
