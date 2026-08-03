# Architecture overview

> Generated/maintained as the repository's architecture SoT. Update when top-level layout or major dependencies change.

## Module layers

```mermaid
flowchart TB
  subgraph presentation [Presentation]
    UI[UI_or_API]
  end
  subgraph application [Application]
    AppCore[AppCore]
  end
  subgraph infrastructure [Infrastructure]
    DataStore[DataStore]
  end
  UI --> AppCore
  AppCore --> DataStore
```

## Key dependencies

```mermaid
flowchart LR
  ModuleA[ModuleA] --> ModuleB[ModuleB]
  ModuleB --> ExternalLib[ExternalLib]
```

## Notes

- **Scope**: …
- **Last updated**: YYYY/MM/DD
- **Verify**: …（how to validate this diagram still matches code）
