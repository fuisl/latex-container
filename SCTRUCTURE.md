## Front matter

- Title Page
- Declaration
- Acknowledgements
- Abstract
- Kurzfassung / German Abstract
- Table of Contents
- List of Figures
- List of Tables
- List of Abbreviations

## 1. Introduction

1.1 Background and Motivation

background of problem, tsc

traffic jam, smart traffic employed.

global motivation (general challenges - paper) + personal motivation

**1.2** Problem Statement

low delay, fair, communication (link from background → current work)

1.3 Research Objectives (key contributions)

study current approaches

study feature representation (MLP / FRAP)

study agent communication (spatio-temporal/spatio dependencies)

study RL optimization schemes

optimize fairness in tsc.

1.4 Research Questions / Hypotheses

**RQ1: How does the proposed graph-aware multi-agent SAC framework perform compared with classical traffic-control methods and deep RL baselines across German RESCO traffic scenarios?**

**RQ2: What is the effect of local encoder design and graph-attention communication on traffic signal control performance and training stability?**

**RQ3: How does the proposed framework behave across traffic networks of different sizes and topologies, such as Cologne and Ingolstadt scenarios with varying numbers of intersections?**

**(optional) RQ4: To what extent can the learned multi-agent control behavior be interpreted as decentralized self-organization that produces network-level coordination?**

## H1

- Graph-aware communication improves coordination between neighboring intersections compared with independent-agent methods.

## H2

- Entropy-regularized SAC improves training stability compared with purely value-based methods in selected multi-agent traffic scenarios.

<aside>

Be careful: SAC may not always be better. Phrase this as an investigation, not as guaranteed truth.

</aside>

## H3

- Phase-aware local encoders such as FRAP do not necessarily improve performance in all German RESCO scenarios because their assumptions about phase competition and movement representation may not align equally well with every network topology.

<aside>

This is excellent because it turns your weaker FRAP result into an analytical contribution.

</aside>

## H4

- Larger and more complex networks reveal stronger differences between independent and graph-aware methods than small single-intersection scenarios.

1.5 Scope and Limitations

scope:

control algo / analysis of algo / come up with new system (maybe)

limitation:

pedestrian

sumo env

no build scenarios (take as it is)

no build rl library (but explore frameworks resco → custom api → sumo rl (cityflow/libsignal), pytsc)

interfaces between rl, env and etc. is provided

1.6 Thesis Structure

## 2. Literature Review

*(Comparison of Prior Studies to make things cohesive)*

2.1 Existing TSC Approaches 

classical

RL

MARL

2.2 RL/MARL in general

model-free vs model-based

discrete action space (choose phase | decide next) vs continous action space ()

on-policy vs. off-policy

2.3 GraphML variants

2.3 Related works to key contributions (Fairness/Representation learning)

2.4 Research Gap + Positioning of This Thesis

## 3. Theoretical Background/Preliminary

2.1 Key Concepts/Problem formulation

MDP

POMDP

2.2 Technical Foundations

DP → RL (solve MDP problems)

Policy Gradient

Advantage Approximation (A2C)

Entropy Regulated Approximation (not yet SAC)

2.3 Traffic Control Theory

movement

phase

etc.

## 4. Methodology

4.1 Proposed Method / Architecture

observation space

action space

4.2 Data Preprocessing

graph topology + agent communication graph construction

4.3 Relevant Models / Algorithms / Frameworks

DQN
PPO
SAC

CoLight

FRAP

4.4 Rewards

- diff waiting time
- delay
- pressure

4.5 Individual Contribution (GNN/Fairness/Representation)

## 5. Experimental Design

5.1 Dataset / Materials / System Context

TapasKoln + InTAS

SUMO (TraCI interface)

5.2 Evaluation setup (device, number of episodes)
5.3 Evaluation Metrics (refer to RESCO, include formulas) + Training / Testing Procedure (eval every 5 episodes, 5 different seed and take average)

5.4 System Architecture

from input → sumo → traci → (rllib + torch + torch-geometric) → wandb SUMO→

## 6. Results and Discussion

6.1 Main Results

6.2 Comparison with Baselines

6.3 Interpretation of Results

6.4 Answering the Research Questions

6.5 Limitations

6.6 Ablation

## 7. Conclusion and Future Work

7.1 Summary

7.2 Contributions

7.3 Future Research Directions

## Back matter

- References
- Appendices
    - Appendix A: Tools and Technologies: hydra, sumo, wandb
    - Appendix B: Loss and Objective of Network (bellman equation)
    

**QUESTIONS (WHERE TO PUT):**