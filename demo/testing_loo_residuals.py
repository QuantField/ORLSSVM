import numpy as np
import pandas as pd
from lssvm.lssvm import lssvm

ZERO = 1.0E-8
# loading banana dataset
df = pd.read_csv("data/banana.csv")
n = 200
df = df.sample(n)
# binary classification, target/(class label) in LSSVM is in {-1,1}
df.loc[df['Class']==1,'Class'] = -1
df.loc[df['Class']==2,'Class'] = 1

net = lssvm()
all = list(range(n))
loo_residuals = np.zeros([n,1])
loo_error     = np.zeros([n,1])
for i in range(n):
    loo_index = all.copy()
    loo_index.remove(i)
    xtrain = df.iloc[loo_index,:]
    ytrain = xtrain.pop('Class')
    xtest  = df.iloc[[i],:]
    ytest  = xtest.pop('Class')
    net.fit(xtrain.values, ytrain.values)
    loo_residuals[i] = float(ytest) - float(net.predict(xtest.values))
    loo_error[i] = np.sign(ytest) != np.sign(net.predict(xtest.values))

loo_err = np.mean(loo_error)

y = df.pop('Class')
net.fit(df.values,y)
loo_residuals_test = net.loo_residuals()

diff = loo_residuals_test - loo_residuals.reshape(-1,)

np.max(np.abs(diff))<=ZERO


loo_err_test = net.loo_error()
loo_err_test - loo_error