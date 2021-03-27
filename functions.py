import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def get_dates_and_closing_prices(n):
    vector = pd.read_csv('cdr.csv')  # dane z stooq
    q = []
    last_index = len(vector['Date']) - 1

    for i in range(n):  # pobieram n najnowszych danych
        x = [vector['Date'][last_index-i], vector['Close'][last_index-i]]
        q.append(x)

    q.reverse()

    return q


def show_plot(stock_data, macd, macd_signal, macd_hist):
    x_points = get_x_axis(stock_data)
    y_points = get_y_axis(stock_data)

    figure, axis = plt.subplots(2)  # two plots

    axis[0].plot(x_points, y_points)
    axis[0].set_xlabel("date (YYYY-MM-DD)")
    axis[0].set_ylabel("closing price (PLN)")
    axis[0].set_title("CD PROJEKT")
    axis[0].set_xticks(np.arange(0, len(y_points), 120))

    axis[1].plot(x_points, macd, "b", label="MACD")
    axis[1].plot(x_points, macd_signal, "r", label="MACD-Signal")
    axis[1].bar(x_points, macd_hist, color='black', width=0.1, label="MACD-Hist")
    axis[1].set_xlabel("date (YYYY-MM-DD)")
    axis[1].set_xticks(np.arange(0, len(y_points), 120))
    axis[1].legend(loc="upper left")

    figure.set_figwidth(14)
    figure.set_figheight(7)
    figure.tight_layout()

    plt.axhline(linewidth=0.5, color='gray', linestyle='dashed')  # y = 0

    plt.show()


def get_x_axis(stock_data):
    x = []

    for q in stock_data:
        x.append(q[0])

    return x


def get_y_axis(stock_data):
    y = []

    for q in stock_data:
        y.append(q[1])

    return y


def count_macd(stock_data, n):
    ema12 = ema(get_y_axis(stock_data), 12, n)
    ema26 = ema(get_y_axis(stock_data), 26, n)
    macd = []

    for i in range(n):
        if ema26[i] is None:
            macd.append(None)
        else:
            x = ema12[i] - ema26[i]
            macd.append(x)

    return macd


def count_macd_signal(macd, n):
    macd_signal = ema(macd, 9, n)

    return macd_signal


def ema(prices, period, n):
    ema_period = []
    alfa = 2/(period+1)

    for i in range(n):
        if (i < (period - 1)) or (prices[i] is None) or (prices[i - (period - 1)] is None):
            ema_period.append(None)
        else:
            nominator = 0
            denominator = 0
            for j in range(period):  # 0...period
                nominator += (pow((1 - alfa), j) * prices[i - j])
                denominator += pow((1 - alfa), j)

            x = nominator/denominator
            ema_period.append(x)

    return ema_period


def count_macd_hist(macd, macd_signal, n):
    macd_hist = []

    for i in range(n):
        if macd[i] is None or macd_signal[i] is None:
            macd_hist.append(float('NaN'))  # float('NaN') instead of None
        else:
            x = macd[i] - macd_signal[i]
            macd_hist.append(x)

    return macd_hist


def simulation(closing_prices, macd_hist, number_of_stock, n):  # all in
    is_investing = True
    final_capital = 0
    q = number_of_stock
    number_of_deals = 0
    for i in range(n):
        if not math.isnan(macd_hist[i]) and not math.isnan(macd_hist[i-1]):
            if macd_hist[i-1] < 0 and macd_hist[i] > 0 and is_investing is False:  # zakup (macd przecina od dolu macd signal)
                q += int(final_capital/closing_prices[i])
                final_capital -= (q * closing_prices[i])
                is_investing = True
                number_of_deals += 1
            if macd_hist[i-1] > 0 and macd_hist[i] < 0 and is_investing is True:  # sprzedaz (macd przecina od gory macd signal)
                final_capital += (q * closing_prices[i])
                q = 0
                is_investing = False
                number_of_deals += 1

    print("Final capital: " + "{:.2f}".format(final_capital))
    print("The equivalent of the final capital in the number of shares: " + str(int(final_capital/closing_prices[n-1])))
    print("Number of shares: " + str(q))
    print("Number of deals: " + str(number_of_deals))

