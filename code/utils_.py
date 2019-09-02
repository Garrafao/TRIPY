import pickle
from scipy.sparse import csr_matrix, load_npz, save_npz, linalg
import numpy as np
import logging


class Space(object):
    """
    Load and save Space objects.
    """
        
    def __init__(self, path=None, matrix=csr_matrix([]), rows=[], columns=[], format='npz'):
        """
        Can be either initialized (i) by providing a path, (ii) by providing a matrix, rows and columns, or (iii) by providing neither, then an empty instance is created
        `path` should be path to a matrix in npz format, expects rows and columns in same folder at '[path]_rows' and '[path]_columns'
        `rows` list with row names
        `columns` list with column names
        `format` format of matrix, can be either of 'npz' or 'w2v'
        """
        
        if path!=None:
            if format=='npz':
                # Load matrix
                matrix = load_npz(path)
                # Load rows
                with open(path + '_rows', 'rb') as f:
                    rows = pickle.load(f)
                # Load columns
                with open(path + '_columns', 'rb') as f:
                    columns = pickle.load(f)
            elif format=='w2v':
                matrix_array = np.loadtxt(path, dtype=object, delimiter=' ', skiprows=1, encoding='utf-8')
                matrix = matrix_array[:,1:].astype(np.float)
                rows = list(matrix_array[:,0].flatten())
                columns = []             
            else:      
                message = "Matrix format {0} unknown."
                logging.error(message.format(format))

        row2id = {r:i for i, r in enumerate(rows)}
        id2row = {i:r for i, r in enumerate(rows)}
        column2id = {c:i for i, c in enumerate(columns)}
        id2column = {i:c for i, c in enumerate(columns)}

        self.matrix = csr_matrix(matrix)
        self.rows = rows
        self.columns = columns
        self.row2id = row2id
        self.id2row = id2row
        self.column2id = column2id
        self.id2column = id2column      
        
    def save(self, path, format='npz'):
        """
        `path` saves matrix at path in npz format, saves rows and columns as pickled lists in same folder at '[path]_rows' and '[path]_columns'
        `format` format of matrix, can be either of 'npz' or 'w2v'
        """
        
        if format=='npz':       
            # Save matrix
            with open(path, 'wb') as f:
                save_npz(f, self.matrix)    
            # Save rows
            with open(path + '_rows', 'wb') as f:
                pickle.dump(self.rows, f)
            # Save columns
            with open(path + '_columns', 'wb') as f:
                pickle.dump(self.columns, f)
        elif format=='w2v':
            matrix = self.matrix.toarray().astype(object)
            rows = np.array(self.rows)
            r, d = matrix.shape
            rows = rows.reshape(-1,1)
            matrix = np.concatenate((rows, matrix), axis=1)
            np.savetxt(path, matrix, fmt=["%s"] + ['%.16g',]*d, delimiter=' ', newline='\n', header='%d %d' %(r, d), comments='', encoding='utf-8')
        else:      
            message = "Matrix format {0} unknown."
            logging.error(message.format(format))

    def l2_normalize(self):
        '''
        L2-normalize all vectors in the matrix.
        '''
        l2norm = linalg.norm(self.matrix, axis=1, ord=2)
        l2norm[l2norm==0.0] = 1.0 # Convert 0 values to 1
        self.matrix = csr_matrix(self.matrix/l2norm.reshape(len(l2norm),1))

    def mean_center(self):
        '''
        Mean center all columns in the matrix.
        '''
        avg = np.mean(self.matrix, axis = 0)
        self.matrix = csr_matrix(self.matrix - avg)
