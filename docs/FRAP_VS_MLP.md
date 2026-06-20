Great question. Let me search for theoretical and empirical reasoning on this.Good — I now have enough to give you a solid, well-structured answer. Let me synthesize this into clear reasoning with supporting evidence.

This is a really interesting empirical finding. Here's a structured breakdown of **why MLP might outperform FRAP as an encoder**, drawing from multiple angles of evidence and reasoning:

---

## 1. FRAP's inductive bias may be too rigid for your task

FRAP's core design is built around **pairwise phase competition with a fixed conflict graph structure** — it uses 1×1 convolutions over a pre-defined phase-pair cube, guided by a hardcoded competition mask. This is a strong, hand-crafted inductive bias.

The key insight from **"Relational Inductive Biases, Deep Learning, and Graph Networks"** (Battaglia et al., 2018) is that inductive biases are only helpful when they align with the true structure of the problem. Inductive bias can be treated as initial beliefs about the model and the data properties. Right initial beliefs lead to better generalization with less data. **Wrong beliefs may constrain a model too much and will ultimately prevent one from finding a good optimum, even with tons of data.**

If the phase conflict structure in your environment doesn't cleanly map to what FRAP assumes (e.g., unbalanced phases, unusual intersection topologies, irregular lane counts), the hardcoded structure becomes a constraint rather than a help.

---

## 2. The parallel with Rendle et al. (2005.09683) — now it makes sense

This is almost certainly why you saved that paper. The exact same argument applies here:

While an MLP can in theory approximate any function, it is non-trivial to learn a dot product with an MLP. MLPs are too costly to use for item recommendation in production environments while dot products allow application of very efficient retrieval algorithms.

The flip side of Rendle's paper is just as important: **FRAP's structured competition encoding is analogous to a manually designed similarity function.** Just as Rendle showed that a simple dot product (not the fancier MLP-based NCF) often wins, your result suggests that a simple MLP encoder (not the fancier FRAP structure) can win — because **FRAP's phase-competition structure imposes a specific relational prior that the data may not actually need**.

---

## 3. "Expressiveness vs. generalization" tradeoff in structured encoders

From GNN theory: Moderately expressive models achieve the lowest test error, while the most expressive ones overfit, and performance deteriorates on unseen graphs. A more plausible explanation is that generalization requires a balance between the model's inductive bias (in its expressivity) and the structure–label correlation present in the data.

FRAP is a *more structured* encoder than a plain MLP. More structure means more assumptions. If those assumptions don't hold in your data distribution, the MLP's flexibility (as a universal approximator) lets it find better representations.

---

## 4. GNN/structured encoders can over-rely on structure when it's not informative

GNNs may over-rely on structure even when it's irrelevant, while structure-agnostic models like DeepSets often generalize well.

FRAP enforces pairwise phase relationships through convolution over the conflict cube. If your traffic patterns don't conform to the binary conflict assumptions (e.g., movements that are technically non-conflicting but still interfere dynamically due to queue spillback, or heterogeneous intersection geometry), the model is **forced to route information through a structure that doesn't match reality**.

---

## 5. MLP's universal approximation is practically effective when data is sufficient

Some graph-augmented MLP models outperform GNNs despite the former's less expressive power in a number of node classification problems, where MLPs use only information from each node to compute feature embeddings of nodes. This fact results in a contradiction between our intuitive understanding of expressive power.

A plain MLP over your flattened intersection state features can learn arbitrary nonlinear encodings **without being constrained to route through the phase-pair geometry**. Given enough training data and the right features (e.g., pressure, demand, queue length), it simply learns a better policy-relevant representation.

---

## 6. FRAP's architecture also adds unnecessary complexity/parameters

From the TinyLight analysis, FRAP has a fairly involved parameter structure: separate embeddings for phase, vehicle count, lane-link, and relationship, then 1×1 convolutions for pair competition and competition masking. FRAP aims to improve transportation efficiency with phase competition — comparing phases in pairs and giving priority to the one with larger traffic movement, making the model invariant to symmetric operations such as flipping and rotation.

If your problem setting already provides a good enough state representation (e.g., Advanced Pressure or demand-based features from Advanced-XLight), the invariance properties FRAP was designed to provide become redundant — you've already removed the need for them at the *feature level*, so encoding through FRAP's structure adds overhead without benefit.

---

## Summary of reasoning for your paper

| Reason | Source |
|---|---|
| FRAP's hardcoded conflict graph is a wrong-prior inductive bias for your data | Battaglia et al. 2018 |
| Structured encoders generalize worse when structure doesn't match data | Graph representational learning theory |
| Simple encoders (MLP) beat specialized ones when the specialization assumption is wrong | Rendle et al. 2020 (your 2005.09683!) |
| FRAP over-relies on phase conflict structure that may not be informative | GNN over-reliance on structure literature |
| MLP universal approximation is sufficient when features are already well-designed | Graph-agnostic MLP literature |

The **key claim** you can make in your paper: *FRAP's value was in providing rotation/flip invariance and sample efficiency in early TSC work where raw state representations were poor. With better-designed state features (e.g., pressure + demand), this structural prior becomes redundant or harmful — a plain MLP encoder learns a more flexible, data-driven representation.*