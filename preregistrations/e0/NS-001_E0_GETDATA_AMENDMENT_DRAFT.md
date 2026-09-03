# DRAFT — NS-001 E0 prospective GetData amendment

**Status:** DRAFT for H1 offline structural review. Not frozen. Not operative.
**Authorization:** This document does not authorize E0 or any network request.

This draft would amend the frozen E0 preregistration only after separate
review and freezing. The original preregistration and its sidecar remain the
unaltered record of the initial prospective specification.

## Proposed interface change

Replace SOAP `GetVelocityGradient` / `None_Fd8` with a GetData request for:

- dataset `isotropic1024coarse`;
- variable `velocity`;
- time `5.028`;
- temporal method `none`;
- spatial method `fd8noint`;
- spatial operator `gradient`;
- the original deterministic, nested, sequential partitions.

The proposed call shape is:

```python
getData(dataset, "velocity", 5.028, "none", "fd8noint", "gradient", points)
```

This draft does not approve a concrete client, an extraction such as
`result[0]`, or any nine-column ordering. Those details remain fail-closed
until the exact pinned client source proves them and they receive prospective
review.

## Proposed structural controls

The package root and run root would be explicit manifest and authorization
inputs. They must be absolute, non-overlapping paths, and the run root must be
outside the Git working tree. No `/workspace/ns-001` path is presumed.

Before any credential provider can be consulted, execution would verify the
reviewed code, original preregistration, original sidecar, and manifest-content
hashes. It would then require exclusive locking, a new run root, no existing
output or consumed marker, and an exact logical-operation budget.

H1's in-process checks establish consistency among the manifest and the
initialization-time and current source files associated with the imported mock
module. They do not prove that those bytes produced the executing Python
bytecode. Loaded-code provenance therefore remains unresolved. Before any
production callback is possible, H2 must provide either a reviewed external
source-only bootstrap or an externally verified, content-addressed, read-only
runtime. It must execute the exact bytes already read and verified, without
timestamp-based or unchecked bytecode-cache substitution.

Attempts and partition statuses would be append-only and flushed before the
next operation. Existing or partial output would never be truncated, replaced,
deleted, or automatically resumed.

Only explicitly classified transient transport failures would be retryable,
at most twice with an identical request identity. HTTP 4xx, unapproved status
codes, response-contract failures, numerical failures, and unclassified errors
would be terminal.

## Unchanged prospective design

This draft proposes no change to the E0 frame, lattice geometry, twelve
partitions, observable, decision threshold, interpretation limits, or
mandatory stop. H1 implements no live transport, credential loader, vorticity
reduction, `hat M_s` calculation, production receipt, final manifest,
authorization record, or execution package.
