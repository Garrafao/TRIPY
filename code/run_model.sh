### THIS SCRIPT CREATES ALIGNED LOW-DIMENSIONAL WORD EMBEDDINGS FOR A SET OF TIME-SPECIFIC CORPORA VIA RANDOM INDEXING AND CALCULATES COSINE DISTANCES FOR A SET OF TARGET WORDS ###

parameterfile=code/params_test.sh # Test parameters

# Load parameters
source $parameterfile

# Get vocabulary from corpus files
mkdir -p $vocabfolder/all
for corpus in "${corpora[@]}"
do
    python3 code/vocab.py $corpus $vocabfolder/all/$(basename "$corpus").txt
done

# Intersect vocabulary files
python3 code/intersect_vocab.py $vocabfolder/all/ $intvocabfile

# Make count-based vector spaces from corpora
mkdir -p $matrixfolder/count
for corpus in "${corpora[@]}"
do
    python3 code/count.py $corpus $intvocabfile $matrixfolder/count/$(basename "$corpus").count $win
done

# Create low-dimensional and sparse random matrix from intersected vocabulary file
python3 code/random.py $intvocabfile $matrixfolder/random $dim

# Create low-dimensional matrices from count matrices by multiplication with random matrix
matrices=($matrixfolder/count/*.count)
mkdir -p $matrixfolder/ri
for matrix in "${matrices[@]}"
do
    python3 code/multiply.py $matrix $matrixfolder/random $matrixfolder/ri/$(basename "$matrix").ri
done

# Get cosine distance for vectors target words in all combinations of reduced vector spaces
matrices1=($matrixfolder/ri/*.ri)
matrices2=($matrixfolder/ri/*.ri)
for matrix1 in "${matrices1[@]}"
do
    for matrix2 in "${matrices2[@]}"
    do
	if [ ! $matrix1 == $matrix2 ];
	then
	    python3 code/cd.py -s $testset $matrix1 $matrix2 $resultfolder/CD-$(basename "$matrix1")-$(basename "$matrix2").tsv
	fi
    done
done
