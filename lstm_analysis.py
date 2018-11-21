# Jake Son
# Child Mind Institute

import numpy as np
import pandas as pd
from sklearn import metrics
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv('tingle_pilot_data_shareable.csv')

data = df[['distance', 'pitch', 'roll', 'target',
           'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4',
           'ontarget', 'participant']]

# data = df[['distance', 'pitch', 'roll', 'target', 'ontarget', 'participant']]

data = data[(data.target == 'rotate-mouth') | (data.target == 'rotate-nose') | (data.target == 'rotate-cheek') |
            (data.target == 'rotate-eyebrow') | (data.target == 'rotate-top-head') |
            (data.target == 'rotate-back-head') | (data.target == 'offbody-ceiling') |
            (data.target == 'offbody-floor') | (data.target == 'offbody-+') |
            (data.target == 'offbody-X') | (data.target == 'offbody-spiral')]

data = data[(data.ontarget == True)]

data = data.drop(labels=['ontarget'], axis=1)

targets = ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head',
                            'rotate-back-head']

results_dict = {}

for part_num in range(1, len(data.participant.unique()) + 1):

    if part_num != 22:

        p1data = data[(data.participant == part_num)].drop(labels=['participant'], axis=1)

        # col_subset = ['distance', 'pitch', 'roll']
        col_subset = ['distance', 'pitch', 'roll', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']

        p1data[col_subset] = StandardScaler().fit_transform(p1data[col_subset])

        for target_loc in targets:

            print(str('Analyzing participant {} target {}').format(part_num, target_loc))

            p1targets = list(p1data['target'].values)
            p1targets = np.array([1 if x == target_loc else 0 for x in p1targets])
            p1signals = p1data.drop(labels=['target'], axis=1).values

            x_train, x_test, y_train, y_test = train_test_split(p1signals, p1targets, test_size=.25, shuffle=True, random_state=1)

            x_train = x_train.reshape((x_train.shape[0], 1, x_train.shape[1]))
            x_test = x_test.reshape((x_test.shape[0], 1, x_test.shape[1]))

            model = Sequential()
            model.add(LSTM(50, input_shape=(x_train.shape[1], x_train.shape[2]), return_sequences=True))
            model.add(LSTM(50, dropout=.2))
            model.add(Dense(1, activation='sigmoid'))
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

            history = model.fit(x_train, y_train, epochs=200, batch_size=32, validation_data=(x_test, y_test), verbose=0, shuffle=False)

            pred = model.predict_classes(x_test)
            fpr, tpr, thresholds = metrics.roc_curve(y_test, pred)

            report = metrics.classification_report(y_test, pred, output_dict=True)
            precision = round(report['weighted avg']['precision'], 2)
            recall = round(report['weighted avg']['recall'], 2)
            f1score = round(report['weighted avg']['f1-score'], 2)
            auroc = (metrics.auc(fpr, tpr))

            print((metrics.auc(fpr, tpr), f1score))

            results_dict[str('{}_{}').format(part_num, target_loc)] = [part_num, target_loc, precision, recall, f1score, auroc]

    else:

        continue

df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['participant', 'target', 'precision', 'recall', 'f1score', 'auroc'])
df = df.set_index('participant')

# df.to_csv('~/Documents/CMI/tingle_pilot_analysis/group_lstm_analysis.csv')


# Analysis using simple paired t-test of AUROC values with and without thermal information

from scipy.stats import ttest_rel

df_n = pd.read_csv('auroc_n_thermal.csv')
df_y = pd.read_csv('auroc_y_thermal.csv')

for target in df_n.target.unique():

    df_n_sub = df_n[df_n.target == target]
    df_y_sub = df_y[df_y.target == target]

    output = ttest_rel(df_n_sub.auroc.tolist(), df_y_sub.auroc.tolist())
    stats = output[0] # negative stats value means values from second input > first input
    p_val = output[1]

    print((target, stats, p_val))
