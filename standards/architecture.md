# Architecture

Apply to module boundaries, dependencies, and changes that affect architecture or durable documentation.

## Owned policy

- Keep related behaviour together under a clear owner. Keep coupling low through small interfaces with explicit contracts.
- Preserve agreed boundaries and caller behaviour. Surface intentional changes to a contract or an ADR for review.
- Keep the implementation as simple as its current responsibilities allow.

## Long-lived documentation

- Use the project glossary for agreed domain terms and ADRs for the rationale behind qualifying decisions.
- Maintain architecture, module, and data model docs where readers need a map of the system, cross-module flows, ownership, or constraints that are hard to infer from one source file. Maintain product, design system, and limitations docs where readers need them to use or change the system.
- Give each fact one authoritative home. Link to code, configuration, schemas, and tests for details they already express. Verify descriptions of current behaviour against implementation evidence, label proposed work, and update affected docs and examples with the change.

## External guidance

Use Matt Pocock's `codebase-design` for modules, interfaces, and seams. Use `domain-modeling` for glossary and ADR changes and `writing-for-agents` for agent-facing guidance. For an explicitly requested deep maintainability review, use `thermo-nuclear-code-quality-review` within the existing `code-review` Standards axis.

## Project decisions and verification

Identify module boundaries, dependency rules, ADR conventions, and canonical documentation. Review affected callers and dependency direction, and run configured checks.
