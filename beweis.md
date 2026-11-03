# Solution for Issue #11

**Definitions**

* A **graph** $G=(V,E)$ is finite, simple (no loops or multiple edges) unless otherwise stated.  
* For $s,t\in V$, a set $\mathcal P=\{P_1,\dots ,P_r\}$ of $s$–$t$ paths is **internally disjoint** if for any distinct $i,j$ we have  
  \[
  V(P_i)\cap V(P_j)=\{s,t\}.
  \]
  In other words no vertex other than the two terminals appears in more than one path.
* The **vertex‑connectivity** $\kappa(G)$ of $G$ is the minimum cardinality of a vertex set $C\subseteq V$ whose removal disconnects $G$ (or makes it trivial).  
  $G$ is **$k$‑vertex‑connected** (or **$k$‑connected**) iff $|V|\ge k+1$ and $\kappa(G)\ge k$; equivalently, the deletion of any set of fewer than $k$ vertices leaves $G$ connected.

---

## Theorem (Menger, vertex version)

*Let $G$ be a graph with $|V(G)|\ge k+1$ and let $k\in\mathbb N$.  
Then $G$ is $k$‑vertex‑connected **iff** for every ordered pair of distinct vertices $s,t\in V(G)$ there exist $k$ internally disjoint $s$–$t$ paths.*

We prove the two implications separately.

--------------------------------------------------------------------

### 1.  $k$‑connectivity  $\Longrightarrow$  $k$ internally disjoint $s$–$t$ paths  

Fix distinct vertices $s,t\in V(G)$.  
We transform $G$ into a directed network $N_{s,t}$ in which each non‑terminal vertex has capacity 1.

* For every vertex $v\in V\setminus\{s,t\}$ create two vertices $v_{\text{in}}$ and $v_{\text{out}}$ and the directed edge $e_v=(v_{\text{in}},v_{\text{out}})$ of **capacity 1**.
* For each original (undirected) edge $uv\in E$ we add the two directed arcs  
  \[
  (u_{\text{out}},v_{\text{in}}),\qquad (v_{\text{out}},u_{\text{in}})
  \]
  each of **infinite capacity** (or any number larger than $k$).
* The source of the network is $s$ (which we keep as a single vertex) and the sink is $t$ (also a single vertex).  
  No capacity restriction is placed on $s$ or $t$.

Denote the resulting directed graph by $N_{s,t}$.  Any $s$–$t$ **flow** in $N_{s,t}$ of value $f$ corresponds to $f$ pairwise internally disjoint $s$–$t$ paths in the original graph $G$: each unit of flow traverses a distinct $v_{\text{in}}\!\to\!v_{\text{out}}$ edge, so no vertex (other than $s,t$) is used by two flow units.

---

#### Claim.  The maximum $s$–$t$ flow in $N_{s,t}$ has value at least $k$.

*Proof.*  By the **max‑flow/min‑cut theorem** for networks with integer capacities, the value of a maximum flow equals the capacity of a minimum $s$–$t$ cut.  
Consider any $s$–$t$ cut $C\subseteq V(N_{s,t})$.  In the original graph $G$ the set  

\[
X=\{v\in V(G)\setminus\{s,t\} : v_{\text{in}}\in C,\;v_{\text{out}}\notin C\}
\]

is a vertex set separating $s$ from $t$.  Its size equals the total capacity of the cut, because the only finite‑capacity arcs crossing from the $s$‑side to the $t$‑side are precisely the edges $e_v=(v_{\text{in}},v_{\text{out}})$ for $v\in X$, each of capacity 1.  Hence  

\[
\operatorname{cap}(C)=|X|.
\]

Since $G$ is $k$‑connected, every $s$–$t$ separating vertex set has size at least $k$, i.e. $|X|\ge k$.  Consequently every $s$–$t$ cut in $N_{s,t}$ has capacity $\ge k$, and the minimum cut capacity is at least $k$.  By max‑flow/min‑cut, the maximum flow value is at least $k$.

∎

Because all capacities are integers, there exists an **integral** maximum flow of value $k$.  Decomposing this flow into $k$ unit‑flows yields $k$ directed $s$–$t$ paths that are pairwise internally vertex‑disjoint in $G$.  Ignoring direction gives $k$ internally disjoint $s$–$t$ (undirected) paths in the original graph.

Thus every pair $s,t$ is linked by $k$ internally disjoint paths.

--------------------------------------------------------------------

### 2.  Existence of $k$ internally disjoint $s$–$t$ paths  $\Longrightarrow$  $k$‑connectivity  

Assume that for **every** ordered pair of distinct vertices $s,t$ there are $k$ internally disjoint $s$–$t$ paths.  
We show $\kappa(G)\ge k$.

Suppose, to the contrary, that $\kappa(G)<k$.  Then there exists a vertex set $C\subseteq V(G)$ with $|C|=c<k$ whose removal separates the graph: there are vertices $s,t\in V(G)\setminus C$ that lie in distinct components of $G-C$.  Every $s$–$t$ path in $G$ must meet $C$, because otherwise it would survive in $G-C$ and join the two components.

Take any family $\mathcal P$ of internally disjoint $s$–$t$ paths.  Since the internal vertices of the paths are pairwise distinct, each path contributes at least one distinct vertex of $C$ (otherwise two different paths would avoid $C$ and stay disjoint, contradicting the separation).  Hence  

\[
|\mathcal P|\le |C|=c<k,
\]

which contradicts the hypothesis that **at least $k$** such paths exist for the pair $(s,t)$.  Therefore no vertex cut of size $<k$ exists, i.e. $\kappa(G)\ge k$.

Because $|V(G)|\ge k+1$ is assumed, the condition “more than $k$ vertices’’ required in the definition of $k$‑connectedness is satisfied.  Hence $G$ is $k$‑vertex‑connected.

--------------------------------------------------------------------

### 3.  Edge‑case verification  

* If $|V(G)|=k+1$, the only $k$‑connected graph is the complete graph $K_{k+1}$.  Between any two vertices there are exactly $k$ internally disjoint paths (each uses a different intermediate vertex), so the theorem holds.
* If $|V(G)|\le k$, the statement’s hypothesis “at least $k+1$ vertices’’ is violated; indeed a graph with fewer vertices cannot be $k$‑connected, and the path condition may fail (e.g., a path on three vertices cannot have two internally disjoint $s$–$t$ paths).  Hence the hypothesis is necessary.

--------------------------------------------------------------------

## Proof summary

* **Forward direction** – model vertex capacities by splitting vertices, apply the max‑flow/min‑cut theorem, obtain a flow of value $k$, and decompose it into $k$ internally disjoint $s$–$t$ paths.
* **Reverse direction** – a vertex cut of size $<k$ would intersect every $s$–$t$ path, limiting the number of internally disjoint paths to $<k$, contradicting the hypothesis.  

Thus the two statements are equivalent, establishing Menger’s theorem for vertex‑connectivity.

\[
\boxed{\;G\text{ is }k\text{-vertex-connected}\iff
\forall\,s\neq t\in V(G)\;\exists\;k\text{ internally disjoint }s\!-\!t\text{ paths}\;}
\]

∎

[WORK_COMPLETE]