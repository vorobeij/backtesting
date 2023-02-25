import talib
import talib
import time
from backtesting import Backtest
from backtesting.lib import TrailingStrategy
from backtesting.lib import crossover

from src.dataplayground import BTC


class MaCrossingStrategy(TrailingStrategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    fastLength = 20
    slowLength = 64
    signalLength = 11

    def init(self):
        super().init()
        # Precompute the two moving averages
        self.fastMA = self.I(talib.MA, self.data.Close, self.fastLength)
        self.slowMA = self.I(talib.MA, self.data.Close, self.slowLength)
        # self.macd = self.fastMA - self.slowMA
        # self.signalMA = self.I(talib.MA, self.macd, self.signalLength)

    def next(self):
        super().next()
        # close any existing
        # short trades, and buy the asset
        if crossover(self.fastMA, self.slowMA) and not self.position:
            self.position.close()
            self.buy(sl=self.data.Close[-1] * 0.95)

        if self.fastMA > self.slowMA and not self.position:
            self.position.close()
            self.buy(sl=self.data.Close[-1] * 0.95)

        # close any existing
        # long trades, and sell the asset
        elif crossover(self.slowMA, self.fastMA):
            self.position.close()


def optimise():
    bt = Backtest(BTC, MaCrossingStrategy, cash=10_000, commission=.004)
    stats, heatmap = bt.optimize(fastLength=range(20, 40, 2),
                                 slowLength=range(48, 70, 4),
                                 signalLength=range(30, 50, 2),
                                 maximize='Equity Final [$]',
                                 constraint=lambda param: param.fastLength < param.slowLength and param.slowLength > param.signalLength > param.fastLength,
                                 max_tries=1000,
                                 return_heatmap=True)
    print(stats)
    bt.run()
    bt.plot()
    # hm = heatmap.groupby(['fastLength', 'slowLength', 'signalLength']).mean().unstack()
    # sns.heatmap(hm[::-1], cmap='viridis')
    # plot_heatmaps(heatmap, agg='mean')


if __name__ == '__main__':
    start_time = time.time()
    optimise()
    print("--- %s seconds ---" % (time.time() - start_time))
