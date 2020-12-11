# Massively parallel interrogation of protein fragment secretability using SECRiFY reveals features influencing secretory system transit

This is the python code for training, evaluating and visualizing a convolutional neural network for secretability prediction. The corresponding paper can be found at 
```https://www.biorxiv.org/content/10.1101/241349v4```

Packages used:
```
tensorflow v1.5.0
numpy v1.16.4
sklearn v0.23.1
```

# (i) Create data files for cross-validation #

From the results tables found online, and put in a directory `initial_data`, you can prepare the datafiles used in these scripts. This can be done by simply running

Uses files:
- `initial_data/Pp_resultstable_enriched.txt`
- `initial_data/Pp_resultstable_depleted.txt`
- `initial_data/Sc_resultstable_enriched.txt`
- `initial_data/Sc_resultstable_depleted.txt`
```
python create_data_files.py
```
The files containing the different folds for cross-validation are saved in the directory `data`.

# (ii) Train a convolutional neural network model #

The neural network model is constructed and trained by executing the `main.py` script.

```
python main.py <dataset> <varlen_reduction_strategy> 
```
Args:
- `dataset` one of `pp`, `sc`
- `varlen_reduction_strategy` one of `global_maxp`, `k_maxp`, `gru`, `zero_padding`

Predictions over all folds are stored in a single file in the `predictions` directory. Trained model parameters for all folds are stored in the `parameters` directory, with one file per fold. Finally, the `AUROC` and `AUPRC` are calculated for all predictions.

It is also possible to calculate the `AUROC` and `AUPRC` afterwards. To this end, execute

```
python eval.py <prediction_file>
```

# (iii) Visualize important input features using integrated gradients #

Using the model parameters (using the stored files with their original names), feature contribution can be calculated by running the following command. Note that output is written to `stdout`.

```
python vis_calc_ig.py <parameter_file> <dataset_name>
```
Args:
- `parameter_file` one of the parameter directories (ending in foldX) in the `parameters` directory
- `dataset` one of `pp`, `sc`

Then, the calculated contributions can be normalized using `vis_normalize_ig`. Note that output is written to `stdout`.
```
python vis_normalize_ig.py <old_file_name> > <normalized_file_name>
```

And finally, the normalized values can be aggregated by running:
```
python vis_quantify_ig.py <normalized_file_name>
```
We recommend to then copy this to an excel spreadsheet to start analyzing the result.