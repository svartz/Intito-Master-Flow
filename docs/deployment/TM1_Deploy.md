# TM1 v12 Deploy

This repository includes a conservative deploy utility for TM1 / Planning Analytics v12:

- script: `tools/tm1_deploy.py`
- config template: `tools/tm1.deploy.example.json`

## Design goals

- no secrets committed to Git
- validate local sources before any remote deploy
- require explicit `--execute` for changes against TM1
- support CI/CD and local operator use
- deploy the v12 process artifacts under `src/processes`

## Current scope

Implemented:

- validates paired process artifacts (`*.json` + linked `*.ti`)
- parses TI regions: `prolog`, `metadata`, `data`, `epilog`
- deploys processes to TM1 through the REST API
- uses a lightweight TM1 preflight against `/Processes?$top=1` before deploy
- validates custom object-definition JSON structure under `src/object-definitions`
- deploys native TM1 dimensions from `src/object-definitions/dimensions`
- deploys native TM1 cubes from `src/object-definitions/cubes`
- applies supported cube seed data through a temporary generated TI process

Not yet implemented:

- process execution after deploy, such as `IMF.P.Init.Project`
- environment-specific auth flows beyond Basic auth or a caller-supplied `Authorization` header

## Configuration

Use either environment variables or a local JSON file that is ignored by Git.

Recommended local file:

- `tools/tm1.deploy.local.json`

Create it from:

- `tools/tm1.deploy.example.json`

Supported environment variables:

- `IMF_TM1_BASE_URL`
- `IMF_TM1_API_PATH`
- `IMF_TM1_AUTH_MODE`
- `IMF_TM1_USER`
- `IMF_TM1_PASSWORD`
- `IMF_TM1_NAMESPACE`
- `IMF_TM1_AUTHORIZATION_HEADER`
- `IMF_TM1_VERIFY_SSL`
- `IMF_TM1_TIMEOUT_S`
- `IMF_TM1_PROCESS_ROOT`
- `IMF_TM1_OBJECT_DEFINITION_ROOT`
- `IMF_TM1_DEPLOY_PROCESSES`
- `IMF_TM1_VALIDATE_OBJECT_DEFINITIONS`
- `IMF_TM1_PROCESS_PREFIX`
- `IMF_TM1_ALLOW_OVERWRITE`

## Base URL patterns

The deploy utility supports two base URL styles:

### Standard TM1 REST root

Use:

- `base_url = https://host:port`
- `api_path = /api/v1`

This results in requests such as:

- `https://host:port/api/v1/Processes`

### Planning Analytics as a Service direct TM1 root

Use:

- `base_url = https://germanywestcentral.planninganalytics.saas.ibm.com/api/<tenant>/v0/tm1/<database>`
- `api_path = ""`

This results in requests such as:

- `https://germanywestcentral.planninganalytics.saas.ibm.com/api/<tenant>/v0/tm1/<database>/Processes`

For PA as a Service environments, this direct TM1 root may work even when the `/api/v1` suffix does not.
The client also sends browser-like `User-Agent`, `Origin`, `Referer`, and `Accept-Language` headers because some PA as a Service tenants block the default Python client signature on object endpoints.

## Safe usage

Validate only:

```powershell
python tools/tm1_deploy.py validate
```

Show deploy plan:

```powershell
python tools/tm1_deploy.py plan
```

Deploy processes:

```powershell
python tools/tm1_deploy.py deploy-processes --execute
```

Deploy native TM1 objects:

```powershell
python tools/tm1_deploy.py deploy-objects --execute
```

Deploy processes and then native TM1 objects:

```powershell
python tools/tm1_deploy.py deploy-processes --deploy-objects --execute
```

Deploy only security processes:

```powershell
python tools/tm1_deploy.py deploy-processes --filter IMF.P.Security. --execute
```

## Authentication

### Basic auth

Set:

- `IMF_TM1_AUTH_MODE=basic`
- `IMF_TM1_USER`
- `IMF_TM1_PASSWORD`

Optional:

- `IMF_TM1_NAMESPACE`

### Prebuilt authorization header

If your environment uses a gateway, reverse proxy, CAM flow, or external token broker, inject:

- `IMF_TM1_AUTHORIZATION_HEADER`

Example:

```powershell
$env:IMF_TM1_AUTHORIZATION_HEADER = 'Bearer <token>'
python tools/tm1_deploy.py deploy-processes --execute
```

## CI/CD guidance

For GitHub Actions or another runner:

- inject secrets as environment variables
- run `validate` on pull requests
- run `deploy-processes --execute` only in approved environment jobs
- keep PROD with `IMF_TM1_ALLOW_OVERWRITE=true` only when change control allows it

## Important limitation

The repository's dimension and cube JSON files under `src/object-definitions` are custom IMF definitions, not native TM1 REST payloads. The deploy script now transforms a supported subset of that schema into native TM1 dimensions, hierarchies, attributes, cubes, and cube seed data. More advanced constructs such as rules, chores, TI-driven post-processing, and broader object classes are still outside the current scope.
