import colored
from colored import stylize
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from itertools import chain
import numpy as np
import os
import pandas as pd
import requests


def combine_coordinators(data):
    """
    Function to combine coordinator rows from 2 to 1.

    Parameter
    ---------
    data : DataFrame
        DataFrame with separate coordinator rows

    Returns
    -------
    data : DataFrame
        DataFrame with combined coordinator rows

    Example
    -------
    >>> import pandas as pd
    >>> import os
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
    >>> fake_data = pd.read_csv(temp_fake_data)
    >>> tuple(
    ...     combine_coordinators(fake_data)[
    ...         [
    ...             "firstCoordinator",
    ...             "secondCoordinator"
    ...         ]
    ...     ].values
    ... )[0]
    array(['Mike Logan', 'Ben Stone'], dtype=object)
    """
    c1 = data[(
        data.thermopile1 != False
    ) & (
        data.thermopile1 != "False"
    )].set_index("human-readable timestamp")
    c2 = data[(
        data.thermopile1 == False
    ) | (
        data.thermopile1 == "False"
    )].set_index("human-readable timestamp")
    c2 = c2.drop_duplicates().reindex(
        c1.drop_duplicates().index,
        method="ffill",
        limit=1
    )
    c1[['firstCoordinator', 'coordinator1']] = c1[
        ['coordinator', 'ontarget']
    ]
    c2[['secondCoordinator', 'step_c2', 'coordinator2']] = c2[
        ['coordinator', 'step', 'ontarget']
    ]
    c2 = c2[['secondCoordinator', 'step_c2', 'coordinator2']].copy()
    c1.drop(["coordinator", "ontarget"], axis=1, inplace=True)
    c = pd.concat([c1, c2], axis=1)
    c["step_c2"] = c["step_c2"].ffill()
    c["ontarget"] = c[
        (c["coordinator1"] == c["coordinator2"])
        &
        (c["step"] == c["step_c2"])
    ]["coordinator1"]
    c["human-readable timestamp"] = pd.to_datetime(
        c["timestamp"]*1000000
    )
    return(
        c
    )


def correct_corrections(df, corrections):
    """
    Function to correct data entry errors

    Parameters
    ----------
    df: DataFrame

    corrections: dictionary
        key: participant number
        value: dictionary
            key: column
            value: dictionary
                key: incorrect value
                value: dictionary
                    key: string
                        "value" or "column"
                    value: anything that can go in a DataFrame cell
                        value or column name

    Returns
    -------
    df2: DataFrame
        updated
        
    Example
    -------
    
    """
    df2 = df.copy()
    for participant in corrections:
        for col in corrections[participant]:
            for incorrect in corrections[
                participant
            ][
                col
            ]:
                value = corrections[
                    participant
                ][
                    col
                ][
                    incorrect
                ][
                    "value"
                ] if "value" in corrections[
                    participant
                ][
                    col
                ][
                    incorrect
                ] else None
                df2.loc[
                    list(
                        df[
                            (
                                df.participant==int(
                                    participant
                                )
                            ) & (
                                df[col].astype(
                                    str
                                ) == str(
                                    incorrect
                                )
                            )
                        ].index
                    ),
                    col
                ] = value if value else df.loc[
                    list(
                        df[
                            (
                                df.participant==int(
                                    participant
                                )
                            ) & (
                                df[col].astype(
                                    str
                                ) == str(
                                    incorrect
                                )
                            )
                        ].index
                    ),
                    corrections[
                        participant
                    ][
                        col
                    ][
                        incorrect
                    ][
                        "column"
                    ]
                ]
    return(df2)


