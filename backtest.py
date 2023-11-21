import glob
import pandas as pd
import numpy as np
import pandas_ta as pta

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
    last_trade_profit = False
    max_consecutive_wins = 0
    max_consecutive_loss = 0
    current_win = 0
    current_loss = 0
    num_of_shares = 0
    trade_progress = False
    buy_price = 0
    cumulative_profit= []
    cumulative_loss = []
    # max_profit = 0
    # max_loss = 0
    for i in range(short_window,len(signal)):
        close_price = df.loc[i, 'close']
        open_price = df.loc[i,'open']
        date_1 = df.loc[i,'date'].split()[0]
        date_2 = df.loc[i+1,'date'].split()[0]
        # print(trade_progress,num_of_shares,close_price,date_1,date_2)
        if signal['signal'].iloc[i] == 1.0 and trade_progress == False  : # Buy signal
            if(sqOff and date_1 == date_2) :
                continue
            shares= 0
            print('buy')
            buy_price =  close_price if open_price > close_price else open_price
            if(capital >= buy_price and date_1 == date_2 ) :
                shares = capital // buy_price
                cost = shares * buy_price
                capital -= cost
            num_of_shares += shares
            trade_progress = True
        elif signal['signal'].iloc[i] == 0.0 and trade_progress and ((open_price >= ( buy_price * (1 + target)) ) or (close_price >= ( buy_price * (1 + target))) or (open_price <= (buy_price * (1 - stop_loss))) or (close_price <= (buy_price * (1 - stop_loss))))  : #Sell Signal
                print('sell')
                target_price = buy_price * (1 + target)
                max_loss = buy_price * (1 - stop_loss)
                trade_progress = False
                if open_price >= target_price or close_price >= target_price :
                    if(open_price > close_price and open_price >= target_price):
                        trade_profit = ((num_of_shares * open_price ) - (buy_price * num_of_shares))
                        capital  = capital + (num_of_shares * open_price)
                    else:
                        trade_profit = ((num_of_shares * close_price ) - (buy_price * num_of_shares))
                        capital  = capital + (num_of_shares * close_price)
                         
                    cumulative_profit.append(trade_profit)
                    num_of_shares -= num_of_shares
                    current_win = current_win + 1 if last_trade_profit else 1
                    max_consecutive_wins = current_win if current_win > max_consecutive_wins else max_consecutive_wins
                    last_trade_profit = True

                    # max_profit = trade_profit
                elif close_price <= max_loss or open_price <= max_loss :
                    if(open_price > close_price and open_price >= (buy_price * (1+target)) ) :
                        trade_loss = (buy_price* num_of_shares) - (num_of_shares * open_price) 
                        capital = capital + (open_price * num_of_shares)
                    else:
                        trade_loss = (buy_price* num_of_shares) - (num_of_shares * close_price) 
                        capital = capital + (num_of_shares * close_price)
                        #  trade_loss = 
                    cumulative_loss.append(trade_loss)
                    num_of_shares -= num_of_shares
                    current_loss = 1 if last_trade_profit else current_loss + 1
                    max_consecutive_loss = current_loss if current_loss > max_consecutive_loss else max_consecutive_loss
                    last_trade_profit = False
        elif sqOff and trade_progress and date_2 > date_1 :
                sold_price = close_price if close_price > open_price else open_price
                bought_at = num_of_shares * buy_price
                sold_at = num_of_shares * sold_price
                # bought_at = num_of_shares 
                capital = capital + sold_price
                trade_progress = False
                num_of_shares -= num_of_shares
                if(bought_at < sold_at):
                    trade_profit =  sold_at - bought_at
                    cumulative_profit.append(trade_profit)
                    current_win = current_win + 1 if last_trade_profit else 1
                    max_consecutive_wins = current_win if current_win > max_consecutive_wins else max_consecutive_wins
                    last_trade_profit = True
                else:

                    trade_loss = bought_at - sold_at
                    cumulative_loss.append(trade_loss)
                    current_loss = 1 if last_trade_profit else current_loss + 1
                    max_consecutive_loss = current_loss if current_loss > max_consecutive_loss else max_consecutive_loss
                    last_trade_profit = False
                     
    # print(cumulative_loss,cumulative_profit)
    loss = max(cumulative_loss) if len(cumulative_loss) > 0 else 0
    profit = max(cumulative_profit) if len(cumulative_profit) > 0 else 0
    max_draw = (loss - profit)/profit
    print(f"Initial Capital: {initial_capital}")          
    print(f"Ending Capital: { capital }")
    print(f"Net Profit: { capital - initial_capital}" )
    print(f"Number of Winning Trades: { len(cumulative_profit) }" )
    print(f"Number of Losing Trades: { len(cumulative_loss) }" )
    print(f"Number of shares held: { num_of_shares } ")
    print(f"Total Profit: { sum(cumulative_profit) } ")
    print(f"Largest Profit: { profit} ")
    print(f"Average Profit: { sum(cumulative_profit)/len(cumulative_profit)} ")
    print(f"Max Consecutive Wins: {max_consecutive_wins}")
    print(f"Total Loss: { sum(cumulative_loss) }")
    print(f"Worst Loss: { loss }")
    print(f"Average Loss: { sum(cumulative_loss)/len(cumulative_loss) }")
    print(f"Max Consecutive Losses: {max_consecutive_loss} ")
    print(f"Max Dropdown: {max_draw}% ")


def calculate_rsi(data, period):
    data['rsi'] = pta.rsi(df['close'],length=period)
    return data

def calculate_wma(data,period):
    data['wma'] = pta.wma(df['rsi'], length=period)
    return data
    
def calculate_ema(data,period):
    data['ema'] = pta.ema(df['rsi'],length=period)
    return data
# Calculate ending capital and net profit

if __name__ == "__main__":
   
    # all_files = glob.glob("*.csv")
    # df = pd.concat((pd.read_csv(f) for f in all_files))
     # Set your target and stop-loss values
    
    target = int(input("Enter target profit in % : "))/100      # 03% target
    stop_loss = int(input("Stop Loss %: "))/100  # 05% stop-loss
    initial_capital = int(input("Initial Capital in Rs: ") )
    sqOff = int(input("Square off by the end of the day (1 - Yes or 0 - No): "))
    short_window = 100
    long_window = 300

    #period for different strategies
    rsi_period = 9
    wma_period = 21
    ema_period = 3

    df = pd.read_csv('NIFTY_BANK2015.csv')

    print('Calculating RSI...')
    
    df = calculate_rsi(df,rsi_period)

    print('Calculating WMA and EMA...')

    df = calculate_wma(df,wma_period)
    df = calculate_ema(df,ema_period)

    print(df)
    exit()


    

    
    print("Calculating Results..",target,stop_loss,initial_capital)
    signals = create_signals(df[0:20000],short_window,long_window)

    #saving generated signals to signal.csv file
    # signals.to_csv('signal.csv')

    trade_results(signals, initial_capital)


   