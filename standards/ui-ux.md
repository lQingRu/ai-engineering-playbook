# UI/UX

Apply to visual design, interaction, and user-facing flows.

## Owned policy

- Use the project's design system and interaction patterns. Agree on substantial changes to visual direction before implementation.
- Keep key flows usable across supported viewports and input methods. Use WCAG 2.2 AA as the default target for web UI and record the applicable target in the project.
- Validate the changed flow in the rendered interface, including error and recovery states where relevant.

## External guidance

- Visual direction or critique → consult `impeccable` within its registry scope.
- Targeted visual and interaction polish → consult `make-interfaces-feel-better`.
- Web UI source review → consult `web-design-guidelines`. Evaluate accessibility against [WCAG 2.2](https://www.w3.org/TR/WCAG22/) using [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/). Where Playwright is already used, [axe checks](https://playwright.dev/docs/accessibility-testing) can supplement manual checks.

## Project decisions and verification

Establish design system ownership, supported browsers or platforms, and accessibility targets. Exercise affected flows in the browser or native runtime. For web interactions, check keyboard operation and focus alongside configured accessibility checks.
