import os
import json
import datetime
import numpy as np
import pandas as pd
from data import dataloader
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, accuracy_score
from sklearn.neural_network import MLPClassifier

pilot_data = pd.read_csv('pilot_data.csv')
pilot_data = pilot_data[pilot_data.ontarget == True]


def separate_participants(df):

    new_index = list(range(len(df)))
    df['reindex'] = new_index

    pilot_data = df.set_index('reindex')

    participant_index = 0
    for i, row in df.iterrows():
        if (row.step == 47) and (i != len(df)-1) and (df.loc[i+1, 'step'] == 1):
            participant_index += 1
            print('New Participant: ' + str(participant_index))

separate_participants(pilot_data)

notepath = "data/notes.csv"
datapath = "data/pilot_data.csv"
corrections_path = "data/corrections.json"

if(
    os.path.exists(notepath) and
    os.path.exists(datapath)
):
    notes = pd.read_csv(notepath)
    pilot_data = pd.read_csv(datapath)

else:
    pilot_data, notes = dataloader.load_from_firebase(
        notes=True,
        start=datetime.datetime(2018, 3, 6, 8),
        combine=True,
        marked=False
    )
    pilot_data.to_csv(
        datapath,
        index=False
    )
    notes.to_csv(
        notepath,
        index=False
    )

if os.path.exists(corrections_path):
    with open("data/corrections.json", "r") as c:
        corrections = json.load(c)
else:
    corrections = {}

for target in list(pilot_data.target.unique()):
    ib =max(
        pilot_data.loc[
            pilot_data.target==target
        ].step.dropna()
    )
    print(": ".join([
        target,
        "{0} on-target samples in {1} iteration block{2}".format(
            str(len(pilot_data.loc[
                (pilot_data.target == target) &
                (pilot_data.ontarget)
            ])),
            "%.0f" % ib,
            "s" if ib != 1 else ""
        )
    ]))

with open("neuralnet/targets.json", 'r') as fp:
    targets = json.load(fp)


def parse_data(data, target, spec):
    on_target = targets[target][0]

    off_targets = targets[target][spec]

    pilot_true = data[(data.target == on_target) & (data.thermopile1 != False)]
    pilot_false = data[(data.target.isin(off_targets)) & (data.thermopile1 != False)]

    return on_target, off_targets, pilot_true, pilot_false


on_target, off_target, pilot_true, pilot_false = parse_data(pilot_data, 'eyebrow', spec=3)


