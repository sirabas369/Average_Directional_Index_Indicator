import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/home/sirabas/Documents/Quant club/qn1 final/stock_prices.csv')
interval  = 14 #look back period


df['-DM'] = df['Low'].shift(1) - df['Low']
df['+DM'] = df['High'] - df['High'].shift(1)
df['+DM'] = np.where((df['+DM'] > df['-DM']) & (df['+DM']>0), df['+DM'], 0.0)
df['-DM'] = np.where((df['-DM'] > df['+DM']) & (df['-DM']>0), df['-DM'], 0.0)
df['TR_TMP1'] = df['High'] - df['Low']
df['TR_TMP2'] = np.abs(df['High'] - df['Adj Close'].shift(1))
df['TR_TMP3'] = np.abs(df['Low'] - df['Adj Close'].shift(1))
df['TR'] = df[['TR_TMP1', 'TR_TMP2', 'TR_TMP3']].max(axis=1)

for i in range(interval-1 , len(df['Close'])):
    if(i == interval - 1):
        df.loc[i,'TR_smt'] = df.loc[0:interval, 'TR'].mean()
        df.loc[i,'+DM_smt'] = df.loc[0:interval, '+DM'].mean()
        df.loc[i,'-DM_smt'] = df.loc[0:interval, '-DM'].mean()
    else:
        df.loc[i,'TR_smt'] = ( (df.loc[i-1,'TR_smt'] * (13)) + df.loc[i,'TR'] )/14
        df.loc[i,'+DM_smt'] = ( (df.loc[i-1,'+DM_smt'] * (13)) + df.loc[i,'+DM'] )/14
        df.loc[i,'-DM_smt'] = ( (df.loc[i-1,'-DM_smt'] * (13)) + df.loc[i,'-DM'] )/14


df['+DI'] = ( df['+DM_smt'] / df['TR_smt'] )*100
df['-DI'] = ( df['-DM_smt'] / df['TR_smt'] )*100

df['DX'] = ( abs(df['+DI'] - df['-DI']) / abs(df['+DI'] + df['-DI']) )*100

for i in range(2*(interval-1) , len(df['Close'])):
    if(i == 2*(interval - 1)):
        df.loc[i,'ADX'] = df.loc[(interval - 1) : 2*(interval - 1), 'DX'].mean()
    else:
        df.loc[i,'ADX'] = ( (df.loc[i-1,'ADX'] * 13) + df.loc[i,'DX'] )/14



#df.to_csv('ADX Data')
fig , axis = plt.subplots(2,1)
axis[0].plot(df['Close'])
axis[1].plot(df['ADX'] , label = 'ADX')
axis[1].plot(df['+DI'] , label = '+DI')
axis[1].plot(df['-DI'] , label = '-DI')
plt.legend()
plt.show()

