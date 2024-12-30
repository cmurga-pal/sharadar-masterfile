import pandas as pd
from tqdm import tqdm

from market_data.sharadar import get_file, current_cache_version, latest_version, get_description, versions, default_version, clear_cache, get_fred_3m_rf

def get_ticker_history( actions_df, 
                        ticker,
                        first_date = pd.Timestamp(1993, 1, 1), # Cambiar por actions_df.date.min()
                        last_date = pd.Timestamp(current_cache_version())):
    result = pd.DataFrame(columns=['ticker', 'ticker_sharadar', 'end_date'])
    ticker_actions = actions_df[(actions_df.ticker == ticker) &
                                (actions_df.action == 'tickerchangefrom')].copy(deep=True)
    ticker_actions.set_index('date', inplace=True, drop=True)
    ticker_actions.sort_index(inplace=True, ascending=False)
    delisting_actions = actions_df[(actions_df.ticker == ticker) &
                                   (actions_df.action == 'delisted')].copy(deep=True)
    result.loc[len(result) + 1] = [ticker, ticker, last_date]
    if len(delisting_actions) == 1:
        result.loc[1, 'end_date'] = delisting_actions.date.iloc[0]
    for date, row in ticker_actions.iterrows():
        previous_ticker = row.contraticker
        result.loc[len(result) + 1] = [previous_ticker, ticker, date]
    result['start_date'] = result.end_date.shift(-1)
    listing_actions = actions_df[(actions_df.ticker == ticker) &
                                 (actions_df.action == 'listed')].copy(deep=True)
    if len(listing_actions) == 1:
        result.loc[len(result), 'start_date'] = listing_actions.date.iloc[0]
    else:
        result.loc[len(result), 'start_date'] = first_date
    if len(delisting_actions) == 1:
        result = result[result['start_date'] < delisting_actions.date.iloc[0]]
    return result

actions_df = get_file('actions')
tickers_df = get_file('tickers')
_dataframes = []
for ticker in tqdm(tickers_df.ticker.unique()):
    _dataframes.append(get_ticker_history(actions_df=actions_df, ticker=ticker))
masterfile = pd.concat(_dataframes)