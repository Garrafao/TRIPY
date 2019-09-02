from docopt import docopt
import logging
import time
from sklearn.random_projection import sparse_random_matrix
from utils_ import Space
import numpy as np


def main():
    """
    Create low-dimensional and sparse random matrix from vocabulary file.
    """

    # Get the arguments
    args = docopt('''Create low-dimensional and sparse random matrix from vocabulary file.

    Usage:
        random.py <vocabFile> <outPath> <dim>

        <vocabFile> = row and column vocabulary
        <outPath> = output path for random matrix
        <dim> = dimensionality for random vectors

    Note:
        Calculates number of seeds automatically as proposed in [1,2]

    References:
        [1] Ping Li, T. Hastie and K. W. Church, 2006,
           "Very Sparse Random Projections".
           http://web.stanford.edu/~hastie/Papers/Ping/KDD06_rp.pdf
        [2] D. Achlioptas, 2001, "Database-friendly random projections",
           http://www.cs.ucsc.edu/~optas/papers/jl.pdf

    ''')
    np.random.seed(0)
    
    vocabFile = args['<vocabFile>']
    outPath = args['<outPath>']
    dim = int(args['<dim>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load vocabulary
    logging.info("Loading vocabulary")
    with open(vocabFile, 'r', encoding='utf-8') as f_in:
        vocabulary = [line.strip() for line in f_in]

    # Generate random vectors
    randomMatrix = sparse_random_matrix(dim,len(vocabulary)).toarray().T
    
    # Store random matrix
    Space(matrix=randomMatrix, rows=vocabulary, columns=[]).save(outPath)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    
if __name__ == '__main__':
    main()
