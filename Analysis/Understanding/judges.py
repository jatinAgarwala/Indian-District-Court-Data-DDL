import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, datetime

csv_path = '../../../csv/'

judges_clean = pd.read_csv(csv_path + 'judges_clean.csv')

print(judges_clean.head())

#    ddl_judge_id  state_code  dist_code  court_no             judge_position female_judge  start_date    end_date
# 0             1           1          1         1  chief judicial magistrate  0 nonfemale  20-09-2013  20-02-2014
# 1             2           1          1         1  chief judicial magistrate  0 nonfemale  31-10-2013  20-02-2014
# 2             3           1          1         1  chief judicial magistrate  0 nonfemale  21-02-2014  31-05-2016
# 3             4           1          1         1  chief judicial magistrate  0 nonfemale  01-06-2016  06-06-2016
# 4             5           1          1         1  chief judicial magistrate  0 nonfemale  06-06-2016  07-07-2018

# Therefore, the 8 columns are given.

print(judges_clean.info())

# info shows that only 80320 non-null entries are present for end_date out of 98478, which means that 98478-80320 = 18158 are still in service
# There is also a judge with a null value for female_judge, which we will be treating as "Prefer Not To Say", wherever needed

# We will now find the number of unique courts, districts and states, and visualise them

for key in judges_clean:
    unique = judges_clean[key].unique()
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

# ddl_judge_id	98478   (1 to 98478)
# state_code	29      (1 to 30)
# dist_code	74          (1 to 75)
# court_no	825         (1 to 999 with some missing)
# judge_position	565
# female_judge	4       (nonfemale, female, unclear, nan)
# start_date	4231    
# end_date	3781

# judges_clean.replace(np.nan,'-1',inplace = True)

# Visualising the number of entries per state, and the gender ratios:

statewise = {'state_code':judges_clean['state_code']}   
sns.countplot(x='state_code', data=statewise)
plt.savefig('plots/state_wise_judges.png')
plt.show()

genderwise = {'female_judge':judges_clean['female_judge']}   
sns.countplot(x='female_judge', data=genderwise)
plt.savefig('plots/gender_wise_judges.png')
plt.show()

# I have assumed that the judges without enddays are still working till date

ended = []
ongoing = []
durations = []
for i,sd in enumerate(judges_clean['start_date']):
    sd = datetime.strptime(sd, '%d-%m-%Y').date()
    ed = judges_clean['end_date'][i]
    try:
        ed = datetime.strptime(ed, '%d-%m-%Y').date()
        ended.append((ed-sd).days)
    except:
        ed = date.today()
        ongoing.append((ed-sd).days)
    durations.append((ed-sd).days)

hist_bins = np.arange(min(durations),max(durations),(max(durations)-min(durations))/50)
plt.hist(durations, bins=hist_bins)
plt.xlabel("Term duration in days")
plt.ylabel("Number of judges")
plt.yscale("log")
plt.savefig("plots/judges_term_duration.png")
plt.show()

plt.hist(ended, bins=hist_bins)
plt.xlabel("Term duration in days")
plt.ylabel("Number of judges")
plt.yscale("log")
plt.savefig("plots/judges_term_duration_ended.png")
plt.show()

plt.hist(ongoing, bins=hist_bins)
plt.xlabel("Term duration in days")
plt.ylabel("Number of judges")
plt.yscale("log")
plt.savefig("plots/judges_term_duration_ongoing.png")
plt.show()
