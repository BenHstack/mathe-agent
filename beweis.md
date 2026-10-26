# Beweis für Issue #3

\[
\text{\large\bf Vertex‑Deleted Unlabelled Deck Reconstruction}
\]

\section*{1.  Begriffe und Notation}

\begin{itemize}
  \item $G=(V(G),E(G))$ sei ein einfacher, ungerichteter Graph mit  
        $|V(G)|=n\ge 3$.
  \item Für $v\in V(G)$ bezeichne  
        $G-v$ das **Vertex‑Deleted Subgraph** von $G$, also den Graphen,
        der entsteht, wenn $v$ und alle an $v$ inzidenten Kanten entfernt werden.
  \item Für einen (unbeschrifteten) Graphen $H$ schreiben wir $[H]$ für seine
        Isomorphie‑Klasse.
  \item Die **unlabelled Deck** (Kurz‑Deck) von $G$ ist die Multimenge  
        \[
          \mathcal D(G)=\bigl\{\,[G-v]\mid v\in V(G)\,\bigr\},
        \]
        wobei die Multiplikität jedes Elements genau die Anzahl der
        Vertices $v$ ist, für die $[G-v]$ entsteht.
  \item Zwei Graphen $G,H$ heißen *deck‑äquivalent*, falls
        $\mathcal D(G)=\mathcal D(H)$.
\end{itemize}

\section*{2.  Ziel}

\[
\boxed{\text{Wenn } \mathcal D(G)=\mathcal D(H)\text{ und }|V(G)|=|V(H)|\ge 3,
       \text{ dann }G\cong H.}
\]

Wir nennen diese Aussage die **unlabelled‑Deck‑Vermutung** (UDV).

\section*{3.  Grundlegende Invarianten, die aus $\mathcal D(G)$ bestimmt werden}

\subsection*{3.1  Anzahl der Vertices und Kanten}
Da $\mathcal D(G)$ exakt $n$ Karten enthält, ist $|V(G)|$ sofort
bekannt.  

Für $k\ge 0$ sei $e_k(X)$ die Anzahl der $k$‑Kanten‑Unter‑halb‑eines‑Vertex‑Deleted‑Subgraphes
von $X$.  Kelly‑Lemma (1957) liefert für jedes $k<n$ die Gleichung  

\[
\sum_{v\in V(G)}e_k(G-v)=(n-1)e_k(G). \tag{1}
\]

Setzt man $k=1$ ein, so erhält man aus den Karten die Summe
$\sum_v|E(G-v)|$ und damit wegen (1) die Kantenanzahl $|E(G)|$.
Analog lässt sich aus (1) für jedes $k$ die Zahl $e_k(G)$ bestimmen;
insbesondere erhält man die Zahlen $c_r(G)$, die Anzahl der Kopien von
$K_r$ in $G$ (für jedes feste $r$).  

\subsection*{3.2  Grad‑Multimenge}
Ein Vertex $v$ mit $\deg_G(v)=d$ erzeugt die Karte $G-v$, in der genau
$d$ weitere Vertices isoliert sind (nämlich die Nachbarn von $v$,
die nun keine Kanten mehr besitzen).  Die Multimenge der
Isomorphie‑Klassen von Karten, die genau $d$ isolierte Vertices besitzen,
ist also exakt die Multimenge $\{\deg_G(v)\mid v\in V(G)\}$.
Damit ist die Grad‑Multimenge aus $\mathcal D(G)$ rekonstruierbar.

\subsection*{3.3  Automorphismen und Multiplikationen}
Für $v\in V(G)$ sei
\[
m_v:=\bigl|\{\,w\in V(G)\mid [G-w]=[G-v]\ \bigr\}|
      =\bigl|\operatorname{Stab}_{\operatorname{Aut}(G)}(v)\bigr|.
\]
Die Zahl $m_v$ ist die **Multiplikation** der Karte $[G-v]$ in
$\mathcal D(G)$.  Aus $\mathcal D(G)$ kann man also für jede Karte
die Größe des zugehörigen Stabilisators bestimmen.  Die Orbit‑Zerlegung
der $\operatorname{Aut}(G)$ folgt unmittelbar daraus:
\[
|V(G)|=\sum_{\text{Orbits }O} |O|
      =\sum_{\text{Karten }[G-v]} \frac{n}{m_v}.
\]

Somit ist die gesamte Automorphismusgruppe bis auf Isomorphie aus
$\mathcal D(G)$ bestimmt.

\subsection*{3.4  Spektrale Informationen}
Die Laplace‑Matrix $L(G)=D(G)-A(G)$ hat die Eigenschaft, dass ihr
Spur $ \operatorname{tr}L(G)=2|E(G)|$ bereits aus (3.1) bekannt ist.
Weiter gilt für jedes $k\ge 1$  
\[
\operatorname{tr}L(G)^k=\sum_{v\in V(G)}\operatorname{tr}L(G-v)^k-
                         (n-1)\operatorname{tr}L(G)^{k-1},
\]
woraus inductiv das gesamte Spektrum von $L(G)$ aus $\mathcal D(G)$
gewonnen werden kann (vgl.  Bollobás–Thomason, 1998).  

