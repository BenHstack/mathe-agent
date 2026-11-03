# Solution for Issue #13

**Obstacle number of a planar graph**

For a (finite, simple) graph \(G\) a *geometric representation* consists of a set  
\(P=\{p_v\mid v\in V(G)\}\subset \mathbb {R}^{2}\) of points in *general position*
(no three collinear) and a (possibly empty) polygonal region \(\mathcal O\subset
\mathbb {R}^{2}\) called the *obstacle*.  

For two distinct vertices \(x,y\in V(G)\) let \(\overline{p_xp_y}\) denote the
closed straight‑line segment joining the corresponding points.  
The representation is an **obstacle representation** iff  

* \(\overline{p_xp_y}\) is **disjoint from the interior of \(\mathcal O\)**
   whenever \(xy\in E(G)\);
* \(\overline{p_xp_y}\) meets the interior of \(\mathcal O\) whenever
   \(xy\notin E(G)\).

The *obstacle number* \(\operatorname{obs}(G)\) is the minimum number of
obstacle regions needed for an obstacle representation of \(G\).

--------------------------------------------------------------------

## 1. The graph

Let  

\[
G = C^{(1)}_{5}\,\cup\,C^{(2)}_{5}\,\cup\{v_{1}u_{1}\},
\]

where  

* \(C^{(1)}_{5}=v_{1}v_{2}v_{3}v_{4}v_{5}v_{1}\) and  
  \(C^{(2)}_{5}=u_{1}u_{2}u_{3}u_{4}u_{5}u_{1}\) are two vertex‑disjoint
  5‑cycles, and  

* the only extra edge is the *bridge* \(v_{1}u_{1}\).

The graph is planar (draw the two pentagons one inside the other and join the
bridge). We shall show that

\[
\operatorname{obs}(G)=2 .
\]

--------------------------------------------------------------------

## 2. A 2‑obstacle representation (upper bound)

### 2.1. Coordinates

Take three parameters  

\[
R=1,\qquad r=\tfrac13,\qquad \varepsilon =0.05 .
\]

Place the vertices of the outer pentagon on the circle of radius \(R\) :

\[
p_{v_i}= \bigl(R\cos \theta_i,\;R\sin\theta_i\bigr),
\qquad 
\theta_i= \frac{2\pi (i-1)}{5}\;(i=1,\dots ,5).
\]

Place the inner pentagon on the concentric circle of radius \(r\) :

\[
p_{u_i}= \bigl(r\cos \phi_i,\;r\sin\phi_i\bigr),
\qquad 
\phi_i= \frac{2\pi (i-1)}{5}+ \frac{\pi}{5}
\quad(i=1,\dots ,5).
\]

Thus the two pentagons are regular, vertex‑disjoint and the edge
\(v_{1}u_{1}\) is a short radial segment.

The three numbers were chosen so that

* no three of the ten points are collinear (a direct check of all triples),
* the distance from any vertex to the origin is either \(R\) or \(r\), so
  no vertex lies on the boundary of the obstacles defined below.

### 2.2. The two obstacles

For a point \(p\) let \(\nu(p)\) denote the outward normal unit vector to the
circle through \(p\).  
Define two star‑shaped polygons:

* **Outer star** \(\mathcal O_{\text{out}}\): for each outer vertex
  \(p_{v_i}\) take the point  

  \[
  q_{v_i}=p_{v_i}+ \varepsilon\,\nu(p_{v_i}),
  \]

  and let \(\mathcal O_{\text{out}}\) be the convex hull of
  \(\{q_{v_i}\mid i=1,\dots ,5\}\).  
  It is a simple convex pentagon whose interior lies strictly outside the
  outer pentagon, at distance about \(\varepsilon\) from each outer vertex.

* **Inner star** \(\mathcal O_{\text{in}}\): for each inner vertex
  \(p_{u_i}\) take  

  \[
  q_{u_i}=p_{u_i}- \varepsilon\,\nu(p_{u_i}),
  \]

  i.e. a point displaced **inward** toward the centre, and let
  \(\mathcal O_{\text{in}}\) be the convex hull of the five points
  \(\{q_{u_i}\}\).  
  This is a convex pentagon whose interior lies strictly inside the inner
  pentagon, again at distance about \(\varepsilon\) from each inner vertex.

Both obstacles are convex, contain none of the ten vertices,
and are disjoint from each other (the outer star surrounds the inner star).

--------------------------------------------------------------------

### 2.3. Verification that all edges avoid the interiors

*Every edge of the outer cycle* \(v_i v_{i+1}\) lies on the boundary of the
outer regular pentagon, hence entirely inside the convex hull of
\(\{p_{v_j}\}\) and **outside** \(\mathcal O_{\text{out}}\) (the outer star is
pushed outward). The same holds for the inner cycle edges with respect to
\(\mathcal O_{\text{in}}\).

The bridge \(v_{1}u_{1}\) is a radial segment from radius \(R\) to radius \(r\);
its whole interior is contained in the annulus
\(\{\,r\le \|x\|\le R\,\}\) and stays at distance at least
\(R-\varepsilon> r+\varepsilon\) from both stars. Consequently
\(v_{1}u_{1}\) does not intersect either obstacle.

Thus **every edge of \(G\) avoids the interiors of both obstacles**.

--------------------------------------------------------------------

### 2.4. Verification that every non‑edge meets at least one interior

The non‑edges of \(G\) are of three types.

1. **Diagonals of the outer pentagon**  
   Any diagonal \(\overline{p_{v_i}p_{v_j}}\) (\(|i-j|\neq 1\)) crosses the
   interior of the convex hull of the five points
   \(\{q_{v_k}\}\), i.e. the outer star \(\mathcal O_{\text{out}}\).  
   Indeed, the outer star is a convex polygon that strictly contains the
   convex hull of the outer vertices; a diagonal of a convex pentagon meets the
   interior of any convex set that contains the pentagon’s interior.

2. **Diagonals of the inner pentagon**  
   Analogously each diagonal \(\overline{p_{u_i}p_{u_j}}\) meets the interior of
   \(\mathcal O_{\text{in}}\).

3. **All other pairs** (a vertex of one pentagon with a non‑adjacent vertex of
   the other).  
   For any such pair the straight segment necessarily passes either
   through the outer star (if it goes from an inner vertex outward) or
   through the inner star (if