import itertools
from pathlib import Path
import pickle

from loguru import logger
import networkx as nx
from tqdm import tqdm
import typer

from src.config import INTERIM_DATA_DIR, PROCESSED_DATA_DIR

app = typer.Typer()


def get_hamming_distance(string1, string2):
    """Calculate the Hamming distance between two equal-length strings."""
    if len(string1) != len(string2):
        raise ValueError("Strings must be of equal length.")
    return sum(char1 != char2 for char1, char2 in zip(string1, string2))


@app.command()
def build_graph(
    output_path: Path = INTERIM_DATA_DIR / "graph_en_len_03.pkl",
    word_length: int = 3,
    alphabet: str = "abcdefghijklmnopqrstuvwxyz",
):
    """
    Build a complete word graph of given word length and alphabet.

    :param output_dir: Description
    :type output_dir: Path
    :param word_length: Description
    :type word_length: int
    """

    # Convert alphabet string to set
    alphabet = list(alphabet)

    # Construct all possible words of given length
    logger.info("Constructing all possible words...")
    nodes = ["".join(p) for p in itertools.product(alphabet, repeat=word_length)]
    logger.success(
        f"Constructed {len(nodes)} words of length {word_length} and alhabet size {len(alphabet)}."
    )

    logger.info("Intializing word graph...")
    G = nx.Graph()
    G.add_nodes_from(nodes)

    logger.info("Adding edges to word graph...")
    # tqdm for progress bar

    for i, node1 in tqdm(enumerate(nodes), total=len(nodes)):
        for j, node2 in enumerate(nodes):
            if i < j and get_hamming_distance(node1, node2) == 1:
                G.add_edge(node1, node2)

    logger.info(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    logger.info(f"Saving graph to {output_path}...")
    pickle.dump(G, open(output_path, "wb"))
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
