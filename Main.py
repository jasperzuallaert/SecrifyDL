__author__ = 'jasper.zuallaert'
import InputManager as im
from NetworkTopologyConstructor import buildNetworkTopology
from TrainingProcedure import TrainingProcedure
from InputManager import getSequences


# The main script for running experiments. It combines calls to different python files.
# - testParameters: an object of TestLauncher.Parameters, indicating what kind of experiment should be executed
def run(testParameters, n, predictions_file):
    if n > 0:
        import tensorflow as tf
        tf.reset_default_graph()

    datafile = testParameters.datafiles

    ### Read in training, validation and test sets ##
    trainFiles,validFiles,testFiles = getFilenames(datafile,n,10)

    train_set = getSequences(datafiles=trainFiles,
                            maxLength=testParameters.maxLength,
                            minimumLength=testParameters.minimumLength,
                            throwAwayTooLong=testParameters.throwAwayTooLong,
                            clipFront=testParameters.clipFront,
                            clipBack=testParameters.clipBack,
                            ss=testParameters.ss,
                            contSS=testParameters.continuousSS,
                            includeSeq = testParameters.includeSeq)
    valid_set = getSequences(datafiles=validFiles,
                            maxLength=testParameters.maxLength,
                            minimumLength=testParameters.minimumLength, # never throw away validation sequences
                            throwAwayTooLong=testParameters.throwAwayTooLong,
                            clipFront=testParameters.clipFront,
                            clipBack=testParameters.clipBack,
                            ss=testParameters.ss,
                            contSS=testParameters.continuousSS,
                            includeSeq = testParameters.includeSeq)
    test_set = getSequences(datafiles=testFiles,
                            maxLength=testParameters.maxLength,
                            minimumLength=testParameters.minimumLength, # never throw away test sequences
                            throwAwayTooLong=testParameters.throwAwayTooLong,
                            clipFront=testParameters.clipFront,
                            clipBack=testParameters.clipBack,
                            ss=testParameters.ss,
                            contSS=testParameters.continuousSS,
                            includeSeq = testParameters.includeSeq)

    ### Build the topology as described in the input file ###
    nn, isTraining = buildNetworkTopology(type = testParameters.type,
                              maxLength = testParameters.maxLength,
                              filterSizes = testParameters.filterSizes,
                              filterAmounts = testParameters.filterAmounts,
                              maxPoolSizes = testParameters.maxPoolSizes,
                              sizeOfFCLayers = testParameters.sizeOfFCLayers,
                              n_of_outputs = train_set.getClassCounts(),
                              dynMaxPoolSize = testParameters.dynMaxPoolSize,
                              GRU_state_size= testParameters.GRU,
                              batchnorm = testParameters.batchnorm,
                              ss = testParameters.ss,
                              includeSeq=testParameters.includeSeq)


    ### Trains the network (and at the end, stores predictions on the test set) ###
    tp = TrainingProcedure(network_object=nn,
                           train_dataset=train_set,
                           valid_dataset=valid_set,
                           test_dataset=test_set,
                           batch_size=testParameters.batchsize,
                           start_learning_rate=testParameters.start_learning_rate,
                           validationFunction=testParameters.validationFunction,
                           update=testParameters.update,
                           dropoutRate=testParameters.dropout,
                           l1reg=testParameters.l1reg,
                           isTraining = isTraining)

    sess = tp.trainNetwork(testParameters.epochs,predictions_file,n)
    sess.close()

def getFilenames(datafile,i,n_of_folds):
    numbers = set(range(n_of_folds))
    validNum = i % n_of_folds
    testNum = (i + 1) % n_of_folds
    trainNum = numbers - {validNum} - {testNum}

    validFiles = [datafile.format(validNum)]
    testFiles = [datafile.format(testNum)]
    trainFiles = [datafile.format(n) for n in trainNum]
    return trainFiles, validFiles, testFiles