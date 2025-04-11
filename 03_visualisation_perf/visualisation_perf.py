'''
visualisation_perf.py - Application Streamlit pour visualiser la performance 
d'une stratégie de trading.

Ce script permet à l'utilisateur d'entrer ses paramètres afin de visualiser les performances d'une 
stratégie de breakout d'une trendline.
'''

import streamlit as st
import pandas as pd
from scipy import stats


def get_historical_data():
    '''
    Récupère les données historiques et les renvoie sous forme de DataFrame.
    
    Returns:
        df (pandas.DataFrame)
        : DataFrame contenant les données historiques
    '''
    uploaded_file = st.file_uploader('Télécharger les données historiques pour le backtesting au format csv', type='csv')
    separator = st.selectbox('Sélectionner le séparateur des données', (',', ';', '|', '\t'), index=0)
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=separator)
        return df
    
def clean_data(historical_data):
    '''
    Nettoie les données historiques et les renvoie sous forme de DataFrame.
    
    Args:    
        datas (pandas.DataFrame)
        : DataFrame contenant les données historiques
    Returns:
        df (pandas.DataFrame)
        : DataFrame contenant les données nettoyées
    '''
    historical_data.columns = ['date', 'time', 'open', 'high', 'low', 'close', 'tickvol', 'vol', 'spread']
    historical_data['datetime'] = pd.to_datetime(historical_data['date'] + ' ' + historical_data['time'])
    historical_data['datetime'] = pd.to_datetime(historical_data['datetime'], format='%Y.%m.%d %H:%M')
    historical_data = historical_data[['datetime', 'open', 'high', 'low', 'close']]
    historical_data.set_index('datetime', inplace=True)
    historical_data.dropna(inplace=True)
    return historical_data

def get_is_peak(historical_data_row):
    '''
    Récupère les sommets d'une série temporelle et les renvoie sous forme de liste de booléens.
    
    Args:
        historical_data_row (pandas.Series)
        : Série temporelle contenant les données historiques
    Returns:
        is_peak (bool)
        : True si le point est un sommet, False sinon
    '''
    is_peak = ((historical_data_row['high'] > historical_data_row['high'].shift(-1)) & (historical_data_row['high'] > historical_data_row['high'].shift(1)))
    return is_peak

def get_trendlines(historical_data):
    '''
    Renvoie une liste de disctionnaires des trendlines à partir des sommets.
    
    Args:
        historical_data (pandas.DataFrame)
        : DataFrame contenant les sommets
    Returns:
        trendlines (pandas.DataFrame)
        : Liste de trendlines
    '''
    peaks = historical_data[historical_data['is_peak']]
    trenlines = []
    curr_trendline = {
        'peaks': [],
        'start_index': None,
        'end_index': None,
        'slope': None,
        'intercept': None,
        'breakout': None
    }
    
    for i in peaks.index:
        if (curr_trendline is not None) and (curr_trendline['peaks']):
            if all(peaks.loc[i]['high'] < p['high'] for p in curr_trendline['peaks']):
                curr_trendline['end_index'] = i
                curr_trendline['peaks'].append({
                    'datetime': i,
                    'high': peaks.loc[i]['high']
                })
                if (len(curr_trendline['peaks']) >= min_peaks):
                    base_time = curr_trendline['peaks'][0]['datetime']
                    x = [(p['datetime'] - base_time).total_seconds() / 3600 for p in curr_trendline['peaks']]  # en heures
                    y = [p['high'] for p in curr_trendline['peaks']]
                    
                    if len(set(x)) > 1:
                        slope, intercept, *_ = stats.linregress(x, y)
                        curr_trendline['slope'] = slope
                        curr_trendline['intercept'] = intercept
                    else:
                        curr_trendline['slope'] = None
                        curr_trendline['intercept'] = None
            elif curr_trendline['peaks'][-1]['high'] < peaks.loc[i]['high'] and len(curr_trendline['peaks']) >= min_peaks and curr_trendline['slope'] < 0:
                for candle_datetime in historical_data.loc[i:].index:
                    x_val = (candle_datetime - curr_trendline['peaks'][0]['datetime']).total_seconds() / 3600
                    trend_price = curr_trendline['slope'] * x_val + curr_trendline['intercept']
                    if historical_data.loc[candle_datetime]['high'] > trend_price:
                        curr_trendline['end_index'] = candle_datetime
                        curr_trendline['breakout'] = {
                            'datetime': candle_datetime,
                            'low': historical_data.loc[candle_datetime]['low']
                        }
                        trenlines.append(curr_trendline)
                        break
                curr_trendline = None
            else:
                curr_trendline = None
        else:
            curr_trendline['start_index'] = i
            curr_trendline['end_index'] = i
            curr_trendline['peaks'].append({
                    'datetime': i,
                    'high': peaks.loc[i]['high']
                    })
        
    return pd.DataFrame(trenlines)

