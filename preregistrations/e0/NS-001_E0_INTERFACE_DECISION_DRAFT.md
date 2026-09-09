# DRAFT — NS-001 E0 interface decision

**Status:** DRAFT for H1 offline structural review. Not frozen. Not an E0 authorization.

## Proposed decision

Prospectively amend E0 to use the GetData interface rather than SOAP
`GetVelocityGradient`.

The completed preflight exercised this call shape:

```python
getData(dataset, "velocity", 5.028, "none", "fd8noint", "gradient", points)
```

It established only that an eight-point request reported shape `[8, 9]` and
72 finite values. The individual values were not retained. It therefore does
not establish numerical equivalence between GetData `fd8noint` and SOAP
`None_Fd8`, does not validate an extraction such as `result[0]`, and does not
prove the order or meaning of the nine returned columns.

GetData is preferred in principle because the 2,000,000-point limit is
evidenced for that interface and selecting it removes the need to claim
SOAP/GetData equivalence. The scientific estimand, frame, lattices,
partitions, and decision rule would remain unchanged.

## Unresolved evidence

No GetData client is selected or imported in H1. A later phase must obtain and
pin the exact client source, inspect its transport behavior and internal retry
policy, and establish an authoritative extraction and gradient-component
ordering.

Loaded-code provenance is also unresolved in H1. Its in-process checks bind
the manifest to the source file associated with the imported mock module, but
do not prove that those source bytes produced the executing Python bytecode.
H2 requires either a reviewed external source-only bootstrap or an externally
verified, content-addressed, read-only runtime. That trust root must execute
the exact bytes it already read and verified, without allowing substitution
from timestamp-based or unchecked bytecode caches.

Until that evidence and external trust root are reviewed and the amendment is
frozen, every live adapter must fail closed and NS-001 E0 remains HOLD.
