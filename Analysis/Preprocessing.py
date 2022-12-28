import pandas as pd
from datetime import date, datetime

csv_path = '../../csv/'

for YEAR in ['2010','2014','2018']:

    cases_2010 = pd.read_csv(csv_path + 'cases/cases/cases_' + YEAR + '.csv')

    # We do some basic pre-processing here to remove bad entries with first hearing or date of decision after the date of filing
    # This is because there have been incorrect entries in the dataset, including years like 0201 and 2030

    bad_data = []

    for i,sd in enumerate(cases_2010['date_of_filing']):
        sd = datetime.strptime(sd, '%Y-%m-%d').date()
        hd = cases_2010['date_first_list'][i]
        ed = cases_2010['date_of_decision'][i]

        try:
            hd = datetime.strptime(hd, '%Y-%m-%d').date()
        except:
            hd = date.today()

        dur_ft = (hd-sd).days
        
        if dur_ft < 0:
            bad_data.append(i)
            continue
        elif dur_ft > 4747:     # number of days between 2010-01-01 and 2022-12-31
            bad_data.append(i)
            continue

        try:
            ed = datetime.strptime(ed, '%Y-%m-%d').date()
        except:
            ed = date.today()

        dur = (ed-sd).days
        if dur < 0:
            bad_data.append(i)
        elif dur > 4747:        # number of days between 2010-01-01 and 2022-12-31
            bad_data.append(i)

    cases_2010.drop(bad_data, axis=0, inplace=True)


    # HEAD

    #                 ddl_case_id  year  state_code  dist_code  court_no              cino  ... disp_name date_of_filing date_of_decision  date_first_list  date_last_list  date_next_list
    # 0  01-01-01-200308002162010  2010           1          1         1  MHNB030013812010  ...        42     2010-12-13       2011-06-19       2011-06-08      2011-06-20      2011-06-24
    # 1  01-01-01-200707000172010  2010           1          1         1  MHNB030004552010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
    # 2  01-01-01-200707000182010  2010           1          1         1  MHNB030004562010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
    # 3  01-01-01-200707000192010  2010           1          1         1  MHNB030004582010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
    # 4  01-01-01-200707000202010  2010           1          1         1  MHNB030004592010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30


    # We observe that judge_case_merge_key.csv is the only file which has ddl_case_id, so we will be using it to get filing judge and decision judge when needed
    # Then, we can use judges_clean.csv to get more information about the judges as per our requirement


    # We create the following datasets:
    #   1. ddl_case_id, state_name, disp_name, type_name, purpose_name, date_of_filing, date_of_decision
    #   2. ddl_case_id, female_defendant, female_petitioner, female_adv_def, female_adv_pet, type_name, purpose_name, disp_name, ddl_decision_judge_id, female_judge
    #   3. ddl_case_id, ddl_filing_judge, date_of_filing, type_name, purpose_name, judge_start_date
    #   4. ddl_case_id, ddl_decision_judge, date_of_decision, disp_name, judge_start_date

    # judges_clean = pd.read_csv(csv_path + 'judges_clean.csv')

    # judges_clean.replace(np.nan,'-1',inplace = True)
    # judges_clean.replace('0 nonfemale','0',inplace = True)
    # judges_clean.replace('1 female','1',inplace = True)
    # judges_clean.replace('-9998 unclear','-1',inplace = True)

    judges_clean = pd.read_csv(csv_path + 'judges_clean.csv')


    all_columns = ['ddl_case_id', 'year', 'state_code', 'dist_code', 'court_no', 'cino', 'judge_position', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_name', 'date_of_filing', 'date_of_decision', 'date_first_list', 'date_last_list', 'date_next_list']

    # State-wise information
    table1 = ['ddl_case_id', 'state_code', 'disp_name', 'type_name', 'purpose_name', 'date_of_filing', 'date_of_decision']  # need to get state_name (from cases_state_key), disp_name (from disp_name_key), type_name (from type_name_key), purpose_name (from purpose_name_key) 

    # Gender information
    table2 = ['ddl_case_id', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_name'] # need to get disp_name (from disp_name_key), ddl_decision_judge_id( from judge_case_merge_key), female_judge (from judges_clean)

    # Filing judges information
    table3 = ['ddl_case_id', 'date_of_filing', 'type_name', 'purpose_name'] # Need to get ddl_filing_judge_id (from judge_case_merge_key), type_name (from type_name_key, purpose_name (from purpose_name_key), start_date (from judges_clean)

    # Decision judge's information
    table4 = ['ddl_case_id', 'date_of_decision', 'disp_name'] # Need to get ddl_decision_judge_id (from judge_case_merge_key), type_name (from type_name_key, disp_name (from disp_name_key), start_date (from judges_clean)

    state_cases = cases_2010.drop(list(set(all_columns).difference(table1)),axis=1)
    state_cases.to_csv('data/' + YEAR + '/state_cases_table.csv')

    del state_cases

    gender_info = cases_2010.drop(list(set(all_columns).difference(table2)),axis=1)
    gender_info.to_csv('data/' + YEAR + 'gender_info_table.csv')

    del gender_info

    filing_judges = cases_2010.drop(list(set(all_columns).difference(table3)),axis=1)
    filing_judges.to_csv('data/' + YEAR + 'filing_judges_table.csv')

    del filing_judges

    decision_judges = cases_2010.drop(list(set(all_columns).difference(table4)),axis=1)
    decision_judges.to_csv('data/' + YEAR + 'decision_judges_table.csv')

    del decision_judges
