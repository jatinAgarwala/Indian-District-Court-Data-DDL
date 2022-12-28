"""
Classification 1:
inputs: state, judge_position, female_defendant, female_petitioner, female_adv_def, female_adv_pet, type_name, purpose_name, date_of_filing, date_of_decision, date_first_list, date_last_list, date_next_list
outputs: disp_name

    Note:
    if outputs for binary classification guilty or not guilty based on 
    guilty_disposals = ['convicted', 'committed','plea bargaining','remanded','probation','plead guilty','prison','confession', 'fine', 'uncontested', 'execution', 'absconded']

Classification 2: Same as Classification 1 without gender inputs
"""
import torch
import pandas as pd
from torch.utils.data import Dataset
from datetime import datetime, date

import numpy as np
from tqdm import tqdm

from sklearn.model_selection import train_test_split

csv_path = '../../csv/'
YEAR = '2010'
cases_path = csv_path + 'cases/cases/cases_' + YEAR + '.csv'

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

START = date(1990, 1, 1)
def numdays(date):
    td = date - START
    return td.days

OUTPUT_SIZE = -1
INPUT_SIZE = -1

input_cols = ['state_code','female_defendant','female_petitioner','female_adv_def','female_adv_pet','type_name','purpose_name']
date_inputs =['date_of_filing','date_of_decision','date_first_list','date_last_list','date_next_list']
judge_input = 'judge_position'
output_col = 'disp_name'

guilty_disposals = ['convicted', 'committed','plea bargaining','remanded','probation','plead guilty','prison','confession', 'fine', 'uncontested', 'execution', 'absconded']

def PreProcessing(path_to_csv, guilty = False):
    cases = pd.read_csv(path_to_csv)
    cases.dropna(inplace=True)
    cases.replace('-9998 unclear', 0, inplace=True)
    cases.replace('-9999 missing name', 0, inplace=True)
    cases.replace(-9999, 0, inplace=True)
    cases.replace(-9998, 0, inplace=True)
    cases.replace('0 male', 0.1, inplace=True)
    cases.replace('0 nonfemale', 0.1, inplace=True)
    cases.replace('1 female', 0.9, inplace=True)

    inputs = []

    for col in input_cols:
        temp_col = cases[col].values
        inputs.append(np.array(temp_col, dtype=np.float32))


    for col in date_inputs:
        temp_col = list(map(lambda x: numdays(datetime.strptime(x, '%Y-%m-%d').date()), cases[col].values))
        inputs.append(np.array(temp_col, dtype=np.float32))

    judge_pos_list = list(cases[judge_input].unique())
    judge_pos_dict = {k: v for v, k in enumerate(judge_pos_list)}
    judge_col = map(lambda x: judge_pos_dict[x], cases['judge_position'].values)
    inputs.append(np.array(list(judge_col), dtype=np.float32))

    inputs = list(map(list, zip(*inputs)))

    outputs = cases['disp_name'].values
    if guilty == True:
        keys_path = csv_path + 'keys/keys/'
        disp_name_key = pd.read_csv('disp_name_key.csv')
        guilty_indices = []
        for disp in guilty_disposals:
            key = disp_name_key[disp_name_key['disp_name_s'] == disp]['disp_name'].values[0]
            guilty_indices.append(key)
        outputs = list(map(lambda x: 1 if x in guilty_indices else 0, outputs))

    global INPUT_SIZE
    global OUTPUT_SIZE
    
    INPUT_SIZE = len(inputs[0])
    OUTPUT_SIZE = cases[output_col].nunique()

    X_train, X_rest, y_train, y_rest = train_test_split(inputs, outputs, random_state=0, train_size = 0.8)
    X_valid, X_test, y_valid, y_test = train_test_split(X_rest,y_rest, train_size=0.5)
    return ((X_train,y_train), (X_valid,y_valid), (X_test,y_test))

class DataDispFem(Dataset):
    def __init__(self, data):
        super().__init__()
        (self.inputs, self.outputs) = data
        self.len = len(self.outputs)
    
    def __getitem__(self, index):
        return (torch.tensor(self.inputs[index]).to(DEVICE), torch.tensor(self.outputs[index]).to(DEVICE))

    def __len__(self):
        return self.len

class DataDispNoFem(Dataset):
    def __init__(self, data):
        super().__init__()
        (self.inputs, self.outputs) = data
    
        self.inputs = np.array(self.inputs)
        female_indices = [1,2,3,4]
        self.inputs = np.delete(self.inputs, female_indices, axis=1)

        global INPUT_SIZE
        INPUT_SIZE = len(self.inputs[0])

        self.len = len(self.outputs)
    
    def __getitem__(self, index):
        return (torch.tensor(self.inputs[index]).to(DEVICE), torch.tensor(self.outputs[index]).to(DEVICE))

    def __len__(self):
        return self.len

train, valid, test = PreProcessing('cases_2010.csv')

print(f"Input size: {INPUT_SIZE}")
print(f"Output size: {OUTPUT_SIZE}")

# inputs: state, judge_position, female_defendant, female_petitioner, female_adv_def, female_adv_pet, type_name, purpose_name, date_of_filing, date_of_decision, date_first_list, date_last_list, date_next_list
# outputs: disp_name