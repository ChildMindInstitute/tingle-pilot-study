# Jake Son
# Child Mind Institute

import numpy as np
import pandas as pd
from sklearn import metrics
from keras.layers import LSTM
from statsmodels import robust
from keras.layers import Dense
from keras.models import Sequential
from scipy.stats import ttest_rel
from itertools import combinations
from scipy.spatial import distance
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#######################################################################################################################
# Distance calculation without thermal data

df = pd.read_csv('tingle_pilot_data_shareable.csv')

data = df[['distance', 'pitch', 'roll', 'target',
           'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4',
           'ontarget', 'participant']]

data = data[(data.target == 'rotate-mouth') | (data.target == 'rotate-nose') | (data.target == 'rotate-cheek') |
            (data.target == 'rotate-eyebrow') | (data.target == 'rotate-top-head') |
            (data.target == 'rotate-back-head') | (data.target == 'offbody-ceiling') |
            (data.target == 'offbody-floor') | (data.target == 'offbody-+') |
            (data.target == 'offbody-X') | (data.target == 'offbody-spiral')]

data = data[(data.ontarget == True)]

data = data.drop(labels=['ontarget'], axis=1)

targets = ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head',
                            'rotate-back-head']

results = {}

for participant_num in data.participant.unique():

    data_subset = data[data.participant == participant_num]

    col_subset = ['distance', 'pitch', 'roll']

    data_subset[col_subset] = StandardScaler().fit_transform(data_subset[col_subset])

    results[participant_num] = {}

    sub_dict = {}

    for u_target in targets:

        target_subset = data_subset[data_subset.target == u_target]

        sub_distance = np.median(data_subset[data_subset.target == u_target].distance.tolist())
        sub_pitch = np.median(data_subset[data_subset.target == u_target].pitch.tolist())
        sub_roll = np.median(data_subset[data_subset.target == u_target].roll.tolist())

        sub_dict[u_target] = [sub_distance, sub_pitch, sub_roll, 0, 0, 0, 0]

    combos = combinations(targets, 2)

    for t1, t2 in combos:

        results[participant_num][str('{}_{}').format(t1, t2)] = distance.euclidean(sub_dict[t1], sub_dict[t2])

df_dict = {}

for combo in results[1].keys():

    df_dict[combo] = []

for participant_num in data.participant.unique():

    for combo in results[participant_num].keys():

        df_dict[combo].append(results[participant_num][combo])

df = pd.DataFrame.from_dict(df_dict)

# df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_n_thermal_vector.csv')
df = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_n_thermal_vector.csv')

for col in df.columns:

    med = np.median(df[col].tolist())
    mad = robust.mad(np.array(df[col].tolist()), axis=0)

    print(col, med, mad)

#######################################################################################################################
# Distance calculation with thermal data

df = pd.read_csv('tingle_pilot_data_shareable.csv')

data = df[['distance', 'pitch', 'roll', 'target',
           'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4',
           'ontarget', 'participant']]

data = data[(data.target == 'rotate-mouth') | (data.target == 'rotate-nose') | (data.target == 'rotate-cheek') |
            (data.target == 'rotate-eyebrow') | (data.target == 'rotate-top-head') |
            (data.target == 'rotate-back-head') | (data.target == 'offbody-ceiling') |
            (data.target == 'offbody-floor') | (data.target == 'offbody-+') |
            (data.target == 'offbody-X') | (data.target == 'offbody-spiral')]

data = data[(data.ontarget == True)]

data = data.drop(labels=['ontarget'], axis=1)

targets = ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head',
                            'rotate-back-head']

results = {}

