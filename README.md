# The Word Ladder Game

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

An exoloartion of the word ladder game thorugh the graph theory. This game is a word puzzle invented by Lewis Carroll in 1878, where players transform one word into another by changing one letter at a time, with each intermediate step being a valid word. In computer science, the Word Ladder became a classic problem for exploring graph traversal algorithms, such as breadth-first search (BFS) and depth-first search (DFS).

## Project Organization

```tree
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         src and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## Workflow

### Dataset

The dataset used in this project is a comprehensive English word list sourced from the NLTK library.
To download the dataset, run the following command:

```bash
pyhton src/dataset.py download
```

`data/raw/corpora/words/en` contains the word list in a text file format, with one word per line.

```bash
wc -l data/raw/corpora/words/en
  235886 data/raw/corpora/words/en
```

```bash
head -n 5 data/raw/corpora/words/en
A
a
aa
aal
aalii
```

We will filter words of the same length for the further analysis. Note, that the dataset contains pronouns, words that start with an uppercase letter. Pronouns will be filtered out as well.

```bash
python src/dataset.py filter --word-length 3
```

```bash
wc -l data/interim/en_words_len_03.txt               
    1135 data/interim/en_words_len_03.txt
```

```bash
head -n 5 data/interim/en_words_len_03.txt 
aal
aam
aba
abb
abu
```

### Graph

Next, we will create a graph where each node represents a word, and an edge connects two nodes if the corresponding words differ by exactly one letter. We will use the NetworkX library to construct and analyze the graph.

To build the graph, run the following command:

```bash
python src/features.py build-graph --word-length 3
```

This command uses the English alphabet (a-z) to find all possible one-letter transformations for each word in the filtered dataset. The resulting graph is saved in the `data/interim` directory in Pickle `.pkl` format.

Next, we assign `is_valid_word` attribute to each node in the graph. A valid word is defined as a word that exists in the original dataset. The, we conncet nodes with `is_valid_word=True` if they differ by one letter.

```bash
python src/features.py assign-valid-words --word-length 3
```

### Plot

Let's visualize the graph to see the connections between words. We will use Plotly to create a visual representation of the graph.

```bash
python src/plots.py plot-graph
```

This command generates an interactive plot of the word ladder graph and saves it as an HTML file in the `reports/figures` directory.

#### Issues

"new text' label appears at the center of the plot. This StackOverflow [thread](https://stackoverflow.com/questions/70792555/plotly-network-graph-new-text-label-appears-at-center-of-plot) discusses this issue.

Another issue is with NetworkX `spring_layout` function that may produce different layouts on different runs due to its random initialization. Even though `seed=42`, every time a new layout is generated.

## References

- [Word Ladder Algorithm](https://bradfieldcs.com/algos/graphs/word-ladder/) by Bradfield CS
- [Laddergrams](https://blogs.mathworks.com/community/2023/01/25/laddergrams/) by Ned Gulley
- [Word Ladder](https://en.wikipedia.org/wiki/Word_ladder) on Wikipedia
- [Word Ladder Analysis](https://www.garrettsidle.com/Blog?id=word-ladder-analysis) at Garrett Sidle blog
- [New Word Ladder Game Bot with Scoring Based on Graphs](https://community.wolfram.com/groups/-/m/t/908570) by Irina Tirosyan
- [Generating Word Ladders Using Adjacency Matrices](https://community.wolfram.com/groups/-/m/t/2928331) by Chase Marangu
- [Word Ladders with Julia](https://numbersandshapes.net/posts/word_ladders_with_julia/) at Numbers and Shapes blog
- [Newtwork Graphs in Pyhton wiht Plotly](https://plotly.com/python/network-graphs/)
