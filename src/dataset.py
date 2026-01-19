from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

import nltk

from src.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


@app.command()
def download(
):
    """Download the NLTK words dataset.
    Downloads `words.zip` to `RAW_DATA_DIR/corpora/` and unzips it to `words/`.
    The unzipped folder contains:
        `en` - a list of English words.
        `en-basic` - a list of basic English words.
        `README` - a README file describing the corpus.
    """    
    logger.info("Download dataset...")
    nltk.download('words', download_dir=RAW_DATA_DIR)
    logger.success("Downloading dataset complete.")

@app.command()
def filter(
    input_path: Path = RAW_DATA_DIR / "corpora" / "words" / "en",
    word_length: int = 3,
    proper_nouns: bool = False,
    output_dir: Path = INTERIM_DATA_DIR,
):
    """Filter the NLTK corpora English n-letter lowercase words.
    """    
    logger.info("Load dataset...")
    with open(input_path, "r") as f:
        words = f.read().splitlines()   
    logger.success("Loading dataset complete.")

    if not proper_nouns:
        logger.info("Remove proper nouns...")
        words =  [word for word in words if word.islower()]
        logger.success("Removal complete.")

    logger.info(f"Filtering {word_length}-letter lowercase words...")
    filtered_words = [word for word in words if len(word) == word_length]
    logger.success("Filtering complete.")

    logger.info(f"Saving filtered words to {output_dir / f'en_words_len_0{word_length}.txt'}...")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"en_words_len_0{word_length}.txt", "w") as f:
        for word in filtered_words:
            f.write(f"{word}\n")
    logger.success("Saving complete.")

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
