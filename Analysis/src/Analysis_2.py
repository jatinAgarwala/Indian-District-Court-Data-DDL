import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from tabulate import tabulate

    # # gender_info_table
    # table2 = ['ddl_case_id', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet', 'type_name', 'purpose_name', 'disp_code'] 
    # # need to get disp_name (from disp_name_key), ddl_decision_judge_id (from judge_case_merge_key), female_judge (from judges_clean)

def get_percentage(gender_info, key):
    m = gender_info[key].value_counts()[0]
    f = gender_info[key].value_counts()[1]
    print(key, f, f/(m+f))
    return (f/(m+f),f)
    
year_wise_percentages = []
year_wise_counts = []
year_wise_pair_percentages = []

year_wise_disp_percentage = []

positions = ['female_judge', 'female_defendant', 'female_petitioner', 'female_adv_def', 'female_adv_pet']   # decision_judge
pairs = ['defendant-judge','petitioner-judge','defendant-advocate','petitioner-advocate']
fem_guilty_pairs = ['Fem def & judge', 'Guilty with fem judge vs total guilty', 'Percentage guilty', 'Guilty with fem judge vs total with fem']

# both the adv columns only have 1, and not '1 female'

for YEAR in ['2010','2014','2018']:
    curr_year_percentages = []
    curr_year_counts = []
    table_path = '../generated_tables/' + YEAR + '/'

    gender_info = pd.read_csv(table_path + 'gender_info_table.csv')
    gender_info.drop('Unnamed: 0',axis=1,inplace=True)
    gender_info.drop('Unnamed: 0.1',axis=1,inplace=True)

    gender_info = gender_info.replace('0 nonfemale',0)
    gender_info = gender_info.replace('0 male',0)
    gender_info = gender_info.replace('1 female',1)

    i = 0
    for pos in positions:
        (percentage, count) = get_percentage(gender_info,pos)         
        curr_year_percentages.append(percentage)
        curr_year_counts.append(count)

    year_wise_percentages.append(curr_year_percentages)
    year_wise_counts.append(curr_year_counts)

    plt.plot(positions,curr_year_percentages)
    plt.savefig('../plots2/Gender-wise percentages of different roles in ' + YEAR + '.png')
    plt.close()

    plt.plot(positions,curr_year_counts)
    plt.savefig('../plots2/Female counts of different roles in ' + YEAR + '.png')
    plt.close()

    fem_def_count = gender_info.value_counts(['female_defendant'])[1]
    fem_judge_count = gender_info.value_counts(['female_judge'])[1]
    fem_pet_count = gender_info.value_counts(['female_petitioner'])[1]

    def_judge_counts = gender_info.value_counts(['female_judge','female_defendant'])[1,1]
    pet_judge_counts = gender_info.value_counts(['female_judge','female_petitioner'])[1,1]
    
    def_adv_counts = gender_info.value_counts(['female_defendant', 'female_adv_def'])[1,1]
    pet_adv_counts = gender_info.value_counts(['female_petitioner', 'female_adv_pet'])[1,1]
    
    def_judge_percentage = def_judge_counts/fem_def_count    # percentage of female defendant getting assigned female judge (random)
    pet_judge_percentage = pet_judge_counts/fem_pet_count    # percentage of female petitioner getting assigned female judge (random)

    def_adv_percentage = def_adv_counts/fem_def_count    # percentage of female defendant getting female advocate (not random)
    pet_adv_percentage = pet_adv_counts/fem_pet_count    # percentage of female petitioner getting female advocate (not random)
    
    percentages = [def_judge_percentage, pet_judge_percentage, def_adv_percentage, pet_adv_percentage]
    print([pairs, percentages])
    year_wise_pair_percentages.append(percentages)

    #######################################################

    # The following is the list of all possible disposals from the dataset

    # possible_disp_names: ['other', 'withdrawn', 'allowed', 'disposition var missing','dismissed', 'abated', 'referred to lok adalat','disposed-otherwise', 'reject', 'decided', 'ex-parte', 'settled','procedural', 'compromise', 'acquitted', 'convicted', 'committed','plea bargaining', '258 crpc', 'transferred', 'bail granted','bail refused', 'bail rejected', 'remanded', 'compounded','probation', 'died', 'judgement', 'disposed', 'otherwise','plead guilty', 'prison', 'quash', 'closed', 'bail order','partly decreed', 'award', 'confession', 'fine', 'converted','stayed', 'sine die', 'uncontested', 'execution', 'untrace','appeal accepted', 'p.o. consign', 'cancelled', 'contest-allowed','not press', 'absconded', 'disposal in lok adalat']

    # From this list, it is observed that the following disposals lead to the defendant being punished:
        # Convicted
        # Committed
        # Plea bargaining
        # Remanded
        # Probation
        # Fine
        # Execution

        # Plead guilty
        # Prison
        # Confession
        # Absconded

    # For the sake of convenience, we will be assumming that the defendant was found not guilty in the other cases, or a settlement was reached
    
    #######################################################

    guilty_disposals = ['convicted', 'committed','plea bargaining','remanded','probation','plead guilty','prison','confession', 'fine', 'uncontested', 'execution', 'absconded']

    guilty_disp_count = 0
    guilty_fem_disp_count = 0
    for disp in guilty_disposals:
        try:
            disp_count = gender_info.value_counts(['female_defendant','disp_names'])[1,disp]
        except:
            continue
        guilty_disp_count += disp_count
        try:
            fem_disp_count = gender_info.value_counts(['female_judge','female_defendant','disp_names'])[1,1,disp]
        except:
            continue
        guilty_fem_disp_count += fem_disp_count
    
    # def_judge_percentage                                          # with fem judge        / total defendant
    guilty_fem_percentage = guilty_fem_disp_count/guilty_disp_count # guilty with fem judge / total guilty
    disp_fem_percentage = guilty_fem_disp_count/def_judge_counts    # guilty with fem judge / total with fem judge
    guilty_percentage = guilty_disp_count/fem_def_count             # guilty percentage

    guilty_disp_info = [def_judge_percentage, disp_fem_percentage, guilty_percentage, guilty_fem_percentage]
    print(fem_guilty_pairs)
    print(guilty_disp_info)
    plt.plot(fem_guilty_pairs,guilty_disp_info)
    plt.savefig('../plots2/Female percentages of guilty disposals in ' + YEAR + '.png')
    plt.close()
    year_wise_disp_percentage.append(guilty_disp_info)

for entry in year_wise_percentages:
    plt.plot(positions, entry)
plt.legend([2010,2014,2018])
plt.savefig('../plots2/Year-wise gender percentages of different roles.png')
plt.close()

for entry in year_wise_counts:
    plt.plot(positions, entry)
plt.legend([2010,2014,2018])
plt.savefig('../plots2/Year-wise female counts of different roles.png')
plt.close()

for entry in year_wise_pair_percentages:
    plt.plot(pairs, entry)
plt.legend([2010,2014,2018])
plt.savefig('../plots2/Year-wise female percentages of different pairs of roles.png')
plt.close()

for entry in year_wise_disp_percentage:
    plt.plot(fem_guilty_pairs, entry)
plt.legend([2010,2014,2018])
plt.savefig('../plots2/Year-wise female percentages of guilty disposals.png')
plt.close()
