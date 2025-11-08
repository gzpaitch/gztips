# React useWindowSize Hook

URL: /hooks/use-window-size
React useWindowSize hook for window dimension tracking. Handle responsive design with automatic resize detection, debouncing, and SSR compatibility using TypeScript.

---

title: React useWindowSize Hook
description: React useWindowSize hook for window dimension tracking. Handle responsive design with automatic resize detection, debouncing, and SSR compatibility using TypeScript.
icon: Monitor

---

<br />

Ever tried to track window dimensions in React and ended up with resize event chaos, SSR hydration nightmares, or performance-killing re-renders? You know the drill—manually adding window resize listeners, forgetting to debounce high-frequency events, dealing with server-side rendering mismatches, missing cleanup causing memory leaks. This free open source React useWindowSize custom hook handles all that viewport tracking complexity so you can focus on building responsive interfaces instead of debugging resize event edge cases in your React applications.

## useWindowSize showcase

Real-time window dimension tracking with debouncing and SSR support:

## Installation

pnpm dlx shadcn@latest add https://www.shadcn.io/registry/use-screen.json

## Why most window dimension tracking implementations suck

Look, you could keep manually adding resize event listeners and tracking dimensions. But then you hit the window size complexity—performance issues from unthrottled resize events, SSR hydration mismatches with undefined dimensions, memory leaks from forgotten cleanup, inconsistent breakpoint detection in React applications.

Most developers manually add window resize listeners without debouncing, causing performance issues when components re-render 60+ times per second during window resize in TypeScript components. Or they forget about SSR considerations and get hydration mismatches when server-rendered content differs from client-side window dimensions. Some skip cleanup entirely and create memory leaks from orphaned event listeners on unmounted components in Next.js projects.

This React hook uses optimized dimension tracking under the hood, with automatic debouncing and SSR-safe initialization in JavaScript applications. The browser handles all the resize events, plus you get comprehensive performance optimization and type safety in one call.

Plus it handles all the edge cases—SSR compatibility with controlled hydration, debounced updates for performance, automatic cleanup and memory management, type-safe dimension access in React development. No more layout shifts or broken responsive behavior.

This free open source React hook manages viewport state while you focus on building features. Whether you're creating React applications, Next.js dashboards, or TypeScript components, reliable window size tracking keeps your JavaScript development responsive.

## Features

- **Real-time tracking** with automatic window resize event handling and instant updates in React applications
- **Performance optimized** using configurable debouncing to prevent excessive re-renders in TypeScript components
- **SSR compatible** with proper server-side rendering support and hydration safety for Next.js projects
- **Type-safe implementation** with comprehensive TypeScript definitions and overloads for JavaScript development
- **Memory efficient** using optimized event listeners with automatic cleanup in React frameworks
- **Flexible initialization** supporting both immediate and undefined states for different environments in modern applications
- **Free open source** designed for modern React development workflows

## When you'll actually use this

Real talk—this isn't for basic responsive design in React applications. CSS media queries handle most viewport-based styling perfectly. But when you need actual window dimensions in JavaScript for dynamic layouts or complex responsive logic, this React hook delivers in Next.js projects.

Perfect for:

- **Dynamic layouts** - Adaptive grid systems and component sizing based on viewport built with TypeScript
- **Canvas and visualization** - Charts, maps, and graphics that need precise dimensions using React patterns
- **Mobile-first components** - Viewport-aware interfaces with conditional rendering in JavaScript applications
- **Performance optimization** - Debounced resize handling for intensive layout calculations in React components
- **Breakpoint detection** - JavaScript-based responsive behavior beyond CSS capabilities in Next.js applications
- **Dashboard interfaces** - Adaptive admin panels and data visualization layouts using TypeScript safety

## API Reference

### useWindowSize

```tsx
useWindowSize<T extends boolean = true>(
  options?: UseWindowSizeOptions<T>
): WindowSize<T extends false ? number | undefined : number>
```

| Parameter | Type                      | Default | Description                                    |
| --------- | ------------------------- | ------- | ---------------------------------------------- |
| `options` | `UseWindowSizeOptions<T>` | `{}`    | Configuration options for window size tracking |

