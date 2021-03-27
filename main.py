from functions import *
import constant


def main():
    stock_data = get_dates_and_closing_prices(constant.N)
    macd = count_macd(stock_data, constant.N)
    macd_signal = count_macd_signal(macd, constant.N)
    macd_hist = count_macd_hist(macd, macd_signal, constant.N)
    show_plot(stock_data, macd, macd_signal, macd_hist)
    simulation(get_y_axis(stock_data), macd_hist, constant.NUMBER_OF_STOCK, constant.N)


main()

