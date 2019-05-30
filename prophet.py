import numpy as np
from fbprophet import Prophet
import pandas as pd

def log_transform(df):
    df['y'] = df['y'] + 1
    df['y'] = np.log(df['y'])
    return df

def inverse_log_transform(df):
    df['yhat'] = np.exp(df['yhat'])-1
    df['yhat_lower'] = np.exp(df['yhat_lower'])-1
    df['yhat_upper'] = np.exp(df['yhat_upper'])-1
    return df

def prophesy(df_popsike):

    curr_release = df_popsike['release_id'].iloc[0]
    curr_release_min = pd.DataFrame({
        'ds': df_popsike[df_popsike['release_id'] == curr_release]['year'],
        'y': df_popsike[df_popsike['release_id'] == curr_release]['min']
    })
    #curr_release_min = log_transform(curr_release_min)

    curr_release_avg = pd.DataFrame({
        'ds': df_popsike[df_popsike['release_id'] == curr_release]['year'],
        'y': df_popsike[df_popsike['release_id'] == curr_release]['avg']
    })
    #curr_release_avg = log_transform(curr_release_avg)

    curr_release_max = pd.DataFrame({
        'ds': df_popsike[df_popsike['release_id'] == curr_release]['year'],
        'y': df_popsike[df_popsike['release_id'] == curr_release]['max']
    })
    #curr_release_max = log_transform(curr_release_max)

    m_min = Prophet()
    m_min.fit(curr_release_min)
    min_future = m_min.make_future_dataframe(periods=8, freq='Y')
    min_forecast = m_min.predict(min_future)
    #min_forecast = inverse_log_transform(min_forecast)
    min_forecast = min_forecast[['ds', 'yhat']].copy()
    mask = (min_forecast['ds'] > '2020-1-1')
    min_hat = min_forecast[mask].copy()

    m_avg = Prophet()
    m_avg.fit(curr_release_avg)
    avg_future = m_avg.make_future_dataframe(periods=8, freq='Y')
    avg_forecast = m_avg.predict(avg_future)
    #avg_forecast = inverse_log_transform(avg_forecast)
    avg_forecast = avg_forecast[['ds', 'yhat']].copy()
    mask = (avg_forecast['ds'] > '2020-1-1')
    avg_hat = avg_forecast[mask].copy()

    m_max = Prophet()
    m_max.fit(curr_release_max)
    max_future = m_max.make_future_dataframe(periods=8, freq='Y')
    max_forecast = m_max.predict(max_future)
    #max_forecast = inverse_log_transform(max_forecast)
    max_forecast = max_forecast[['ds', 'yhat']].copy()
    mask = (max_forecast['ds'] > '2020-1-1')
    max_hat = max_forecast[mask].copy()

    min_hat.rename(columns={
        'ds': 'year',
        'yhat': 'min'
    }, inplace=True)

    avg_hat.rename(columns={
        'ds': 'year',
        'yhat': 'avg'
    }, inplace=True)

    max_hat.rename(columns={
        'ds': 'year',
        'yhat': 'max'
        }, inplace=True)

    df_merge = min_hat.merge(avg_hat, on='year')
    df_merge = df_merge.merge(max_hat, on='year')

    df_merge['release_id'] = curr_release
    df_merge['title'] = df_popsike[df_popsike['release_id'] == curr_release]['title'].iloc[0]
    df_merge['artist'] = df_popsike[df_popsike['release_id'] == curr_release]['artist'].iloc[0]

    df_merge = df_merge[['release_id', 'year', 'title', 'artist', 'min', 'avg', 'max']]

    return df_merge