### UseWindowSizeOptions

| Property              | Type      | Default     | Description                                                           |
| --------------------- | --------- | ----------- | --------------------------------------------------------------------- |
| `initializeWithValue` | `boolean` | `true`      | Whether to initialize with actual dimensions (set to `false` for SSR) |
| `debounceDelay`       | `number`  | `undefined` | Debounce delay in milliseconds for resize events                      |

### Return Value (WindowSize)

| Property | Type                  | Description                                            |
| -------- | --------------------- | ------------------------------------------------------ |
| `width`  | `number \| undefined` | Current window width in pixels (undefined during SSR)  |
| `height` | `number \| undefined` | Current window height in pixels (undefined during SSR) |

## Things to watch out for

**SSR requires careful initialization**: Use `initializeWithValue: false` to prevent hydration mismatches in React applications. The React hook will return `undefined` initially and update with actual dimensions after client hydration in TypeScript components.

**Debouncing affects responsiveness**: While debouncing improves performance during rapid resize events, it delays updates in Next.js projects. Choose the right balance between performance and real-time responsiveness for your use case in JavaScript applications.

**innerWidth includes scrollbars**: The React hook uses `window.innerWidth` and `window.innerHeight`, which include scrollbars in the measurement in React frameworks. This matches viewport behavior but differs from `clientWidth` in TypeScript projects.

**Memory management is automatic**: The React hook properly cleans up resize event listeners on component unmount in modern applications. Multiple components can use the hook simultaneously without conflicts.

## Related hooks you will also like

<Cards>
  <Card href="/hooks/use-resize-observer" title="useResizeObserver" description="Element-specific size tracking for component-level resize detection" />

  <Card href="/hooks/use-media-query" title="useMediaQuery" description="Responsive breakpoint detection for viewport-based logic" />

  <Card href="/hooks/use-screen" title="useScreen" description="Screen properties for display and hardware information" />

  <Card href="/hooks/use-is-client" title="useIsClient" description="Client detection needed for safe window dimension access" />

  <Card href="/hooks/use-event-listener" title="useEventListener" description="Event handling foundation for resize and window events" />

  <Card href="/hooks/use-debounce-value" title="useDebounceValue" description="Debounced updates for performance optimization patterns" />
</Cards>

## Questions you might have

<Accordions type="single">
  <Accordion id="useWindowSize-vs-css" title="When should I use this instead of CSS media queries?">
    Use this when you need actual pixel values in JavaScript - like for canvas sizing, dynamic grid columns, or conditional rendering in React applications. CSS media queries are perfect for styling, but when your component logic needs to know "is this exactly 768px wide?", that's when you need this React hook in TypeScript components.
  </Accordion>

{" "}

  <Accordion id="useWindowSize-ssr-crash" title="Why is my component crashing on server-side rendering?">
    The server doesn't have a `window` object, so the React hook returns `undefined` initially in Next.js projects. Set `initializeWithValue: false` and always check if width/height exist before using them: `if (!width) return <div>Loading...</div>` in JavaScript applications.
  </Accordion>

{" "}

  <Accordion id="useWindowSize-performance" title="Does this cause performance issues when resizing?">
    Not by default, but if you're doing expensive calculations on every resize, add `debounceDelay: 250` to the options in React applications. This prevents your component from re-rendering 60 times per second during window resize in TypeScript components.
  </Accordion>

{" "}

  <Accordion id="useWindowSize-mobile-rotation" title="Can I track when the user rotates their phone?">
    Yes! The React hook automatically detects orientation changes and mobile browser UI changes (like when the address bar hides) in Next.js projects. Both will trigger width/height updates, so you can respond to device rotation immediately in JavaScript applications.
  </Accordion>

  <Accordion id="useWindowSize-flickering" title="How do I avoid flickering during page load?">
    Set `initializeWithValue: false` and show a loading state until dimensions are available in React applications. This prevents the component from rendering with wrong dimensions first, then jumping to the correct size after hydration in TypeScript components.
  </Accordion>
</Accordions>
