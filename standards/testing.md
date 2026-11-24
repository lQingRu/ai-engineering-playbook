# Testing

Apply to new behaviour, behaviour changes, and regressions.

## Owned policy

- Test observable behaviour through supported interfaces. Use deterministic setup and independent expected results.
- Cover changed behaviour and meaningful failure cases. Add a regression test for a bug and show that it detects the original failure.
- Use test-first for behavioural changes in pairing. If automation is impractical, use the [exception process](README.md) and provide alternate evidence.

## External guidance

Use Matt Pocock's `tdd` for test seams, the red–green cycle, and mocking guidance. Use the project's chosen test framework documentation for implementation details.

## Project decisions and verification

Establish test levels, commands, fixtures, and CI gates. Run affected tests and map the evidence to the acceptance criteria.
