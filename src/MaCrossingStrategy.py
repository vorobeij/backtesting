import talib
import time
from backtesting import Backtest
from backtesting.lib import TrailingStrategy

import dataplayground as data


class MaCrossingStrategy(TrailingStrategy):
    slowLength = 60

    def init(self):
        super().init()
        self.slowMA = self.I(talib.MA, self.data.Close, self.slowLength)

    def next(self):
        super().next()
        if self.slowMA < self.data.Low[-1] and not self.position:
            self.position.close()
            self.buy(sl=self.data.Close[-1] * 0.95)

        elif self.data.High[-1] < self.slowMA:
            self.position.close()


def printCharts(data, name):
    print("=============== " + name + " ===============")
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats = bt.run()
    # print(stats.iloc[6:11])
    # stats.to_csv("output/" + name + ".csv")
    bt.plot(filename="output/" + name, superimpose=False)


def optimise(data):
    bt = Backtest(data, MaCrossingStrategy, cash=10_000, commission=.004)
    stats, heatmap = bt.optimize(slowLength=range(30, 100, 3),
                                 maximize='Return [%]',
                                 return_heatmap=True)
    print(stats.iloc[6:11])
    print(heatmap.idxmax())


def showCharts():
    printCharts(data.BTC, "BTC")
    printCharts(data.SOL, "SOL")
    printCharts(data.DOT, "DOT")
    printCharts(data.ETH, "ETH")
    printCharts(data.ATOM, "ATOM")


if __name__ == '__main__':
    start_time = time.time()
    # optimise(data.BTC)
    # optimise(data.SOL)
    # optimise(data.DOT)
    # optimise(data.ETH)
    # optimise(data.ATOM)
    showCharts()
    print("--- %s seconds ---" % (time.time() - start_time))
