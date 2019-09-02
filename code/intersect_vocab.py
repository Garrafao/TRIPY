from docopt import docopt
import logging
import time
import os


def main():
    """
    Intersect vocabulary files.
    """

    # Get the arguments
    args = docopt("""Intersect vocabulary files.

    Usage:
        intersect_vocab.py <inputDir> <outPath>

        <inputDir> = path to folder with vocabulary files
        <outPath> = output path for result file

    """)
    
    inputDir = args['<inputDir>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    logging.info("Iterating over input files")

    vocab_out = set()
    for subdir, dirs, files in os.walk(inputDir):
        for i, f in enumerate(files):
            path = os.path.join(subdir, f)
            logging.info("Loading %s" % (path))
            with open(path, 'r', encoding='utf-8') as f_in:
                vocab_in = set([line.strip() for line in f_in])
            if i==0:
                vocab_out = vocab_in
            else:    
                vocab_out = vocab_out.intersection(vocab_in)
        
    logging.info("Exporting vocabulary")
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for v in sorted(list(vocab_out)):   
            f_out.write(v+'\n')
                
    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    

if __name__ == '__main__':
    main()
