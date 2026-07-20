# Citation Check Report — src/main.tex (full sweep)

Date: 2026-07-20 · Scope: `src/refs.bib` (all 65 entries as of the start of this
sweep) + `src/main.tex` (57 cited keys)

Supersedes `CITATION_CHECK_2026-07-17.md`, which deep-verified only 11 entries
(the 2 author-flagged placeholders + 9 forward-dated 2025/2026 entries) and
left ~46 older entries structurally-checked only. **This sweep closes that
gap**: every remaining entry was verified against a primary source (DOI
landing page, arXiv abstract page, publisher/conference page, or book
front-matter), in four parallel batches, with per-field found-vs-recorded
values recorded for audit.

## Format change since the last report

Between 2026-07-17 and this sweep, the manuscript switched from
`\documentclass{article}` + `format.sty` (NeurIPS-style preprint, `plainnat`
author-year) to `\documentclass[journal]{IEEEtran}` with
`\usepackage[numbers,sort&compress]{natbib}` and
`\bibliographystyle{IEEEtranN}` (IEEE numbered). `IEEEtranN.bst` is not
vendored in `src/` — it is supplied by the TeX Live distribution
(`texmf-dist/bibtex/bst/ieeetran/IEEEtranN.bst`), so this is not a missing-file
risk on a standard TeX Live install. Recompiled clean under the new style:
**0 BibTeX warnings, 0 undefined citations**, both before and after this
sweep's corrections.

## Summary

| Metric | Count |
|---|---|
| Bib entries at start of sweep | 65 |
| Bib entries after sweep (1 exact duplicate removed) | 64 |
| Distinct keys cited in `main.tex` | 57 |
| Orphan in-text citations (cited, no bib entry) | **0** |
| Orphan references (bib entry, never cited) | 7 (informational — see below) |
| Entries newly deep-verified against primary sources this sweep | 51 |
| **Fabricated author lists found this sweep** | **3** (`flowstability2022`, `stmarl2020`, `lucchini2023intraod`) |
| Other metadata errors found and corrected this sweep | 3 (`bokade2023representational` DOI, `liu2023gplight` pages, `mfdpartition2020` title) |
| Structural fix (wrong entry type/venue/year) | 1 (`libsignal`) |
| Duplicate-key entries removed | 1 (`lucchini2023intraod2`) |
| Entries confirmed fully correct as recorded | 44 |
| BibTeX warnings after fixes | 0 |

**Combined with the 2026-07-17 pass, every one of the 65 original entries has
now been deep-verified against a primary source at least once.**

## Corrections applied this sweep

### 1. `flowstability2022` — fabricated author list

Recorded `author = {Ghosh, Sayan and Schaub, Michael T. and Froyland, Gary and
Delvenne, Jean-Charles}`. Independently confirmed via the paper's arXiv listing
(arXiv:2101.06131) that the real authors are:

> Bovet, A., Delvenne, J.-C., & Lambiotte, R. (2022). Flow stability for
> dynamic community detection. *Science Advances*, 8(19), eabj3063.
> DOI: 10.1126/sciadv.abj3063

Title, venue, year, volume/issue/pages, and DOI were all already correct —
only the author field was wrong, and none of the three fabricated names
(Ghosh, Schaub, Froyland) appear on the real paper at all. Fixed.

### 2. `stmarl2020` — fabricated author list

Recorded `author = {Wang, Tianyu and Cao, Junfei and Hussain, Azhar}`.
Independently confirmed via arXiv:1908.10577 that the real authors are:

> Wang, Y., Xu, T., Niu, X., Tan, C., Chen, E., & Xiong, H. (2022). STMARL: A
> spatio-temporal multi-agent reinforcement learning approach for cooperative
> traffic light control. *IEEE Transactions on Mobile Computing*, 21(6),
> 2228–2242. DOI: 10.1109/TMC.2020.3033782

Only "Wang" survives from the recorded list; 5 of the real 6 authors were
missing entirely, and "Cao, Junfei" / "Hussain, Azhar" do not appear on this
paper. Title, venue, year, and DOI were correct. Fixed.

### 3. `lucchini2023intraod` (+ duplicate `lucchini2023intraod2`) — fabricated author list on an uncited entry

Recorded `author = {Lucchini, Luca and Gauvin, Laetitia and Cattuto, Ciro and
Panisson, André}`. Independently confirmed via arXiv:2309.12691 that the real
authors are:

