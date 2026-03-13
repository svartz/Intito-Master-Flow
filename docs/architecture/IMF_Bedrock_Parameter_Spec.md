# IMF Bedrock Parameter Specification

## Purpose
This document defines the verified Bedrock v5 parameter contracts for the Bedrock processes currently referenced by IMF, and compares them to the current IMF source implementation.

It exists because IMF currently uses Bedrock as an optional integration seam, but some IMF processes still assume wrapper-style parameter names that do not match the actual Bedrock v5 process contracts.

## Source of truth
Verified against the `bedrock-5` GitHub repository on March 13, 2026:

- `https://github.com/cubewise-code/bedrock-5`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.dim.create.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.dim.clone.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.hier.clone.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.dim.attr.create.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.security.group.create.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.security.object.assign.json`
- `https://raw.githubusercontent.com/cubewise-code/bedrock-5/master/bedrock_processes_json/}bedrock.server.writetomessagelog.json`

## Scope
The Bedrock processes currently referenced by IMF are:

- `}bedrock.dim.create`
- `}bedrock.dim.clone`
- `}bedrock.hier.clone`
- `}bedrock.dim.attr.create`
- `}bedrock.security.group.create`
- `}bedrock.security.object.assign`
- `}bedrock.server.writetomessagelog`

## Verified Bedrock parameter contracts

### `}bedrock.dim.create`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pDim` | Yes |  | Delimited list of dimensions |
| `pDelim` | No | `&` | Delimiter for list parameters |
| `pLogOutput` | No | `0` | Write summary to server message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF must not call this process with `pDimension`.
- The correct Bedrock-native parameter is `pDim`.

### `}bedrock.dim.clone`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pSrcDim` | Yes |  | Source dimension |
| `pTgtDim` | No | `pSrcDim | '_Clone'` | Target dimension |
| `pHier` | No | `*` | Delimited list of hierarchies |
| `pAttr` | No | `0` | Include attributes |
| `pUnwind` | No | `0` | Unwind after process |
| `pDelim` | No | `&` | Delimiter |
| `pSub` | No | `0` | Include subsets |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF must not call this process with `pDimension`.
- `IMF.P.Dimension.Clear` currently points to `}bedrock.dim.clone`, but does not provide a valid clone contract.
- `IMF.P.Dimension.Clear` should either:
  - stop delegating to Bedrock until a proper clear strategy is defined, or
  - switch to a wrapper that maps an IMF clear intent onto a Bedrock clone strategy.

### `}bedrock.hier.clone`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pSrcDim` | Yes |  | Source dimension |
| `pSrcHier` | Yes |  | Source hierarchy |
| `pTgtDim` | No | `pSrcDim` | Target dimension |
| `pTgtHier` | No | derived | Target hierarchy |
| `pAttr` | No | `0` | Include attributes |
| `pUnwind` | No | `0` | Unwind after process |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF must not call this process with `pSourceDimension` and `pTargetDimension`.
- A Bedrock-native call must provide at least `pSrcDim` and `pSrcHier`.
- For single-hierarchy IMF use, the natural default is:
  - `pSrcDim = <source dimension>`
  - `pSrcHier = <source dimension>`
  - `pTgtDim = <target dimension>`
  - `pTgtHier = <target dimension>` or a deliberately chosen hierarchy name

### `}bedrock.dim.attr.create`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pDim` | Yes |  | Delimited list of dimensions |
| `pAttr` | Yes |  | Delimited list of attributes |
| `pPrevAttr` | No |  | Insert position |
| `pAttrType` | No | `S` | Attribute type |
| `pDelim` | No | `&` | Delimiter |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF cannot hand Bedrock only source and target dimensions and expect it to infer the attribute list.
- `IMF.P.Attribute.CopyDefinitions` must either:
  - loop through source attributes and call Bedrock once per attribute, or
  - build a delimited attribute list and call Bedrock with `pDim = <target>` and `pAttr = <list>`.

### `}bedrock.security.group.create`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pGroup` | Yes |  | Delimited list of groups |
| `pAlias` | No |  | Alias for subset |
| `pDelim` | No | `&` | Delimiter |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF-native naming such as `pGroupName` is not valid for direct Bedrock delegation.
- `IMF.P.Security.CreateGroups` should map the IMF group list into `pGroup`.

### `}bedrock.security.object.assign`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pGroup` | Yes |  | Delimited list of groups |
| `pObjectType` | Yes |  | `Cube`, `Dimension`, `Process`, `Chore`, or similar supported object type |
| `pObject` | Yes |  | Delimited list of objects |
| `pSecurityLevel` | Yes |  | `Read`, `Write`, `Admin`, `None` |
| `pSecurityRefresh` | No | `Yes` | Refresh security after execution |
| `pDelim` | No | `&` | Delimiter |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF-native names like `pGroupName`, `pCubeName`, `pDimensionName`, and `pAccess` are not valid for direct Bedrock delegation.
- Mapping must be:
  - cube security:
    - `pGroup = pGroupName`
    - `pObjectType = 'Cube'`
    - `pObject = pCubeName`
    - `pSecurityLevel = ProperCase(pAccess)`
  - dimension security:
    - `pGroup = pGroupName`
    - `pObjectType = 'Dimension'`
    - `pObject = pDimensionName`
    - `pSecurityLevel = ProperCase(pAccess)`

