import glob
import pandas as pd
import numpy as np

#creating signals on moving average crossover strategy
def create_signals(df,short_window,long_window):
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    # signals['target'] = 0.0
    # signals['stop_loss'] = 0.0
    signals['profit_loss']= 0.0
    signals['short_avg'] = 0.0
    signals['long_avg'] = 0.0
    for i in range(short_window,len(df)):
        signals['signal'].iloc[i] = 0.0
        # signals['target'].iloc[i] = 0.0

        # signals['stop_loss'].iloc[i] = 0.0
        signals['profit_loss'].iloc[i] = 0.0


        #calculating short and long term moving averages
        short = i+short_window
        long = i+long_window
        signals['short_avg'].iloc[i] = df['close'].iloc[-short:].mean()
        # signals['long_avg'] = df['close'].rolling(long_window).mean()
        signals['long_avg'].iloc[i] = df['close'].iloc[-long:].mean()

        #determining buy or sell signal by comparing averages
        signals['signal'].iloc[i] = np.where(signals['short_avg'].iloc[i] > signals['long_avg'].iloc[i], 1.0, 0.0)   

        
    return signals

def trade_results(signal,initial_capital):
    capital = initial_capital
    num_winning_trades = 0
    num_losing_trades = 0
    num_of_shares = 0
    trade_progress = False
    buy_price = 0
    trade_profit= 0
    trade_loss = 0
    
    for i in range(short_window,len(signal)):
        close_price = df.loc[i, 'close']
        if signal['signal'].iloc[i] == 1.0 and trade_progress == False : #Buy signal
            shares= 0
            buy_price =  close_price
            if(capital >= close_price) :
                shares = capital // close_price
                cost = shares * close_price
                capital -= cost
            num_of_shares += shares
            trade_progress = True
        elif signal['signal'].iloc[i] == 0.0 and trade_progress and ((close_price >=  buy_price * (1 + target) )or (close_price <= buy_price * (1 - stop_loss)))  : #Sell Signal
                target_price = buy_price * (1 + target)
                max_loss = buy_price * (1 - stop_loss)
                capital = capital + ( num_of_shares * close_price)
                trade_progress = False
                if close_price >= target_price :
                    num_winning_trades += 1
                    trade_profit = trade_profit + ((num_of_shares * close_price ) - (buy_price * num_of_shares))
                    num_of_shares -= num_of_shares
                elif close_price <= max_loss :
                    # trade_progress = False
                    # capital = capital +  (num_of_shares * close_price)
                    num_losing_trades += 1
                    trade_loss = trade_loss + ((buy_price* num_of_shares) - (num_of_shares * close_price) )
                    # print('sell',num_of_shares)
                    num_of_shares -= num_of_shares

    print(f"Initial Capital: {initial_capital}")          
    print(f"Ending Capital: { capital }")
    print(f"Net Profit: { capital - initial_capital}")
    print(f"Number of Winning Trades: { num_winning_trades }")
    print(f"Number of Losing Trades: { num_losing_trades }")
    print(f"Number of shares held: { num_of_shares }")
    print(f"Winners Profit: { trade_profit }")
    print(f"Winners Lose: { trade_loss }")

# Calculate ending capital and net profit

if __name__ == "__main__":
   
    # all_files = glob.glob("*.csv")
    # df = pd.concat((pd.read_csv(f) for f in all_files))
     # Set your target and stop-loss values
    target = 0.03  # 03% target
    stop_loss = 0.5 # 05% stop-loss
    initial_capital = 50000
    short_window = 15
    long_window= 30
    
    df = pd.read_csv('NIFTY_BANK2015.csv')

    signals = create_signals(df,short_window,long_window)
    # print(signals)
   
    # results = determine_results(signals)
    # signals.to_csv('signal.csv')

    # global capital, num_losing_trades, num_winning_trades,trade_in_progress
    trade_results(signals,initial_capital)


   