def get_trade_from_trendlines(trendline, historical_data):
    '''
    Récupère les trades d'une liste de trendlines et les renvoie sous forme de liste de dictionnaires.
    
    Args:
        trendline (dict)
        : Dictionnaire contenant une trendline
        historical_data (pandas.DataFrame)
        : DataFrame contenant les données historiques
    Returns:
        trades (dict)
        : Dictionnaire contenant le trade
    ''' 
    breakout_candle = trendline['breakout']
    entry_index = historical_data.index.get_loc(breakout_candle['datetime']) + 1
    entry_time = historical_data.index[entry_index]
    entry_price = historical_data.loc[entry_time]['open']
    
    # Initialisation du trade
    trade = {
                'entry_time': entry_time,
                'entry_price': entry_price,
                'sl': breakout_candle['low'],
                'risk': entry_price - breakout_candle['low'],
                'tp': entry_price + (tp_trade * risk_trade * 100),
                'exit_time': None,
                'exit_price': None,
                'exit_reason': None
            }
    
    # On vérifie si le trade a été clôturé par le take profit ou le stop loss
    for candle_datetime in historical_data.loc[entry_time:].index:
        if (historical_data.loc[candle_datetime]['high'] > trade['tp']):
            trade['exit_time'] = candle_datetime
            trade['exit_price'] = historical_data.loc[candle_datetime]['close']
            trade['exit_reason'] = 'TP'
        elif (historical_data.loc[candle_datetime]['low'] < trade['sl']):
            trade['exit_time'] = candle_datetime
            trade['exit_price'] = historical_data.loc[candle_datetime]['close']
            trade['exit_reason'] = 'SL'
    return trade

def get_trades_from_backtest(historical_data):
    '''
    Récupère les trades d'un backtest et les renvoie sous forme de liste de dictionnaires.
    
    Args:
        historical_data (pandas.DataFrame)
        : DataFrame contenant les données historiques
    Returns: 
        trades (list)
        : Liste de dictionnaires contenant les trades
    '''
    historical_data = clean_data(historical_data)
    
    # On récupère les sommets de la série temporelle
    historical_data['is_peak'] = historical_data.apply(get_is_peak, axis=1)
    
    trendlines = get_trendlines(historical_data)
    return trendlines.apply(lambda trendline: get_trade_from_trendlines(trendline, historical_data), axis=1)


st.title('Visualisation de la performance d\'une stratégie de trading')

st.markdown('Explication de la stratégie de trading : \n'
            'La stratégie prend position apres une trendline de X sommets parametrables. \n'
            'Le stop loss est de X pourcentage de risque du capital et le take profit est de X pourcentage du capital. \n'
            'L\'orsque le profit ou le stop loss est atteint, le trade est cloturé. Inverve\n'
            'Ces parametres sont modifiables via les inputs ci dessous. \n')

min_peaks = st.number_input('Entrez le nombre de sommets pour la trendline', 0)
capital = st.number_input('Entre le capital de départ pour la simulation', 0)
risk_trade = st.number_input('Entrez le pourcentage de risque par trade', 0)
tp_trade = st.number_input('Entrez le pourcentage de take profit par trade', 0)

if st.button('Calculer la performance', type='primary'):
    while True:
        historical_data_uploaded = get_historical_data()
        if historical_data_uploaded is not None:
            break
        else:
            st.error('Erreur : Veuillez télécharger un fichier CSV valide contenant les données historiques.')
    trades = get_trades_from_backtest(historical_data_uploaded)
