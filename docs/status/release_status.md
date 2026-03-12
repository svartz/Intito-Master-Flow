# IMF Release Status

## Purpose

This document shows the latest known release state by environment.

## Environment Baseline

| Environment | Release ID | Commit | Deployment state | Validation state | Notes |
|---|---|---|---|---|---|
| DEV | not set | not set | not deployed | not verified | Initialize when first IMF deploy occurs. |
| TEST | not set | not set | not deployed | not verified | Initialize when first IMF deploy occurs. |
| PROD | not set | not set | not deployed | not verified | Initialize when first IMF deploy occurs. |

## Current Working Release

- Unreleased notes: [unreleased.md](/c:/Programming/Intito-Master-Flow/docs/releases/unreleased.md)
- Build template: [imf-build-template.json](/c:/Programming/Intito-Master-Flow/build/manifests/imf-build-template.json)

## Update Rule

After each real deploy:

1. update this document
2. store the final manifest
3. make sure a matching release note exists
4. confirm the Git tag and commit hash
