__author__ = 'jasper.zuallaert'
from network_topology_constructor import build_network_topology
from training_procedure import TrainingProcedure
from input_manager import get_sequences
import sys
from datetime import time
import tensorflow as tf

dataset_loc = {
    'pp': ('data/pp_perProtein/file_{}.dat'),
    'sc': ('data/sc_perProtein/file_{}.dat')
}

# The main script for running experiments. It combines calls to different python files.
def run(crossval_pt, dataset_name, predictions_file, varlen_red_strat, timestamp):
    if crossval_pt > 0:
        tf.reset_default_graph()

    ### Read in training, validation and test sets ##
    train_files,valid_files,test_files = get_filenames(dataset_loc[dataset_name],crossval_pt,10)

    train_set = get_sequences(datafiles=train_files)
    valid_set = get_sequences(datafiles=valid_files)
    test_set = get_sequences(datafiles=test_files)

    ### Build the topology ###
    nn, is_training = build_network_topology(varlen_red_strat = varlen_red_strat)


    ### Trains the network (and at the end, stores predictions on the test set) ###
    tp = TrainingProcedure(network_object=nn,
                           train_dataset=train_set,
                           valid_dataset=valid_set,
                           test_dataset=test_set,
                           is_training = is_training)

    sess = tp.train_network(predictions_file, crossval_pt, dataset_name, timestamp)
    sess.close()

def get_filenames(datafile_template, i, n_of_folds):
    numbers = set(range(n_of_folds))
    valid_num = i % n_of_folds
    test_num = (i + 1) % n_of_folds
    train_num = numbers - {valid_num} - {test_num}

    valid_files = [datafile_template.format(valid_num)]
    test_files = [datafile_template.format(test_num)]
    train_files = [datafile_template.format(n) for n in train_num]
    return train_files, valid_files, test_files

# run as: main.py <dataset> <varlen_reduction_strategy>
# with <dataset> one of: sc, pp
# with <varlen_reduction_strategy> one of: global_maxp, k_maxp, gru, zero_padding
if __name__ == '__main__':
    time = time()
    timestamp = time.strftime('%y%m%d-%H%M%S')
    dataset_name = sys.argv[1]
    varlen_red_strat = sys.argv[2]
    assert dataset_name in ['pp','sc']
    assert varlen_red_strat in ['global_maxp', 'k_maxp', 'gru', 'zero_padding']
    predictions_filename = 'predictions/{}_{}.txt'.format(dataset_name,timestamp)
    predictions_file = open(predictions_filename,'w')

    for crossval_pt in range(10):
        run(crossval_pt, dataset_name, predictions_file, varlen_red_strat, timestamp)

    predictions_file.close()
    import eval
    eval.run_eval(predictions_filename)

