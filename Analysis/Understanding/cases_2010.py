import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, datetime

csv_path = '../../../csv/'

cases_2010 = pd.read_csv(csv_path + 'cases/cases/cases_2010.csv')

print(cases_2010.head())

#                 ddl_case_id  year  state_code  dist_code  court_no              cino  ... disp_name date_of_filing date_of_decision  date_first_list  date_last_list  date_next_list
# 0  01-01-01-200308002162010  2010           1          1         1  MHNB030013812010  ...        42     2010-12-13       2011-06-19       2011-06-08      2011-06-20      2011-06-24
# 1  01-01-01-200707000172010  2010           1          1         1  MHNB030004552010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
# 2  01-01-01-200707000182010  2010           1          1         1  MHNB030004562010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
# 3  01-01-01-200707000192010  2010           1          1         1  MHNB030004582010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30
# 4  01-01-01-200707000202010  2010           1          1         1  MHNB030004592010  ...        42     2010-02-25       2010-11-21       2010-08-06      2010-08-06      2010-11-30

print(cases_2010.info())

# RangeIndex: 4281327 entries, 0 to 4281326
# Data columns (total 19 columns):
#  #   Column             Dtype  
# ---  ------             -----  
#  0   ddl_case_id        object 
#  1   year               int64  
#  2   state_code         int64  
#  3   dist_code          int64  
#  4   court_no           int64  
#  5   cino               object 
#  6   judge_position     object 
#  7   female_defendant   object 
#  8   female_petitioner  object 
#  9   female_adv_def     int64  
#  10  female_adv_pet     int64  
#  11  type_name          int64  
#  12  purpose_name       float64
#  13  disp_name          int64  
#  14  date_of_filing     object 
#  15  date_of_decision   object 
#  16  date_first_list    object 
#  17  date_last_list     object 
#  18  date_next_list     object 
# dtypes: float64(1), int64(8), object(10)

for key in cases_2010:
    unique = cases_2010[key].unique()
    print(f"{key}\t{len(unique)}")
    try:
        unique = np.sort(unique)
    except:
        pass
    try:
        print(f"Min: {min(unique)}")
        print(f"Max: {max(unique)}")
    except:
        pass
    print(unique)
    print()

# ddl_case_id           xx-xx-xx-xxxxxxxxxxxxxxx
# year                  2010
# state_code            31 (1 to 32) (28 missing)
# dist_code             75 (1 to 76) (72 missing)
# court_no              68 (1 to 75 with missing numbers)
# cino                  4275094 (some are therefore repeated)
# judge_position	    434     (565 for cases_2010.csv)  (can be used to see increase in judge-positions over the years)

# female_defendant	    4 (nonfemale, female, unclear, nan)
# female_petitioner	    4 (nonfemale, female, unclear, nan)
# female_adv_def	    4 (nonfemale, female, unclear, nan)
# female_adv_pet	    4 (nonfemale, female, unclear, nan)

# type_name             5452 (1 to 5452)
# purpose_name          5266 (1 to 5265 and nan)
# disp_name             51 (1 to 51)

# date_of_filing        YYYY-MM-DD (365)
# date_of_decision      YYYY-MM-DD (4270)
# date_first_list	    4638
# date_last_list    	4352
# date_next_list        5242

ended = []
ongoing = []
durations = []

no_hearing = []
duration_first_trial = []

bad_data = 0
large_val = 0

for i,sd in enumerate(cases_2010['date_of_filing']):
    sd = datetime.strptime(sd, '%Y-%m-%d').date()
    hd = cases_2010['date_first_list'][i]
    ed = cases_2010['date_of_decision'][i]

    try:
        hd = datetime.strptime(hd, '%Y-%m-%d').date()
    except:
        hd = date.today()
        no_hearing.append((hd-sd).days)

    dur_ft = (hd-sd).days
    
    if dur_ft < 0:
        pass
    elif dur_ft > 4747:    # number of days between 2010-01-01 and 2022-12-31
        pass
    else:
        duration_first_trial.append(dur_ft)

    try:
        ed = datetime.strptime(ed, '%Y-%m-%d').date()
        ended.append((ed-sd).days)
    except:
        ed = date.today()
        ongoing.append((ed-sd).days)

    dur = (ed-sd).days
    if dur < 0:
        bad_data += 1
    elif dur > 4747:    # number of days between 2010-01-01 and 2022-12-31
        large_val += 1
    else:
        durations.append(dur)

# count of bad_data
# 25758
# count of large_val
# 132

# Therefore, we do some basic pre-processing here to remove these types of data before plotting

hist_bins = np.arange(min(duration_first_trial),max(duration_first_trial),(max(duration_first_trial)-min(duration_first_trial))/100)
plt.hist(duration_first_trial, bins=hist_bins)
plt.xlabel("Duration between filing and first trial in days")
plt.ylabel("Number of days")
plt.yscale("log")
plt.savefig("plots/first_trial_duration.png")
plt.show()

hist_bins = np.arange(min(durations),max(durations),(max(durations)-min(durations))/100)
plt.hist(durations, bins=hist_bins)
plt.xlabel("Case duration in days")
plt.ylabel("Number of days")
plt.yscale("log")
plt.savefig("plots/cases_duration.png")
plt.show()

plt.hist(ended, bins=hist_bins)
plt.xlabel("Case duration in days")
plt.ylabel("Number of judges")
plt.yscale("log")
plt.savefig("plots/cases_duration_ended.png")
plt.show()

plt.hist(ongoing, bins=hist_bins)
plt.xlabel("Term duration in days")
plt.ylabel("Number of judges")
plt.yscale("log")
plt.savefig("plots/cases_duration_ongoing.png")
plt.show()
