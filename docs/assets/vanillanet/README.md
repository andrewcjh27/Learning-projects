# VanillaNet Seminar — assets

Materials for the **Neurocle Researcher** interview seminar on
*VanillaNet: the Power of Minimalism in Deep Learning* (arXiv:2305.12972).

## What's here

| File | Use |
|------|-----|
| `../vanillanet.html` | **Interactive 15-slide deck.** Open in a browser, present live or screen-record. Two live demos: the deep-training λ collapse and the series-activation curve. |
| `vanillanet-seminar.pdf` | **Browser-free backup** — all 15 slides, one per page (export from the deck via the steps below). |
| `architecture.svg` | VanillaNet-6 block diagram (stem → 4 stages → head). |
| `deep-training.svg` | The 3-step collapse: two convs + activation → one conv. |
| `series-activation.svg` | Serial vs. parallel activation stacking. |
| `depth-vs-latency.svg` | Bar chart — depth, not FLOPs, sets GPU latency. |

## Keyboard controls (live deck)

| Key | Action |
|-----|--------|
| `→` / `Space` / `←` | Next / previous slide |
| `Home` / `End` | Jump to first / last slide |
| `S` | Toggle **speaker notes** (talking points + per-slide timing for the 30-min talk) |
| `F` | Fullscreen |

Speaker notes are presenter-only — they never appear in the PDF export, so you
can keep them open on your laptop while the deck shows on the projector.

## Re-exporting the PDF (or a PNG set)

The committed `vanillanet-seminar.pdf` was generated headlessly; to rebuild it
(or change the look), use Chrome’s print pipeline — the deck has a dedicated
`@media print` layout that drops the chrome and lays out one slide per page:

```bash
chrome --headless --no-pdf-header-footer --virtual-time-budget=4000 \
  --print-to-pdf=vanillanet-seminar.pdf vanillanet.html
# PNG set (one image per slide):
pdftoppm -png -r 96 vanillanet-seminar.pdf slide
```

Or just open `vanillanet.html` and **Print → Save as PDF** (set margins to None).

## Dropping the SVGs into Figma

1. Drag an `.svg` straight onto the Figma canvas (or **File → Place image**).
2. Figma imports it as a group of editable vectors + text layers.
3. Right-click → **Ungroup** to recolour, restyle, or pull single elements
   into your own slides. Text stays editable (set in Inter / JetBrains Mono).

Palette used (matches the deck, so screen-recorded clips and Figma frames
stay consistent):

- bg `#0e1628` · card `#121c30` · border `#1e2d47`
- primary `#4f8ef7` · accent `#34d399` · violet `#a78bfa` · amber `#fbbf24`
- text `#dde8f5` · muted `#7a8faa`

## Suggested 30-minute flow

1. **Thesis + problem** (slides 1–4) — why minimalism, and the depth-≠-FLOPs insight. *~7 min*
2. **Lineage** (slide 5) — the U-turn from the ResNet era. *~3 min*
3. **Architecture + the catch** (slides 6–7) — what the net is, why it's weak naively. *~5 min*
4. **The two tricks** (slides 8–9) — drive both live demos; open the math panels on demand. *~8 min*
5. **Ablations + results + limits** (slides 10–13) — evidence each piece earns its place. *~5 min*
6. **Takeaways + Q&A** (slides 14–15). *~2 min*
