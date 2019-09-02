from docopt import docopt
import logging
import time
import numpy as np
from utils_ import Space


def main():
    """
    Create low-dimensional matrix from count matrix by multiplication with random matrix.
    """

    # Get the arguments
    args = docopt('''Create low-dimensional matrix from count matrix by multiplication with random matrix.

    Usage:
        multiply.py [-l] [-c] <countPath> <randomPath> <outPath>

        <countPath> = path to count matrix
        <randomPath> = path to random matrix
        <outPath> = output path for reduced matrix

    Options:
        -l, --len   normalize final vectors to unit length
        -c, --cen   mean center columns of final matrix

    ''')
    
    is_len = args['--len']
    is_cen = args['--cen']
    countPath = args['<countPath>']
    randomPath = args['<randomPath>']
    outPath = args['<outPath>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices
    countSpace = Space(countPath)   
    countMatrix = countSpace.matrix
    randomSpace = Space(randomPath)   
    randomMatrix = randomSpace.matrix

    logging.info("Multiplying matrices")
    reducedMatrix = np.dot(countMatrix,randomMatrix)    
    reducedSpace = Space(matrix=reducedMatrix, rows=countSpace.rows, columns=[])
        
    if is_len:
        logging.info("L2-normalize vectors")
        reducedSpace.l2_normalize()

    if is_cen:
        logging.info("Mean center columns")
        reducedSpace.mean_center()
        
    # Save the reduced matrix
    reducedSpace.save(outPath)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
