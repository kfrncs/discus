import numpy as np
from fbprophet import Prophet

def log_transform(df):
    df['y'] = df['y'] + 1
    df['y'] = np.log(df['y'])
    return df

def inverse_log_transform(df):
    df['yhat'] = np.exp(df['yhat'])-1
    df['yhat_lower'] = np.exp(df['yhat_lower'])-1
    df['yhat_upper'] = np.exp(df['yhat_upper'])-1
    return df

def prophesy(df_current):
    curr_release_min = pd.DataFrame({
        'ds': df_current['year'],
        'y': df_current['min']
    })
    curr_release_min = log_transform(curr_release_min)

    curr_release_avg = pd.DataFrame({
        'ds': df_current['year'],
        'y': df_current['avg']
    })
    curr_release_avg = log_transform(curr_release_avg)

    curr_release_max = pd.DataFrame({
        'ds': df_current['year'],
        'y': df_current['max']
    })
    curr_release_max = log_transform(curr_release_max)
    
    # one model each for min, avg, max
    m_min = Prophet()
    m_min.fit(curr_release_min)

    m_avg = Prophet()
    m_avg.fit(curr_release_avg)

    m_max = Prophet()
    m_max.fit(curr_release_max)


    # [release_id, year, title, artist, min, avg, max]
    return df_future

