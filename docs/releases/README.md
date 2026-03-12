# IMF Releases

This folder contains two types of release documents:

- `unreleased.md`: the working release note during active development
- `imf-vX.Y.Z.md`: frozen release snapshots for tagged builds

Recommended workflow:

1. add ongoing implementation notes to `unreleased.md`
2. when cutting a release, create a new release file from `imf-release-template.md`
3. generate the matching build manifest under `build/manifests/`
4. create the Git tag for the same release id
