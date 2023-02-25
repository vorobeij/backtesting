import seaborn as sns
import seaborn as sns
import talib
import time
from backtesting import Backtest
from backtesting.lib import TrailingStrategy
from backtesting.lib import plot_heatmaps

import src.dataplayground as data


class MaCrossingStrategy(TrailingStrategy):
    slowLength = 96
    fastLength = 32

    def init(self):
        super().init()
        self.slowMA = self.I(talib.MA, self.data.Close, self.slowLength)
        self.fastMA = self.I(talib.MA, self.data.Close, self.fastLength)

    def next(self):
        super().next()
        if self.slowMA < self.data.Low[-1] and not self.position and self.slowMA < self.fastMA:
            self.position.close()
            self.buy(sl=self.data.Close[-1] * 0.95)

        elif self.data.High[-1] < self.slowMA:
            self.position.close()


def printCharts(data, name):
    print("=============== " + name + " ===============")
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats = bt.run()
    print(stats.iloc[6:11])
    stats.to_csv("output/" + name + ".csv")
    bt.plot(filename="output/" + name, superimpose=False)


def optimise(data, name):
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats, heatmap = bt.optimize(slowLength=range(30, 100, 3),
                                 fastLength=range(30, 100, 3),
                                 maximize='Return [%]',
                                 constraint=lambda param: param.fastLength < param.slowLength,
                                 return_heatmap=True)
    hm = heatmap.groupby(['fastLength', 'slowLength']).mean().unstack()
    sns.heatmap(hm[::-1], cmap='viridis')
    plot_heatmaps(heatmap, agg='mean', filename=name)
    print(stats)


def showCharts():
    # printCharts(data.GOOG, "GOOG")
    # printCharts(data.MSFT, "MSFT")
    # printCharts(data.ADBE, "ADBE")
    # printCharts(data.NVDA, "NVDA")
    # printCharts(data.ZM, "ZM")
    printCharts(data.BTC, "BTC")
    printCharts(data.SOL, "SOL")
    printCharts(data.DOT, "DOT")
    printCharts(data.ETH, "ETH")
    printCharts(data.ATOM, "ATOM")


if __name__ == '__main__':
    start_time = time.time()
    # optimise(data.BTC, 'BTC')
    # optimise(data.SOL, 'SOL')
    # optimise(data.DOT, 'DOT')
    # optimise(data.ETH, 'ETH')
    # optimise(data.ATOM, 'ATOM')
    showCharts()
    print("--- %s seconds ---" % (time.time() - start_time))
