import dataplayground as data
import seaborn as sns
import talib
import time
from backtesting import Backtest
from backtesting.lib import TrailingStrategy, plot_heatmaps


class MaCrossingStrategy(TrailingStrategy):
    slowLength = 60
    macdFastPeriod = 12
    macdSlowPeriod = 40
    macdSignalPeriod = 9

    def init(self):
        super().init()
        self.slowMA = self.I(talib.MA, self.data.Close, self.slowLength)
        self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, self.data.Close, self.macdFastPeriod, self.macdSlowPeriod, self.macdSignalPeriod)

    def next(self):
        super().next()

        macdGrowing = 0 < self.macd[-2] < self.macd[-1]
        if self.macdsignal < self.macd and macdGrowing and not self.position:
            self.position.close()
            self.buy(sl=self.data.Close[-1] * 0.95)

        elif self.data.High[-1] < self.slowMA:
            self.position.close()


def printCharts(data, name):
    print("=============== " + name + " ===============")
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats = bt.run()
    print(stats.iloc[6:11])
    # stats.to_csv("output/" + name + ".csv")
    bt.plot(filename="output/" + name, superimpose=False)


def optimise(data):
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats, heatmap = bt.optimize(
        # slowLength=range(30, 100, 3),
        macdFastPeriod=range(10, 20, 1),
        macdSlowPeriod=range(30, 50, 1),
        constraint=lambda param: param.macdFastPeriod < param.macdSlowPeriod,
        maximize='Return [%]',
        return_heatmap=True)
    hm = heatmap.groupby(['macdFastPeriod', 'macdSlowPeriod']).mean().unstack()
    sns.heatmap(hm[::-1], cmap='viridis')
    plot_heatmaps(heatmap, agg='mean')


def showCharts():
    printCharts(data.BTC, "BTC")
    printCharts(data.SOL, "SOL")
    printCharts(data.DOT, "DOT")


if __name__ == '__main__':
    start_time = time.time()
    # optimise(data.BTC)
    showCharts()
    print("--- %s seconds ---" % (time.time() - start_time))
