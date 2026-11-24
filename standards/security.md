# Security

Apply to changes involving access, sensitive data, dependencies, or trust boundaries.

## Owned policy

- Keep secrets out of source code, configuration committed to Git, test fixtures, and logs. Store them in the project's approved secret store.
- Grant users, services, and automation the minimum privileges required. Enforce authorization at the boundary that controls access to protected actions or data.
- Review changes to trust boundaries, data exposure, and dependencies before release.

## External guidance

For web applications and services, use applicable [OWASP ASVS](https://asvs.owasp.org/) requirements. For other systems, use platform security guidance and the project's threat model. Prefer configured secret and dependency scanning for repeatable checks.

## Project decisions and verification

Establish trust boundaries, sensitive data handling, secrets ownership, and security checks. Verify permitted and denied paths for affected access controls and run the relevant scans.
