import glob
import pandas as pd
import numpy as np

#creating signals on moving average crossover strategy
def create_signals(df,short_window,long_window,target,stop_loss):
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    signals['target'] = 0.0

    signals['stop_loss'] = 0.0
    signals['profit_loss'] = 0.0


    #calculating short and long term moving averages
    signals['short_avg'] = df['close'].rolling(short_window).mean()
    signals['long_avg'] = df['close'].rolling(long_window).mean()

    #determining buy or sell signal by comparing averages
    signals['signal'][short_window:] = np.where(signals['short_avg'][short_window:] > signals['long_avg'][short_window:], 1.0, 0.0)   

    
    # Set target and stop-loss values
    signals['target'][short_window:] = df['close'][short_window:] * (1 + target)
    signals['stop_loss'][short_window:] = df['close'][short_window:] * (1 - stop_loss)
    return signals
       

def determine_results(signals):
    for i in range(1, len(signals)):
       
        if  signals['signal'].iloc[i] == 1.0:  # Buy signal

            if df['close'].iloc[i] >= signals['target'].iloc[i]:
                signals['profit_loss'].iloc[i] = df['close'].iloc[i] - df['close'].iloc[i - 1]
            elif df['close'].iloc[i] <= signals['stop_loss'].iloc[i]:
                signals['profit_loss'].iloc[i] = df['close'].iloc[i] - df['close'].iloc[i - 1]
        elif   signals['signal'].iloc[i] == 0.0:  # Sell signal
            if df['close'].iloc[i] <= signals['target'].iloc[i]:
                signals['profit_loss'].iloc[i] = df['close'].iloc[i - 1] - df['close'].iloc[i]
            elif df['close'].iloc[i] >= signals['stop_loss'].iloc[i]:
                signals['profit_loss'].iloc[i] = df['close'].iloc[i - 1] - df['close'].iloc[i]

    return signals


if __name__ == "__main__":
   
    all_files = glob.glob("*.csv")
    df = pd.concat((pd.read_csv(f) for f in all_files))
     # Set your target and stop-loss values
    target = 0.3  # 3% target
    stop_loss = 0.1  # 1% stop-loss

    signals = create_signals(df,20,80,target,stop_loss)

    results = determine_results(signals)
    #saving results to results/results.csv
    results.to_csv("../results.csv")

    print(results)
    

   