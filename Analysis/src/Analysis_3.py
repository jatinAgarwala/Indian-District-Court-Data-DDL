import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

for YEAR in ['2010', '2014', '2018']:
    table_path = '../generated_tables/' + YEAR + '/'

    decision_judges = pd.read_csv(table_path + 'decision_judges_table.csv')
    decision_judges = decision_judges.dropna(subset=['start_date','disp_names'])

# I misunderstood the dataset to mean that the start_date was the start of the judge's term, and wanted to find the most common first case assigned to a newly appointed judge
# Since the start_date is the start of the case, I cannot do this now, and have left this analysis empty.
