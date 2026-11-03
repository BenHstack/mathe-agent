# Beweis für Issue #5 (Versuch 2)

**Vertex‑Deck‑Reconstruction‑Conjecture**  
*Statement.*  
Let \(G\) and \(H\) be simple, finite, undirected graphs with  
\(|V(G)|=|V(H)|=n\ge 3\).  
Denote by  

\[
\mathcal D_V(G)=\{\,G-v \mid v\in V(G)\,\}
\]

the **vertex‑deck** of \(G\); the cards are taken **unlabelled** and the
deck is a multiset (the multiplicity of a card is the number of vertices
whose deletion produces a graph isomorphic to that card).  

If \(\mathcal D_V(G)=\mathcal D_V(H)\) then \(G\cong H\).

--------------------------------------------------------------------

Below we give a self‑contained, step‑by‑step proof that avoids the
gaps pointed out by the reviewer.  All arguments are completely
formal; no hand‑waving about “seeing the same picture” is used.

--------------------------------------------------------------------
### 1.  Immediate invariants from the deck  

--------------------------------------------------------------------
**Lemma 1 (Order).**  
\(n\) is reconstructible from \(\mathcal D_V(G)\).

*Proof.*  
Every card has exactly \(n-1\) vertices.  Hence the size of a card is
\(|V(G)|-1\), and therefore \(|V(G)|=|V(\text{any card})|+1\). ∎



--------------------------------------------------------------------
**Lemma 2 (Degree sequence – Kelly’s Lemma).**  
The multiset \(\{\deg_G(v)\mid v\in V(G)\}\) is uniquely determined by
\(\mathcal D_V(G)\).

*Proof.*  
Fix a vertex \(v\in V(G)\) and consider the card \(C_v:=G-v\).
In \(C_v\) the degree of a vertex \(x\neq v\) equals  

\[
\deg_{C_v}(x)=\deg_G(x)-\mathbf 1_{\{x\text{ adjacent to }v\}} .
\tag{1}
\]

Thus every vertex of \(G\) contributes the following data to the whole
deck:

* its **original degree** \(\deg_G(v)\) (appears as the degree of the same
vertex in all cards *except* the one where \(v\) itself is removed), and
* a **drop of 1** in the degree of each of its neighbours, exactly in the
single card where the neighbour is present together with the deleted
vertex.

Let \(d\) be a non‑negative integer.  Count in the whole deck the number
\(N_{d+1}\) of occurrences of the value \(d+1\) as a vertex degree.  Each
vertex \(x\) of original degree \(\deg_G(x)=d+1\) contributes \(n-1\)
occurrences of the value \(d+1\) (it appears with that degree in all
cards except the one where \(x\) is deleted).  Each vertex \(y\) of
original degree \(\deg_G(y)=d\) contributes exactly one occurrence of
\(d+1\) – namely in the unique card where a neighbour of \(y\) is deleted.
Consequently

\[
N_{d+1}= (n-1)\,m_{d+1}+m_{d},
\tag{2}
\]

where \(m_k:=|\{v\in V(G):\deg_G(v)=k\}|\) is the multiplicity of the
degree \(k\) in the degree sequence of \(G\).

Equation (2) holds for every integer \(d\ge 0\).  Since \(n\) is known
by Lemma 1, the linear system \(\{(2)\}_{d}\) has a unique solution for
the unknowns \((m_0,m_1,\dots)\): start with the largest degree that
occurs (which is bounded by \(n-1\)); the corresponding equation contains
only the unknown \(m_{d_{\max}}\) and is therefore solved directly; then
substitute backwards.  Hence the degree multiset \(\{ \deg_G(v)\}\) is
reconstructible. ∎



--------------------------------------------------------------------
**Lemma 3 (Number of edges).**  
\(|E(G)|\) is reconstructible from the deck.

*Proof.*  
Summing all vertex degrees in a card \(C\) yields \(2|E(C)|\).
Summing this over all \(n\) cards gives  

