# --------------
#Importing header files
import pandas as pd
import scipy.stats as stats
import math
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.weightstats import ztest
from statsmodels.stats.weightstats import ztest
from scipy.stats import chi2_contingency

import warnings

warnings.filterwarnings('ignore')
#Sample_Size
sample_size=2000

#Z_Critical Score
z_critical = stats.norm.ppf(q = 0.95)  

# Critical Value
critical_value = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence*
                      df = 6)   # Df = number of variable categories(in purpose) - 1


#Reading file
data=pd.read_csv(path)

#Code starts here
#create sample of data 
data_sample = data.sample(n = sample_size , random_state = 0) 

sample_mean = data_sample['installment'].mean()
population_std = data['installment'].std()
margin_of_error = z_critical * (population_std/math.sqrt(sample_size))
confidence_interval = (sample_mean - margin_of_error,
                       sample_mean + margin_of_error)
true_mean = data['installment'].mean()
print(confidence_interval)
print(true_mean)

sample_size = np.array([20, 50, 100])

fig, axes = plt.subplots(3,1, figsize = (10,20))

#running loop to iterate over rows
for i in range(len(sample_size)):
    m = []
    #loop to implement number of samples
    for j in range(1000):
        mean = data['installment'].sample(sample_size[i]).mean()
        #mean = j +1
        m.append(mean)
    #convert list to series
    mean_series = pd.Series(m)
    axes[i].hist(mean_series, normed = True)
#plt.show()


#Small busiess interests
data["int.rate"] = data["int.rate"].map(lambda x: str(x)[:-1])
print(data["int.rate"].head())
data["int.rate"] = data["int.rate"].astype(float)/100
z_statistic_1, p_value_1 = ztest(data[data['purpose'] == 'small_business']['int.rate'], value=data['int.rate'].mean(), alternative = 'larger')

print(('z-statistic_1 is :{}'.format(z_statistic_1)))
print(('p_value_1 is :{}'.format(p_value_1)))

#Loan defaulting
z_statistic_2, p_value_2 = ztest(x1 = data[data['paid.back.loan'] == 'No']['installment'], x2= data[data['paid.back.loan'] == 'Yes']['installment'] )
print(('z-statistic_2 is :{}'.format(z_statistic_2)))
print(('p_value_2 is :{}'.format(p_value_2)))

#Chi2 test
critical_value = stats.chi2.ppf(q=0.95, df = 6)
yes = data[data['paid.back.loan'] == 'Yes']['purpose'].value_counts()
no = data[data['paid.back.loan'] == 'No']['purpose'].value_counts()

observed = pd.concat([yes.transpose(), no.transpose()], 1, keys = ['Yes', 'No'])
print(observed)

chi2, p, dof, ex = chi2_contingency(observed)

print (critical_value, chi2)





