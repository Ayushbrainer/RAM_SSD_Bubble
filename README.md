# The 2026 Memory Price Surge and the AI Bubble

Data Visualisation project (NTU CCDS), Group 04

| Student | Matric ID |
|---|---|
| Ayush Bhatt | G2610412E |
| Bu Dinglin | G2609929D |

How AI spending pushed RAM and SSD prices up 20x from their 2023 low, who pays, who profits, and whether the AI build-out is a bubble.

## What we submit

| File | What it is |
|---|---|
| `summary.pdf` | 2-page Summary Report (still needs: Bu Dinglin's contribution) |
| Recorded video | 6 minutes max, recorded from `RAM_AI_Bubble.pptx` |

## Files

| Path | Contents |
|---|---|
| `CONTRIBUTIONS.md` | Who did what; each member records their own contributions |
| `RAM_AI_Bubble.pptx` | 14-slide deck. Each slide plays one animated chart; the narration is in the speaker notes |
| `video_script.pdf` | The same narration as a printable script: Ayush does the intro and data story (scenes 1-5), Bu Dinglin takes scenes 6-10 and the conclusion |
| `clips/` | The 11 animated charts as MP4 (1920x1080) |
| `data/` | The 3 datasets we compiled (CSV) |
| `report.pdf` | Full written report with all references (not submitted; use it to check numbers) |
| `explainer.pdf` | Plain-English walkthrough of the project |
| `*.tex`, `style.tex`, `figures/` | LaTeX sources for the PDFs (upload the whole repo to Overleaf to edit) |
| `code/` | Scripts that regenerate the clips (`make_clips.py`), report figures, deck (`build_deck.js`) and script PDF (`make_script.py`); the narration lives in `narration.json` |

## Datasets

- `data/ddr4_contract_price.csv`: DDR4 8Gb monthly contract price, Jan 2022 to Sep 2026 (DRAMeXchange, compiled by Silicon Analysts)
- `data/hyperscaler_capex_quarterly.csv`: quarterly capex of Microsoft, Amazon, Alphabet, Meta and Oracle, 2022 to 2025 (Epoch AI, from SEC filings)
- `data/skhynix_operating_profit.csv`: SK hynix quarterly operating profit, 4Q22 to 2Q26 (company results releases)

## Recording the video

1. Open `RAM_AI_Bubble.pptx`. On each clip slide, select the video, then Playback > Start: Automatically.
2. Slide Show > Record. The speaker notes show the script in presenter view.
3. File > Export > Create a Video (1080p). Keep it under 6:00.
