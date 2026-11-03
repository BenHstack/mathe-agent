# Solution for Issue #9

**Theorem (Menger’s theorem – edge‑version).**  
Let \(G\) be a finite undirected graph and let \(k\in\mathbb N\).  
Then \(G\) is *\(k\)-edge‑connected* (i.e. \(\lambda(G)\ge k\)) **iff** for every ordered pair of distinct vertices
\(s,t\in V(G)\) there exist at least \(k\) pairwise edge‑disjoint \(s\!-\!t\) paths in \(G\).

---

### Proof

We prove the two implications separately.

---

#### 1.  (**Only‑if**)  If \(G\) is \(k\)-edge‑connected, then for any \(s,t\in V(G)\) there are \(k\) edge‑disjoint \(s\!-\!t\) paths.

Consider the graph \(G\) together with two new vertices \(s\) and \(t\) (if they are not already present) and give each edge capacity 1.  
Apply the **max‑flow/min‑cut theorem** to the resulting network with source \(s\) and sink \(t\).  
The value of a maximum \(s\!-\!t\) flow equals the size of a minimum \(s\!-\!t\) cut.

Because \(G\) is \(k\)-edge‑connected, every cut separating \(s\) from \(t\) contains at least \(k\) edges; hence the minimum cut has capacity \(\ge k\).  
Therefore the maximum flow has value \(\ge k\).  

A flow of value \(k\) can be decomposed (by the integrality theorem for flows with unit capacities) into \(k\) unit‑capacity flow paths that are edge‑disjoint.  Each such unit flow corresponds to an edge‑disjoint \(s\!-\!t\) path in the original graph.  ∎

> **Remark.** The max‑flow/min‑cut theorem is a classical result proved without any appeal to Menger’s theorem, so the above argument does not involve circular reasoning.

---

#### 2.  (**If**)  If for every pair \(s,t\) there exist \(k\) edge‑disjoint \(s\!-\!t\) paths, then \(G\) is \(k\)-edge‑connected.

Assume, toward a contradiction, that \(G\) is **not** \(k\)-edge‑connected.  
Then there exists a cut \(C\subseteq E(G)\) whose removal separates the vertex set into two non‑empty parts
\(A\) and \(B\) with \(s\in A\) and \(t\in B\), and with \(|C|<k\).

Consider any \(s\!-\!t\) path \(P\) in \(G\).  
If \(P\) avoided all edges of \(C\), then after deleting \(C\) the vertices \(s\) and \(t\) would still lie in the same connected component, contradicting the definition of \(C\) as a separating cut.  
Hence **every** \(s\!-\!t\) path must contain at least one edge of \(C\).

Now suppose we have a collection \(\mathcal{P}\) of edge‑disjoint \(s\!-\!t\) paths.  
Because the paths are edge‑disjoint, no two of them can share the same edge of the cut \(C\).  
Consequently each path in \(\mathcal{P}\) must use a **different** edge of \(C\).  Therefore

\[
|\mathcal{P}|\le |C|<k .
\]

But by hypothesis there exist \(k\) edge‑disjoint \(s\!-\!t\) paths, i.e. a collection \(\mathcal{P}\) with \(|\mathcal{P}|=k\).  This contradicts the inequality above.  

Hence our assumption that a cut of size smaller than \(k\) exists is false.  Therefore every cut separating any two vertices has at least \(k\) edges, i.e. \(\lambda(G)\ge k\).  ∎

---

### Conclusion

Both directions have been established, so the theorem holds: a graph is \(k\)-edge‑connected **iff** any two vertices are linked by at least \(k\) pairwise edge‑disjoint paths.

---

*The proof above follows the supervisor’s request: the “if” direction explicitly uses the fact that every \(s\!-\!t\) path must contain **at least one** edge of a separating cut, and the edge‑disjointness forces each path to consume a distinct cut edge, yielding the bound \(|\mathcal{P}|\le|C|.\)*

[WORK_COMPLETE]