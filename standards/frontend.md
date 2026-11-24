# Frontend

Apply to client-side components, state, and data flow.

## Owned policy

- Give each component a clear responsibility. Reuse established components when they fit.
- Give each piece of state a clear owner. Derive values from their source where possible and make shared state and side effects explicit.
- Make loading, empty, error, and success states explicit where they affect the user.

## External guidance

For React component APIs, consult `vercel-composition-patterns`. For React or Next.js performance, consult `vercel-react-best-practices` and the version-matched [React](https://react.dev/versions) or [Next.js](https://nextjs.org/docs) docs. For other stacks, start with the platform maintainer's guidance.

## Project decisions and verification

Establish component boundaries, state and data-fetching conventions, and applicable performance budgets. Review state ownership, run affected component tests, and measure performance when the change targets it.
