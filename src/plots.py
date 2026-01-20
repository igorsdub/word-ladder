from pathlib import Path

from bokeh.io import save
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
from bokeh.palettes import Viridis256
from bokeh.plotting import figure, from_networkx
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
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len03_networkx.png",
    plot_title: str = "3-letter English word graph",
):
    """
    Plot a graph using NetworkX.draw.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len03.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len03.png".
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
def graph_bokeh(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len03_bokeh.html",
    plot_title: str = "3-letter English word graph",
):
    """
    Plot a graph using Bokeh.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len03.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len03_bokeh.html".
        plot_title (str, optional): _description_. Defaults to "3-letter English word graph".
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

    logger.info("Creating Bokeh figure...")
    p = figure(
        title=plot_title,
        x_range=(-1.2, 1.2),
        y_range=(-1.2, 1.2),
        x_axis_location=None,
        y_axis_location=None,
        width=800,
        height=800,
        sizing_mode="stretch_both",
        tools="hover,pan,wheel_zoom,box_zoom,reset",
        tooltips=[("word", "@word"), ("degree", "@degree")],
        background_fill_color=None,
        border_fill_color=None,
    )
    p.grid.grid_line_color = None

    logger.info("Creating graph renderer...")
    graph = from_networkx(G, node_positions, scale=1, center=(0, 0))
    p.renderers.append(graph)

    # Add node data
    node_degrees = dict(G.degree())
    degrees = [node_degrees[node] for node in G.nodes()]

    # Map degrees to colors using reversed Viridis
    min_degree = min(degrees)
    max_degree = max(degrees)
    palette_r = list(reversed(Viridis256))
    color_mapper = LinearColorMapper(palette=palette_r, low=min_degree, high=max_degree)

    graph.node_renderer.data_source.data["word"] = list(G.nodes())
    graph.node_renderer.data_source.data["degree"] = degrees

    graph.node_renderer.glyph.update(
        size=8,
        fill_alpha=0.9,
        fill_color={"field": "degree", "transform": color_mapper},
    )
    graph.edge_renderer.glyph.update(line_color="#888888", line_alpha=0.1)

    # Add color bar
    color_bar = ColorBar(
        color_mapper=color_mapper,
        ticker=BasicTicker(desired_num_ticks=8),
        width=200,
        height=20,
        location=(0, 0),
        title="Degree",
        title_text_align="center",
    )
    p.add_layout(color_bar, "below")

    logger.info(f"Saving figure to {output_path}...")
    save(p, filename=str(output_path), title=plot_title)

    logger.success("Plotting complete.")


@app.command()
def graph_plotly(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len03.html",
    plot_title: str = "Word graph for 3-letter English words",
):
    """
    Plot a graph using Plotly.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len03.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len03.png".
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
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    output_path: Path = FIGURES_DIR / "graph_en_len03.html",
    plot_title: str = "Word graph for 3-letter English words",
):
    """
    Plot a graph using pyvis.

    Args:
        input_path (Path, optional): _description_. Defaults to INTERIM_DATA_DIR/"graph_en_len03.pkl".
        output_path (Path, optional): _description_. Defaults to FIGURES_DIR/"graph_en_len03.png".
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
