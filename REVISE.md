In MARL, “dependency between agents” means: does agent i’s action, state, observation, message, or reward meaningfully affect agent j, or the team outcome? There is no single universal metric. People measure it in several ways depending on what kind of dependency they care about.

1. Main ways people measure agent dependency

1. Transition / dynamics dependency

This asks:

\text{Does } a_i^t \text{ affect } s_j^{t+1}, o_j^{t+1}, \text{ or } r_j^{t+1}?

A practical form is:

D_{i \rightarrow j}
=
\mathbb{E}
\left[
d\left(
P(o_j^{t+1} \mid s_t, a_i, a_{-i}),
P(o_j^{t+1} \mid s_t, a_i', a_{-i})
\right)
\right]

where d(\cdot,\cdot) could be KL divergence, total variation distance, or simply an empirical change in next observation/reward.

Interpretation: if changing agent i’s action changes what agent j observes next, then i causally influences j. Recent causal-influence MARL work often measures this using interventions and conditional mutual information.  

For traffic signal control, this would mean:

\text{Does intersection } i\text{'s phase choice affect queue/delay at neighbor }j?

That is a real physical dependency through vehicle spillback and flow propagation.

⸻

2. Reward dependency

This asks:

\text{How much of the global reward is caused by agent } i?

A classical method is the difference reward:

D_i(z) = G(z) - G(z_{-i} + c_i)

where:

* G(z) is the actual global team reward,
* z_{-i} + c_i means “replace agent i’s behavior with some default/counterfactual behavior,”
* D_i estimates agent i’s marginal contribution.

Difference rewards are explicitly designed to capture an agent’s contribution to system performance, especially when many agents act simultaneously and the raw global reward does not reveal who caused the outcome.  

In traffic:

D_i =
\text{Total network improvement}
-
\text{Network improvement if intersection }i\text{ used a default phase}

If this value is large, intersection i has strong credit/dependency.

⸻

3. Value-function dependency

This asks:

\text{Can the joint value be decomposed into individual agent values?}

If the team value is approximately additive:

Q_{\text{tot}}(s, \mathbf{a})
\approx
\sum_i Q_i(o_i, a_i)

then dependencies are weak or mostly separable. This is the idea behind VDN, which studies cooperative MARL with a single shared reward and decomposes the team value into agent-wise utilities.  

If the relation is not additive but still monotonic:

\frac{\partial Q_{\text{tot}}}{\partial Q_i} \geq 0

then methods like QMIX use a mixing network to combine individual utilities into a centralized joint value while preserving decentralized action selection.  

If dependencies are pairwise or local, people use coordination graphs:

Q_{\text{tot}}(\mathbf{a})
=
\sum_i Q_i(a_i)
+
\sum_{(i,j)\in E} Q_{ij}(a_i,a_j)

Here, an edge (i,j) means agents i and j are dependent. Deep Coordination Graphs explicitly factor the joint value function according to a coordination graph into pairwise payoffs.  

This is very related to your traffic-signal setting: if two intersections strongly exchange flow, they should probably be connected in the coordination graph.

⸻

4. Statistical dependency

People also use correlation-like metrics:

I(A_i; A_j), \quad I(O_i; O_j), \quad I(A_i; R_j), \quad I(\tau_i; \tau_j)

where I(\cdot;\cdot) is mutual information.

Examples:

I(a_i^t; r_j^{t+k})

means: does knowing agent i’s action reduce uncertainty about agent j’s future reward?

This is useful, but dangerous: mutual information measures association, not necessarily causation. Two agents may appear dependent simply because they both respond to the same global state.

For traffic, two far intersections may show correlated queues during rush hour, but that does not mean one causes the other. Causal or intervention-based tests are stronger.

⸻

5. Perturbation / ablation dependency

This is the most intuitive experimental method:

1. Run the trained MARL system normally.
2. Freeze or randomize agent i.
3. Measure how much the return of agent j or the whole team changes.

For example:

\Delta_{i \rightarrow j}
=
J_{\text{normal}}
-
J_{\text{agent }i\text{ perturbed}}

If removing or corrupting agent i’s policy causes large degradation, then agent i is important.

This is easy to explain in a paper because it is close to a causal question: what breaks if this agent stops behaving intelligently?

⸻

2. How dependency relates to credit assignment

Credit assignment asks:

Given a team reward, which agent/action deserves credit or blame?

Dependency measurement asks:

Which agents actually influence each other or the team outcome?

So dependency is almost the structural side of credit assignment.

Suppose the global reward is:

R = -\text{total waiting time of all vehicles}

All traffic lights receive the same reward. But if the reward improves, who caused it?

* Intersection A?
* Intersection B?
* Their combination?
* A downstream effect from 10 seconds ago?
* A neighbor preventing spillback?

That is the credit assignment problem.

Dependency tells you where credit can reasonably flow.

⸻

3. Low dependency vs high dependency

Case 1: weak dependency

If agents barely affect each other:

R \approx \sum_i R_i

then credit assignment is easy. You can use local rewards or independent learners.

Example: two intersections far apart with no vehicle flow between them.

In this case, global reward is unnecessary noise. Local reward may learn faster.

⸻

Case 2: sparse dependency

If each agent depends only on neighbors:

R_i \text{ depends on } \{i\} \cup \mathcal{N}(i)

then you should not use a fully global critic blindly. A factored critic, coordination graph, or local reward with neighbor shaping is more appropriate.

For traffic:

R_i = -(\text{waiting time at } i + \lambda \cdot \text{waiting time of downstream neighbors})

This gives credit to the agents that are physically coupled.

This is where graph-based MARL makes sense.

⸻

Case 3: strong global dependency

If every agent’s action can affect many others:

R \not\approx \sum_i R_i

then credit assignment is hard. You usually need centralized training, counterfactual baselines, value decomposition, or Shapley-style marginal contribution.

COMA is a classic example: it uses a centralized critic and a counterfactual baseline that holds other agents’ actions fixed while comparing what would happen if one agent changed its action. This directly addresses multi-agent credit assignment.  

Its agent-specific advantage is roughly:

A_i(s,\mathbf{a})
=
Q(s,\mathbf{a})
-
\sum_{a_i'} \pi_i(a_i' \mid o_i)Q(s,(a_i',a_{-i}))

Meaning:

How much better was agent i’s actual action compared with its average alternative actions, given what everyone else did?

That is credit assignment through counterfactual dependency.

⸻

4. Clean mental model

Think of MARL like this:

\textbf{Dependency graph} \rightarrow \textbf{credit assignment structure} \rightarrow \textbf{learning algorithm}

For example:

Dependency pattern	Credit assignment choice	Suitable MARL style
Almost independent agents	Local rewards	IQL, IPPO with local reward
Neighbor-only dependencies	Local/factored credit	Graph critic, coordination graph, reward shaping
Dense team dependency	Global counterfactual credit	COMA, MAPPO, centralized critic
Additive team value	Individual utility decomposition	VDN
Monotonic but non-additive value	Mixed credit through value mixer	QMIX
Unknown dependencies	Learn graph/attention	GNN critic, attention-based MARL

VDN and QMIX are especially important because they do not explicitly say “agent i gets reward r_i.” Instead, they learn a decomposition of the team value so that individual utilities can support decentralized decisions under a shared team objective.  

⸻

5. For your traffic-signal MARL case

A good dependency measure would be something like:

D_{i \rightarrow j}
=
I(a_i^t; W_j^{t+k} \mid s_t)

where:

* a_i^t: phase chosen by intersection i,
* W_j^{t+k}: future waiting time at intersection j,
* k: time lag for traffic to propagate,
* conditioning on s_t reduces fake correlation from shared rush-hour demand.

Even better, use a perturbation version:

D_{i \rightarrow j}
=
\mathbb{E}
[
W_j^{t+k} \mid do(a_i = a)
]
-
\mathbb{E}
[
W_j^{t+k} \mid do(a_i = a')
]

This says:

If I intervene on intersection i’s phase, how much does neighbor j’s future waiting time change?

Then credit assignment can follow that graph:

R_i =
-\left(
W_i
+
\lambda \sum_{j \in \mathcal{N}(i)} D_{i \rightarrow j} W_j
\right)

or the critic can condition only on the most dependent neighbors.

That is exactly the bridge:

\boxed{
\text{Measure dependency} \Rightarrow \text{know whose outcomes agent }i\text{ influences} \Rightarrow \text{assign credit more cleanly}
}

You can use Adjusted Mutual Information (AMI), but usually not as a direct replacement for mutual information when measuring MARL agent dependency.

The reason is subtle:

\textbf{MI measures statistical dependence between variables.}

\textbf{AMI measures similarity between two clusterings, adjusted for chance.}

So the question is: are you measuring dependency between agent variables, or similarity between partitions of agents?

⸻

1. What MI is doing in MARL

Suppose you measure:

I(a_i^t ; W_j^{t+k})

This asks:

Does knowing agent i’s action reduce uncertainty about agent j’s future waiting time?

Or more carefully:

I(a_i^t ; W_j^{t+k} \mid s_t)

This asks:

Given the current state, does agent i’s action still tell us something about agent j’s future outcome?

That is a dependency measure between random variables: actions, states, rewards, queues, observations, messages, etc.

This is why causal-influence MARL papers often use conditional mutual information or interventional variants to measure influence between agents. For example, situation-dependent causal influence methods define influence using conditional mutual information, often with intervention/counterfactual logic.  

⸻

2. What AMI is actually for

Adjusted Mutual Information is usually defined for two clusterings/partitions U and V:

AMI(U,V)
=
\frac{
MI(U,V) - \mathbb{E}[MI(U,V)]
}{
\text{normalizer} - \mathbb{E}[MI(U,V)]
}

The adjustment subtracts the expected MI between random clusterings, because raw MI tends to be higher when there are more clusters, even if the clustering agreement is mostly accidental. Scikit-learn describes AMI exactly this way: an adjustment of MI “to account for chance” in clustering comparison.   Vinh, Epps, and Bailey’s JMLR paper is one of the standard references for chance-adjusted information-theoretic clustering measures.  

So AMI answers:

Are these two partitions of the same samples similar beyond what random clusterings would produce?

That is different from:

Does agent i’s action influence agent j’s future outcome?

⸻

3. When AMI is useful in MARL

AMI is useful if your dependency question is about partitions or modules.

For example, suppose you have:

* Partition P_{\text{flow}}: groups of intersections discovered from OD flow / InfoMap.
* Partition P_{\text{dependency}}: groups discovered from learned influence, attention weights, Jacobian dependency, or causal influence.
* Partition P_{\text{topology}}: groups discovered from road adjacency / METIS.

Then AMI is very reasonable:

AMI(P_{\text{flow}}, P_{\text{dependency}})

This tells you whether your flow-based modules match your learned dependency modules beyond chance.

In your traffic MARL context, AMI would be good for saying:

“Does the partition produced by InfoMap align with the empirical agent-dependency partition better than a topology-based partition?”

That is a partition-quality question.

⸻

4. When AMI is not the right replacement

AMI is not ideal if you want an edge weight like:

D_{i \rightarrow j}

meaning:

How much does agent i affect agent j?

For that, MI or conditional MI is more natural:

D_{i \rightarrow j}
=
I(a_i^t ; o_j^{t+k} \mid s_t)

or:

D_{i \rightarrow j}
=
I(a_i^t ; r_j^{t+k} \mid s_t)

or even better, an interventional version:

D_{i \rightarrow j}
=
I(do(a_i^t); o_j^{t+k} \mid s_t)

AMI does not naturally give you a directed dependency edge. It gives you an adjusted similarity score between two label assignments.

⸻

5. The real issue: raw MI can be biased

Your instinct is correct: raw MI can be misleading.

MI can be inflated by:

* finite sample size,
* many discrete bins,
* high-dimensional variables,
* non-uniform state visitation,
* shared environmental causes,
* rush-hour-like common demand patterns,
* correlations caused by both agents reacting to the same state.

But AMI is only one kind of correction, and it is mainly designed for clustering.

For MARL dependency, better alternatives are usually:

Option A: Conditional MI

I(a_i ; y_j \mid s)

This removes dependency caused merely by shared state s.

Example:

I(a_i^t ; W_j^{t+k} \mid \text{current traffic demand})

This is stronger than plain MI because it asks whether i’s action adds information after accounting for the current situation.

⸻

Option B: Permutation-adjusted MI

This is closer to what you may want if your concern is chance correlation.

You can define:

I_{\text{adj}}(X;Y)
=
I(X;Y)
-
\mathbb{E}_{\pi}[I(X;Y_{\pi})]

where Y_{\pi} is a shuffled version of Y.

For agent dependency:

D_{i,j}
=
I(a_i^t ; W_j^{t+k})
-
\mathbb{E}_{\pi}
[
I(a_i^t ; W_{j,\pi}^{t+k})
]

This asks:

Is the dependency larger than what I would get if I destroyed the temporal/agent alignment?

This is very useful experimentally.

You can also normalize it:

\tilde{D}_{i,j}
=
\frac{
I(a_i^t ; W_j^{t+k}) - \mathbb{E}_{\pi}[I(a_i^t ; W_{j,\pi}^{t+k})]
}{
H(W_j^{t+k})
}

This gives a more comparable dependency score across agents.

⸻

Option C: Interventional / counterfactual influence

This is best when you care about credit assignment.

Instead of asking:

\text{Are } a_i \text{ and } W_j \text{ statistically related?}

ask:

\text{What happens to } W_j \text{ if I change } a_i?

For traffic:

D_{i \rightarrow j}
=
\mathbb{E}
[
W_j^{t+k} \mid do(a_i = \text{phase A})
]
-
\mathbb{E}
[
W_j^{t+k} \mid do(a_i = \text{phase B})
]

This is much closer to credit assignment, because credit is about causal contribution, not just correlation.

⸻

6. How this connects to credit assignment

Credit assignment asks:

Which agent/action should receive credit for the final reward?

If you use raw MI:

I(a_i ; R)

you may discover that agent i’s action is correlated with the return.

But that does not prove agent i caused the return. It may only be correlated because all agents respond to the same global traffic condition.

AMI helps only if you are comparing clusters of agents. It does not solve the causal credit problem by itself.

For credit assignment, you want something more like:

\text{credit}_i
=
Q(s, \mathbf{a})
-
Q(s, a_i', a_{-i})

This is the COMA-style counterfactual idea: compare the actual joint action with an alternative where only agent i’s action is changed.

So the hierarchy is:

\text{AMI} \rightarrow \text{good for comparing partitions}

\text{MI / CMI} \rightarrow \text{good for measuring statistical dependency}

\text{Counterfactual / interventional influence} \rightarrow \text{best for credit assignment}

⸻

7. Practical recommendation for your case

For traffic-signal MARL, I would not replace MI with AMI directly.

I would use this structure:

For edge-level dependency

Use conditional or adjusted-by-permutation MI:

D_{i \rightarrow j}
=
I(a_i^t ; W_j^{t+k} \mid s_t)

or:

D_{i \rightarrow j}
=
I(a_i^t ; W_j^{t+k})
-
\mathbb{E}_{\pi}[I(a_i^t ; W_{j,\pi}^{t+k})]

This gives you a weighted dependency graph.

For partition comparison

Use AMI:

AMI(P_{\text{InfoMap}}, P_{\text{empirical dependency}})

or:

AMI(P_{\text{METIS}}, P_{\text{empirical dependency}})

This tells you whether a partition preserves meaningful dependency structure better than chance.

For credit assignment

Use counterfactual dependency:

C_i
=
G(\mathbf{a})
-
G(a_i', a_{-i})

or a learned centralized critic approximation.

⸻

My opinion: AMI is a good evaluation metric for module alignment, but not a good primary dependency measure between MARL agents. For your paper, the clean framing would be:

\boxed{
\text{Use MI/CMI/Jacobian/counterfactuals to estimate dependencies.}
}

\boxed{
\text{Use AMI to compare the resulting dependency partition against InfoMap/METIS partitions.}
}

That separation is scientifically cleaner.

Verdict

Your direction is strong and publishable, but the claim must be reshaped.

The strongest defensible thesis is not:

“InfoMap is always better than classical partitioning, and our metric proves final MARL performance will be optimal.”

That is too strong. MARL performance depends on optimization noise, model capacity, seed variance, module size, reward design, and algorithm-specific failure modes.

The stronger and safer thesis is:

Flow-based partitioning minimizes a theoretically meaningful coordination-loss surrogate: the amount of traffic-induced dependency cut by module boundaries. This retained dependency can be measured by standardized retention metrics, and under locality assumptions it upper-bounds the approximation loss of regional MARL.

That is a much better paper.

Your own theory note is already pointing in the right direction: it says the old H1/H2 gate is fragile, while retention metrics such as \Phi and \Psi are more robust and should become the theoretical primitive.   Your current draft still presents H1/H2 as verified causal mechanisms in the abstract and method, which is risky if some evidence has failed or is underpowered.  

⸻

1. The main conceptual move: stop proving “InfoMap wins”; prove “InfoMap preserves the right dependency mass”

You should frame the paper around partition quality, not directly around final reward.

A partition \mathcal P is good when it keeps highly coupled agents inside the same region and cuts weakly coupled agents:

\Psi(\mathcal P, D)
=
\frac{
\sum_{k}\sum_{i,j\in P_k} D_{ij}
}{
\sum_{i,j}D_{ij}
}

where D_{ij} is an empirical dependency measure: mutual information, conditional MI, critic Jacobian, attention/Jacobian influence, or counterfactual influence.

Then your central argument becomes:

\text{InfoMap}
\Rightarrow
\text{high flow retention}
\Rightarrow
\text{high dependency retention}
\Rightarrow
\text{lower regional MARL approximation loss}

This is much more defensible than:

\text{InfoMap}
\Rightarrow
\text{always better MARL reward}

because final MARL reward is not purely structural; it is also an optimization outcome.

⸻

2. The proof chain you should build

Proposition 1 — Map equation implies flow retention

Define OD flow matrix:

W_{ij} \geq 0

and partition \mathcal P = \{P_1,\dots,P_K\}.

Define flow retention:

\Phi(\mathcal P,W)
=
\frac{
\sum_k\sum_{i,j\in P_k} W_{ij}
}{
\sum_{i,j}W_{ij}
}

Then:

1-\Phi(\mathcal P,W)
=
\frac{
\sum_{i,j:c(i)\neq c(j)}W_{ij}
}{
\sum_{i,j}W_{ij}
}

This is exactly the fraction of OD random-walk flow that crosses module boundaries.

The map equation is designed to compress random-walk flow by assigning reusable codebooks to modules; it favors partitions where a walker stays inside modules for longer periods. The recent Infomap review states that the map equation describes communities by analyzing dynamic processes on networks and uses the minimum description length principle to identify modules that best capture flow regularities.  

So your first theoretical result should be:

\boxed{
\text{InfoMap approximately maximizes entropy-regularized flow retention.}
}

Important caveat: Infomap is a heuristic search over an NP-hard community-detection landscape, so do not claim it always finds the global optimum. The Infomap review explicitly notes that Infomap uses greedy stochastic search and cannot guarantee the global map-equation minimum.  

⸻

Proposition 2 — Flow retention upper-bounds dependency loss

This is the heart of the paper.

You want a lemma like:

1-\Psi(\mathcal P,D)
\leq
\kappa\bigl(1-\Phi(\mathcal P,\widetilde W)\bigr)
+
\epsilon_{\text{confound}}

where:

* \Phi = retained OD flow,
* \Psi = retained dependency,
* \widetilde W = possibly symmetrized or lagged flow matrix,
* \kappa = traffic propagation constant,
* \epsilon_{\text{confound}} = dependency from common demand, global rush-hour effects, weather, route synchronization, etc.

This says:

If a partition cuts little vehicle flow, then under reasonable traffic dynamics it also cuts little dependency.

This is your theoretical bridge from traffic flow to MARL coordination dependency.

You do not need to prove it for full SUMO. Prove it under a stylized model: CTM, spatial queue, or link-queue dynamics. The claim should be conditional:

\text{Under flow-local traffic dynamics, dependency propagates along flow-carrying corridors.}

That is enough.

Then your empirical results estimate whether real SUMO behaves close enough to the stylized model.

⸻

Proposition 3 — Dependency retention bounds regional MARL value loss

This is where you connect to credit assignment.

A regional MARL method ignores cross-module influence. Therefore, the error is controlled by the amount of dependency cut by the partition:

J^\star - J_{\mathcal P}
\leq
C\bigl(1-\Psi(\mathcal P,D)\bigr)
+
\epsilon_{\text{approx}}
+
\epsilon_{\text{opt}}

where:

* J^\star = ideal global coordination performance,
* J_{\mathcal P} = regional MARL performance under partition \mathcal P,
* 1-\Psi = discarded dependency mass,
* \epsilon_{\text{approx}} = neural approximation error,
* \epsilon_{\text{opt}} = training/optimization error.

This is not fantasy; it is aligned with existing networked MARL theory. Qu et al. show that in networked MARL, when influence decays with graph distance, localized policies can approximate global policies while scaling with local neighborhood size rather than full state-action size.   Their earlier discounted setting similarly gives an O(\rho^\kappa)-style approximation under localized interaction assumptions.  

Influence-based abstraction also gives a clean theoretical connection: if a local subproblem approximates the influence of the rest of the system well, then value loss can be bounded; Congeduti et al. explicitly derive sufficient conditions for small value loss from approximate influence representations and show approximation error estimators correlate with value loss.  

So your contribution is not to invent value-loss theory from zero. Your contribution is to connect:

\text{OD flow}
\rightarrow
\text{partition}
\rightarrow
\text{retained dependency}
\rightarrow
\text{regional MARL approximation quality}

That is novel enough if executed cleanly.

⸻

3. What your contribution should become

I would write your contributions like this:

Contribution 1 — Flow-based regional MARL partitioning.
You apply InfoMap to OD-demand graphs to construct regional coordination modules for traffic-signal MARL across reward sharing, centralized critics, and graph attention.

Contribution 2 — Retention-based partition quality theory.
You derive a three-step theoretical chain showing that map-equation minimization preserves OD flow, OD-flow retention bounds dependency retention under traffic-local dynamics, and dependency retention bounds regional MARL approximation loss under networked MARL locality assumptions.

Contribution 3 — Standardized partition quality metrics.
You introduce \Phi, \Psi, and an adjusted/permutation-normalized \Psi_{\text{rel}} to evaluate partition quality independent of the MARL algorithm.

Contribution 4 — Empirical validation.
You show that \Psi predicts performance trends better than topology-only criteria across InfoMap, METIS, spectral, random, local, and global baselines.

Notice the wording: predicts performance trends, not guarantees optimal performance.

⸻

4. You need an adjusted metric, but not necessarily AMI

Your previous AMI idea is useful, but I would not make AMI the main metric.

Raw \Psi has a serious bias: large modules automatically retain more dependency. If one partition has fewer/larger modules, it may get a higher \Psi simply because it cuts less of everything.

So define an adjusted retention score:

\Psi_{\text{adj}}(\mathcal P,D)
=
\frac{
\Psi(\mathcal P,D)
-
\mathbb E_{\mathcal P'\sim \mathcal R(\mathcal P)}[\Psi(\mathcal P',D)]
}{
1-
\mathbb E_{\mathcal P'\sim \mathcal R(\mathcal P)}[\Psi(\mathcal P',D)]
}

where \mathcal R(\mathcal P) is a random partition distribution preserving:

* number of modules,
* module-size sequence,
* optionally spatial contiguity,
* optionally maximum module size.

This is the metric I would use.

It has the same spirit as adjusted mutual information, but it is tailored to your actual object: retained dependency mass, not clustering-label agreement.

Then your headline metric becomes:

\boxed{
\Psi_{\text{adj}}
=
\text{excess retained dependency beyond size-matched random partitions}
}

That is very clean.

⸻

5. Replace the failed H1/H2 gate with better tests

Your H1/H2 problem is not fatal. It means your earlier hypothesis was too microscopic.

Pairwise MI tests are noisy. Spillback events can be sparse. Your own note says H1 is marginal and H2 lacks usable events, while \Phi and \Psi are stronger.  

So change the epistemic structure.

Do not say:

\text{H2 must hold} \Rightarrow \text{H1 must hold} \Rightarrow \text{InfoMap is valid}

Instead say:

\text{Retention is the primitive. H1/H2 are mechanism signatures.}

Then replace pairwise tests with aggregate tests:

\sum_{i,j:c(i)=c(j)}D_{ij}
>
\mathbb E_{\text{random partition}}
\left[
\sum_{i,j:c'(i)=c'(j)}D_{ij}
\right]

This gives one strong partition-level statistic instead of hundreds of weak pairwise tests.

Use permutation testing:

1. Keep D fixed.
2. Randomize partitions with same module sizes.
3. Compute \Psi for each random partition.
4. Report percentile / p-value of InfoMap and METIS.

This is much more aligned with your theory.

⸻

6. Use conditional MI instead of plain MI

Plain MI can fail badly in traffic because of common demand.

For example, two far intersections may both become congested during rush hour. Then:

I(X_i;X_j)

is high, even if no vehicle flow connects them directly.

So use:

D^{\text{CMI}}_{ij}
=
I(X_i(t);X_j(t+\tau)\mid Z_t)

where Z_t could be:

* total network occupancy,
* total inflow,
* total waiting time,
* time-of-day bin,
* episode demand regime,
* region-level aggregate demand.

This removes fake dependency caused by global traffic intensity.

For your paper, this is important. If \Psi(D^{MI}) drops on a larger network, reviewers may say MI is just measuring shared rush-hour effects. Conditional MI directly answers that criticism.

Your dependency instruments should become:

D^{\text{flow}} = W

D^{\text{phys}} = I(X_i;X_j^+ \mid Z)

D^{Q}_{i\leftarrow j}
=
\left\|
\frac{\partial Q_i}{\partial X_j}
\right\|

D^{G}_{i\leftarrow j}
=
\left\|
\frac{\partial h_i^{(L)}}{\partial X_j}
\right\|

Then \Psi can be evaluated under each dependency instrument.

⸻

7. What not to claim

Avoid these claims:

1. “InfoMap is theoretically optimal for MARL.”
    Too strong. InfoMap optimizes compression of flow, not MARL return directly.
2. “High \Psi guarantees better performance.”
    Too strong. Optimization error can dominate.
3. “H1/H2 prove the causal mechanism.”
    Too risky, especially given your failed evidence.
4. “METIS is wrong.”
    Better: METIS optimizes a different object — topology cut balance — while InfoMap optimizes flow retention. In traffic-signal MARL, flow retention is often more aligned with coordination dependency.
5. “No resolution limit.”
    Be careful. Map equation is less affected by some resolution-limit problems than modularity, but it has field-of-view and over-partitioning issues in constrained/geographic networks. The Infomap review explicitly discusses field-of-view limitations and over-partitioning in transportation-like constrained networks.  

⸻

8. What you should do now

Step 1 — Rewrite the paper around retention

Change the paper’s causal chain from:

\text{spillback}
\Rightarrow
\text{MI}
\Rightarrow
\text{performance}

to:

\Phi
\Rightarrow
\Psi
\Rightarrow
J

H1/H2 become supporting diagnostics, not mandatory gates.

⸻

Step 2 — Add three formal statements

Add these as propositions/theorems:

Proposition 1.

1-\Phi(\mathcal P,W)

equals the OD random-walk inter-module transition rate.

Proposition 2.

Under flow-local traffic dynamics:

1-\Psi(\mathcal P,D)
\leq
\kappa(1-\Phi(\mathcal P,\widetilde W))
+
\epsilon_{\text{confound}}

Theorem 1.

Under networked MARL locality / approximate influence assumptions:

J^\star - J_{\mathcal P}
\leq
C(1-\Psi(\mathcal P,D))
+
\epsilon_{\text{approx}}
+
\epsilon_{\text{opt}}

This theorem can be mostly imported from networked MARL and influence-based abstraction theory, with your novelty being the construction of D, \Psi, and the flow-to-dependency bridge.

⸻

Step 3 — Create the adjusted metric

Report:

\Phi,\quad
\Psi,\quad
\Psi_{\text{adj}}

For every partition:

* InfoMap,
* METIS,
* spectral,
* random size-matched,
* local/singleton,
* global/all-in-one.

Without random/spectral baselines, reviewers may say InfoMap only beats one weak topology baseline.

⸻

Step 4 — Test whether \Psi predicts performance

Make a scatter plot:

x = \Psi_{\text{adj}}(\mathcal P,D)

y = -\text{waiting time}
\quad \text{or} \quad
\Delta J

Use all partition methods, all k, all seeds, and maybe all algorithms.

Fit a simple model:

J
=
\beta_0
+
\beta_1\Psi_{\text{adj}}
+
\beta_2 K
+
\beta_3 \max_k |P_k|
+
\beta_4 \text{algorithm}
+
\beta_5 \text{network}
+
\epsilon

The key question:

\beta_1 > 0?

If yes, your metric is useful.

⸻

Step 5 — Handle algorithm-specific anomalies honestly

Your draft has signs that CoLight behaves differently from IPPO/MAPPO. That is not necessarily a weakness.

It may mean:

* L1 reward sharing benefits from flow-coherent outcome correlation.
* L2 regional critics benefit from reducing irrelevant global input.
* L3 graph attention can fail if modules become smaller than the influence radius needed for message passing.

So you can present a nuanced theory:

\text{Too-large modules}
\Rightarrow
\text{high computation/noise}

\text{Too-small modules}
\Rightarrow
\text{cut needed influence}

Optimal partitioning is therefore a tradeoff:

\text{quality}(\mathcal P)
=
\Psi_{\text{adj}}(\mathcal P,D)
-
\lambda\cdot \text{cost}(\mathcal P)

where cost could be:

\text{cost}(\mathcal P)
=
\sum_k |P_k|^2
\quad \text{or} \quad
\max_k |P_k|

This gives you a more mature metric:

\Omega(\mathcal P,D)
=
\Psi_{\text{adj}}(\mathcal P,D)
-
\lambda\frac{\sum_k |P_k|^2}{N^2}

That measures retention under tractability constraint.

⸻

9. My recommendation for your final thesis

I would title the theoretical contribution something like:

Dependency Retention as a Partition Quality Principle for Regional MARL in Traffic Signal Control

And the core claim:

We show that OD-flow partitions are theoretically meaningful because the map equation minimizes an entropy-regularized boundary-flow objective; under flow-local traffic dynamics, boundary flow upper-bounds boundary dependency; and under networked MARL locality assumptions, boundary dependency controls the approximation loss of regional coordination.

This is strong, precise, and defendable.

Your paper becomes less about “InfoMap is a magic better partitioner” and more about:

What should a traffic MARL partition preserve?
It should preserve dependency.
How can we estimate dependency before training?
Use OD flow as a training-free surrogate.
How do we evaluate partitions consistently?
Use \Psi and \Psi_{\text{adj}}.
Why does this matter for MARL?
Because credit assignment and regional critics fail when high-influence dependencies are cut.

That is a real contribution.