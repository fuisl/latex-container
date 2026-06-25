## Scope

The current proposal contains several potential gaps and expected contributions. 
This work span around:
- spatio partitioning
- sample efficiency  
- attention range
- information bottleneck
- coordination graph
- transferability
- spillback containment
- etc.
  
Although all the points above are valid, combining too many objectives makes the study broad rather than deep, making it difficult to clearly demonstrate the novel contribution and provide in-depth analysis for each component.


Try to break down into 2-3 works in sequence, we can target them one-by-one. Target 2-3 contributions for each work, it is sufficient. 

## Narrative
Things should be taken into consideration when plotting the narrative for this work:
- Hierarchical or not? If similar to SHLight, partitions need coordinations, and hierarchy helps coordination. If no hierarchy, then the motivation for paritioning may become communication efficiency (who talks to who, about what).
- Flow-based methods vs other methods: why need flow-based
- Implicit flow-based vs Explicit flow-based: if flow-based is a suitable approach, then is it different between explicit paritioning (InfoMap, etc.) and implicit (GCN, GNN styles).

The narrative/target may not necessarily the new algorithm, it can be about proposing a solution approach (e.g., using flow-based methods for TSC problems) and showing that this approach can be applied to different algorithms (PPO, MAPPO, VDN, etc.) and provide better performance.


## Experiments
### Table 6 result
Depending on your narrative, it is better to have 1-2 more approaches (not algorithms) to complete this result table.

## Writing

### Abstract
- do we do anything with community detection? You may use more standard terms, e.g., "clustering"
- Three-level protocol -> this is essentially 3 empirical approaches you are trying to integrate with the flow paritioning module, not a "3-step/3-layer" proposed for this field of study.
- If it something is a conjecture, don't need to specify them in the abstract.

### Background
#### 2.1 Network Distributed POMDP (ND-POMDP) 
is a structured subclass of the Dec-POMDP introduced by Nair, Varakantham, Tambe & Yokoo (AAAI 2005, "Networked Distributed POMDPs: A Synthesis of DCOP and POMDPs"), which needs 3 components in its heart: (i) transition independence, (ii) observation independence, and (iii) reward locality. If this work doesn't leverage those components, then ND-POMDP may not be the suitable model.

#### 2.2 InfoMap
Don't need to describe in detail the properties or characteristics of prior work. You can briefly describe and cite the work, and only need to mention what properties/characteristics important to this work.

### Related work
In summary, this is not the correct way to write an literature review/related work. This section should be written as a synthesis, not summary of works.
  - what others doing, any assumptions/agree/disagree/etc. 
  - what are the insights/takeaways
  - etc.

Also, put less priority in preprinted works (e.g., arXiv), peer-reviewed works have more credibility/reliability, especially top venues.

HiLight [36] check the reference carefully. HiLight is a hierarchical policy with sub-policies, optimizing trip time. It does not have partitioning or subregion work.

IMAC[4] work is about communication in limited bandwidth constraint, there is no "80% message reduction". This may be conflated with other work(s).

[18] is not about traffic signal control, it is about clustering travel patterns. There is no "adjacent-based methods on average delay and average speed"

GPLight [11] mutual information (MI) should be considered as a kind of flow-based/topology.

[12]'s method didn't use InfoMap

Section 3.5 Evaluation in DRL: off-topic


### Framework
Similarly to Background, this section doesn't need to detail descriptions of other works.

4.3 Hypothesis: These works are large, consider split into 2 separate ones.

Ma & Wu [13] this work use GNN, which is essentially a kind of (implicit) flow-based.

4.4 Codebook: this may be appropriate or not, depending on your narrative.





 Everything else is about scoping works.

