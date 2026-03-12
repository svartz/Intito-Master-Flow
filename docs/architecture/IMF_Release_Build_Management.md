# IMF Release And Build Management

## Purpose
This document defines how IMF should be versioned, built, documented, and traced across environments.

The goal is to keep these concerns connected:

- source code in Git
- deployable build artifacts
- live implementation status
- frozen release snapshots
- environment deployment state

## Core Principles

### Git Commit Is The Technical Truth
Every IMF change is anchored to a Git commit.

### Git Tag Is The Release Truth
Every releasable IMF build should have a Git tag.

Recommended pattern:

- `imf-v0.1.0`
- `imf-v0.1.1`
- `imf-v0.2.0`

### Build Manifest Is The Deploy Truth
Every deployable IMF build should have a manifest that records:

- release id
- commit hash
- build date
- target environment
- object/process scope
- known blockers or notes

### Status Documents Are The Live Truth
Status documents describe the current evolving state of the implementation.

They are allowed to change frequently.

### Release Documents Are Frozen Snapshots
Release notes capture what was true at the time of a specific release.

They should not be continuously rewritten after release except for critical correction notes.

## Recommended Repository Structure

- `build/manifests/`
- `docs/releases/`
- `docs/status/`
- `docs/adr/`

Purpose by folder:

- `build/manifests/`: machine-readable build and deploy metadata
- `docs/releases/`: immutable release snapshots plus `unreleased`
- `docs/status/`: living implementation and deployment state
- `docs/adr/`: design and governance decisions that should persist across releases

## Versioning Model

Recommended release model:

1. Use semantic versioning for planned releases.
2. Use Git tags with `imf-vX.Y.Z`.
3. Store the active release id in deployment metadata.

Examples:

- `imf-v0.3.0`
- `imf-v0.3.1`
- `imf-v1.0.0`

## Build Identity

Each IMF build should carry:

- `releaseId`
- `gitCommit`
- `buildDateUtc`
- `environment`
- `artifactScope`
- `documentationBaseline`
- `deploymentMode`
- `languageSupport`

## Documentation Model

IMF documentation should be treated as three related layers.

### 1. Stable Architecture Documentation
Used for design intent and principles.

Examples:

- architecture blueprints
- Bedrock adoption design
- security model
- release/build management design

### 2. Living Status Documentation
Used for current implementation state.

Examples:

- process implementation status
- Bedrock refactor status
- release status by environment

### 3. Release Snapshots
Used to freeze what was delivered in a specific build.

Examples:

- `docs/releases/imf-v0.3.0.md`
- `docs/releases/imf-v0.3.1.md`

## Working Model During Development

For ongoing development:

1. Update source in `src/`
2. Update the appropriate live status document in `docs/status/`
3. Add the change to `docs/releases/unreleased.md`
4. If a design decision changed, add or update an ADR

This keeps live documentation current without corrupting release history.

## Release Flow

Recommended release flow:

1. Confirm repo validation passes
2. Update `docs/releases/unreleased.md`
3. Generate `build/manifests/<release>.json`
4. Create `docs/releases/<release>.md`
5. Tag the commit
6. Deploy
7. Update `docs/status/release_status.md`

## Minimum Release Gate

An IMF release should not be considered complete until:

1. all intended process pairs have `.ti` and `.json`
2. `tools/tm1_deploy.py validate` passes
3. release notes exist
4. a build manifest exists
5. a Git tag exists
6. deployment status is recorded

## Environment Traceability

Each environment should be traceable to:

- deployed release id
- deployed commit hash
- deployment date
- deployment operator
- validation status

This can be stored:

- in build manifest history
- in `docs/status/release_status.md`
- optionally in IMF control metadata inside TM1 later

## Recommended Future TM1 Traceability

When the IMF control model is mature enough, store these values in TM1:

- `ReleaseId`
- `GitCommit`
- `BuildDateUtc`
- `DeployedBy`
- `ManifestName`

Suggested location:

- `IMF.C.Config`
- or a future `IMF.C.Release`

## Change Control Guidance

Use `docs/releases/unreleased.md` as the single working release note during active development.

When a release is cut:

- copy relevant items into a new release file
- clear or reset `unreleased.md`
- tag the release commit

## Decision

IMF should use:

- Git commit for technical traceability
- Git tag for release identity
- build manifest for deploy identity
- living status documents for current implementation state
- frozen release documents for historic release traceability