for participant_num in data.participant.unique():

    data_subset = data[data.participant == participant_num]

    col_subset = ['distance', 'pitch', 'roll', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']

    data_subset[col_subset] = StandardScaler().fit_transform(data_subset[col_subset])

    results[participant_num] = {}

    sub_dict = {}

    for u_target in targets:

        target_subset = data_subset[data_subset.target == u_target]

        sub_distance = np.median(data_subset[data_subset.target == u_target].distance.tolist())
        sub_pitch = np.median(data_subset[data_subset.target == u_target].pitch.tolist())
        sub_roll = np.median(data_subset[data_subset.target == u_target].roll.tolist())
        sub_thermopile1 = np.median(data_subset[data_subset.target == u_target].thermopile1.tolist())
        sub_thermopile2 = np.median(data_subset[data_subset.target == u_target].thermopile2.tolist())
        sub_thermopile3 = np.median(data_subset[data_subset.target == u_target].thermopile3.tolist())
        sub_thermopile4 = np.median(data_subset[data_subset.target == u_target].thermopile4.tolist())

        sub_dict[u_target] = [sub_distance, sub_pitch, sub_roll, sub_thermopile1, sub_thermopile2,
                              sub_thermopile3, sub_thermopile4]

    combos = combinations(targets, 2)

    for t1, t2 in combos:

        results[participant_num][str('{}_{}').format(t1, t2)] = distance.euclidean(sub_dict[t1], sub_dict[t2])

df_dict = {}

for combo in results[1].keys():

    df_dict[combo] = []

for participant_num in data.participant.unique():

    for combo in results[participant_num].keys():

        df_dict[combo].append(results[participant_num][combo])

df = pd.DataFrame.from_dict(df_dict)

# df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_y_thermal.csv')
df = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_y_thermal.csv')

for col in df.columns:

    med = np.median(df[col].tolist())
    mad = robust.mad(np.array(df[col].tolist()), axis=0)

    print(col, med, mad)

#######################################################################################################################
# Paired t-test test between Euclidean distances

df_y = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_y_thermal.csv')
df_n = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_n_thermal_vector.csv')

for col in df_n.columns[1:]:

    med = np.median(df_n[col].tolist())
    mad = robust.mad(np.array(df_n[col].tolist()), axis=0)

    print(col, ttest_rel(df_y[col], df_n[col])[1]/15)

# Calculate effect size

combs = df_y.columns

for comb in combs[1:]:

    y_list = df_y[comb].tolist()
    n_list = df_n[comb].tolist()

    v = (np.median(y_list) - np.median(n_list)) / (robust.mad(np.concatenate([y_list, n_list])))
    print(comb, v)

#######################################################################################################################
# Calculate distributions without thermal data

from numpy.random import shuffle

targets = ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head',
                            'rotate-back-head']

df = pd.read_csv('tingle_pilot_data_shareable.csv')

pd.options.mode.chained_assignment = None

for participant_num in df.participant.unique():

    if participant_num != 22:

        print(str('Analyzing participant {}').format(participant_num))

        results = {}
        sep = '_'
        combos = combinations(targets, 2)

        for col1, col2 in combos:

            results[sep.join([col1, col2])] = []

        data_subset = df[df.participant == participant_num]

        col_subset = ['distance', 'pitch', 'roll']

        data_subset[col_subset] = StandardScaler().fit_transform(data_subset[col_subset])

        for i in range(1000):

            combos = combinations(targets, 2)

            for col1, col2 in combos:

                df_comp = data_subset[(data_subset.target == col1) | (data_subset.target == col2)]

                target_list = df_comp.target.tolist()
                shuffle(target_list)

                df_comp['target'] = target_list

                df1 = df_comp[df_comp.target == col1]
                df2 = df_comp[df_comp.target == col2]

                df1_distance = np.median(df1.distance.tolist())
                df1_pitch = np.median(df1.pitch.tolist())
                df1_roll = np.median(df1.roll.tolist())

                df2_distance = np.median(df2.distance.tolist())
                df2_pitch = np.median(df2.pitch.tolist())
                df2_roll = np.median(df2.roll.tolist())

                e_dist = distance.euclidean([df1_distance, df1_pitch, df1_roll], [df2_distance, df2_pitch, df2_roll])

                results[sep.join([col1, col2])].append(e_dist)

        results_df = pd.DataFrame.from_dict(results)
        file_savename = str('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/permutation_results_wo/{}_permutations.csv').format(participant_num)
        results_df.to_csv(file_savename)


# Calculate distributions with thermal data

from numpy.random import shuffle

targets = ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head',
                            'rotate-back-head']

df = pd.read_csv('tingle_pilot_data_shareable.csv')

pd.options.mode.chained_assignment = None

