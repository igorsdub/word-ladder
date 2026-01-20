from pathlib import Path

from loguru import logger
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
from pyvis.network import Network
from tqdm import tqdm
import typer

from src.config import FIGURES_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR
from src.features import load_graph

app = typer.Typer()


@app.command()
def graph_networkx(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len_03_valid.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len_03_networkx.png",
    plot_title: str = "3-letter English word graph",
):
    """
    Plot graph using NetworkX.draw.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len_03_valid.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len_03_valid.png".
        plot_title (str, optional): _description_. Defaults to "Word graph for 3-letter English words".
    """
    logger.info("Loading graph...")
    G = load_graph(input_path)
    logger.success(
        f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    logger.info("Selecting valid word nodes...")
    valid_nodes = [n for n, attr in G.nodes(data=True) if attr.get("is_valid_word")]
    G = G.subgraph(valid_nodes)
    logger.success(
        f"Filtered graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    logger.info("Calculating spring layout...")
    node_positions = nx.spring_layout(G, seed=42)

    logger.info("Creating figure...")
    fig, ax = plt.subplots(figsize=(5, 5))

    # Draw edges
    nx.draw_networkx_edges(
        G,
        node_positions,
        ax=ax,
        width=0.5,
        edge_color="#888888",
        alpha=0.1,
    )

    # Draw nodes with degree-based coloring
    node_degrees = dict(G.degree())
    node_colors = [node_degrees[node] for node in G.nodes()]

    nodes = nx.draw_networkx_nodes(
        G,
        node_positions,
        ax=ax,
        node_color=node_colors,
        node_size=20,
        cmap="viridis_r",
        alpha=0.9,
    )

    ax.set_title(plot_title, fontsize=16)
    ax.axis("off")
    plt.colorbar(nodes, ax=ax, label="Degree", fraction=0.03, pad=0.04)

    logger.info(f"Saving figure to {output_path}...")
    plt.savefig(output_path, facecolor="white", dpi=300)
    plt.close()

    logger.success("Plotting complete.")


@app.command()
def graph_plotly(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len_03_valid.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len_03_valid.html",
    plot_title: str = "Word graph for 3-letter English words",
):
    """
    Plot graph using Plotly.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len_03_valid.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len_03_valid.png".
    """
    logger.info("Loading graph...")
    G = load_graph(input_path)
    logger.success(
        f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    logger.info("Selecting valid word nodes...")
    valid_nodes = [n for n, attr in G.nodes(data=True) if attr.get("is_valid_word")]
    G = G.subgraph(valid_nodes)
    logger.success(
        f"Filtered graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    logger.info("Calculating spring layout...")
    node_positions = nx.spring_layout(G, seed=42)

    logger.info("Creating edge traces...")
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = node_positions[edge[0]]
        x1, y1 = node_positions[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
        opacity=0.1,
    )

    logger.info("Creating node traces...")
    node_x = []
    node_y = []
    for node_position_idx in node_positions:
        x, y = node_positions[node_position_idx]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Viridis",
            reversescale=True,
            color=[],
            size=16,
            colorbar=dict(
                thickness=20,
                lenmode="pixels",
                len=400,
                title=dict(
                    text="Degree",
                    side="top",
                    font=dict(size=20),
                ),
                tickfont=dict(size=16),
                xanchor="left",
            ),
            line_width=0.5,
            opacity=0.9,
        ),
    )

    logger.info("Find node adjacencies...")
    node_names = list(G.nodes())
    node_adjacencies = []
    node_text = []
    for node_idx, adjacencies in enumerate(G.adjacency()):
        degree = len(adjacencies[1])
        node_adjacencies.append(degree)
        node_text.append(f"word: {node_names[node_idx]}<br>degree: {degree}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    logger.info("Generating figure...")
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text=plot_title, font=dict(size=24)),
            showlegend=False,
            hovermode="closest",
            # margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            # width=500,
            # height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        ),
    )

    config = {
        "responsive": True,
        "scrollZoom": True,
        "modeBarButtonsToAdd": [
            "drawline",
            "drawopenpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ],
    }

    logger.info(f"Saving figure to {output_path}...")
    if output_path.suffix.lower() == ".html":
        fig.write_html(output_path, config=config)
    else:
        fig.write_image(output_path)

    logger.success("Plotting complete.")


@app.command()
def graph_pyvis(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len_03_valid.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len_03_valid.html",
    plot_title: str = "Word graph for 3-letter English words",
):
    """
    Plot graph using pyvis.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len_03_valid.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len_03_valid.png".
    """
    logger.info("Loading graph...")
    G = load_graph(input_path)
    logger.success(
        f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    logger.info("Selecting valid word nodes...")
    valid_nodes = [n for n, attr in G.nodes(data=True) if attr.get("is_valid_word")]
    G = G.subgraph(valid_nodes)
    logger.success(
        f"Filtered graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
    )

    # logger.info("Calculating spring layout...")
    # node_positions = nx.spring_layout(G, seed=42)

    logger.info("Creating pyvis network...")
    nt = Network(
        heading=plot_title, height="2160px", width="100%", notebook=False, bgcolor="rgba(0,0,0,0)"
    )
    nt.toggle_physics(True)

    logger.info("Generating figure...")
    nt.from_nx(G)

    logger.info(f"Saving figure to {output_path}...")
    nt.save_graph(str(output_path))

    logger.success("Plotting complete.")


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
