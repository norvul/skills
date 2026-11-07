# Python Review Guide

Apply this pass to `.py` modules, packages, scripts, tests, and Python-adjacent templates or config loaders after the general audit pass.

## Correctness And Contracts

- Check input validation, output correctness, and contract alignment.
- Check `None`, empty, missing, and partial-input handling.
- Check default values, sentinel logic, and fallback behavior.
- Check boundary conditions, off-by-one behavior, iteration ordering assumptions, and deterministic behavior.
- Check time, timezone, locale, encoding, and numeric precision behavior when those concerns exist.

## Python Design And Readability

- Prefer modules and functions with one clear responsibility.
- Check naming, module boundaries, import hygiene, and util-module sprawl.
- Remove dead helpers, commented dead code, and repeated near-duplicate logic.
- Prefer direct standard-library solutions over hand-rolled complexity when they are actually clearer.

## Types And Models

- Check type hints for usefulness, not decoration.
- Flag `Any` overuse, unsafe casts, and `Optional` misuse when the type can be made explicit.
- Check dataclass, pydantic, attrs, or model design for clear ownership and valid defaults.
- Watch for mutable default arguments, hidden mutation, and misleading field defaults.

## Reliability And Resource Safety

- Flag broad `except Exception`, swallowed exceptions, and fallback paths that hide failure.
- Check cleanup and resource safety for files, sockets, subprocesses, temp files, and locks.
- Prefer context managers when they improve safety and clarity.
- Check atomicity, retry behavior, timeout handling, and partial-write behavior where relevant.

## Security

- Check `subprocess` usage for command construction problems and `shell=True` misuse.
- Check `eval`, `exec`, dynamic imports, unsafe path handling, and temp-file handling.
- Check unsafe deserialization such as `pickle` or unsafe YAML loaders.
- Check secrets handling and sensitive logging.

## Performance

- Flag unnecessary list materialization, repeated scans, and accidental quadratic work.
- Check ORM, query-builder, pandas, and dataframe code for obviously poor query or transformation patterns.
- Check expensive work inside loops or request handlers.
- Check serialization, parsing, regex, and filesystem work for avoidable repetition on hot paths.
- Prefer streaming, iterators, batching, indexing, or precomputation when they materially reduce active-path cost.

## Testing

- Check whether Python tests actually cover boundary and failure paths.
- Prefer assertions on behavior and contracts over implementation trivia.
