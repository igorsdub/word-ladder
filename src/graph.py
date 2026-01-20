import itertools
from pathlib import Path
import pickle
from typing import Annotated

from loguru import logger
import networkx as nx
from rich import print
from tqdm import tqdm
import typer

from src.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT

app = typer.Typer()


##### Graph ######
def save_graph(
    G: nx.Graph,
    output_path: Path = PROJ_ROOT / "graph.pkl",
):
    """
    Save a graph to a pickle file.

    :param input_path: Description
    :type input_path: Path
    """

    pickle.dump(G, open(output_path, "wb"))
    return None


def load_graph(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
):
    """
    Load a graph from a pickle file.

    :param input_path: Description
    :type input_path: Path
    """

    G = pickle.load(open(input_path, "rb"))
    return G


def find_hamming_distance(string1, string2):
    """Find the Hamming distance between two equal-length strings."""
    if len(string1) != len(string2):
        raise ValueError("Strings must be of equal length.")
    return sum(char1 != char2 for char1, char2 in zip(string1, string2))


##### Analysis ######
def find_betweenness_centrality(Graph):
    """Find and display the 5 most central words by betweenness centrality."""
    betweenness = nx.betweenness_centrality(Graph)
    print()
    print("Most Central Words (Betweenness Centrality):")
    for node, centrality in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {node}: {centrality:.4f}")
    print()

def find_community(Graph):
    """Find and display communities using Louvain method."""
    communities_list = nx.community.louvain_communities(Graph)
    print()
    print(f"Found {len(communities_list)} Communities:")
    for community_id, community in enumerate(communities_list):
        words = sorted(list(community))
        print(f"  Community {community_id} ({len(words)} words): {', '.join(words[:5])}")
    print()


def find_diameter(Graph):
    """Find and display the diameter (longest shortest path) of the graph."""
    diameter = nx.diameter(Graph)
    eccentricity = nx.eccentricity(Graph)
    periphery = nx.periphery(Graph)

    # Find a path between two peripheral nodes
    node1, node2 = periphery[0], periphery[1]
    diameter_path = nx.shortest_path(Graph, source=node1, target=node2)

    print()
    print(f"Graph Diameter: {diameter} steps")
    print(f"Diameter path: {' - '.join(diameter_path)}")
    print()


@app.command()
def build(
    input_path: Path = INTERIM_DATA_DIR / "en_len03.txt",
    output_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    word_length: int = 3,
    alphabet: str = "abcdefghijklmnopqrstuvwxyz",
):
    """
    Build a word graph with valid words and connect them by Hamming distance.

    :param input_path: Path to file with valid words
    :type input_path: Path
    :param output_path: Path to save the graph
    :type output_path: Path
    :param word_length: Length of words
    :type word_length: int
    :param alphabet: Alphabet to use for generating all possible words
    :type alphabet: str
    """
    alphabet = list(alphabet)

    logger.info("Constructing all possible words...")
    nodes = ["".join(p) for p in itertools.product(alphabet, repeat=word_length)]
    logger.success(
        f"Constructed {len(nodes)} words of length {word_length} and alphabet size {len(alphabet)}."
    )

    logger.info(f"Loading valid words from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as file:
        valid_words = set(file.read().splitlines())
    logger.success(f"Loaded {len(valid_words)} valid words.")

    logger.info("Initializing word graph...")
    G = nx.Graph()
    G.add_nodes_from(nodes)

    logger.info("Assigning valid word attributes to nodes...")
    for node in G.nodes():
        G.nodes[node]["is_valid_word"] = node in valid_words

    logger.info("Connecting valid words by Hamming distance...")
    valid_word_nodes = [node for node in G.nodes() if G.nodes[node]["is_valid_word"]]
    for i, n1 in tqdm(enumerate(valid_word_nodes), total=len(valid_word_nodes)):
        for j, n2 in enumerate(valid_word_nodes):
            if i < j and find_hamming_distance(n1, n2) == 1:
                G.add_edge(n1, n2)

    logger.success(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    logger.info(f"Saving graph to {output_path}...")
    save_graph(G, output_path)
    logger.success("Graph saved successfully.")


@app.command()
def analyze(
    input_path: Path = INTERIM_DATA_DIR / "graph_en_len03.pkl",
    output_path: Path = PROCESSED_DATA_DIR / "analysis_en_len03.txt",
    word_length: int = 3,
    diameter: Annotated[bool, typer.Option(help="Find graph diameter.")] = False,
    betweenness: Annotated[bool, typer.Option(help="Find graph betweenness.")] = False,
    community: Annotated[bool, typer.Option(help="Find graph communities.")] = False,
    aloof: Annotated[bool, typer.Option(help="Include aloof words")] = False,
    alphabet: str = "abcdefghijklmnopqrstuvwxyz",
):
    """
    Analyze a word graph from a pickle file.

    Includes betweenness centrality, community detection, and diameter analysis.

    :param input_path: Path to the graph pickle file
    :type input_path: Path
    """
    logger.info(f"Loading graph from {input_path}...")
    G = load_graph(input_path)
    logger.success(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    if not aloof:
        logger.info("Excluding aloof (degree=0) words...")
        no_aloof_nodes = [n for n, d in G.degree() if d > 0]
        G = G.subgraph(no_aloof_nodes)
        logger.success(
            f"Filtered graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges."
        )
    else:
        logger.info("Including aloof (degree=0) words...")

    if betweenness:
        logger.info("Finding betweenness centrality...")
        find_betweenness_centrality(G)

    if diameter:
        logger.info("Finding diameter...")
        find_diameter(G)

    if community:
        logger.info("Finding communities...")
        find_community(G)

    logger.success("Analysis complete.")


@app.command()
def main(
    input_path: Path = INTERIM_DATA_DIR / "en_words_len_03.txt",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
):
    logger.info("Loading data...")
    with open(input_path, "r", encoding="utf-8") as file:
        words = file.read()
    logger.info(f"Loaded {len(words.splitlines())} words.")

    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")


if __name__ == "__main__":
    app()
