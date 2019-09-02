win=1 # window size
dim=100 # vector dimensionality
corpora=(corpora/test/*)
vocabfolder=vocab/test
intvocabfile=($vocabfolder/intersected_vocab.txt)
matrixfolder=matrices/test
resultfolder=results/test
testset=testsets/test/targets.tsv

mkdir -p $vocabfolder
mkdir -p $matrixfolder
mkdir -p $resultfolder
