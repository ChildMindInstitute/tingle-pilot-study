import numpy as np


def define_activation(df, targets, input_columns, test_blocks, n_samples=None, exclude=None, scale=1):
    """
    Function to build training objects for neural networks from
    a DataFrame
    
    Parameters
    ----------
    df: DataFrame
    
    targets: list of strings
        list of targets (values in df.target)
            
    input_columns: list of strings
        columns to include as inputs
        
    test_blocks: list of numerics
        steps to include
        
    n_samples: int, optional
        exact number of samples to use
        
    exclude: int, optional
        exact number of initial samples to exclude
        
    scale: list of floats, optional
        divisors to scale inputs, one per input column
        
    Returns
    -------
    inputs: list of lists
        inputs[]: list of numeric
            input values
    """
    scale = [
        df[input_column].astype(float).max() for input_column in input_columns
    ]
    inputs = []
    num_targets = len(targets)
    df = df[
        (df.ontarget) &
        (df.step.isin(test_blocks))
    ].copy()
    for i, target in enumerate(targets):
        sample_n = 0
        for row in df[
            df.target==target
        ][input_columns].values.tolist():
            if (exclude and sample_n < exclude):
                sample_n = sample_n + 1
                continue
            elif (
                (not n_samples)
                or
                (sample_n < n_samples)
            ):
                inputs.append(
                    [
                        float(num)/float(
                            scale[row_i]
                        ) for row_i, num in enumerate(row)
                    ]
                )
                sample_n = sample_n + 1
    return(inputs)


def define_trainer_data(df, targets, training_columns, n_samples=None):
    """
    Function to build training objects for neural networks from
    a DataFrame, casting training columns to relative z-scores.
    
    Parameters
    ----------
    df: DataFrame
    
    targets: dictionary
        targets["target"]: list of strings
            list of targets (values in df.target)
        targets["offtarget"]: list of strings
            list of offtargets (values in df.target)
            
    training_columns: list of strings
        columns to include as inputs
        
    n_samples: int, optional
        exact number of samples to use
        
    Returns
    -------
    on_target: list of dictionaries
        on_target[]["input"]: list of numeric
            input values
        on_target[]["output"]: list of numeric
            output values
            
    Example
    -------
    >>> import pandas as pd
    >>> import os
    >>> import sys
    >>> sys.path.append(os.path.abspath(
    ...     os.getcwd()
    ... ))
    >>> from data.dataloader import correct_targets, combine_coordinators
    >>> from urllib.request import urlretrieve
    >>> temp_fake_data = "temp_fake_data.csv"
    >>> if not os.path.exists(
    ...     os.path.abspath(
    ...         os.path.dirname(temp_fake_data)
    ...     )
    ... ):
    ...     os.makedirs(
    ...         os.path.abspath(
    ...             os.path.dirname(temp_fake_data)
    ...         )
    ...     )
    >>> temp_file = urlretrieve(
    ...     "{1}{0}{2}".format(
    ...         "1kgZJrKTDSI5xg9uAD_LAYq2PrM20nAmxEiyJ597coKk",
    ...         'https://docs.google.com/spreadsheets/d/',
    ...         '/export?format=csv'
    ...     ),
    ...     temp_fake_data
    ... )
    >>> fake_data = correct_targets(
    ...     combine_coordinators(
    ...         pd.read_csv(temp_fake_data)
    ...     ),
    ...     'http://matter.childmind.org/js/tinglePilotAppScript.json'
    ... )
    >>> fake_data.loc["2018-03-22 17:23:33", "ontarget"] = True
    >>> define_trainer_data(
    ...     fake_data,
    ...     {'target': ['food'], 'offtarget': ['offbody-spiral']},
    ...     ["distance", "thermopile1", "thermopile2", "thermopile3", "thermopile4"]
    ... )[1]['input'][0]
    0.7071067811865475
    """
    on_target = []
    num_targets = len(targets["target"])
    df = df[
        (df.ontarget)
    ].copy()
    for column in training_columns:
        df[column] = df[column].astype(float)
        df[column] = (
            df[column] - df[column].mean()
        ) / df[column].std()
    for i, target in enumerate(targets["target"]):
        sample_n = 0
        for row in df[
            df.target==target
        ][training_columns].values.tolist():
            if (
                (not n_samples)
                or
                (sample_n < n_samples)
            ):
                on_target.append(
                    {
                        'input': [
                            float(num) for num in row
                        ],
                        'output': place_true(
                            num_targets,
                            i
                        )
                    }
                )
                sample_n = sample_n + 1
    for offtarget in targets["offtarget"]:
        sample_n = 0
        for row in df[
            df.target==offtarget
        ][training_columns].values.tolist():
            if (
                (not n_samples)
                or
                (sample_n < n_samples//3)
            ):
                on_target.append(
                    {
                        'input': [
                            float(num) for num in row
                        ],
                        'output': list(
                            np.zeros(
                                num_targets,
                                float
                            )
                        )
                    }
                )
    return(on_target)


def place_true(total, index):
    """
    Function to place one 1 in a list of 0s
    
    Parameters
    ----------
    total: int
        length of list of zeroes
        
    index: int
        0-indexed placement of 1
        
    Returns
    -------
    l: list of ints
        one-hot list
    """
    l = list(
        np.zeros(
            total,
            float
        )
    )
    l[index] = 1.0
    return(l)