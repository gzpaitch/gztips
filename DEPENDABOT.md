# DEPENDABOT.md

--- dependabot.yml

version: 2
updates:

## DEPENDENCIES

# Keep npm dependencies up to date

- package-ecosystem: "npm"
  directory: "/"
  schedule:
  interval: "daily"
  time: "03:00"
  timezone: "America/Sao_Paulo"
  open-pull-requests-limit: 5
  labels:
  - "dependencies"
  - "npm"
    commit-message:
    prefix: "chore"
    include: "scope"
  # Group minor and patch automatically, major stays separate
  groups:
  non-major-dependencies:
  update-types: - "minor" - "patch"
  # Major updates remain as individual PRs for manual review

## DOCKERFILE

# Keep Dockerfile up to date

- package-ecosystem: "docker"
  directory: "/"
  schedule:
  interval: "daily"
  time: "03:00"
  timezone: "America/Sao_Paulo"
  open-pull-requests-limit: 3
  labels:
  - "dependencies"
  - "docker"
    commit-message:
    prefix: "chore"
    include: "scope"
  # Group minor and patch, major stays separate
  groups:
  non-major-docker:
  update-types: - "minor" - "patch"
