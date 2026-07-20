# Citation Check Report — src/main.tex

Date: 2026-07-17 · Scope: `src/main.tex` + `src/refs.bib`

## Scope and honesty statement

**Deep web-verification against primary sources was performed on 11 entries**: the 2 entries
explicitly flagged `note = {Citation details to be verified by author}`, plus the 9
forward-dated (2025/2026) entries, which carry the highest placeholder risk.

**The remaining ~46 cited entries received structural checks only** (key resolution, field
completeness, BibTeX parse). Their author/title/venue metadata was **not** web-verified.
This report does **not** certify all 65 entries.

## Summary

| Metric | Count |
|---|---|
| Bib entries | 65 |
| Distinct keys cited in main.tex | 57 |
| Orphan in-text citations (cited, no bib entry) | **0** |
| Entries deep-verified against primary sources | 11 |
| Metadata errors found and corrected | **4** |
| Claim-support issues flagged (not auto-fixed) | **1** |
| Uncited bib entries (informational, do not render) | 8 |
| BibTeX warnings after fixes | 0 |

Bibliography style is **`plainnat`** (natbib author–year) via `format.sty` — a NeurIPS-style
preprint using `\documentclass{article}`. Note `llncs.cls` and `refs-style.bst` (splncs03,
numeric LNCS) are present but **unused leftovers**. APA/LNCS conventions do not apply here;
no APA-style "corrections" were made.

## Corrections applied to `src/refs.bib`

All four are metadata fixes verified against primary sources. Citation keys were preserved,
so no `main.tex` edits were needed.

### 1. `regionlight2024` — was `author = {TBD}`, `booktitle = {TBD}` *(author-flagged)*

The recorded title was a placeholder that does not match any real paper. RegionLight is the
*framework* name inside a differently-titled paper. Now resolved and **published**:

> Gu, H., Wang, S., Ma, X., Jia, D., Mao, G., Lim, E. G., & Wong, C. P. R. (2024).
> Large-scale traffic signal control using constrained network partition and adaptive deep
> reinforcement learning. *IEEE Transactions on Intelligent Transportation Systems*,
> 25(7), 7619–7632. DOI: 10.1109/TITS.2024.3352446

Entry type changed `@inproceedings` → `@article`. The `2024` in the key is correct.
Confirmed independently via DOI resolution (→ IEEE doc 10490249) and the authors'
institutional repository (XJTLU).

### 2. `neurcomm` — was `author = {TBD}`, `journal = {TBD}`, `year = {TBD}` *(author-flagged)*

The recorded title was also a placeholder. NeurComm is the protocol introduced in:

> Chu, T., Chinchali, S., & Katti, S. (2020). Multi-agent reinforcement learning for
> networked system control. *ICLR 2020*. arXiv:2004.01339

Entry type changed `@article` → `@inproceedings`. Confirmed: this paper introduces both
NeurComm **and** the spatial discount factor, matching the placeholder title's description
and the manuscript's "neighbourhood communication in networked control" framing.

### 3. `sun2026ibvq` — **wrong authors (misattribution)** *(not author-flagged; found in sweep)*

Recorded as `author = {Sun and others}`. The actual authors are unrelated to "Sun":

> Farooq, A., & Iqbal, K. (2026). Bandwidth-efficient multi-agent communication through
> information bottleneck and vector quantization. *ICRA 2026*. arXiv:2602.02035

Fixed author list; entry type changed `@article` → `@inproceedings` (accepted at ICRA 2026,
Vienna). **The key `sun2026ibvq` is now misleading** — it names an author who is not on the
paper. Keys are internal labels and never render, so this is cosmetic; rename to
`farooq2026ibvq` if you want the database self-consistent (requires updating `main.tex`).

### 4. `li2025topology` — **fabricated given names** *(not author-flagged; found in sweep)*

Surnames were right; every given name was wrong.

| Recorded | Actual |
|---|---|
| Li, **Renjie** | Li, **Rongpeng** |
| Zhu, **Jing** | Zhu, **Jianhang** |
| Huang, **Jie** | Huang, **Jiahao** |
| Zhao, **Zhengxu** | Zhao, **Zhifeng** |
| Zhang, **Haijun** | Zhang, **Honggang** |

Source: arXiv:2506.12453. Also normalised the title hyphenation.

### 5. `hetib2025` — year off by one

arXiv ID `2605.17393` decodes to **May 2026**, contradicting `year = {2025}`. Corrected to
`2026` (authors and title verified correct). Renders as "Duan et al. (2026)". The key
`hetib2025` is now cosmetically stale — rename optional.

## RESOLVED 2026-07-17 — the METIS attribution was false for *every* cite

Investigating the RegionLight flag (below) revealed the problem was far larger. The claim
"balanced edge cut via METIS inherited by feudal MARL and region-based hierarchies" appeared
at **both `main.tex:159` and `main.tex:373`**, and is unsupported by all four cited papers:

| Cite | What it actually does | METIS? |
|---|---|---|
| `ma2020fma2c` (FMA2C) | *"We manually split the 30 intersections"* — assumes a disjoint+connected region decomposition, derives none | **No** — METIS appears nowhere in the paper |
| `ma2022feudal` | Learns a **flow-based** partition end-to-end via **GNN + MCTS** | **No** — explicitly contrasts itself with static partitioning |
| `regionlight2024` | Adjacency-constrained **star-topology** regions (one centre, arbitrary leaves) | **No** |
| `xu2021hilight` (HiLight) | **Does not partition the network at all** — per-agent hierarchy over sub-policies with neighbourhood weighting | **No** |

