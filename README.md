# TRIPY
A highly efficient Python implementation of Temporal Random Indexing (TRI)

This is a re-implementation of major parts from the [original TRI implementation](https://github.com/pippokill/tri). With the code in this repository you can create aligned low-dimensional word embeddings for a set of time-specific corpora via Random Indexing. You can then track how the vectors of words change over time with cosine distance, indicating changes in word usage.

If you use this software for academic research, please [cite](#bibtex) these papers:

- Dominik Schlechtweg, Anna Hätty, Marco del Tredici, and Sabine Schulte im Walde. 2019. [A Wind of Change: Detecting and Evaluating Lexical Semantic Change across Times and Domains](https://www.aclweb.org/anthology/papers/P/P19/P19-1072/). In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pages 732-746, Florence, Italy. ACL.

- Pierpaolo Basile, Annalina Caputo, and Giovanni Semeraro. 2014. [Analysing Word Meaning over Time by Exploiting Temporal Random Indexing](http://ceur-ws.org/Vol-1568/paper7.pdf). In Proceedings of the First Italian Conference on Computational Linguistics CLiC-it 2014, Pisa.

### Usage

All scripts can be run directly from the command line:

	python3 code/vocab.py <corpDir> <outPath>

e.g.

	python3 code/vocab.py corpora/test/corpus1/ vocab1.txt

The usage of each script can be understood by running it with help option `-h`, e.g.:

	python3 code/vocab.py -h

We recommend you to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.7.4. Install the required packages running `pip install -r requirements.txt`.

### Model

The model creates aligned low-dimensional word embeddings for a set of time-specific corpora via Random Indexing. It runs through the following steps using the scripts under `code/`:

1. get vocabulary for each corpus (`vocab.py`)
2. build common vocabulary (`intersect_vocab.py`)
3. make count-based vector spaces from corpora (`count.py`)
4. create shared low-dimensional sparse random matrix (`random.py`)
5. create low-dimensional embeddings from count matrices by multiplication with shared random matrix (`multiply.py`)

You can then get cosine distances for vectors of chosen target words from the aligned low-dimensional embeddings with `cd.py`.

The script `run_model.sh` runs the model over two small test corpora. Assuming you are working on a UNIX-based system, first make the scripts executable with

	chmod 755 code/*.sh

Then run the following command from the main directory

	bash -e code/run_model.sh

The script reads the two test corpora `corpora/test/corpus1/` and `corpora/test/corpus2/`, and executes the steps described above. Then, it calculates cosine distances for the test targets in `testsets/test/targets.tsv` and writes them under `results/`.

The easiest way to run the model on your own data is to change the parameters in `params_test.sh`.

__Matrix Format__: Matrices are stored as sparse scipy matrices in [npz format](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.save_npz.html). To learn more about how matrices are loaded and stored check out `utils_.py`.

__Corpus Format__: The scripts assume a corpus format of one sentence per line in UTF-8 encoded (optionally zipped) text files. You can specify either a file path or a folder. In the latter case the scripts will iterate over all files in the folder.

__Note__: The number of corpora that can be compared is not limited to 2, but unlimited. Also, the corpora do not have to be time-specific but can be e.g. domain-specific (see Schlechtweg et al., 2019, for an application).


### Performance

Find an evaluation and comparison of TRI in Schlechtweg et al. (2019). Models and evaluation data for lexical semantic change detection can be found at [LSCDetection](https://github.com/Garrafao/LSCDetection).


BibTex
--------

```
@inproceedings{Schlechtwegetal19,
	title = {{A Wind of Change: Detecting and Evaluating Lexical Semantic Change across Times and Domains}},
	author = {Dominik Schlechtweg and Anna H\"{a}tty and Marco del Tredici and Sabine {Schulte im Walde}},
    booktitle = {Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics},
	year =  {2019},
	address =  {Florence, Italy},
	publisher =  {Association for Computational Linguistics},
	pages     = {732--746}
}
```
```
@inproceedings{Basileetal14,
	title = {{Analysing Word Meaning over Time by Exploiting Temporal Random Indexing}},
	year = {2014},
	author = {Pierpaolo Basile and Annalina Caputo and Giovanni Semeraro},
	booktitle = {First Italian Conference on Computational Linguistics CLiC-it 2014},
	editor = {Roberto Basili and Alessandro Lenci and Bernardo Magnini},
	publisher = {Pisa University Press}
}
```

