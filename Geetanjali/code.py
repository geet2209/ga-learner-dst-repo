# --------------
# Importing header files
import numpy as np
import pandas as pd
from scipy.stats import mode 
 
import warnings
warnings.filterwarnings('ignore')


#Reading file
bank = pd.read_csv(path)



#Code starts here
categorical_var = bank.select_dtypes(include = 'object')
print(categorical_var.info())

numerical_var = bank.select_dtypes(include = 'number')
print(numerical_var.info())

banks = bank.drop(columns = 'Loan_ID')
print(banks.isnull().sum())
bank_mode = banks.mode().iloc[0]
banks.fillna(bank_mode, inplace=True)
print(banks.isnull().sum())
avg_loan_amount = pd.pivot_table(banks,
                  values = 'LoanAmount',
                  index = ['Gender', 'Married', 'Self_Employed'],
                  aggfunc=np.mean)
print(avg_loan_amount['LoanAmount'][1],2)

loan_approved_se = banks.loc[(banks['Self_Employed'] == 'Yes') 
                   & (banks['Loan_Status'] == 'Y') ]
loan_approved_nse = banks.loc[(banks['Self_Employed'] == 'Yes') 
                   & (banks['Loan_Status'] == 'N') ]
#print (loan_approved_se)
percentage_se = loan_approved_se[loan_approved_se['Self_Employed'] == 'Yes']['Self_Employed'].value_counts()*100/614
percentage_nse = loan_approved_se[loan_approved_se['Self_Employed'] == 'No']['Self_Employed'].value_counts()*100/614

print(percentage_se)
print(percentage_nse)

############### Step 5

banks['loan_term'] = banks['Loan_Amount_Term'].apply(lambda x: int(x)/12)
big_loan_term = banks[banks['loan_term'] >= 25]['loan_term'].value_counts()
#print(big_loan_term)
loan_groupby = banks.groupby('Loan_Status')['ApplicantIncome','Credit_History']
mean_values = loan_groupby.agg([np.mean])
print(mean_values.iloc[1,0],2)









