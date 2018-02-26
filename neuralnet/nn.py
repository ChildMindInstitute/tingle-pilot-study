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
    l = list(np.zeros(total, int))
    l[index] = 1
    return(l)


def define_trainer_data(df, targets, training_columns, train_blocks):
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
    df = df[df.ontarget].copy()
    for i, target in enumerate(targets["target"]):
        for row in df[
            df.target==target
        ][training_columns].values.tolist():
            on_target.append(
                {
                    "input": row,
                    "output": place_true(
                        num_targets,
                        i
                    )
                }
            )
    for offtarget in targets["offtarget"]:
        for row in df[
            df.target==offtarget
        ][training_columns].values.tolist():
            on_target.append(
                {
                    "input": row,
                    "output": list(
                        np.zeros(
                            num_targets,
                            int
                        )
                    )
                }
            )
    return(on_target)