"""
Utilidades compartidas para los notebooks de metaheurísticas.
Problema base compartido: Coloración de Grafos (Graph Coloring).
"""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Paleta de colores distinguibles para hasta 15 colores
# ---------------------------------------------------------------------------
PALETA = [
    "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
    "#a65628", "#f781bf", "#aaaaaa", "#66c2a5", "#fc8d62",
    "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494",
]

# ---------------------------------------------------------------------------
# Creación de la instancia compartida
# ---------------------------------------------------------------------------

def crear_grafo(n=20, prob=0.35, seed=42):
    """
    Genera un grafo aleatorio de Erdős-Rényi para el problema de coloración.
    - n=20 y prob=0.35 para las metaheurísticas (Notebooks 2-5).
    - n=12 y prob=0.40 para el método exacto    (Notebook 1).
    Se garantiza que el grafo sea conexo.
    """
    rng_seed = seed
    G = nx.erdos_renyi_graph(n, prob, seed=rng_seed)
    intentos = 0
    while not nx.is_connected(G) and intentos < 50:
        rng_seed += 1
        intentos += 1
        G = nx.erdos_renyi_graph(n, prob, seed=rng_seed)
    if not nx.is_connected(G):
        # Fallback: árbol generador + aristas aleatorias
        G = nx.random_tree(n, seed=seed)
        rng = np.random.default_rng(seed)
        nodos = list(range(n))
        for _ in range(int(prob * n * (n - 1) / 2)):
            u, v = rng.choice(nodos, 2, replace=False)
            G.add_edge(int(u), int(v))
    return G


def posiciones_grafo(G, seed=42):
    """Layout fijo para reproducibilidad visual."""
    return nx.spring_layout(G, seed=seed)


# ---------------------------------------------------------------------------
# Funciones de evaluación para coloración de grafos
# ---------------------------------------------------------------------------

def calcular_conflictos(colores, G):
    """Número de aristas cuyos extremos tienen el mismo color."""
    return sum(1 for u, v in G.edges() if colores[u] == colores[v])


def coloracion_valida(colores, G):
    """True si la coloración no tiene ningún conflicto."""
    return calcular_conflictos(colores, G) == 0


def num_colores(colores):
    """Número de colores distintos usados."""
    return len(set(colores))


def costo(colores, G, lambda_conflicto=100):
    """
    Función de costo combinada (para minimizar):
        costo = num_colores + lambda_conflicto * num_conflictos
    El peso lambda_conflicto penaliza fuertemente las soluciones inválidas,
    de modo que una solución válida con k colores siempre es mejor que
    cualquier solución inválida.
    """
    return num_colores(colores) + lambda_conflicto * calcular_conflictos(colores, G)


def coloracion_greedy(G, seed=0):
    """
    Coloración voraz (greedy) como solución inicial.
    Recorre los nodos en orden aleatorio y asigna el menor color disponible.
    Garantiza una solución válida aunque no necesariamente con el mínimo de colores.
    """
    rng = np.random.default_rng(seed)
    orden = list(map(int, rng.permutation(G.number_of_nodes())))
    colores = [-1] * G.number_of_nodes()
    for v in orden:
        usados = {colores[u] for u in G.neighbors(v) if colores[u] >= 0}
        c = 0
        while c in usados:
            c += 1
        colores[v] = c
    return colores


# ---------------------------------------------------------------------------
# Visualización
# ---------------------------------------------------------------------------

def plot_grafo(G, colores, titulo="", ax=None, pos=None):
    """
    Dibuja el grafo coloreado.
    - Nodos: coloreados según su asignación.
    - Aristas: rojas si hay conflicto (mismo color en ambos extremos), grises si no.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 6))
    if pos is None:
        pos = posiciones_grafo(G)

    node_colors = [PALETA[c % len(PALETA)] for c in colores]
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                           node_size=700, edgecolors="black", linewidths=0.8)

    edge_colors = [
        "red" if colores[u] == colores[v] else "#888888"
        for u, v in G.edges()
    ]
    edge_widths = [2.5 if colores[u] == colores[v] else 1.2 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                           width=edge_widths, alpha=0.8)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="white",
                            font_weight="bold", font_size=9)

    k = num_colores(colores)
    conf = calcular_conflictos(colores, G)
    estado = "✓ válida" if conf == 0 else f"✗ {conf} conflictos"
    ax.set_title(f"{titulo}\n{k} colores — {estado}", fontsize=11)

    colores_usados = sorted(set(colores))
    parches = [mpatches.Patch(color=PALETA[c % len(PALETA)], label=f"Color {c}")
               for c in colores_usados]
    ax.legend(handles=parches, loc="upper right", fontsize=8, framealpha=0.7)
    ax.axis("off")
    return ax


def plot_convergencia(historia, titulo="Convergencia", etiqueta_y="Mejor costo",
                      ax=None, color="tab:blue", historia2=None, etiqueta2="actual"):
    """Gráfica de convergencia del mejor valor encontrado a lo largo de las iteraciones."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 4))
    ax.plot(historia, color=color, linewidth=1.8, label="mejor")
    if historia2 is not None:
        ax.plot(historia2, color="lightsteelblue", linewidth=0.8,
                alpha=0.7, label=etiqueta2)
        ax.legend()
    ax.set_title(titulo)
    ax.set_xlabel("Iteración")
    ax.set_ylabel(etiqueta_y)
    ax.grid(True, alpha=0.3)
    return ax
