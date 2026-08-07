# Brand assets

The mark is an anvil: one continuous filleted silhouette in paper `#FAFBFC`, with the working
face struck in brass `#E0A32E` — brass is heat, and it is the only palette colour that can read
as hot metal.

**The logo has exactly one accent, and it is brass.** The trailing period in `CODEFORGE.` is
brass too, so the mark and the wordmark agree; an earlier version had a teal period beside a
brass face, and two accents inside one logo read as unresolved. Teal `#0E7C7B` keeps its own
job as the *interface* accent — rules, links, focus rings — and never appears inside the logo.

The name is code + forge, as in the forges where weapons were made — not a machine shop. Marks
that read as milling or fabrication miss the brief.

## Files

| File | Use |
|---|---|
| `avatar.svg` / `avatar.png` | Square mark on iron. Social avatars, app icon. |
| `avatar-light.svg` | Same mark on paper, for light surfaces. |
| `lockup-dark.svg` / `lockup-light.svg` | Mark + wordmark, horizontal. Headers, signatures, decks. |
| `cover.svg` / `cover.png` | 1640×624 social cover. |
| `build_marks.py` | Geometry **and** asset generation. Run it; do not edit the SVGs. |

## Rules

- Never redraw the silhouette by hand. Edit `PROFILE` in `build_marks.py` and re-render, so
  every junction keeps its fillet and the brass stays clipped to the top edge.
- Check every change at **32px and 48px** before accepting it. That is where marks fail, and
  it is the size a Facebook feed and a browser tab actually render.
- Typeface is Archivo 700 for the wordmark. Letter-spacing 1, and the trailing period is brass.
- The mark is centred on `ANCHOR`, halfway between its bounding box and its area centroid. The
  horn is thin while the face and base carry the mass, so centring on the bounding box alone
  puts the silhouette visibly right of centre — about 60px of it at 1024.

## Rendering

Requires `rsvg-convert` and Archivo on the fontconfig path.

```sh
python3 brand/build_marks.py
```

That regenerates every SVG and PNG in this directory from `PROFILE`.