def correct_targets(df, targets):
    """
    Function to update targets that were steamrolled
    during data collection. 🧖

    Parameters
    ----------
    df: DataFrame

    targets: dictionary
        key: numeric
            step
        value: string
            target
        or string
            URL to JSON with respective
            labels "number" and "target" for key and
            value

    Returns
    -------
    df: DataFrame
    """
    if isinstance(
        targets,
        str
    ):
        targets = pd.DataFrame(
            requests.get(
                url=targets
            ).json()
        )[
            [
                "number",
                "target"
            ]
        ].set_index(
            "number"
        ).drop(
            999,
            axis=0
        ).T.to_dict(
            "records"
        )[0]
    df["target"] = df.step.apply(
        lambda x: targets[x]
    )
    return(df)


def count_ontarget_samples(df, human_readable=False):
    """
    Function to count usable samples.

    Parameters
    ----------
    df: DataFrame

    human_readable: Boolean, optional
        default=False

    Returns
    -------
    ontarget_counts: DataFrame
        MultiIndexed if human_readable, otherwise
        "step" by "participant"
    """
    ontarget_counts = df[
        (df["ontarget"]==True)
    ][
        ["step", "target", "participant", "ontarget"]
    ].groupby(
        ["step", "target", "participant"]
    ).count().unstack(fill_value=0)
    if human_readable:
        return(ontarget_counts)
    ontarget_counts.set_index(
        ontarget_counts.index.droplevel("target"),
        inplace=True
    )
    ontarget_counts.columns = ontarget_counts.columns.droplevel()
    return(ontarget_counts)


def dropX(df, X=["X", "x"]):
    """
    Function to drop data annotated to drop.

    Parameters
    ----------
    df: DataFrame

    X: list of strings, optional
        notes values indicating to drop an iteration

    Returns
    -------
    df: DataFrame
    """
    drop = []
    for i, row in df[df["notes"].apply(
        lambda x: str(x).strip()
    ).isin(X)][
        ["step", "human-readable timestamp"]
    ].iterrows():
        drop.extend(
            list(
                df[
                    (df["step"] == row.step)
                    &
                    (df["human-readable timestamp"] >= row[
                        "human-readable timestamp"
                    ] - datetime.timedelta(minutes=5))
                    &
                    (df["human-readable timestamp"] <= row[
                        "human-readable timestamp"
                    ])
                ].index
            )
        )
    return(df.drop(drop))


def index_participants(df, starting_index=1):
    """
    Function to index participants

    Parameter
    ---------
    df: DataFrame
    
    starting_index: int
        index for first participant found

    Returns
    -------
    participants_df: DataFrame

    Example
    -------
    >>> import pandas as pd
    >>> import os
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
    >>> fake_data = pd.read_csv(temp_fake_data)
    >>> fake_data = fake_data.reset_index(drop=True)
    >>> index_participants(fake_data).participant.unique()
    array([1, 2])
    """
    participants = {}
    # initialize as if participant 0 just finished
    participant = starting_index - 1
    task = 47
    p_index = []
    for i, r in df.iterrows():
        if (r.step == 1) and (task > r.step):
            participant = participant + 1
            participants[participant] = r["human-readable timestamp"]
        task = r.step
        p_index.append(participant)
    df["participant"] = p_index
    return(df)


