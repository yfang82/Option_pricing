import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf

def get_market_cap(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}'
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    soup = BeautifulSoup(response.text, 'html.parser')
        # Locate the Market Cap element using the identified attribute
    try:
        # Find the section with data-testid="quote-statistics"
        statistics_section = soup.find('div', {'data-testid': 'quote-statistics'})
        if not statistics_section:
            raise ValueError("Could not find the quote statistics section.")
        
        # Find the list item (li) that contains the Market Cap information
        market_cap_item = statistics_section.find('span', string='Market Cap (intraday)').find_parent('li')
        if not market_cap_item:
            raise ValueError("Could not find the Market Cap list item.")
        
        # Extract the Market Cap value(measured in Trillion)
        market_cap_value = market_cap_item.find('span', class_='value').text
        mc = 0
        
        if market_cap_value[-2] == "T":
            mc = float(market_cap_value[:-2])
        if market_cap_value[-2] == "B":
            mc = float(market_cap_value[:-2])*0.001

        return mc
    except AttributeError as e:
        raise ValueError("Error while parsing the market cap information.") from e

def market_cap_df(names = ['MSFT','NVDA','AAPL','AMZN','META','GOOG','AVGO','LLY']):
    market_cap_list = []
    for name in names:
        market_cap_list.append(get_market_cap(name))
    return pd.DataFrame({'names':names, "market_cap":market_cap_list})

def exreturn_adclose_df(names = ['MSFT','NVDA','AAPL','AMZN','META','GOOG','AVGO','LLY']):
    df = pd.DataFrame()
    for name in names:
        df[name] = pd.read_csv(name+'.csv',index_col='Date')['Adj Close'].pct_change()
    # SP = yf.download("^GSPC",start = '2023-07-10', 
    #                         end = '2024-07-05')['Adj Close']
    df = df.dropna()
    # mk_ret = SP.pct_change().dropna()
    # mk_ret.index = mk_ret.index.strftime('%Y-%m-%d')
    # df = df.loc[mk_ret.index]
    return df

def get_cov_matrix(df):
    return df.cov()

def get_delta(risk_free_rate):
    SP = yf.download("^GSPC",start = '2023-07-06', 
                            end = '2024-07-06')['Adj Close']
    ret = SP.pct_change(fill_method='bfill').dropna()
    R_market = ret.mean()*252
    R_f = risk_free_rate
    Var_market = ret.var()*252
    return (R_market-R_f)/Var_market