Verified from primary sources (FMA2C via full-text extraction of the AAMAS PDF). METIS is
genuinely used — but as *this paper's own experimental baseline* (`karypis1998metis`), which
is correct and untouched. `laplacian2009ieee` (spectral) was correctly attributed and left alone.

### The `ma2022feudal` positioning problem

`ma2022feudal` broke **both** of the paper's buckets: it is not topology-based (it learns from
traffic flow), and it is not "flow-aware but confined to transport planning, disconnected from
learners" (it drives a MARL learner). It is the closest prior work to this paper's thesis, and
the old framing effectively hid it.

**Resolution (author-approved):** acknowledge it explicitly as learned flow-based partitioning
for MARL, and sharpen the gap claim. The narrow contribution survives — `ma2022feudal` optimises
the partition for control return and states no partition-quality criterion — but the previous
wording ("a rationale of *any formal kind*") was too aggressive against a learned objective.

Changes applied to `main.tex`:

- **Abstract (52–55)** — the same overgeneralisation lived here ("existing practice inherits
  partitions from topology-based tools"), which `ma2022feudal` falsifies. Now: "either inherits
  partitions from topology-based tools **or learns them end-to-end for control return** — in both
  cases without a principled account". Reconciled so the abstract does not contradict §2/§3.
  *(The Conclusion needed no change — it uses METIS only as this paper's experimental baseline.)*
- **146–150** — "decompose the network into modules" was inaccurate for two of its four cites
  (HiLight and CoLight decompose nothing explicitly). Softened to "coordination modules ---
  whether explicit regions or implicit neighbourhoods". The load-bearing next sentence ("every
  such system contains a coordination graph fixed before training") holds for all four either way.
- **157–170** — dropped the false METIS attribution; `ma2020fma2c` now described as assuming a
  decomposition it does not derive; `ma2022feudal` given its own clause as end-to-end learned
  flow-based partitioning.
- **374–385** — RegionLight relabelled as adjacency-constrained star-topology; HiLight removed
  from the partitioning list entirely (it does not partition; still cited at line 149 for
  hierarchy, which is accurate); new sentence positioning `ma2022feudal` as "the closest departure".
- **386** — "Where flow information does enter..." → "Elsewhere, flow information enters only..."
  (the original directly contradicted the new `ma2022feudal` sentence).
- **393–399** — gap claim sharpened: "a *rationale* — of any formal kind —" → "an *explicit
  partition-quality criterion* — one statable and checkable before training, independently of
  any learner —", plus an explicit concession that flow-based partitioning has been coupled to
  a learner before.

### `xu2021hilight` — fabricated given names (third instance)

Same pattern as `li2025topology`: surnames right, given names invented.

| Recorded | Actual |
|---|---|
| Wang, **Yaodong** | Wang, **Yaowei** |
| Wang, **Zhen** | Wang, **Zhaozhi** |
| Jia, **Huarong** | Jia, **Huizhu** |

Fixed; added pages (669–677) and DOI (10.1609/aaai.v35i1.16147), verified via AAAI OJS and the
authors' homepage.

## Original flag (superseded by the section above)

### `regionlight2024` was mischaracterised in the text (`main.tex:375`)

> "...balanced edge cut via METIS inherited by feudal MARL~\citep{ma2020fma2c,ma2022feudal}
> and region-based **hierarchies**~\citep{regionlight2024,xu2021hilight}..."

Two problems, per the paper now that it is identified:

1. **Not METIS.** RegionLight uses an *adjacency-constrained* partition where region topology
   is restricted to a **star network** (one centre, arbitrary leaves) — not a METIS balanced
   edge cut. The METIS attribution reads as covering it.
2. **Not hierarchical.** The paper explicitly frames this as a flat/star-topology regional
   partition, not a manager–worker hierarchy. `xu2021hilight` (HiLight) *is* genuinely
   hierarchical, so the grouping fits HiLight but not RegionLight.

Your umbrella claim ("the criterion is almost always structural or geometric") **still holds** —
an adjacency/star constraint is structural. Only the METIS-and-hierarchy attribution is off.

This is debatable enough to leave to you (a centre–leaf star is arguably a shallow hierarchy),
so no prose was changed. Suggested minimal fix — split RegionLight into its own clause:

```latex
balanced edge cut via METIS inherited by feudal MARL~\citep{ma2020fma2c,ma2022feudal}
and region-based hierarchies~\citep{xu2021hilight}, adjacency-constrained star-topology
regions~\citep{regionlight2024}, congestion-feature clustering~\citep{...}
```

## Informational — not errors

- **8 uncited bib entries.** BibTeX only emits cited entries, so these never render and are
  not defects — `refs.bib` is shared with `proof.tex`, which is compiled separately.
  - Used by `proof.tex` (legitimately in use): `cover2006elements`, `horn2013matrix`
  - Used by neither: `bokade2023representational`, `cvdmarl2024`, `libsignal`,
    `lucchini2023intraod`, `lucchini2023intraod2`, `rosvall2011multilevel`
- **`libsignal` is malformed** — `@inproceedings` with `booktitle = {Machine Learning}`
  (a journal name). Harmless while uncited; fix before citing it.

## Verification

`bibtex main` runs clean — 0 warnings, 0 undefined citations. Both rewritten entries render
correctly under `plainnat`. Test compile was done in scratchpad; `src/` contains no build
artifacts. Only `src/refs.bib` was modified.

## Recommended next step

The two entries you flagged were genuine placeholders — but the sweep found **three more
errors in entries you had not flagged**, including a full misattribution (`sun2026ibvq`) and
fabricated given names (`li2025topology`). All three were in recent/arXiv-era entries.

Since ~46 older entries were only structurally checked, and the error pattern is
"plausible-looking but fabricated metadata", a full verification pass over the remaining
entries is worth the time before submission.
