# Brand assets

The mark is an anvil: one continuous filleted silhouette in paper `#FAFBFC`, with the working
face struck in brass `#E0A32E` — brass is heat, and it is the only palette colour that can read
as hot metal. Teal `#0E7C7B` stays the accent in the `CODEFORGE.` wordmark and in the site UI,
so the mark and the type share one rule instead of competing.

The name is code + forge, as in the forges where weapons were made — not a machine shop. Marks
that read as milling or fabrication miss the brief.

## Files

| File | Use |
|---|---|
| `avatar.svg` / `codeforge-avatar.png` | Square mark on iron. Social avatars, app icon. |
| `avatar-light.svg` | Same mark on paper, for light surfaces. |
| `lockup-dark.svg` / `lockup-light.svg` | Mark + wordmark, horizontal. Headers, signatures, decks. |
| `cover.svg` / `codeforge-cover.png` | 1640×624 social cover. |
| `build_marks.py` | Geometry source. The profile lives here, not in the SVGs. |

## Rules

- Never redraw the silhouette by hand. Edit `PROFILE` in `build_marks.py` and re-render, so
  every junction keeps its fillet and the brass stays clipped to the top edge.
- Check every change at **32px and 48px** before accepting it. That is where marks fail, and
  it is the size a Facebook feed and a browser tab actually render.
- Typeface is Archivo 700 for the wordmark. Letter-spacing 1, and the trailing period is teal.

## Rendering

Requires `rsvg-convert` and Archivo on the fontconfig path.

```sh
rsvg-convert -w 1024 -h 1024 brand/avatar.svg -o brand/codeforge-avatar.png
```
