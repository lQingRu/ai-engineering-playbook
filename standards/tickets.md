# Ticket Creation Standards

## Purpose

Tickets must represent cohesive, independently verifiable pieces of functionality suitable for incremental development and meaningful human review. Apply this standard when breaking down a specification, plan, or agreed request.

## Granularity

- Prefer vertical slices over horizontal implementation layers.
- Give each ticket one clear outcome. Put unrelated functionality in separate tickets.
- Split tickets that introduce multiple independent technical decisions or cannot reasonably be reviewed in one focused session.
- Keep infrastructure and abstractions tied to the current outcome.
- Make blocking dependencies explicit.

## Required information

- Link to the parent specification when one exists.
- State the intended behaviour and business outcome.
- Include independently verifiable acceptance criteria and the evidence expected to verify them.
- Identify dependencies, relevant constraints, and existing decisions.

Use the project's configured tracker and the primary framework's existing ticket format. Reference the specification where it already supplies context.

## Specification lifecycle

A `to-spec` issue is a temporary planning artifact for agreed scope and test expectations. Keep it available while open tickets or reviews depend on it. Once the work and its reviews are complete, archive or close it under the project's tracker conventions and treat any retained copy as history.

Capture ongoing verification in tests and carry forward durable context in the appropriate [long-lived documentation](architecture.md#long-lived-documentation). [Matt Pocock's post](https://x.com/mattpocockuk/status/2083563195671667176) · [Follow-up on archiving](https://x.com/mattpocockuk/status/2083565169313980721)

## Reviewability

Before publishing tickets, present the complete proposed breakdown, explain why the slices are cohesive, identify unusually large or risky tickets, and surface significant unresolved decisions. Obtain human approval under the [personal approval policy](../global/AGENTS.md).

Check that each outcome can be verified under the project's completion convention and that every listed blocker genuinely gates the work.

## Implementation increments

A ticket may contain several smaller implementation increments and atomic commits. Prefer behavioural increments that are understandable, testable, and reviewable. Open separate GitHub issues for increments only when they deliver independently useful functionality.

## External guidance

Use Matt Pocock's `to-tickets` for slicing, tracker formats, and parent and blocker relationships. Use `to-spec` when the work needs a specification. For wide mechanical refactors, use the upstream expand–contract exception.
