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
    Warning! This function is brute-force and slow (~O(n)). 
    
    Parameter
    ---------
    data : DataFrame
        DataFrame with separate coordinator rows
        
    Returns
    -------
    data : DataFrame
        DataFrame with combined coordinator rows
    """
    data["coordinator2"] = pd.Series()
    for i, row in data.iterrows():
        if row.name > 0:
            if row.thermopile1 != False:
                data.loc[
                    row.name,
                    "coordinator1"
                ] = data.loc[
                    row.name,
                    "ontarget"
                ]
                j = 1
                while(
                    row.timestamp - data.loc[
                        row.name - j,
                        "timestamp"
                    ] <= 150
                ):
                    if np.isnan(
                        data.loc[
                            row.name,
                            "coordinator2"
                        ]
                    ):
                        data.loc[
                            row.name,
                            "coordinator2"
                        ] = data.loc[
                            row.name - j,
                            "ontarget"
                        ]
                        data.loc[
                            row.name,
                            "secondCoordinator"
                        ] = data.loc[
                            row.name - j,
                            "coordinator"
                        ]
                        data.loc[
                            row.name,
                            "ontarget"
                        ] = data.loc[
                            row.name,
                            "ontarget"
                        ] if data.loc[
                            row.name,
                            "coordinator1"
                        ] == data.loc[
                            row.name,
                            "coordinator2"
                        ] else False
                    j = j + 1
    return(data)


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
        notes = notes[notes["timestamp"] > 0].sort_values("timestamp")
    return(data, notes)