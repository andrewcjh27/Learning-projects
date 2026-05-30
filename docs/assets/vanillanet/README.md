# VanillaNet Seminar — assets

Materials for the **Neurocle Researcher** interview seminar on
*VanillaNet: the Power of Minimalism in Deep Learning* (arXiv:2305.12972).

## What's here

| File | Use |
|------|-----|
| `../vanillanet.html` | **Interactive 15-slide deck.** Open in a browser, present live or screen-record. Arrow keys / Space to navigate, `F` for fullscreen. Two live demos: the deep-training λ collapse and the series-activation curve. |
| `architecture.svg` | VanillaNet-6 block diagram (stem → 4 stages → head). |
| `deep-training.svg` | The 3-step collapse: two convs + activation → one conv. |
| `series-activation.svg` | Serial vs. parallel activation stacking. |
| `depth-vs-latency.svg` | Bar chart — depth, not FLOPs, sets GPU latency. |

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