def load_from_firebase(
    dbURL="https://tingle-pilot-collected-data.firebaseio.com/",
    notes=False,
    start=None,
    stop=None,
    combine=False,
    marked=False
): # pragma: no cover
    """
    Function to load data from Firebase.
    Requires [Firebase service account credentials](https://console.firebase.google.com/project/tingle-pilot-collected-data/settings/serviceaccounts/adminsdk)
    in JSON format.

    Parameters
    ----------
    dbURL : string (optional)
        Firebase database to pull data from

    notes : Boolean (optional)
        Return notes as well as data?

    start : date or datetime (optional)
        start time of data to include (eg, `datetime.date(2018,3,6)`)

    stop : date or datetime (optional)
        stop time of data to include (eg, `datetime.date(2018,3,6)`)

    combine : Boolean (optional)
        combine coordinators into a single row?

    marked : Boolean (optional)
        only include ontarget==True rows?

    Returns
    -------
    data : DataFrame
        Pandas DataFrame of data from Firebase

    notes : DataFrame (optional)
        Pandas DataFrame of notes from Firebase iff parameter notes==True,
    """
    # Fetch the service account key JSON file contents
    try:
        creds = [
            key for key in os.listdir(
                os.path.join(
                    'firebase-credentials'
                )
            ) if (
                "tingle-pilot-collected-data-firebase-adminsdk" in key
            ) and key.endswith(
                ".json"
            )
        ]
        cred = credentials.Certificate(os.path.join(
            "firebase-credentials",
            creds[0]
        ))
    except:
        print(stylize(
            "Data not loaded from Firebase!",
            colored.fg(
                "red"
            ) + colored.bg(
                226
            )
        ))
        if len(creds):
            print(
                "Save Firebase service account credentials "
                "in the directory \"firebase-credentials\" in JSON format with "
                "\"tingle-pilot-collected-data-firebase-adminsdk\" in the "
                "filename. Current files in \"firebase-credentials\":{0}".format(
                    "\n\t".join(creds)
                )
            )
        else:
            print(
                "Save Firebase service account credentials "
                "in the directory \"firebase-credentials\" in JSON format with "
                "\"tingle-pilot-collected-data-firebase-adminsdk\" in the "
                "filename."
            )
        print(
            "\nDownload credentials JSON from https://console.firebase.google.com"
            "/project/tingle-pilot-collected-data/settings/serviceaccounts/"
            "adminsdk"
        )
        return(pd.DataFrame())
    try:
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': dbURL
        })
    except ValueError as e:
        print(e)
    samples = db.reference('samples').get()
    batches = {
        k: v for d in [
            samples[key] for key in samples
        ] for k, v in d.items()
    }
    for batch in batches:
        b2 = []
        for row in batches[batch]['batchedData']:
            b2.append(
                {
                    **row,
                    'coordinator': batches[
                        batch
                    ][
                        'username'
                    ]
                }
            )
        batches[batch]['batchedData'] = b2
    data = pd.DataFrame(
        list(
            chain.from_iterable(
                [
                    batches[
                        batch
                    ][
                        'batchedData'
                    ] for batch in batches
                ]
            )
        )
    )
    data["human-readable timestamp"] = pd.to_datetime(
        data["timestamp"]*1000000
    )
    if stop:
        stop = start + datetime.timedelta(days=1) if (
            (start) and
            (stop == start)
        ) else stop
    data = data[
            (data["human-readable timestamp"] >= start) &
            (data["human-readable timestamp"] <= stop)
        ] if (start and stop) else data[
            data["human-readable timestamp"] >= start
        ] if start else data[
            data["human-readable timestamp"] <= stop
        ] if stop else data
    data.sort_values(
        "timestamp",
        inplace=True
    )
    data = data.reset_index(drop=True)
    data = combine_coordinators(data) if combine else data
    data = data[data.ontarget == True] if marked else data
    data = data.reset_index(drop=True)
    print(stylize(
        "Data loaded from Firebase!",
        colored.fg(
            "green"
        )
    ))
    if not notes:
        return(data)
    else:
        notesNotesNotes = db.reference('notes').get()
        notesBatches = {
            k: v for d in [
                notesNotesNotes[
                    key
                ] for key in notesNotesNotes
            ] for k, v in d.items()
        }
        notes = pd.DataFrame([{
            k if k!= "lastsample" else "timestamp": notesBatches[
                i
            ][
                k
            ] if k != "lastsample" else notesBatches[
                i
            ][
                k
            ][
                "timestamp"
            ] if "timestamp" in notesBatches[
                i
            ][
                k
            ] else None for k in [
                "notes",
                "lastsample",
                "username"
            ] if k in notesBatches[i]
        } for i in notesBatches])
        notes["human-readable timestamp"] = pd.to_datetime(
            notes["timestamp"]*1000000
        )
        notes = notes[
                (notes["human-readable timestamp"] >= start) &
                (notes["human-readable timestamp"] <= stop)
            ] if (start and stop) else notes[
                notes["human-readable timestamp"] >= start
            ] if start else notes[
                notes["human-readable timestamp"] <= stop
            ] if stop else notes
        notes = notes[
            notes["timestamp"] > 0
        ].sort_values("timestamp")
        data = pd.merge(
            data,
            notes.set_index(
                "human-readable timestamp"
            ).reindex(
                data["human-readable timestamp"],
                method="ffill"
            ).drop(
                "timestamp",
                axis=1
            ).drop_duplicates(),
            left_on="human-readable timestamp",
            right_index=True,
            how="outer"
        )
        data = dropX(data)
    return(data, notes)


