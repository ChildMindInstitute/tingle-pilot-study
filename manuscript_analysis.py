# Jake Son
# Child Mind Institute

import numpy as np
import pandas as pd
from statsmodels import robust
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel
from itertools import combinations
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler

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
        # sub_thermopile1 = np.median(data_subset[data_subset.target == u_target].thermopile1.tolist())
        # sub_thermopile2 = np.median(data_subset[data_subset.target == u_target].thermopile2.tolist())
        # sub_thermopile3 = np.median(data_subset[data_subset.target == u_target].thermopile3.tolist())
        # sub_thermopile4 = np.median(data_subset[data_subset.target == u_target].thermopile4.tolist())

        sub_dict[u_target] = [sub_distance, sub_pitch, sub_roll, 0, 0, 0, 0]

        # sub_dict[u_target] = [sub_distance, sub_pitch, sub_roll, sub_thermopile1, sub_thermopile2,
        #                       sub_thermopile3, sub_thermopile4]

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

for col in df.columns:

    med = np.median(df[col].tolist())
    mad = robust.mad(np.array(df[col].tolist()), axis=0)

    print(col, med, mad)

df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_n_thermal_vector.csv')


df_y = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_y_thermal.csv')
df_n = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/distance_n_thermal_vector.csv')

combs = df_y.columns

for comb in combs[1:]:

    y_list = df_y[comb].tolist()
    n_list = df_n[comb].tolist()

    v = (np.median(y_list) - np.median(n_list)) / (robust.mad(np.concatenate([y_list, n_list])))
    print(comb, v)

df_y = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/auroc_y_thermal.csv')
df_n = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/results/auroc_n_thermal.csv')

y_auroc_effect = {x: [] for x in df_y.Target.unique()}
n_auroc_effect = {x: [] for x in df_n.Target.unique()}

for loc in df_y.Target.unique():

    df_subset_y = df_y[df_y.Target == loc].AUROC.tolist()
    df_subset_n = df_n[df_n.Target == loc].AUROC.tolist()

    v = (np.median(df_subset_y) - np.median(df_subset_n)) / (robust.mad(np.concatenate([df_subset_y, df_subset_n])))

    print(loc, v)


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

        sub_dict[u_target] = [sub_distance, sub_pitch, sub_roll]

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

for col in df.columns:

    med = np.median(df[col].tolist())
    mad = robust.mad(np.array(df[col].tolist()), axis=0)

df.boxplot(column=df.columns[:5].tolist())
df.boxplot(column=df.columns[5:10].tolist())
df.boxplot(column=df.columns[10:15].tolist())

df.boxplot()
plt.savefig('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_n_thermal.png')

df.to_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_n_thermal.csv')

# Analysis

y_df = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_y_thermal.csv')
n_df = pd.read_csv('/Users/jakeson/Documents/CMI/tingle_pilot_analysis/distance_n_thermal.csv')

for col in n_df.columns[1:]:

    med = np.median(n_df[col].tolist())
    mad = robust.mad(np.array(n_df[col].tolist()), axis=0)

    print(col, med, mad)

    print(col, ttest_rel(y_df[col], n_df[col]))

    # print(str('{}: {}').format(col, ttest_rel(y_df[col], n_df[col])[1]))


for loc in ['rotate-mouth', 'rotate-nose', 'rotate-cheek', 'rotate-eyebrow', 'rotate-top-head', 'rotate-back-head']:

    # med = np.median(y_df[y_df.target == zz].auroc.tolist())
    # mad = robust.mad(np.array(y_df[y_df.target == zz].auroc.tolist()))
    #
    # print(loc, med, mad)

    n_sub = n_df[n_df.target == loc].auroc.tolist()
    y_sub = y_df[y_df.target == loc].auroc.tolist()

    print(loc, ttest_rel(y_sub, n_sub))