> Chen, X.-J., Zhao, Y., Kang, C., Xing, X., Dong, Q., & Liu, Y. (2023).
> Characterizing the temporally stable structure of community evolution in
> intra-urban origin-destination networks. arXiv:2309.12691.

None of the four recorded names appear on the real paper. Title, arXiv ID,
and year were correct — only authorship was invented. This entry is **uncited**
in `main.tex` (informational only, shared with no other compiled document),
so it has zero effect on the rendered manuscript, but it is still fabricated
metadata sitting in the project's bibliography. Fixed the surviving key
(`lucchini2023intraod`) and **deleted `lucchini2023intraod2`**, which was a
byte-identical duplicate of the same fabricated entry under a second key.

### 4. `bokade2023representational` — fabricated given names + wrong DOI

| Field | Recorded | Actual |
|---|---|---|
| Author 1 | Bokade, **Rushikesh** | Bokade, **Rohit** |
| Author 2 | Jin, **Xueru** | Jin, **Xiaoning** |
| DOI | 10.1109/ACCESS.2023.3275**000** | 10.1109/ACCESS.2023.3275**883** |

Surnames, title, venue, year all correct — the given-name-fabrication pattern
from the 2026-07-17 report (`li2025topology`, `xu2021hilight`) recurs here.
Confirmed via arXiv:2310.02435 and dblp. Fixed.

### 5. `liu2023gplight` — wrong pages

Recorded `pages = {201--209}`; the IJCAI-23 proceedings page gives
`199--207`. Also added the official DOI `10.24963/ijcai.2023/23`, which was
previously absent. Fixed.

### 6. `mfdpartition2020` — truncated title

Recorded title dropped the paper's actual subtitle and abbreviated a term.
Corrected from "Traffic network partitioning for hierarchical MFD
applications" to the full real title: "Traffic network partitioning for
hierarchical macroscopic fundamental diagram applications based on fusion of
GPS probe and loop detector data" (confirmed via arXiv:2011.09075). Fixed.

### 7. `libsignal` — wrong entry type, wrong title, wrong year

| Field | Recorded | Actual |
|---|---|---|
| Entry type | `@inproceedings`, `booktitle={Machine Learning}` | `@article` — *Machine Learning* is a Springer **journal**, not a conference |
| Title | "LibSignal: Library for reinforcement learning-based traffic signal control" | "LibSignal: An Open Library for Traffic Signal Control" |
| Year | 2023 | 2024 (journal print date; arXiv preprint was 2022, workshop version 2022, journal version *Machine Learning* 113(8):5235–5271, 2024) |
| DOI | none | 10.1007/s10994-023-06412-y |

Authors (Mei, Lei, Da, Shi, Wei) were already correct. Fixed; converted to
`@article` with the correct venue metadata, retaining the arXiv URL as a
secondary link.

## Confirmed correct — no action needed (44 entries)

All of the following were checked field-by-field against a primary source and
matched exactly: `rosvall2008maps`, `rosvall2009mapequation`,
`rosvall2011multilevel`, `delvenne2010stability`, `lambiotte2014multiscale`,
`rosvall2014memory`, `newmangirvan2004`, `traag2019leiden`, `traag2011cpm`,
`evans1999percolation`, `shimalik2000`, `benjamini1995fdr`, `qu2022scalable`,
`qu2020average`, `congeduti2021iba`, `wei2019colight`, `jiang2018atoc`,
`wang2020imac`, `aamas2021correlated`, `peng2020structured`, `i2c2021`,
`nair2005ndpomdp`, `oliehoek2012ndpomdp`, `kok2006ndpomdp`, `daganzo1994ctm`,
`jin2012linkqueue`, `tassiulas1992stability`, `varaiya2013maxpressure`,
`laplacian2009ieee`, `odflow2019partition`, `communitydetection2021plosone`,
`cvdmarl2024`, `agarwal2021rliable`, `henderson2018matters`,
`abnar2020rollout`, `simonyan2013saliency`, `sundararajan2017axiomatic`,
`yu2023lowentropymarl`, `kraskov2004ksg`, `karypis1998metis`,
`polyanskiy2017sdpi`, `cover2006elements`, `horn2013matrix`.