def train_test(on_target, off_target, pilot_true, pilot_false, prop=.75):
    train_size_true = int(np.round(prop * len(pilot_true), 0))  # Number of on-target training samples used for training

    pilot_true_array = []
    pilot_false_array = []
    train_targets = []
    test_targets = []

    on_targets = []
    off_targets = []

    for row in pilot_true[(pilot_true.target == on_target) & (pilot_true.ontarget)][
        ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist():
        pilot_true_array.append({'in': row, 'out': 1})

    for item in off_target:
        if ('rotate' in item) or ('paint' in item):
            size = pilot_false[pilot_false.target == item].shape[0]
            size = int(np.round(prop * size, 0))
            for row in pilot_false[(pilot_false.target == item)][
                           ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[
                       :size]:
                pilot_false_array.append({'in': row, 'out': 0})
        else:
            size = pilot_false[pilot_false.target == item].shape[0]
            for row in pilot_false[(pilot_false.target == item)][
                ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist():
                pilot_false_array.append({'in': row, 'out': 0})

    train_data = []
    train_data_p = []
    test_data = []
    test_data_p = []
    train_targets = []
    test_targets = []

    train_size_false = int(np.round(prop * len(pilot_false_array), 0))

    train_data_p.extend(pilot_true_array[:train_size_true])  #
    train_data_p.extend(pilot_false_array[:train_size_false])

    for row in train_data_p:
        on_targets.append(row['out'])
        row = [np.round(float(x) / 150, 3) for x in row['in']]
        train_data.append(row)

    test_data_p.extend(pilot_true_array[train_size_true:])
    test_data_p.extend(pilot_false_array[train_size_false:])

    for row in test_data_p:
        row = [np.round(float(x) / 150, 3) for x in row['in']]
        test_data.append(row)

    train_targets.extend(on_targets[:train_size_true])
    train_targets.extend(off_targets[:train_size_false])
    test_targets.extend(on_targets[train_size_true:])
    test_targets.extend(off_targets[train_size_false:])

    return train_data_p, train_targets, test_data_p, test_targets

train_data, train_targets, test_data, test_targets = train_test(on_target, off_target, pilot_true, pilot_false,
                                                                prop=.50)


def nn_iterations(train_data, train_targets, test_data, test_targets, iterations=1):
    true_pos_sum = []
    true_neg_sum = []
    fals_pos_sum = []
    fals_neg_sum = []
    sum_stats = []

    plt.figure(figsize=(5, 5))

    for num in range(iterations):

        clf = MLPClassifier(solver='adam', alpha=.0001,
                            hidden_layer_sizes=(5, 2),
                            max_iter=2000, verbose=False,
                            tol=.0001)

        clf.fit(train_data, train_targets)

        predictions = clf.predict(test_data)

        predi_probs = clf.predict_proba(test_data)

        acc_score = accuracy_score(predictions, test_targets)

        print(acc_score)

        fpr, tpr, thresholds = roc_curve(test_targets, predi_probs[:, 1], drop_intermediate=True)
        roc_auc = auc(fpr, tpr)
        if roc_auc > .55:
            plt.plot(fpr, tpr, lw=1, alpha=0.5, label='ROC fold (AUC = %0.2f)' % (roc_auc))

        predi_fals = [x for x, y in predi_probs]
        predi_true = [y for x, y in predi_probs]

        for item in range(len(predictions)):

            if predictions[item] == test_targets[item]:
                pred = 'correct'
            else:
                pred = 'incorrect'

            sum_stats.append({str(num + 1): [test_targets[item], predictions[item], predi_probs[item][0],
                                             predi_probs[item][1], pred]})

        count_neg = len([x for x in test_targets if x == 0])
        count_pos = len([x for x in test_targets if x == 1])

        true_pos = []
        true_neg = []
        fals_pos = []
        fals_neg = []

        for sample in range(len(test_data)):
            if test_targets[sample] == 0:
                if predictions[sample] == test_targets[sample]:
                    true_neg.append(sample)
                else:
                    fals_neg.append(sample)
            elif test_targets[sample] == 1:
                if predictions[sample] == test_targets[sample]:
                    true_pos.append(sample)
                else:
                    fals_pos.append(sample)

                    #         fals_pos_sum.append(str(len(fals_pos)/count_pos))
                    #         fals_neg_sum.append(str(len(fals_neg)/count_neg))
                    #         true_pos_sum.append(str(len(true_pos)/count_pos))
                    #         true_neg_sum.append(str(len(true_neg)/count_neg))

        print(roc_auc)

        if roc_auc > .55:
            print(str(len(fals_pos) / count_pos), str(len(fals_neg) / count_neg), str(len(true_pos) / count_pos),
                  str(len(true_neg) / count_neg))

    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Luck', alpha=.8)
    plt.legend()
    plt.grid(True)
    plt.show()

    #     fals_pos_sum = [float(x) for x in fals_pos_sum]
    #     fals_neg_sum = [float(x) for x in fals_neg_sum]
    #     true_pos_sum = [float(x) for x in true_pos_sum]
    #     true_neg_sum = [float(x) for x in true_neg_sum]

    #     fals_pos_sum = np.average(np.array(fals_pos_sum))
    #     fals_neg_sum = np.average(np.array(fals_neg_sum))
    #     true_pos_sum = np.average(np.array(true_pos_sum))
    #     true_neg_sum = np.average(np.array(true_neg_sum))

    #     print('Summary statistics after ' + str(iterations) + ' iterations:')
    #     print('True positive rate:  ' + str(np.round(true_pos_sum,3)))
    #     print('False positive rate: ' + str(np.round(fals_pos_sum,3)))
    #     print('True negative rate:  ' + str(np.round(true_neg_sum,3)))
    #     print('False negative rate: ' + str(np.round(fals_neg_sum,3)))

    return predi_probs, sum_stats


predi_probs, sum_stats = nn_iterations(train_data, train_targets, test_data, test_targets, iterations=1)
