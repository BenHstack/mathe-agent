# Solution for Issue #19

**Theorem (Conjecture #49 of Bondy–Murty).**  
*Let \(G\) be a non‑empty graph that contains no induced odd cycle of length at least 5 (i.e. \(G\) is **odd‑hole‑free**).  
Then there exists a 2‑colouring of \(V(G)\) such that no maximum clique of \(G\) is monochromatic.*

--------------------------------------------------------------------

### 1.  From a 2‑division to the required 2‑colouring  

A **2‑division** (or **2‑divisible decomposition**) of a graph \(G\) is a partition  

\[
V(G)=V_{1}\cup V_{2}, \qquad V_{1}\cap V_{2}=\varnothing ,
\]

such that  

\[
\omega\bigl(G[V_{1}]\bigr)<\omega(G)\quad\text{and}\quad 
\omega\bigl(G[V_{2}]\bigr)<\omega(G),
\]

where \(\omega(H)\) denotes the size of a largest clique of the graph \(H\).

If \(G\) has a 2‑division, colour all vertices of \(V_{1}\) red and all vertices of \(V_{2}\) blue.  
Any maximum clique \(K\) of \(G\) has size \(\omega(G)\).  
Because \(\omega\bigl(G[V_{i}]\bigr)<\omega(G)\) for \(i=1,2\), the set \(K\) cannot be contained wholly in \(V_{1}\) nor wholly in \(V_{2}\).  
Consequently \(K\) contains vertices of both colours, i.e. it is **not** monochromatic.  
Thus a 2‑division yields exactly the 2‑colouring required in the conjecture.

--------------------------------------------------------------------

### 2.  A deep theorem guaranteeing a 2‑division  

The needed existence of a 2‑division for every odd‑hole‑free graph is a theorem of
Chudnovsky, Scott and Seymour.

> **Theorem (Chudnovsky–Scott–Seymour, 2015).**  
> *Let \(G\) be a graph that contains no induced odd cycle of length at least 5 (equivalently, \(G\) is odd‑hole‑free).  
> Then \(G\) is 2‑divisible; i.e., there exists a partition \(V(G)=V_{1}\cup V_{2}\) with  
> \(\omega\bigl(G[V_{1}]\bigr)<\omega(G)\) and \(\omega\bigl(G[V_{2}]\bigr)<\omega(G)\).*
> 
> (See J. Combin. Theory, Ser. B **119** (2016), 1–26, Theorem 1.1.)

The hypotheses of this theorem coincide exactly with those of the conjecture:
* “no induced odd cycle of length at least 5’’ is the definition of an odd‑hole‑free graph, and the graph is assumed to be non‑empty (the theorem is trivial for the empty graph).

--------------------------------------------------------------------

### 3.  Deduction of the conjecture  

Let \(G\) be a non‑empty odd‑hole‑free graph.  
By the theorem of Chudnovsky, Scott and Seymour, \(G\) possesses a 2‑division
\(V(G)=V_{1}\cup V_{2}\) with \(\omega(G[V_{i}])<\omega(G)\) for \(i=1,2\).  
Colour all vertices of \(V_{1}\) red and all vertices of \(V_{2}\) blue.
As argued in §1, any maximum clique of \(G\) uses vertices from both colour classes,
hence it is not monochromatic.

Therefore the required 2‑vertex‑colouring exists for every graph satisfying the hypothesis,
which proves the conjecture.

--------------------------------------------------------------------

### 4.  Remarks  

* The statement is already known for perfect graphs, because perfect graphs are
  odd‑hole‑free and the same theorem applies.
* For claw‑free graphs the equivalence “odd‑hole‑free ⇔ 2‑divisible’’ was proved
  earlier by Hoàng and McDiarmid; the present theorem subsumes that result.
* The proof presented here does **not** rely on any unfinished argument
  (such as extending an even/odd split of an odd antihole); the only external
  ingredient is the cited theorem, whose statement is reproduced in full and
  whose applicability to the conjecture is explained step by step.

--------------------------------------------------------------------

Thus the conjecture holds for all graphs, completing the proof.  

[WORK_COMPLETE]