### `}bedrock.server.writetomessagelog`
Required and optional parameters:

| Parameter | Required | Default | Meaning |
|---|---|---:|---|
| `pLevel` | Yes |  | Severity such as `INFO`, `DEBUG`, `ERROR` |
| `pMessage` | Yes |  | Message text |
| `pLogOutput` | No | `0` | Write summary to message log |
| `pStrictErrorHandling` | No | `0` | Quit on first major error |
| `pJson` | No | `{}` | JSON override object |

IMF impact:
- IMF must not call this process with only `pMessage`.
- `IMF.P.Log.Event` should pass:
  - `pLevel = pSeverity`
  - `pMessage = <formatted IMF message>`

## Current IMF mismatch summary

| IMF process | Bedrock process | Current IMF assumption | Verified Bedrock parameter(s) | Status |
|---|---|---|---|---|
| `IMF.P.Dimension.Create` | `}bedrock.dim.create` | `pDimension` | `pDim` | Wrong |
| `IMF.P.Dimension.Clear` | `}bedrock.dim.clone` | `pDimension` | `pSrcDim`, optional `pTgtDim` | Wrong and semantically weak |
| `IMF.P.Dimension.CopyRelations` | `}bedrock.hier.clone` | `pSourceDimension`, `pTargetDimension` | `pSrcDim`, `pSrcHier`, `pTgtDim`, `pTgtHier` | Wrong |
| `IMF.P.Attribute.CopyDefinitions` | `}bedrock.dim.attr.create` | No concrete mapping yet | `pDim`, `pAttr`, optional `pPrevAttr`, `pAttrType` | Incomplete |
| `IMF.P.Security.CreateGroups` | `}bedrock.security.group.create` | No concrete mapping yet | `pGroup` | Incomplete |
| `IMF.P.Security.SetCubeAccess` | `}bedrock.security.object.assign` | No concrete mapping yet | `pGroup`, `pObjectType`, `pObject`, `pSecurityLevel` | Incomplete |
| `IMF.P.Security.SetDimensionAccess` | `}bedrock.security.object.assign` | No concrete mapping yet | `pGroup`, `pObjectType`, `pObject`, `pSecurityLevel` | Incomplete |
| `IMF.P.Log.Event` | `}bedrock.server.writetomessagelog` | `pMessage` only | `pLevel`, `pMessage` | Wrong |

## Recommended integration pattern
Do not call Bedrock directly from IMF until the parameter contract is explicitly mapped.

Recommended pattern:

1. Keep IMF parameters IMF-oriented.
2. Map them in one place before Bedrock `ExecuteProcess`.
3. Convert IMF conventions into Bedrock conventions explicitly.
4. Keep native IMF fallback when Bedrock is missing or when delegation fails.

Example mapping for `IMF.P.Dimension.Create`:

```ti
nBedrockReturn = ExecuteProcess(
  sBedrockProcess,
  'pDim', sTargetDimension,
  'pLogOutput', '0',
  'pStrictErrorHandling', If(sStrictBedrock @= 'Y', '1', '0')
);
```

Example mapping for `IMF.P.Log.Event`:

```ti
nBedrockReturn = ExecuteProcess(
  sBedrockProcess,
  'pLevel', sSeverity,
  'pMessage', sFormattedMessage,
  'pLogOutput', '0',
  'pStrictErrorHandling', If(sStrictBedrock @= 'Y', '1', '0')
);
```

## Recommended next actions
1. Refactor all IMF Bedrock calls to use the verified Bedrock parameter names in this document.
2. Introduce a shared Bedrock mapping convention in IMF, so direct Bedrock calls follow one standard.
3. Consider wrapper processes where IMF intent and Bedrock mechanics do not align cleanly, especially:
   - `IMF.P.Dimension.Clear`
   - `IMF.P.Attribute.CopyDefinitions`
   - `IMF.P.Security.CreateGroups`
4. Add a static verification test that fails if IMF Bedrock calls use non-Bedrock parameter names.

## Current recommendation by process
- Safe to refactor immediately:
  - `IMF.P.Dimension.Create`
  - `IMF.P.Log.Event`
- Requires design decision before Bedrock activation:
  - `IMF.P.Dimension.Clear`
  - `IMF.P.Dimension.CopyRelations`
  - `IMF.P.Attribute.CopyDefinitions`
  - `IMF.P.Security.CreateGroups`
  - `IMF.P.Security.SetCubeAccess`
  - `IMF.P.Security.SetDimensionAccess`
