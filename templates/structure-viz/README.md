# Structure visualization template

Copy parts into a **target repository** as needed.

## Tier 1 (docs)

Copy `architecture.md` → `<target-repo>/docs/architecture.md` and edit diagrams.

## Tier 3 (static site)

```powershell
$dest = "<target-repo>\docs\structure-viz"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "site\*" $dest
```

Open `index.html` in a browser (file:// or local static server). No build step required.

Keep `architecture.md` and the site in sync when both exist (same module names and edges).

## Tier 2

Use Cursor's bundled `canvas` skill; do not copy this folder for Tier 2.