Two cosmetic-only notes, no field change made:
- `peng2020structured` and `i2c2021` have citekeys that don't match their own
  `year` field (e.g. `i2c2021` has `year={2020}`) — a naming artifact from
  when the keys were assigned, not a metadata error. The recorded
  bibliographic data itself is correct. Renaming the keys is optional and
  would require corresponding edits in `main.tex`.
- `laplacian2009ieee`'s recorded venue string ("IEEE Intelligent
  Transportation Systems Conference (ITSC)") is a standard abbreviation of the
  formal name ("2009 12th International IEEE Conference on Intelligent
  Transportation Systems"), not an error.

## Informational — uncited entries (do not render)

After removing the `lucchini2023intraod2` duplicate, 7 bib entries remain
uncited by `main.tex` (BibTeX only emits cited entries, so these have zero
effect on the compiled manuscript):

- Used by `proof.tex` (legitimately in use, compiled separately):
  `cover2006elements`, `horn2013matrix`
- Used by neither document: `bokade2023representational`, `cvdmarl2024`,
  `libsignal`, `lucchini2023intraod`, `rosvall2011multilevel`

All were still verified/fixed above regardless of citation status, since the
brief was to check every reference in the project, not just the ones that
render.

## Verification

Test-compiled in scratchpad (never in `src/`, per project convention):
`bibtex main` under `IEEEtranN` — **0 warnings**, 0 undefined citations,
before and after this sweep's fixes. Only `src/refs.bib` was modified (7
entries corrected, 1 duplicate removed; 65 → 64 total entries). No changes to
`src/main.tex` were needed — all fixes were metadata-only and none of the
corrected keys' in-text citation commands needed to change.

## Claim-support flag (not a metadata error — needs author judgment)

### `stmarl2020` may not support the claim at `main.tex:625`

> "Spatial MI dominance in TSC networks is established by~\citet{stmarl2020},
> and its mechanistic link to spill-back is established
> by~\citet{dependencydyn2025}, grounding $D^{\mathrm{MI}}$ as the natural
> physical dependency measure."

STMARL (Wang et al. 2022, the corrected author list above) is a
spatio-temporal MARL **method** paper: it builds a spatial adjacency graph
over intersections, folds in history via an RNN, and coordinates decisions
via a GNN + distributed deep Q-learning. A full-text search of the paper
(arXiv:1908.10577) turned up **no mention of "mutual information"** or any
information-theoretic dependency measure anywhere in the text. The paper
does not appear to "establish spatial MI dominance" in any sense — it
doesn't measure MI at all.

This is the same *failure category* as the 2026-07-17 METIS finding: a
correct, real citation attached to a claim the cited paper doesn't actually
support. Same location also appears at `main.tex:426` ("Spatio-temporal
mutual information between intersections is established for
TSC~\citep{stmarl2020}").

This is flagged, not auto-corrected — deciding the right citation for "MI
dominance is empirically established in TSC" (or softening the claim to what
STMARL actually shows — spatial+temporal graph structure helps coordination,
not an MI measurement) is a judgment call for the author, not a mechanical
fix. Recommend either finding a paper that actually measures MI between
intersections, or rewording lines 426 and 625 to claim what STMARL actually
supports (graph-structured spatio-temporal correlation, not MI specifically).

## Bottom line

Across the two sweeps (2026-07-17 + 2026-07-20), **6 of 65 original entries
had fabricated author lists** (`sun2026ibvq`, `li2025topology`, `xu2021hilight`,
`flowstability2022`, `stmarl2020`, `lucchini2023intraod`), 2 had fabricated
titles (`regionlight2024`, `neurcomm`), 1 had a wrong year
(`hetib2025`), and 3 more had smaller metadata errors (wrong DOI, wrong pages,
truncated title). That is 12 of 65 entries (18%) with a real error, none of
which BibTeX or a casual read would catch — every one compiled clean and
looked plausible. All 65 original entries have now been resolved against
primary sources; the bibliography is at 64 entries (one exact duplicate
removed) with 0 known remaining metadata errors. The two corrected/added
DOIs (`bokade2023representational`, `liu2023gplight`) were independently
re-resolved via CrossRef/IJCAI after the fix and both land on the exact
right paper.

One claim-support issue remains open for the author to resolve: see
"Claim-support flag" above — `stmarl2020` is cited at `main.tex:426,625` for
an MI-dominance claim its full text does not appear to support.