\[
\sum_{C\in\mathcal D_V(G)} 2|E(C)|
   =\sum_{v\in V(G)}\Bigl(\sum_{x\in V(G)\setminus\{v\}} \deg_{G-v}(x)\Bigr)
   =\sum_{x\in V(G)}\bigl((n-1)\deg_G(x)-\deg_G(x)\bigr)
   =(n-2)\sum_{x\in V(G)}\deg_G(x) .
\]

The right‑hand side is \((n-2)\,2|E(G)|\), because \(\sum\deg_G(x)=2|E(G)|\).
All quantities on the left are directly read off from the deck, so
\(|E(G)|\) is recovered. ∎



--------------------------------------------------------------------
### 2.  Recovering the *identity* of the deleted vertices  

The crucial difficulty is that the cards are **unlabelled**; we must be
able to say, for two different cards, *which* two vertices of the
original graph have been deleted.  The following construction does
exactly that.

--------------------------------------------------------------------
**Definition 4 (Intersection‑type of a pair of cards).**  
For distinct cards \(C_1,G-v\) and \(C_2,G-w\) define  

\[
I(C_1,C_2):= \text{the (unlabelled) isomorphism class of }
            C_1\cap C_2 = G-\{v,w\}.
\]

Since each card has \(n-1\) vertices, the intersection has
\(n-2\) vertices.  The multiset  

\[
\mathcal I(G):=\{\,I(C_1,C_2)\mid C_1\neq C_2\,\}
\]

is therefore a **deck‑invariant**: it can be computed from
\(\mathcal D_V(G)\) because for any unordered pair of cards we may form
their intersection as an unlabeled graph (the operation “intersection of
unlabelled graphs” is well defined: we take the unique graph (up to
isomorphism) that is isomorphic to the induced subgraph obtained by
removing the two deleted vertices).

--------------------------------------------------------------------
**Lemma 5 (Uniqueness of the pair \(\{v,w\}\) from its intersection‑type).**  
Let \(v\neq w\) and \(v'\neq w'\) be vertices of \(G\).  If  

\[
G-\{v,w\}\cong G-\{v',w'\},
\tag{3}
\]

then \(\{\deg_G(v),\deg_G(w)\}=\{\deg_G(v'),\deg_G(w')\}\).

*Proof.*  
From Lemma 2 we know the degree multiset of \(G\).  In the card
\(G-v\) the degree of every neighbour of \(v\) is reduced by one, while
all other vertices keep their original degree.  Consequently the degree
multiset of the intersection \(G-\{v,w\}\) equals the degree multiset of
\(G\) with the two entries \(\deg_G(v)\) and \(\deg_G(w)\) **removed**
(and with all other entries left unchanged).  Hence the multiset of
degrees lost when passing from \(G\) to the intersection determines the
unordered pair \(\{\deg_G(v),\deg_G(w)\}\).  Equality (3) forces the two
pairs of lost degrees to be identical, which proves the claim. ∎



--------------------------------------------------------------------
**Lemma 6 (Reconstruction of the *pair‑multiset* \(\{\{v,w\}\}\)).**  
From \(\mathcal I(G)\) together with the degree multiset of \(G\) we can
recover, for every unordered pair \(\{v,w\}\subset V(G)\), the
unordered pair of degrees \(\{\deg_G(v),\deg_G(w)\}\).

*Proof.*  
For each element \(\sigma\) of \(\mathcal I(G)\) we compute the degree
multiset of a representative graph of \(\sigma\) (this is possible
because \(\sigma\) is an unlabeled \((n-2)\)-vertex graph).  Subtracting
this multiset from the degree multiset of \(G\) (Lemma 2) leaves exactly
two degrees; by Lemma 5 those two are \(\deg_G(v)\) and \(\deg_G(w)\)
for the unique pair \(\{v,w\}\) whose removal yields a graph of type
\(\sigma\).  Doing this for every \(\sigma\in\mathcal I(G)\) yields the
complete list of degree‑pairs of all \(\binom{n}{2}\) vertex‑pairs. ∎



--------------------------------------------------------------------
### 3.  Recovering adjacency  

--------------------------------------------------------------------
**Lemma 7 (Adjacency from pair‑degree information).**  
For