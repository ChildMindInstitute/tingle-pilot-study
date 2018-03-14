import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, accuracy_score
from sklearn.neural_network import MLPClassifier

pilot_data = pd.read_csv('pilot_data.csv')
pilot_data = pilot_data[pilot_data.ontarget == True]

def separate_participants(df):

    new_index = list(range(len(df)))
    df['reindex'] = new_index
    df = df.set_index('reindex')

    new_index = []

    participant_index = 1
    for i, row in df.iterrows():
        if (row.step == 47) and (i != len(df)-1) and (df.loc[i+1, 'step'] == 1):
            participant_index += 1
            new_index.append(participant_index)
        else:
            new_index.append(participant_index)

    df['participant_index'] = new_index

    return df

pilot_data = separate_participants(pilot_data)
pilot_data = pilot_data[pilot_data.participant_index <= 8]

########################################################################
# Return number of on-target samples for each motion

def data_summary(df):

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

########################################################################
# Load dictionaries with on-target and sub-levels of off-targets based on specificity

with open("neuralnet/targets.json", 'r') as fp:
    targets = json.load(fp)

########################################################################
# Data processing before training neural network


def parse_data(data, target, spec):

    on_target = targets[target][0]

    off_targets = targets[target][spec]

    pilot_true = data[(data.target == on_target) & (data.thermopile1 != False)]
    pilot_false = data[(data.target.isin(off_targets)) & (data.thermopile1 != False)]

    return on_target, off_targets, pilot_true, pilot_false


def train_test(on_target, off_target, pilot_true, pilot_false, prop=.75, off_prop=.75):

    train_size_true = int(np.round(prop * len(pilot_true), 0))
    train_size_false = int(np.round(prop * len(pilot_false), 0))

    on_target_train = []
    on_target_test = []

    for row in pilot_true[(pilot_true.target == on_target) & (pilot_true.ontarget)][
        ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[:train_size_true]:
        row = [np.round(float(x) / 150, 3) for x in row]
        on_target_train.append({'in': row, 'out': 1})

    for row in pilot_true[(pilot_true.target == on_target) & (pilot_true.ontarget)][
        ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[train_size_true:]:
        row = [np.round(float(x) / 150, 3) for x in row]
        on_target_test.append({'in': row, 'out': 1})




    ################################################################################################################

    off_target_train = []
    off_target_test = []

    for item in off_target:
        if ('offbody' in item) or ('paint' in item):
            size = pilot_false[pilot_false.target == item].shape[0]
            size = int(np.round(off_prop * size, 0))
            for row in pilot_false[(pilot_false.target == item)][
                           ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[
                       :size]:
                row = [np.round(float(x)/150, 3) for x in row]
                off_target_train.append({'in': row, 'out': 0})
            for row in pilot_false[(pilot_false.target == item)][
                           ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[
                       size:]:
                row = [np.round(float(x) / 150, 3) for x in row]
                off_target_test.append({'in': row, 'out': 0})
        else:
            size = pilot_false[pilot_false.target == item].shape[0]
            for row in pilot_false[(pilot_false.target == item)][
                ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[:size]:
                row = [np.round(float(x) / 150, 3) for x in row]
                off_target_train.append({'in': row, 'out': 0})
            for row in pilot_false[(pilot_false.target == item)][
                ['distance', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']].values.tolist()[size:]:
                row = [np.round(float(x) / 150, 3) for x in row]
                off_target_test.append({'in': row, 'out': 0})

    train_data = []
    test_data = []
    train_targets = []
    test_targets = []

    for row in on_target_train:
        train_targets.append(row['out'])
        train_data.append(row['in'])

    for row in off_target_train:
        train_targets.append(row['out'])
        train_data.append(row['in'])

    for row in on_target_test:
        test_targets.append(row['out'])
        test_data.append(row['in'])

    for row in off_target_test:
        test_targets.append(row['out'])
        test_data.append(row['in'])

    return train_data, train_targets, test_data, test_targets

########################################################################
# Training and testing the neural network


def nn_iterations(train_data, train_targets, test_data, test_targets, iterations=1):
    true_pos_sum = []
    true_neg_sum = []
    fals_pos_sum = []
    fals_neg_sum = []
    sum_stats = []

    plt.figure(figsize=(5, 5))
    plt.title('Target: ' + str(target) + ', specificity=' + str(specificity_level))

    for num in range(iterations):

        print('Iteration: ' + str(num+1))

        clf = MLPClassifier(solver='adam', alpha=.0001,
                            hidden_layer_sizes=(5, 2),
                            max_iter=2000, verbose=False,
                            tol=.0001)

        clf.fit(train_data, train_targets)

        predictions = clf.predict(test_data)

        predi_probs = clf.predict_proba(test_data)

        acc_score = accuracy_score(predictions, test_targets)

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

    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Luck', alpha=.8)
    plt.legend()
    plt.grid(True)
    plt.show()

    return predi_probs, sum_stats

# on_target, off_target, pilot_true, pilot_false = parse_data(pilot_data, 'eyebrow', spec=4)
# train_data, train_targets, test_data, test_targets = train_test(on_target, off_target, pilot_true, pilot_false,
#                                                                 prop=.75, off_prop=.75)
# predi_probs, sum_stats = nn_iterations(train_data, train_targets, test_data, test_targets, iterations=10)

for target in ['eyebrow']:
    for specificity_level in [1, 2]:
        print('Starting analysis on ' + target + ' with specificity ' + str(specificity_level))
        on_target, off_target, pilot_true, pilot_false = parse_data(pilot_data, target, spec=specificity_level)
        train_data, train_targets, test_data, test_targets = train_test(on_target, off_target, pilot_true, pilot_false,
                                                                        prop=.75, off_prop=.75)
        predi_probs, sum_stats = nn_iterations(train_data, train_targets, test_data, test_targets, iterations=10)
