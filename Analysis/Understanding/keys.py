# act_key               : name and count of every act (can be used to plot most common acts under which crimes are committed)
# cases_court_key       : court names of all the courts district-wise (can be used to get count of courts per state or district)
# cases_district_key    : state and district names and codes (can be used as a foreign key later maybe)
# cases_state_key       : state name, code and id (can be used as a foreign key later maybe)
# disp_name_key         : disp name and corresponding count (can be used as key and for most common disposals)
# judge_case_merged_key : <too large for manual checking, has been done by code>
# purpose_name_key      : purpose name and count (can be used as key and for most common purposes)
# section_key           : section name and count (can be used as key and for most common sections)
# type_name_key         : type name and count (can be used as key and for most common types)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, datetime

keys_path = '../../../csv/keys/keys/'

act_key = pd.read_csv(keys_path + 'act_key.csv')
print(act_key.head())
print(act_key.info())
print(act_key.describe())

#               count           act
# count  2.985700e+04  29856.000000
# mean   2.571109e+03  14928.500000
# std    1.355349e+05   8618.829155
# min    1.000000e+00      1.000000
# 25%    2.000000e+00   7464.750000
# 50%    7.000000e+00  14928.500000
# 75%    5.000000e+01  22392.250000
# max    2.090000e+07  29856.000000

plt.plot(act_key['act'],act_key['count'])
plt.yscale('log')
plt.savefig('plots/act_wise_count.png')
plt.show()

act_key = act_key.sort_values(by='count', ascending=False)
act_key.head()

print(act_key[0:20])

#                                         act_s       count      act
# 17353                   The Indian Penal Code  20900000.0  17353.0
# 4759               Code of Criminal Procedure   8630668.0   4759.0
# 10581                      Motor Vehicles Act   3124278.0  10581.0
# 4747                  Code of Civil Procedure   2679956.0   4747.0
# 4650                     Civil Procedure Code   1746442.0   4650.0
# 11007              Negotiable Instruments Act   1740873.0  11007.0
# 4069                  CODE OF CIVIL PROCEDURE   1341937.0   4069.0
# 7416                            I.P.C(Police)   1227504.0   7416.0
# 9846                       MOTOR VEHICLES ACT   1079427.0   9846.0
# 10564                       Motor Vehicle Act   1049607.0  10564.0
# 4074       CODE OF CIVIL PROCEDURE, 1908 (HB)    990106.0   4074.0
# 7276                       Hindu Marriage Act    909387.0   7276.0
# 6748   GUJARAT (BOMBAY) PROHIBITION ACT, 1949    876446.0   6748.0
# 10809        NEGOTIABLE INSTRUMENTS ACT, 1881    790884.0  10809.0
# 10808              NEGOTIABLE INSTRUMENTS ACT    780690.0  10808.0
# 9847                 MOTOR VEHICLES ACT, 1988    666677.0   9847.0
# 4763                     CodeofCivilProcedure    584990.0   4763.0
# 13504           Prohibition Act (Maharashtra)    473702.0  13504.0
# 10584                 Motor Vehicles Act 1988    461580.0  10584.0
# 6260                          Excise Act 1915    454158.0   6260.0

del act_key
print()

cases_court_key = pd.read_csv(keys_path + 'cases_court_key.csv')
print(cases_court_key.head())
print(cases_court_key.info())
print(cases_court_key.describe())

statewise = {'state_code':cases_court_key['state_code']}   
sns.countplot(x='state_code', data=statewise)
plt.savefig('plots/state_wise_courts.png')
plt.show()

districtwise = {'dist_code':cases_court_key['dist_code']}   
sns.countplot(x='dist_code', data=districtwise)
plt.savefig('plots/district_wise_courts.png')
plt.show()

del cases_court_key
print()

disp_name_key = pd.read_csv(keys_path + 'disp_name_key.csv')
print(disp_name_key.head())
print(disp_name_key.info())
print(disp_name_key.describe())

plt.plot(disp_name_key['count'])
plt.yscale('log')
plt.savefig('plots/verdict_wise_count.png')
plt.show()

disp_name_key = disp_name_key.sort_values(by='count', ascending=False)
disp_name_key.head()

print(disp_name_key[0:20])

#      year  disp_name              disp_name_s    count
# 436  2018         27  disposition var missing  6338472
# 384  2017         27  disposition var missing  4521012
# 332  2016         27  disposition var missing  3260488
# 280  2015         26  disposition var missing  2259042
# 229  2014         26  disposition var missing  1607071
# 178  2013         26  disposition var missing  1244271
# 414  2018          5                  allowed  1104047
# 362  2017          5                  allowed  1101941
# 276  2015         22                dismissed   961444
# 225  2014         22                dismissed   957554
# 310  2016          5                  allowed   938736
# 127  2012         26  disposition var missing   899879
# 382  2017         25                 disposed   892083
# 174  2013         22                dismissed   885011
# 259  2015          5                  allowed   881581
# 123  2012         22                dismissed   839733
# 328  2016         23                dismissed   820324
# 434  2018         25                 disposed   778906
# 208  2014          5                  allowed   767580
# 387  2017         30                     fine   763001

del disp_name_key
print()

judge_case_merge_key = pd.read_csv(keys_path + 'judge_case_merge_key.csv')
print(judge_case_merge_key.head())

#                 ddl_case_id  ddl_filing_judge_id  ddl_decision_judge_id
# 0  01-01-01-201900000022018                  5.0                    5.0
# 1  01-01-01-201900000032017                  5.0                    5.0
# 2  01-01-01-201900000032018                 94.0                   94.0
# 3  01-01-01-201900000042016                  3.0                    5.0
# 4  01-01-01-201900000042018                156.0                  156.0

print(judge_case_merge_key.info())
print(judge_case_merge_key.describe())

judgewise = {'ddl_filing_judge_id':judge_case_merge_key['ddl_filing_judge_id']}   
sns.countplot(x='ddl_filing_judge_id', data=judgewise)
plt.savefig('plots/ddl_filing_judge_wise_count.png')
plt.show()

del judgewise

judgewise = {'ddl_decision_judge_id':judge_case_merge_key['ddl_decision_judge_id']}   
sns.countplot(x='ddl_decision_judge_id', data=judgewise)
plt.savefig('plots/ddl_decision_judge_count.png')
plt.show()

del judgewise

del judge_case_merge_key
print()

purpose_name_key = pd.read_csv(keys_path + 'purpose_name_key.csv')
print(purpose_name_key.head())
print(purpose_name_key.info())
print(purpose_name_key.describe())

plt.plot(purpose_name_key['count'])
plt.yscale('log')
plt.savefig('plots/purpose_wise_count.png')
plt.show()

del purpose_name_key
print()

section_key = pd.read_csv(keys_path + 'section_key.csv')
print(section_key.head())
print(section_key.info())
print(section_key.describe())

plt.plot(section_key['count'])
plt.yscale('log')
plt.savefig('plots/section_wise_count.png')
plt.show()

del section_key
print()

type_name_key = pd.read_csv(keys_path + 'type_name_key.csv')
print(type_name_key.head())
print(type_name_key.info())
print(type_name_key.describe())

plt.plot(type_name_key['count'])
plt.yscale('log')
plt.savefig('plots/type_wise_count.png')
plt.show()

del type_name_key
print()