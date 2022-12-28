import pandas as pd

keys_path = '../../csv/keys/keys/'
csv_path = '../../csv/'

# We first generate dictionaries for lookup from the key csv's

for YEAR in [2010,2014,2018]:

    #states
    cases_state_key = pd.read_csv(keys_path + 'cases_state_key.csv')
    cases_state_key.drop(cases_state_key.index[(cases_state_key['year'] != YEAR)], axis=0, inplace=True)    # Drop values not of year YEAR

    cases_state_key = pd.DataFrame({'code': cases_state_key['state_code'], 'name': cases_state_key['state_name']})
    state_dict = dict(cases_state_key.values)
    del cases_state_key

    #disposals
    disp_name_key = pd.read_csv(keys_path + 'disp_name_key.csv')
    disp_name_key.drop(disp_name_key.index[(disp_name_key['year'] != YEAR)], axis=0, inplace=True)    # Drop values not of year YEAR

    disp_name_key = pd.DataFrame({'code': disp_name_key['disp_name'], 'name': disp_name_key['disp_name_s']})
    disp_dict = dict(disp_name_key.values)
    del disp_name_key

    #types
    type_name_key = pd.read_csv(keys_path + 'type_name_key.csv')
    type_name_key.drop(type_name_key.index[(type_name_key['year'] != YEAR)], axis=0, inplace=True)    # Drop values not of year YEAR

    type_name_key = pd.DataFrame({'code': type_name_key['type_name'], 'name': type_name_key['type_name_s']})
    type_dict = dict(type_name_key.values)
    del type_name_key

    #purpose
    purpose_name_key = pd.read_csv(keys_path + 'purpose_name_key.csv')
    purpose_name_key.drop(purpose_name_key.index[(purpose_name_key['year'] != YEAR)], axis=0, inplace=True)    # Drop values not of year YEAR

    purpose_name_key = pd.DataFrame({'code': purpose_name_key['purpose_name'], 'name': purpose_name_key['purpose_name_s']})
    purpose_dict = dict(purpose_name_key.values)
    del purpose_name_key

    #judge_id from ddl_id
    judge_case_merge_key = pd.read_csv(keys_path + 'judge_case_merge_key.csv')

    filing_judge_key = pd.DataFrame({'code': judge_case_merge_key['ddl_case_id'], 'name': judge_case_merge_key['ddl_filing_judge_id']})
    filing_judge_dict = dict(filing_judge_key.values)

    decision_judge_key = pd.DataFrame({'code': judge_case_merge_key['ddl_case_id'], 'name': judge_case_merge_key['ddl_decision_judge_id']})
    decision_judge_dict = dict(decision_judge_key.values)

    del judge_case_merge_key
    del filing_judge_key
    del decision_judge_key

    #judge_pos, female, start_date, end_date from judge_id
    judges_clean = pd.read_csv(csv_path + 'judges_clean.csv')

    judges_pos = pd.DataFrame({'code': judges_clean['ddl_judge_id'], 'name': judges_clean['judge_position']})
    judges_pos_dict = dict(judges_pos.values)

    judges_female = pd.DataFrame({'code': judges_clean['ddl_judge_id'], 'name': judges_clean['female_judge']})
    judges_female_dict = dict(judges_female.values)

    judges_start = pd.DataFrame({'code': judges_clean['ddl_judge_id'], 'name': judges_clean['start_date']})
    judges_start_dict = dict(judges_start.values)

    judges_end = pd.DataFrame({'code': judges_clean['ddl_judge_id'], 'name': judges_clean['end_date']})
    judges_end_dict = dict(judges_end.values)

    del judges_clean
    del judges_pos
    del judges_female
    del judges_start
    del judges_end


    ############################################################################
    # We need to complete the following tables:

        # state_cases_table.csv
        # table1 = ['ddl_case_id', 'state_code', 'disp_code', 'type_name', 'purpose_name', 'date_of_filing', 'date_of_decision']  
        # # need to get state_name (from cases_state_key), disp_name (from disp_name_key), type_name (from type_name_key), purpose_name (from purpose_name_key) 

    data_path = 'data/' + str(YEAR) + '/'

    state_cases = pd.read_csv(data_path + 'state_cases_table.csv')

    state_names = list(pd.Series(state_cases['state_code']).map(state_dict))
    state_cases.drop('state_code',axis=1,inplace=True)
    state_cases['state_names'] = state_names
    del state_names

    disp_names = list(pd.Series(state_cases['disp_name']).map(disp_dict))
    state_cases.drop('disp_name',axis=1,inplace=True)
    state_cases['disp_names'] = disp_names
    del disp_names

    type_names = list(pd.Series(state_cases['type_name']).map(type_dict))
    state_cases.drop('type_name',axis=1,inplace=True)
    state_cases['type_names'] = type_names
    del type_names

    purpose_names = list(pd.Series(state_cases['purpose_name']).map(purpose_dict))
    state_cases.drop('purpose_name',axis=1,inplace=True)
    state_cases['purpose_names'] = purpose_names
    del purpose_names

    state_cases.to_csv('generated_tables/' + str(YEAR) + '/state_cases_table.csv')
    del state_cases

        # # gender_info_table
        # table2 = ['ddl_case_id', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_code'] 
        # # need to get disp_name (from disp_name_key), ddl_decision_judge_id (from judge_case_merge_key), female_judge (from judges_clean)

    gender_info = pd.read_csv(data_path + 'gender_info_table.csv')

    disp_names = list(pd.Series(gender_info['disp_name']).map(disp_dict))
    gender_info.drop('disp_name',axis=1,inplace=True)
    gender_info['disp_names'] = disp_names
    del disp_names

    ddl_decision_judge_id = list(pd.Series(gender_info['ddl_case_id']).map(decision_judge_dict))
    gender_info['ddl_decision_judge_id'] = ddl_decision_judge_id
    del ddl_decision_judge_id

    female_judge = list(pd.Series(gender_info['ddl_decision_judge_id']).map(judges_female_dict))
    gender_info['female_judge'] = female_judge
    del female_judge

    gender_info.to_csv('generated_tables/' + str(YEAR) + '/gender_info_table.csv')
    del gender_info

        # # filing_judges_table
        # table3 = ['ddl_case_id', 'date_of_filing', 'type_name', 'purpose_name'] 
        # # need to get ddl_filing_judge_id (from judge_case_merge_key), type_name (from type_name_key, purpose_name (from purpose_name_key), start_date (from judges_clean)

    filing_judges = pd.read_csv(data_path + 'filing_judges_table.csv')

    ddl_filing_judge_id = list(pd.Series(filing_judges['ddl_case_id']).map(filing_judge_dict))
    filing_judges['ddl_filing_judge_id'] = ddl_filing_judge_id
    del ddl_filing_judge_id

    type_names = list(pd.Series(filing_judges['type_name']).map(type_dict))
    filing_judges.drop('type_name',axis=1,inplace=True)
    filing_judges['type_names'] = type_names
    del type_names

    purpose_names = list(pd.Series(filing_judges['purpose_name']).map(purpose_dict))
    filing_judges.drop('purpose_name',axis=1,inplace=True)
    filing_judges['purpose_names'] = purpose_names
    del purpose_names

    start_date = list(pd.Series(filing_judges['ddl_filing_judge_id']).map(judges_start_dict))
    filing_judges['start_date'] = start_date
    del start_date

    filing_judges.to_csv('generated_tables/' + str(YEAR) + '/filing_judges_table.csv')
    del filing_judges

        # # Decision judge's information
        # table4 = ['ddl_case_id', 'date_of_decision', 'disp_name'] 
        # # need to get ddl_decision_judge_id (from judge_case_merge_key), type_name (from type_name_key, disp_name (from disp_name_key), start_date (from judges_clean)

    decision_judges = pd.read_csv(data_path + 'decision_judges_table.csv')

    ddl_decision_judge_id = list(pd.Series(decision_judges['ddl_case_id']).map(decision_judge_dict))
    decision_judges['ddl_decision_judge_id'] = ddl_decision_judge_id
    del ddl_decision_judge_id

    disp_names = list(pd.Series(decision_judges['disp_name']).map(disp_dict))
    decision_judges.drop('disp_name',axis=1,inplace=True)
    decision_judges['disp_names'] = disp_names
    del disp_names

    start_date = list(pd.Series(decision_judges['ddl_decision_judge_id']).map(judges_start_dict))
    decision_judges['start_date'] = start_date
    del start_date

    decision_judges.to_csv('generated_tables/' + str(YEAR) + '/decision_judges_table.csv')
    del decision_judges
