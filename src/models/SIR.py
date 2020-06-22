import pandas as pd
import numpy as np
from datetime import datetime
from scipy import optimize
from scipy import integrate

def SIR_model_t(SIR, t, beta, gamma):
    S,I,R=SIR
    dS_dt = -beta*I*S/N0
    dI_dt = beta*I*S/N0 - gamma*I
    dR_dt = gamma*I

    return dS_dt, dI_dt, dR_dt

def fit_odeint(x, beta, gamma):
    return integrate.odeint(SIR_model_t, (S0, I0, R0), x, args=(beta, gamma))[:,1]


if __name__ == '__main__':

    df_analyse=pd.read_csv('E:/ads_covid-19/data/raw/COVID-19/csse_covid_19_data/SIR_raw.csv',sep=';')

    df_analyse.sort_values('Date',ascending=True)
    N0 = 1000000
    df_data = df_analyse[35:] ## We will consider data from 35th day, which is 26th Feb 2020
    t = np.arange(df_data.shape[0])

    for country in df_data.columns[1:]:
        ydata = np.array(df_data[df_data[country]>0][country])
        t = np.arange(len(ydata))
        I0=ydata[0]
        S0=N0-I0
        R0=0
        popt=[0.4,0.1]
        fit_odeint(t, *popt)
        popt, pcov = optimize.curve_fit(fit_odeint, t, ydata, maxfev=5000)
        perr = np.sqrt(np.diag(pcov))
        fitted=fit_odeint(t, *popt)
        f_padded = np.concatenate((np.zeros(df_data.shape[0]-len(fitted)) ,fitted)) #to make dimentions equal
        df_data[country + '_fitted'] = f_padded
    df_data.to_csv("E:/ads_covid-19/data/processed/SIR_calculated.csv", sep = ';', index=False)
