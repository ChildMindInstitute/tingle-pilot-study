import colored
from colored import stylize
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from itertools import chain
import pandas as pd
import os


def load_from_firebase(dbURL="https://tingle-pilot-collected-data.firebaseio.com/", notes=False):
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
        
    Returns
    -------
    data : DataFrame
        Pandas DataFrame of data from Firebase
        
    notes : DataFrame (optional)
        Pandas DataFrame of notes from Firebase iff parameter notes==True
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

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': dbURL
    })
    samples = db.reference('samples').get()
    batches = {
        k: v for d in [
            samples[key] for key in samples
        ] for k, v in d.items()
    }
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
            k if k!= "lastsample" else "timestamp": notesBatches[i][k] if k != "lastsample" else notesBatches[i][k]["timestamp"] if "timestamp" in notesBatches[i][k] else None for k in [
                "notes",
                "lastsample",
                "username"
            ] if k in notesBatches[i]
        } for i in notesBatches])
        notes["human-readable timestamp"] = pd.to_datetime(
            notes["timestamp"]*1000000
        )
    return(data, notes)


def break_out_blocks(pilot_data):
    """
    Function to indicate separate blocks of collected data in an "iteration_block" column.
    
    Parameter
    ---------
    pilot_data: DataFrame
    
    Returns
    -------
    pilot_data: DataFrame
    """
    on_target_blocks = {}
    row_indices = []
    for i, t in enumerate(pilot_data.target):
        if (i > 0):
            if(pilot_data.ontarget[i - 1] and not pilot_data.ontarget[i]):
                if t in on_target_blocks:
                    on_target_blocks[t][
                        max(
                            [k for k in on_target_blocks[t]]
                        ) + 1
                    ] = row_indices
                else:
                    on_target_blocks[t] = {}
                    on_target_blocks[t][1] = row_indices
                row_indices = []
            elif(pilot_data.ontarget[i]):
                row_indices.append(i)
    for target in on_target_blocks:
        for block in on_target_blocks[target]:
            for row in on_target_blocks[target][block]:
                pilot_data.loc[row, "iteration_block"] = block
    return(pilot_data)