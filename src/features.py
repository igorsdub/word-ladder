import itertools
from pathlib import Path
import pickle

from loguru import logger
import networkx as nx
from tqdm import tqdm
import typer

from src.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR, PROJ_ROOT

app = typer.Typer()


def get_hamming_distance(string1, string2):
    """Calculate the Hamming distance between two equal-length strings."""
    if len(string1) != len(string2):
        raise ValueError("Strings must be of equal length.")
    return sum(char1 != char2 for char1, char2 in zip(string1, string2))


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


@app.command()
def build_graph(
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
            if i < j and get_hamming_distance(n1, n2) == 1:
                G.add_edge(n1, n2)

    logger.success(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    logger.info(f"Saving graph to {output_path}...")
    save_graph(G, output_path)
    logger.success("Graph saved successfully.")


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
