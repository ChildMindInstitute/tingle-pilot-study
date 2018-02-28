import numpy as np

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
        iteration blocks to include
        
    n_samples: int, optional
        exact number of samples to use
        
    exclude: int, optional
        exact number of initial samples to exclude
        
    scale: float, optional
        divisor to scale inputs
        
    Returns
    -------
    inputs: list of lists
        inputs[]: list of numeric
            input values
    """
    inputs = []
    num_targets = len(targets)
    df = df[
        (df.ontarget) &
        (df.iteration_block.isin(test_blocks))
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
                    [float(num)/float(scale) for num in row]
                )
                sample_n = sample_n + 1
    return(inputs)


def define_trainer_data(df, targets, training_columns, train_blocks, n_samples=None, scale=1):
    """
    Function to build training objects for neural networks from
    a DataFrame
    
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
        
    train_blocks: list of numerics
        iteration blocks to include
        
    n_samples: int, optional
        exact number of samples to use
        
    scale: float, optional
        divisor to scale inputs
        
    Returns
    -------
    on_target: list of dictionaries
        on_target[]["input"]: list of numeric
            input values
        on_target[]["output"]: list of numeric
            output values
    """
    on_target = []
    num_targets = len(targets["target"])
    df = df[
        (df.ontarget) &
        (df.iteration_block.isin(train_blocks))
    ].copy()
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
                        'input': [float(num)/float(scale) for num in row],
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
                (sample_n < n_samples)
            ):
                on_target.append(
                    {
                        'input': [float(num)/float(scale) for num in row],
                        'output': list(
                            np.zeros(
                                num_targets,
                                float
                            )
                        )
                    }
                )
    return(on_target)