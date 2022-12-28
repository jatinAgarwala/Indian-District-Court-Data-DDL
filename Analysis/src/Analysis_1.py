import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate

    # state_cases_table.csv
    # table1 = ['ddl_case_id', 'state_code', 'disp_code', 'type_name', 'purpose_name', 'date_of_filing', 'date_of_decision']  
    # # need to get state_name (from cases_state_key), disp_name (from disp_name_key), type_name (from type_name_key), purpose_name (from purpose_name_key) 

year_wise_counts = []

for YEAR in ['2010','2014','2018']:

    table_path = '../generated_tables/' + YEAR + '/'

    state_cases = pd.read_csv(table_path + 'state_cases_table.csv')
    state_cases.drop('Unnamed: 0',axis=1,inplace=True)
    state_cases.drop('Unnamed: 0.1',axis=1,inplace=True)

    state_wise_count = state_cases.groupby(['state_names'])['state_names'].count().sort_index()
    year_wise_counts.append(state_wise_count)
    state_wise_count = state_wise_count.sort_values(ascending=False)
    print(state_wise_count)
    fig, axes = plt.subplots()
    plt.plot(state_wise_count)
    plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='small')
    plt.savefig('../plots1/State-wise number of cases in ' + YEAR + '.png')
    plt.close()

    # state_wise_type_count = state_cases.groupby(['state_names','type_names'])['type_names'].count().reset_index(name='counts')

    # type
    state_wise_type_count = state_cases.groupby(['state_names','type_names'])['type_names'].count()

    legend = []
    fig, axes = plt.subplots()
    for state in state_cases['state_names'].unique():
        top_types = state_wise_type_count[state].sort_values(ascending=False)[:3]
        top_types_ratio = np.divide(top_types,state_wise_count[state])
        plt.bar(x = top_types.keys()[0], height = top_types_ratio.values[0], width=0.2)
        legend.append(state)
        # plt.bar(top_types.keys, np.divide(top_types,state_wise_count[state]))

    plt.legend(legend)
    plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.savefig('../plots1/State-wise highest ratio of type of case in ' + YEAR + '.png')
    plt.close()

    # purpose
    state_wise_purpose_count = state_cases.groupby(['state_names','purpose_names'])['purpose_names'].count()

    legend = []
    fig, axes = plt.subplots()
    for state in state_cases['state_names'].unique():
        top_types = state_wise_purpose_count[state].sort_values(ascending=False)[:3]
        top_types_ratio = np.divide(top_types,state_wise_count[state])
        plt.bar(x = top_types.keys()[0], height = top_types_ratio.values[0], width=0.2)
        legend.append(state)
        # plt.bar(top_types.keys, np.divide(top_types,state_wise_count[state]))

    plt.legend(legend)
    plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.savefig('../plots1/State-wise highest ratio of purpose of case in ' + YEAR + '.png')
    plt.close()

    # disp
    state_wise_disp_count = state_cases.groupby(['state_names','disp_names'])['disp_names'].count()

    legend = []
    fig, axes = plt.subplots()
    for state in state_cases['state_names'].unique():
        top_types = state_wise_disp_count[state].sort_values(ascending=False)[:3]
        top_types_ratio = np.divide(top_types,state_wise_count[state])
        plt.bar(x = top_types.keys()[0], height = top_types_ratio.values[0], width=0.2)
        legend.append(state)
        # plt.bar(top_types.keys, np.divide(top_types,state_wise_count[state]))

    plt.legend(legend)
    plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
    plt.savefig('../plots1/State-wise highest ratio of disposal of case in ' + YEAR + '.png')
    plt.close()

fig, axes = plt.subplots()
for entry in year_wise_counts:
    plt.plot(entry)

plt.setp(axes.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
plt.legend([2010,2014,2018])
# plt.savefig('../plots1/Year-wise number of cases per state.png', dpi = 100)
plt.show()