def lookup_counts(
    row,
    lookup_table,
    index="step",
    columns="participant",
    default=False
):
    """
    Function to apply to a DataFrame to cross-reference
    counts in a lookup_table.

    Parameters
    ----------
    row: Series
        row of a DataFrame

    lookup_table: DataFrame
        DataFrame to cross-reference

    index: string or numeric, opitional
        name of column in row that contains an index value
        for lookup_table, default = "step"

    columns: string or numeric, opitional
        name of column in row that contains a column name
        for lookup_table, default = "participant"

    default: boolean or other, optional
        value to return if lookup not in lookup table
        default = False

    Returns
    -------
    value: boolean or other
        the value at index, columns; otherwise default
    """
    try:
        return(
            lookup_table.loc[
                row[index],
                row[columns]
            ].all()
        )
    except:
        return(default)


def update_from_one(row):
    """
    Function to update rows that need updated
    from agreement to single_coordinator

    Parameter
    ---------
    row: Series

    Returns
    -------
    updated: Boolean or other

    Examples
    --------
    >>> import pandas as pd
    >>> row = pd.Series(
    ...     {
    ...         "one_coordinator": True,
    ...         "both_coordinators": False,
    ...         "needs_updated": True
    ...     }
    ... )
    >>> update_from_one(row)
    True

    >>> import pandas as pd
    >>> row = pd.Series(
    ...     {
    ...         "one_coordinator": True,
    ...         "both_coordinators": False,
    ...         "needs_updated": False
    ...     }
    ... )
    >>> update_from_one(row)
    False

    >>> import pandas as pd
    >>> row = pd.Series(
    ...     {
    ...         "one_coordinator": False,
    ...         "both_coordinators": False,
    ...         "needs_updated": True
    ...     }
    ... )
    >>> update_from_one(row)
    False
    """
    try:
        return(
            row.one_coordinator if row.needs_updated \
            else row.both_coordinators
        )
    except:
        print("except")
        print(row)


def update_too_few(df, condition):
    """
    Function to update a DataFrame with an inappropriate
    number of samples in coordinator agreement.

    Parameters
    ----------
    df: DataFrame
        DataFrame to update

    condition: string
        definition of inappropriate count, eg, "< 5"

    Returns
    -------
    df: DataFrame
        DataFrame updated with single-rater matches
        replacing dual-rater agreement in cases indicated
        by condition
    """
    on_target_counts = count_ontarget_samples(
        df
    )
    default = eval(
        " ".join([
            "0",
            condition
        ])
    )
    df["ontarget"] = pd.DataFrame({
        "needs_updated": df.apply(
            lookup_counts,
            axis=1,
            lookup_table=eval(
                "({0} {1})".format(
                    "on_target_counts",
                    condition
                )
            ),
            default=default
        ),
        "one_coordinator": (
            (
                df.coordinator1 == True
            ) | (
                df.coordinator2 == True
            )
        ) & (
            df.step == df.step_c2
        ),
        "both_coordinators": df[
            "ontarget"
        ]
    }).apply(
        update_from_one,
        axis=1
    )
    return(df)
