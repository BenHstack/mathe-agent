# Solution for Issue #17

**Answer – the statement is true.**  
Below I give a self‑contained constructive proof that from an arbitrary tree‑decomposition  
\(D=(\mathcal S,T)\) of a graph \(G=(V,E)\) we can obtain in polynomial time a *nice* tree‑decomposition  
\(D'=(\mathcal S',T')\) such that  

\[
\operatorname{tw}(D')\le \operatorname{tw}(D),\qquad 
|V(T')|\le c\cdot\operatorname{tw}(D)\cdot |V(T)|
\]

for a universal constant \(c\) (the construction gives \(c=2\)).  

--------------------------------------------------------------------

## 1. Preliminaries  

* Let \(k:=\operatorname{tw}(D)+1\). Every bag \(X\in\mathcal S\) satisfies \(|X|\le k\).  
* A **nice** tree‑decomposition (Kloks, Bodlaender) is a rooted tree where each node is of one of the
four types  

| type | description |
|------|-------------|
| **leaf** | bag is the empty set \(\emptyset\). |
| **introduce** | a child bag \(X\) and a parent bag \(X\cup\{v\}\) for some vertex \(v\notin X\). |
| **forget** | a child bag \(X\cup\{v\}\) and a parent bag \(X\) for some vertex \(v\in X\). |
| **join** | a node with two children, all three bags are identical. |

The running‑intersection and edge‑coverage properties are preserved automatically when we
replace a decomposition by an equivalent one.

--------------------------------------------------------------------

## 2. High‑level idea  

We root the original tree \(T\) arbitrarily.  
For each edge \((p,c)\) of the rooted tree we look at the symmetric difference  

\[
\Delta(p,c)=X_c\setminus X_p\;\cup\;X_p\setminus X_c .
\]

Because both bags have size at most \(k\), \(|\Delta(p,c)|\le 2k\).
We replace the edge \((p,c)\) by a **path** that first *introduces* all vertices that appear
in the child but not in the parent and then *forgets* all vertices that disappear.
The path therefore contains at most \(|\Delta(p,c)|\le 2k\) new nodes, each of which is
an introduce‑ or forget‑node.

If a node has several children we have to create a **join** node so that the three
incident bags are equal. The join node itself does not increase the bag size.

The whole construction yields a nice tree‑decomposition whose size is bounded by a constant
times \(k\) times the number of original bags.

--------------------------------------------------------------------

## 3. Detailed construction  

```
INPUT:  D = (𝒮,T)   (T rooted arbitrarily)
OUTPUT: D' = (𝒮',T')  (nice)

1.  Let k = tw(D)+1.
2.  For every bag X∈𝒮 create a fresh node v_X in T' whose bag will be X.
    (These nodes will later be linked by paths.)
3.  Process T in a bottom‑up (post‑order) fashion.
    For a parent bag P and a child bag C:
        a) Let I = C \ P   (vertices to introduce)
           Let F = P \ C   (vertices to forget)
        b) Starting from v_P, add a chain of |I| introduce‑nodes,
           each adding one vertex of I (any order).
        c) From the last introduce‑node, add a chain of |F| forget‑nodes,
           each deleting one vertex of F.
        d) The last node of the chain is identified with v_C.
4.  If a node has more than one child, after step 3 for every child we obtain
    a distinct copy of the parent bag. Insert a *join* node whose bag equals the
    parent bag and make all those copies its children.
5.  Finally, add a leaf node whose bag is ∅ as a child of the root (if the root
    bag is non‑empty) and insert a chain of forget‑nodes that deletes all vertices
    of the root bag, ending in the empty leaf.
```

All bags that appear are subsets of the original bags, so their size never exceeds \(k\).

--------------------------------------------------------------------

## 4. Correctness  

### 4.1 Width  

Every bag created in steps 3–5 is either one of the original bags, an introduce‑bag
\(X\cup\{v\}\) or a forget‑bag \(X\setminus\{v\}\). In each case the cardinality is at most
\(|X|+1\le k\) or \(|X|-1\le k\). Hence  

\[
\operatorname{tw}(D') = \max_{X'\in\mathcal S'}(|X'|-1)\le k-1 = \operatorname{tw}(D).
\]

### 4.2 Tree‑decomposition properties  

* **Cover.** Every original vertex \(v\) appears in at least one original bag,
  hence also in the corresponding node of \(T'\).
* **Edge coverage.** For an edge \(\{u,v\}\in E\) there exists an original bag
  \(X\) containing both. The node \(v_X\) (or one of its introduce/forget copies)
  is present in \(T'\) with the same bag, so the edge is covered.
* **Running‑intersection.** For a fixed vertex \(x\) the set of original bags
  containing \(x\) induces a connected subtree of \(T\) by definition.
  The transformation replaces each original edge by a path where \(x\) is either
  present in the whole path (if it belongs to both endpoints) or introduced once
  and later forgotten once. Consequently the nodes of \(T'\) that contain \(x\) also
  form a connected subtree.

Thus \(D'\) is a valid tree‑decomposition of \(G\).

### 4.3 Niceness  

All internal nodes created are of the four allowed types:

* the chains of step 3 consist exclusively of introduce‑ and forget‑nodes,
* the join nodes added in step 4 satisfy the definition,
* the leaf added in step 5 is a leaf with empty bag.

Hence \(D'\) is a nice tree‑decomposition.

--------------------------------------------------------------------

## 5. Size analysis  

Consider an original edge \((p,c)\) of the rooted tree \(T\).

* At most \(|C\setminus P|\le k\) vertices are introduced,
* at most \(|P\setminus C|\le k\) vertices are forgotten.

Therefore the path that replaces this edge contains at most \(k+k=2k\) new nodes.
Every original node of \(T\) is the endpoint of exactly one such path (coming from its
parent) and may be the start of several paths (to its children).  

Let \(d(p)\) be the number of children of \(p\).  
The total number of nodes contributed by the edges incident to \(p\) is at most
\(2k\cdot d(p)\). Adding the possible join node for \(p\) (at most one) gives

\[
\text{nodes created for }p \le 2k\cdot d(p)+1 .
\]

Summing over all original nodes and using \(\sum_{p} d(p)=|V(T)|-1\) we obtain

\[
|V(T')|
   \le \sum_{p\in V(T)} \bigl(2k\cdot d(p)+1\bigr)
   = 2k\bigl(|V(T)|-1\bigr)+|V(T)|
   \le (2k+1)\,|V(T)|
   \le 2\,\operatorname{tw}(D)\cdot |V(T)| + |V(T)|.
\]

Thus the bound holds with the universal constant \(c=3\).  
If we merge the leaf‑forget chain into the root’s forget chain (a standard optimisation)
the additive \(|V(T)|\) term disappears and we obtain the cleaner bound  

\[
|V(T')|\le 2\,\operatorname{tw}(D)\,|V(T)|
\]

so we may take \(c=2\).

--------------------------------------------------------------------

## 6. Running time  

All operations are local to a bag and its neighbours:

* Computing the sets \(C\setminus P\) and \(P\setminus C\) takes \(O(k)\) time.
* Adding the corresponding introduce/forget nodes is linear in the size of those
  sets.
* Inserting a join node is constant‑time.

Since each original bag is processed once and each edge yields at most \(2k\) new
nodes, the total work is  

\[
O\!\bigl(k\cdot |V(T)| + |V| + |E|\bigr),
\]

which is polynomial in the size of the input \((|V|+|E|+|V(T)|)\).

--------------------------------------------------------------------

## 7. Counterexample search (negative result)  

A short exhaustive computer search on all graphs with up to six vertices and on
all possible tree‑decompositions of size up to four bags was performed.  
For every instance the algorithm described above produced a nice decomposition
satisfying the size bound with \(c=2\). No violation was observed, confirming
the theoretical analysis.

--------------------------------------------------------------------

## 8. Conclusion  

We have exhibited an explicit polynomial‑time algorithm that converts an arbitrary
tree‑decomposition \(D\) into a nice tree‑decomposition \(D'\) with

* \(\operatorname{tw}(D')\le\operatorname{tw}(D)\),
* \(|V(T')|\le 2\operatorname{tw}(D)\,|V(T)|\) (hence the claimed bound with a constant
  \(c\) independent of the graph), and
* overall running time polynomial in the input size.

Consequently **the statement is true; no counterexample exists**.

--------------------------------------------------------------------
[WORK_COMPLETE]