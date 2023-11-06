import glob
import pandas as pd
import numpy as np

#creating signals on moving average crossover strategy
def create_signals(df,short_window,long_window,target,stop_loss):
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    signals['target'] = 0.0
    signals['stop_loss'] = 0.0
    signals['profit_loss']= 0.0
    signals['short_avg'] = 0.0
    signals['long_avg'] = 0.0
    for i in range(short_window,len(df)):
        signals['signal'].iloc[i] = 0.0
        signals['target'].iloc[i] = 0.0

        signals['stop_loss'].iloc[i] = 0.0
        signals['profit_loss'].iloc[i] = 0.0


        #calculating short and long term moving averages
        short = i+short_window
        long = i+long_window
        signals['short_avg'].iloc[i] = df['close'].iloc[-short:].mean()
        # signals['long_avg'] = df['close'].rolling(long_window).mean()
        signals['long_avg'].iloc[i] = df['close'].iloc[-long:].mean()

        #determining buy or sell signal by comparing averages
        signals['signal'].iloc[i] = np.where(signals['short_avg'].iloc[i] > signals['long_avg'].iloc[i], 1.0, 0.0)   

        
        
        # Set target and stop-loss values
        signals['target'].iloc[i] = df['close'].iloc[i] * (1 + target)
        signals['stop_loss'].iloc[i] = df['close'].iloc[i] * (1 - stop_loss)
    return signals

# def determine_results(signals):
#     for i in range(1, len(signals)):
       
#         if  signals['signal'].iloc[i] == 1.0:   # Buy signal

#             if df['close'].iloc[i] >= signals['target'].iloc[i]:
#                 signals['profit_loss'].iloc[i] = df['close'].iloc[i] - df['close'].iloc[i - 1]
#             elif df['close'].iloc[i] <= signals['stop_loss'].iloc[i]:
#                 signals['profit_loss'].iloc[i] = df['close'].iloc[i] - df['close'].iloc[i - 1]
#         elif   signals['signal'].iloc[i] == 0.0:  # Sell signal
#             if df['close'].iloc[i] <= signals['target'].iloc[i]:
#                 signals['profit_loss'].iloc[i] = df['close'].iloc[i - 1] - df['close'].iloc[i]
#             elif df['close'].iloc[i] >= signals['stop_loss'].iloc[i]:
#                 signals['profit_loss'].iloc[i] = df['close'].iloc[i - 1] - df['close'].iloc[i]

#     return signals
# Calculate results based on signals
def trade_results(signal,initial_capital):
    capital = initial_capital
    num_winning_trades = 0
    num_losing_trades = 0
    num_of_shares = 0
    for i in range(1,len(signal)):
        close_price = df.loc[i, 'close']
        print(signal['signal'].iloc[i])
        if signal['signal'].iloc[i] == 1.0  :
        # Buy signal
            shares = capital // close_price
            cost = shares * close_price
            capital -= cost
            num_of_shares += shares
        elif signal['signal'].iloc[i] == 0.0 and df['close'].iloc[i] >= signal['target'].iloc[i] or df['close'].iloc[i] <= signal['stop_loss'].iloc[i] :
            # Sell signal (target or stop-loss hit)
            # if close_price >= target_price or close_price <= stop_loss_price:
                capital = num_of_shares * close_price
                num_of_shares -= num_of_shares
                if close_price >=  signal['target'].iloc[i]:
                    num_winning_trades += 1
                else:
                    num_losing_trades += 1
               
    print(f"Ending Capital: {capital}")
    print(f"Net Profit: { capital - initial_capital}")
    print(f"Number of Winning Trades: {num_winning_trades}")
    print(f"Number of Losing Trades: {num_losing_trades}")

# Calculate ending capital and net profit

if __name__ == "__main__":
   
    # all_files = glob.glob("*.csv")
    # df = pd.concat((pd.read_csv(f) for f in all_files))
     # Set your target and stop-loss values
    target = 0.3  # 3% target
    stop_loss = 0.1 # 1% stop-loss
    initial_capital = 100000
    short_window = 20
    long_window=30
    # global capital, num_losing_trades, num_winning_trades,trade_in_progress
    
    df = pd.read_csv('NIFTY_BANK2015.csv')

    signals = create_signals(df[0:100],short_window,long_window,target,stop_loss)
   
    # results = determine_results(signals)
    signals.to_csv('signal.csv')

    trade_results(signals,initial_capital)


   