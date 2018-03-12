import colored
from colored import stylize
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from itertools import chain
import numpy as np
import pandas as pd
import os


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
    """
    c1 = data[data.thermopile1 != False].set_index("human-readable timestamp")
    c2 = data[data.thermopile1 == False].set_index("human-readable timestamp")
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
    c["ontarget"] = c[
        (c["coordinator1"] == c["coordinator2"])
        &
        (c["step"] == c["step_c2"])
    ]["coordinator1"]
    c.drop(["step_c2"], axis=1, inplace=True)
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
            value: corrected value
    
    Returns
    -------
    df: DataFrame
        updated
    """
    for participant in corrections:
        for col in corrections[participant]:
            df.loc[
                list(
                    df[
                        df.participant==int(
                            participant
                        )
                    ].index
                ),
                col
            ] = corrections[participant][col]
    return(df)


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


def index_participants(df):
    """
    Function to index participants
    
    Parameter
    ---------
    df: DataFrame
    
    Returns
    -------
    participants_df: DataFrame
    """
    participants = {}
    # initialize as if participant 0 just finished 
    participant = 0
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
):
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
        notes = notes[notes["timestamp"] > 0].sort_values("timestamp")
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


def split_participants(df):
    """
    Function to split DataFrame into separate participants
    
    Parameter
    ---------
    df: DataFrame
    
    Returns
    -------
    dfs: list of DataFrames
    """
    dfs = []
    rolling = 0 if df.loc[0, "step"] == 1 else None
    for i, row in df.iterrows():
        if i > 0:
            if not rolling:
                rolling = i if row.step == 1 else None
            if row.step == 1 and df.loc[i-1, "step"] > row.step:
                dfs.append(
                    df.loc[
                        rolling:i,
                        :
                    ].reset_index(
                        drop=True
                    )
                )
                rolling = i
            if row.step == 47:
                last_one = i
    dfs.append(
        df.loc[
            rolling:last_one-1,
            :
        ].reset_index(
            drop=True
        )
    )
    return(dfs)