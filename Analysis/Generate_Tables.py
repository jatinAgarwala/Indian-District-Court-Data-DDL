import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# We need to complete the following tables:

    # state_cases_table.csv
    # table1 = ['ddl_case_id', 'state_code', 'disp_code', 'type_name', 'purpose_name', 'date_of_filing', 'date_of_decision']  
    # # need to get state_name (from cases_state_key), disp_name (from disp_name_key), type_name (from type_name_key), purpose_name (from purpose_name_key) 

    # # Gender information
    # table2 = ['ddl_case_id', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_code'] 
    # # need to get disp_name (from disp_name_key), ddl_decision_judge_id( from judge_case_merge_key), female_judge (from judges_clean)

    # # Filing judges information
    # table3 = ['ddl_case_id', 'date_of_filing', 'type_name', 'purpose_name'] 
    # # need to get ddl_filing_judge_id (from judge_case_merge_key), type_name (from type_name_key, purpose_name (from purpose_name_key), start_date (from judges_clean)

    # # Decision judge's information
    # table4 = ['ddl_case_id', 'date_of_decision', 'disp_name'] 
    # # need to get ddl_decision_judge_id (from judge_case_merge_key), type_name (from type_name_key, disp_name (from disp_name_key), start_date (from judges_clean)


data_path = "data/"
csv_path = '../../csv/'
keys_path = '../../csv/keys/keys/'

state_cases = pd.read_csv(data_path + 'state_cases_table.csv')

#states
cases_state_key = pd.read_csv(keys_path + 'cases_state_key.csv')
cases_state_key.drop(cases_state_key.index[(cases_state_key['year'] != 2010)], axis=0, inplace=True)    # Drop values not of year 2010

cases_state_key = pd.DataFrame({'code': cases_state_key['state_code'], 'name': cases_state_key['state_name']})
state_dict = dict(cases_state_key.values)
del cases_state_key

#disposals
disp_name_key = pd.read_csv(keys_path + 'disp_name_key.csv')
disp_name_key.drop(disp_name_key.index[(disp_name_key['year'] != 2010)], axis=0, inplace=True)    # Drop values not of year 2010

disp_name_key = pd.DataFrame({'code': disp_name_key['disp_name'], 'name': disp_name_key['disp_name_s']})
disp_dict = dict(disp_name_key.values)
del disp_name_key

#types
type_name_key = pd.read_csv(keys_path + 'type_name_key.csv')
type_name_key.drop(type_name_key.index[(type_name_key['year'] != 2010)], axis=0, inplace=True)    # Drop values not of year 2010

type_name_key = pd.DataFrame({'code': type_name_key['type_name'], 'name': type_name_key['type_name_s']})
type_dict = dict(type_name_key.values)
del type_name_key

#purpose
purpose_name_key = pd.read_csv(keys_path + 'purpose_name_key.csv')
purpose_name_key.drop(purpose_name_key.index[(purpose_name_key['year'] != 2010)], axis=0, inplace=True)    # Drop values not of year 2010

purpose_name_key = pd.DataFrame({'code': purpose_name_key['purpose_name'], 'name': purpose_name_key['purpose_name_s']})
purpose_dict = dict(purpose_name_key.values)
del purpose_name_key


state_names = list(pd.Series(state_cases['state_code']).map(state_dict))
state_cases.drop('state_code',axis=1,inplace=True)
state_cases['state_names'] = state_names
del state_names

disp_names = list(pd.Series(state_cases['disp_name']).map(state_dict))
state_cases.drop('disp_name',axis=1,inplace=True)
state_cases['disp_names'] = disp_names
del disp_names

type_names = list(pd.Series(state_cases['type_name']).map(state_dict))
state_cases.drop('type_name',axis=1,inplace=True)
state_cases['type_names'] = type_names
del type_names

purpose_names = list(pd.Series(state_cases['purpose_name']).map(state_dict))
state_cases.drop('purpose_name',axis=1,inplace=True)
state_cases['purpose_names'] = purpose_names
del purpose_names

state_cases.to_csv('data/state_cases_table.csv')
del state_cases