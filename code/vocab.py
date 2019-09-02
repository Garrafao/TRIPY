from docopt import docopt
import logging
import time
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Get vocabulary from corpus file.
    """

    # Get the arguments
    args = docopt("""Get vocabulary from corpus file.

    Usage:
        vocab.py <corpDir> <outPath>

        <corpDir> = path to corpus or corpus directory (iterates through files)
        <outPath> = output path for result file
        
    Note:
        Skips one-word sentences to avoid zero-vectors.

    """)
    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    logging.info("Building vocabulary")
    sentences = PathLineSentences(corpDir)
    vocabulary = sorted(list(set([word for sentence in sentences for word in sentence if len(sentence)>1]))) # Skip one-word sentences to avoid zero-vectors
        
    logging.info("Exporting vocabulary")
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for v in vocabulary:   
            f_out.write(v+'\n')
                
    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    

if __name__ == '__main__':
    main()
