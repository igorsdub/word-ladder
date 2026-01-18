# The Word Ladder Game

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

An exoloartion of the word ladder game thorugh the graph theory. This game is a word puzzle invented by Lewis Carroll in 1878, where players transform one word into another by changing one letter at a time, with each intermediate step being a valid word. In computer science, the Word Ladder became a classic problem for exploring graph traversal algorithms, such as breadth-first search (BFS) and depth-first search (DFS).

## Project Organization

```
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

# References

- [Word Ladder Algorithm](https://bradfieldcs.com/algos/graphs/word-ladder/) by Bradfield CS
- [Laddergrams](https://blogs.mathworks.com/community/2023/01/25/laddergrams/) by Ned Gulley
- [Word Ladder](https://en.wikipedia.org/wiki/Word_ladder) on Wikipedia
- [Word Ladder Analysis](https://www.garrettsidle.com/Blog?id=word-ladder-analysis) at Garrett Sidle blog
- [New Word Ladder Game Bot with Scoring Based on Graphs](https://community.wolfram.com/groups/-/m/t/908570) by Irina Tirosyan
- [Generating Word Ladders Using Adjacency Matrices](https://community.wolfram.com/groups/-/m/t/2928331) by Chase Marangu
- [Word Ladders with Julia](https://numbersandshapes.net/posts/word_ladders_with_julia/) at Numbers and Shapes blog 
