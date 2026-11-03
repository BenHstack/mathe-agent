# Proof for Issue #7

Let \(G=(V,E)\) be a finite simple graph.  
Recall the definitions  

* A **chordal** graph is a graph in which every cycle of length \(\ge 4\) has a chord (an edge joining two non‑consecutive vertices of the cycle).  

* A vertex \(v\in V(G)\) is **simplicial** if its neighbourhood \(N_G(v)=\{u\in V(G): uv\in E(G)\}\) induces a complete subgraph (a **clique**) of \(G\).

We prove

\[
\boxed{\text{If }G\text{ is chordal, then }G\text{ contains a simplicial vertex.}}
\]

---------------------------------------------------------------------

### 1.  Maximal cliques and a clique tree  

For a chordal graph \(G\) let \(\mathcal{C}\) be the family of its maximal cliques.  
A classical theorem (see e.g. [Dirac 1961] or any text on chordal graphs) states:

> **Clique‑tree theorem.**  
> There exists a tree \(T\) whose vertex set is \(\mathcal{C}\) such that for every vertex
> \(x\in V(G)\) the set \(\{C\in\mathcal{C}:x\in C\}\) induces a (connected) subtree of \(T\).
> This tree is called a *clique tree* (or *junction tree*) of \(G\).

We shall use only two elementary consequences of this theorem.

* **(C1)** The tree \(T\) has at least one leaf.  
* **(C2)** If \(C\) is a leaf of \(T\) and \(D\) is the unique neighbour of \(C\) in \(T\) (if
\(T\) consists of a single node we put \(D=\varnothing\)), then every vertex
\(v\in C\setminus D\) belongs to no maximal clique other than \(C\).

---------------------------------------------------------------------

### 2.  The leaf‑clique argument  

Assume first that \(G\) is a complete graph.  Then every vertex has neighbourhood
\(V(G)\setminus\{v\}\), which is a clique; hence any vertex is simplicial and we are done.

Henceforth suppose that \(G\) is **not** complete.  
Let \(T\) be a clique tree of \(G\) and let \(C\) be a leaf of \(T\).
Denote by \(D\) the (possibly empty) neighbour of \(C\) in \(T\).

Because \(C\) is a maximal clique, \(C\neq\varnothing\).  
If \(C\setminus D\neq\varnothing\) pick any vertex \(v\in C\setminus D\).
By (C2) the vertex \(v\) occurs only in the maximal clique \(C\).
Consequently the neighbourhood of \(v\) is exactly

\[
N_G(v)=C\setminus\{v\},
\]

since any neighbour of \(v\) must lie in a maximal clique that contains \(v\), and the only such clique is \(C\).
The set \(C\setminus\{v\}\) is a clique (it is a subset of the clique \(C\)).
Thus \(v\) is simplicial.

It remains to see that the set \(C\setminus D\) cannot be empty.
If it were empty, then \(C\subseteq D\); but \(C\) is a maximal clique, while
\(D\) is also a clique (every node of the tree represents a maximal clique).
The inclusion \(C\subseteq D\) would force \(C=D\), contradicting the fact that
\(C\) is a leaf distinct from its neighbour.  Hence \(C\setminus D\neq\varnothing\).

Therefore a simplicial vertex exists in \(G\).

---------------------------------------------------------------------

### 3.  Conclusion  

We have shown that every chordal graph either is complete (in which case any
vertex is simplicial) or possesses a leaf maximal clique in a clique tree; a
vertex belonging uniquely to that leaf clique is simplicial.  Hence every
chordal graph contains at least one simplicial vertex. ∎

[PROOF_COMPLETE]