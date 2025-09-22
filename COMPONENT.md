# Practical Guide: Building the Perfect React Component

This guide provides best practices for creating functional, organized, and scalable components in React (and Next.js).

---

## Naming Conventions

- **File name:** Use kebab-case (e.g., `my-component.tsx`) for consistency and to prevent issues on case-sensitive systems.
- **Component name:** Use PascalCase (e.g., `MyComponent`), the community standard for React components.

---

## Structure and Export

- **Declaration:** Use a function declaration for the component. This helps tools and linters correctly identify the component’s name.

---

## Props: Interface or Type?

- **Prefer interfaces:** Use interfaces instead of types for typing props in TypeScript.
  - Interfaces are extendable.
  - Provide clearer error messages.
  - Match conventions found in large codebases.
- **Naming:** Name the interface following the `[ComponentName]Props` pattern.

---

## Props: Destructuring

- **Up to 3 props:** Destructure directly in the function parameters.
- **More than 3 props:** Use a single `props` object for clarity.

---

## Internal Component Organization

Follow this internal order for maintainability and readability:

1. **Custom Hooks** – Project-specific or external custom hooks.
2. **React Hooks** – useState, useRef, etc.
3. **useEffect** – Always after other hooks.
4. **Helper functions** – Only keep helpers here if they rely on local variables. Otherwise, place them in external utility files.
5. **Event handlers** – Functions for click, submit, etc.
6. **Early returns** – E.g., loading or error states handled via early returns.
7. **Render logic** – Compute or prepare variables right before the JSX.
8. **JSX** – Keep markup clean and minimally nested.

---

## JSX: Clean and Semantic

- Minimize excess `<div>` usage. Prefer semantic tags like `<section>`, `<main>`, `<header>`, `<footer>`.
- Use only one styling system per component. Don’t mix Tailwind, CSS Modules, and inline styles.
- Keep the final JSX block as direct and simple as possible.

---

## Reusable Components and Hooks

- **Large JSX:** Split sections into subcomponents.
- **Growing logic:** Extract logic into a custom hook.

---

## Example Project Structure

src/
├── components/
│ ├── MyComponent/
│ │ ├── MyComponent.tsx
│ └── OtherComponent/
├── hooks/
│ └── useMyHook.ts
├── utils/
│ └── helperFunctions.ts

---

## Final Tips

- Only comment JSX regions if truly necessary. Ideally, extract into smaller components.
- Use early returns for states like loading.
- For server components: prefer approaches like Next.js’s `loading.tsx` or React’s Suspense instead of classic in-component loading.

---

These guidelines summarize modern practices for writing elegant, readable, and scalable React components, ready for maintenance and teamwork.
