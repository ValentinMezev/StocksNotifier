from pandas_datareader import data as pdr
import datetime
import os
from tabulate import tabulate

import yfinance as yf

from config import Config


def get_change(previous, current):
    if current == previous:
        return 0
    try:
        return round((abs(current - previous) / previous) * 100.0, 2)
    except ZeroDivisionError:
        return float('inf')


def calculate_percentage_change(prev, current):
    if prev > current:
        sign = "-"
    else:
        sign = "+"
    return sign + str(get_change(prev, current)) + "%"


def del_for_company(num):
    res = ""
    for i in range(0, num):
        res += "-"
    return res


def print_company_name(company):
    print("------------------------------------------------------" + del_for_company(len(company)))
    print("---------------------------" + company + "---------------------------")
    print("------------------------------------------------------" + del_for_company(len(company)))


def validate_companies_validity(companies, start, end):
    for company in companies:
        data = pdr.get_data_yahoo(company, start=start, end=end)
        if data is None or len(data) == 0:
            raise ValueError("Company " + str(company) + " is not valid")


def run():
    config = Config()
    companies = config.companies()

    yf.pdr_override()

    end = datetime.date.today()
    start = end - datetime.timedelta(days=config.report_for_days())
    validate_companies_validity(companies, start, end)

    companies_with_desired_change = set()
    for company in companies:
        print_company_name(company)
        data = pdr.get_data_yahoo(company, start=start, end=end)
        indexLast = len(data.High.values) - 1
        dateLast = data.High.axes[0].date[indexLast]
        highLast = data.High.values[indexLast]
        result = list(list())

        previous = None
        for i in range(0, indexLast):
            current = data.High.values[i]
            currentDate = data.High.axes[0].date[i]
            comparedToLast = calculate_percentage_change(highLast, current)
            comparedToPrevious = calculate_percentage_change(previous, current) if previous else "N/A"
            result.append([currentDate, current, comparedToLast, comparedToPrevious])
            previous = current

            if highLast > current and get_change(highLast, current) > float(config.percent_change()):
                companies_with_desired_change.add(company)

        comparedToPrevious = calculate_percentage_change(highLast, previous)
        result.append([dateLast, highLast, "N/A", comparedToPrevious])
        print(tabulate(result,
                       headers=['Date', 'High', 'Compared to last', "Compared to previous"]))

    if len(companies_with_desired_change) > 0:
        notify("Stocks change", companies_to_notify_for(companies_with_desired_change))


def companies_to_notify_for(companies):
    limit = 10  # limit of companies to show in the notification
    if len (companies) > limit:
        companies = companies[:10]
        companies.append("... and more")

    return companies


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


if __name__ == '__main__':
    run()