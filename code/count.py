from docopt import docopt
import logging
import time
from collections import defaultdict
from scipy.sparse import dok_matrix
from utils_ import Space
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Make count-based vector space from corpus.
    """

    # Get the arguments
    args = docopt("""Make count-based vector space from corpus.

    Usage:
        count.py <corpDir> <vocabFile> <outPath> <windowSize>
               
        <corpDir> = path to corpus or corpus directory (iterates through files)
        <vocabFile> = row and column vocabulary
        <outPath> = output path for vectors
        <windowSize> = the linear distance of context words to consider in each direction
        
    Note:
        Skips one-word sentences to avoid zero-vectors. Does not increase window size when out-of-vocabulary words are found.

    """)
    
    corpDir = args['<corpDir>']
    vocabFile = args['<vocabFile>']
    outPath = args['<outPath>']
    windowSize = int(args['<windowSize>'])    
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load vocabulary
    logging.info("Loading vocabulary")
    with open(vocabFile, 'r', encoding='utf-8') as f_in:
        vocabulary = [line.strip() for line in f_in]

    w2i = {w: i for i, w in enumerate(vocabulary)}
    
    # Initialize co-occurrence matrix as dictionary
    cooc_mat = defaultdict(lambda: 0)

    # Get counts from corpus
    logging.info("Counting context words")
    sentences = PathLineSentences(corpDir)
    for sentence in sentences:
        for i, word in enumerate(sentence):
            try:
                windex = w2i[word]
            except KeyError:
                continue
            lowerWindowSize = max(i-windowSize, 0)
            upperWindowSize = min(i+windowSize, len(sentence))
            window = sentence[lowerWindowSize:i] + sentence[i+1:upperWindowSize+1]
            if len(window)==0: # Skip one-word sentences
                continue
            for contextWord in window:
                try:
                    cindex = w2i[contextWord]
                except KeyError:
                    continue                
                cooc_mat[(windex,cindex)] += 1

    
    # Convert dictionary to sparse matrix
    logging.info("Converting dictionary to matrix")
    cooc_mat_sparse = dok_matrix((len(vocabulary),len(vocabulary)), dtype=float)
    try:
        cooc_mat_sparse.update(cooc_mat)
    except NotImplementedError:
        cooc_mat_sparse._update(cooc_mat)

    outSpace = Space(matrix=cooc_mat_sparse, rows=vocabulary, columns=vocabulary)
        
    # Save the matrix
    outSpace.save(outPath)

    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