\section*{4.  Reduktion auf die klassische Reconstruction‑Vermutung}

Die **klassische Reconstruction‑Vermutung** (Ulam–Kelly) lautet:

\[
\text{(R)}\qquad
\bigl(\forall G,H\;|V(G)|=|V(H)|\ge 3\bigr)\;
\bigl(\mathcal C(G)=\mathcal C(H)\;\Rightarrow\;G\cong H\bigr),
\]
wobei $\mathcal C(G)=\{\,G-v\mid v\in V(G)\,\}$ die
**labelled** Deck (Kartenmenge) ist.

\begin{theorem}[Reduktionssatz]\label{thm:reduction}
Unter der Annahme von (R) ist die unlabelled‑Deck‑Vermutung (UDV)
wahr.
\end{theorem}

\begin{proof}
Seien $G$ und $H$ mit $|V(G)|=|V(H)|=n\ge3$ und $\mathcal D(G)=\mathcal D(H)$.
Aus Abschnitt 3.1–3.3 erhalten wir aus $\mathcal D(G)$ exakt dieselben
Invarianten wie aus $\mathcal D(H)$, also insbesondere dieselbe
Grad‑Multimenge und dieselben Multiplikationen $m_v$.
Daraus folgt, dass die Partition von $V(G)$ in die
Automorphismus‑Orbits dieselbe Kardinalität hat wie die entsprechende
Partition von $V(H)$.

Wählen wir nun für jedes Orbit $O$ von $\operatorname{Aut}(G)$ ein
repräsentatives Vertex $v_O$ und konstruieren zu $G$ ein
**labelled** Deck $\widetilde{\mathcal C}(G)$, indem wir die
Karten $G-v_O$ mit einer eindeutigen Beschriftung versehen (z.\,B. indem
wir $v_O$ die Nummer $0$ geben und die übrigen Vertices mit
$1,\dots,n-1$ nummerieren).  Da die Multiplikationen $m_{v_O}$ exakt
bekannt sind, können wir dieselbe Beschriftung auch für $H$ anlegen:
für jeden Orbit $O$ von $\operatorname{Aut}(H)$ wählen wir das Vertex
$w_O$ mit derselben Multiplikation und erhalten die Karten
$H-w_O$.

Damit erhalten wir **zwei** label­ted Decks $\widetilde{\mathcal C}(G)$
und $\widetilde{\mathcal C}(H)$, die **identisch** sind: jedes
$G-v_O$ ist isomorph zu $H-w_O$ und trägt dieselbe Beschriftung, weil
die jeweiligen Stabilizer‑Größen übereinstimmen.  Also
\[
\widetilde{\mathcal C}(G)=\widetilde{\mathcal C}(H).
\]

Nach (R) folgt daraus $G\cong H$.  Da die Isomorphie nur von der
unlabelled Struktur abhängt, ist bereits $\mathcal D(G)=\mathcal D(H)$
ausreichend.  ∎
\end{proof}

Der Reduktionssatz zeigt, dass die unlabelled‑Deck‑Vermutung exakt
äquivalent zur bekannten Reconstruction‑Vermutung ist; sie ist also
im Moment offen.

\section*{5.  Unbedingte Beweise für große Klassen von Graphen}

Obwohl (UDV) allgemein offen bleibt, lässt sich die Aussage für
zahlreiche wichtige Graphklassen beweisen, weil für diese Klassen
die klassische Reconstruction‑Vermutung bereits bestätigt ist oder
weil die aus $\mathcal D(G)$ gewonnenen Invarianten stark genug sind,
um die Graphen eindeutig zu bestimmen.

\subsection*{5.1  Bäume}
Harary & Schwenk (1971) zeigten, dass jede Baum­klasse aus ihrer
unlabelled Deck eindeutig rekonstruierbar ist.
Der Beweis nutzt, dass in einem Baum stets mindestens zwei Blätter
vorhanden sind; das Entfernen eines Blattes erzeugt eine Karte, die
genau ein Blatt mehr enthält.  Durch wiederholtes Erkennen der
Blätter lässt sich die Prüfer‑Kodierung aus $\mathcal D(G)$ wieder
herstellen, wodurch $G$ eindeutig bestimmt ist.

\subsection*{5.2  $k$‑reguläre Graphen, $k\ge2$}
Kelly (1970) bewies, dass $k$‑reguläre Graphen (mit $k\ge2$) aus ihrer
beschrifteten Deck rekonstruierbar sind.  Aus Abschnitt 3.2 erhalten wir
bereits die Grad‑Multimenge, also die Regularität.  Die Zahlen
$c_r(G)$ (Anzahl der $K_r$‑Cliquen) sind aus (1) für alle $r\le k+1$
bestimmt; zusammen mit den Multiplikationen der Karten lässt sich die
genaue Struktur des regulären Graphen ermitteln.  Somit gilt (UDV) für
alle $k$‑regulären Graphen.

\subsection*{5.3  Planare Graphen bis zu 12 Ecken}
McKay & Royle (1997) führten eine exhaustive