for participant_num in df.participant.unique():

    if participant_num != 22:

        print(str('Analyzing participant {}').format(participant_num))

        results = {}
        sep = '_'
        combos = combinations(targets, 2)

        for col1, col2 in combos:

            results[sep.join([col1, col2])] = []

        data_subset = df[df.participant == participant_num]

        col_subset = ['distance', 'pitch', 'roll', 'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4']

        data_subset[col_subset] = StandardScaler().fit_transform(data_subset[col_subset])

        for i in range(1000):

            combos = combinations(targets, 2)

            for col1, col2 in combos:

                df_comp = data_subset[(data_subset.target == col1) | (data_subset.target == col2)]

                target_list = df_comp.target.tolist()
                shuffle(target_list)

                df_comp['target'] = target_list

                df1 = df_comp[df_comp.target == col1]
                df2 = df_comp[df_comp.target == col2]

                df1_distance = np.median(df1.distance.tolist())
                df1_pitch = np.median(df1.pitch.tolist())
                df1_roll = np.median(df1.roll.tolist())
                df1_t1 = np.median(df1.thermopile1.tolist())
                df1_t2 = np.median(df1.thermopile2.tolist())
                df1_t3 = np.median(df1.thermopile3.tolist())
                df1_t4 = np.median(df1.thermopile4.tolist())

                df2_distance = np.median(df2.distance.tolist())
                df2_pitch = np.median(df2.pitch.tolist())
                df2_roll = np.median(df2.roll.tolist())
                df2_t1 = np.median(df2.thermopile1.tolist())
                df2_t2 = np.median(df2.thermopile2.tolist())
                df2_t3 = np.median(df2.thermopile3.tolist())
                df2_t4 = np.median(df2.thermopile4.tolist())

                e_dist = distance.euclidean([df1_distance, df1_pitch, df1_roll, df1_t1, df1_t2, df1_t3, df1_t4],
                                            [df2_distance, df2_pitch, df2_roll, df2_t1, df2_t2, df2_t3, df2_t4])

                results[sep.join([col1, col2])].append(e_dist)

        results_df = pd.DataFrame.from_dict(results)
        file_savename = str('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/permutation_results_w/{}_permutations.csv').format(participant_num)
        results_df.to_csv(file_savename)

#######################################################################################################################
# LSTM Analysis without thermal data

df = pd.read_csv('tingle_pilot_data_shareable.csv')

data = df[['distance', 'pitch', 'roll', 'target',
           'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4',
           'ontarget', 'participant']]

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

cm_results = {'rotate-mouth': [],
              'rotate-nose': [],
              'rotate-cheek': [],
              'rotate-eyebrow': [],
              'rotate-top-head': [],
              'rotate-back-head': []}

for part_num in range(1, len(data.participant.unique()) + 1):

    if part_num != 22:

        p1data = data[(data.participant == part_num)].drop(labels=['participant'], axis=1)

        col_subset = ['distance', 'pitch', 'roll']

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

            auroc = (metrics.auc(fpr, tpr))

            cm = confusion_matrix(y_test, pred)

            cm_results[target_loc].append(cm)

            results_dict[str('{}_{}').format(part_num, target_loc)] = [part_num, target_loc, auroc]

    else:

        continue

df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['participant', 'target', 'auroc'])
df = df.set_index('participant')

df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/auroc_n_thermal.csv')

# LSTM Analysis with thermal data

df = pd.read_csv('tingle_pilot_data_shareable.csv')

data = df[['distance', 'pitch', 'roll', 'target',
           'thermopile1', 'thermopile2', 'thermopile3', 'thermopile4',
           'ontarget', 'participant']]

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

cm_results = {'rotate-mouth': [],
              'rotate-nose': [],
              'rotate-cheek': [],
              'rotate-eyebrow': [],
              'rotate-top-head': [],
              'rotate-back-head': []}

for part_num in range(1, len(data.participant.unique()) + 1):

    if part_num != 22:

        p1data = data[(data.participant == part_num)].drop(labels=['participant'], axis=1)

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

            auroc = (metrics.auc(fpr, tpr))

            cm = confusion_matrix(y_test, pred)

            cm_results[target_loc].append(cm)

            results_dict[str('{}_{}').format(part_num, target_loc)] = [part_num, target_loc, auroc]

    else:

        continue

df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['participant', 'target', 'auroc'])
df = df.set_index('participant')

df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/auroc_y_thermal.csv')

# Confusion Matrices

for num in range(6):

    cm_results[targets[num]] = np.stack(cm_results[targets[num]])
    np.save(str('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/confusion_matrices/{}').format(targets[num]), cm_results[targets[num]])


