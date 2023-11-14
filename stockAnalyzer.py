import unittest
from datetime import datetime
from unittest.mock import patch


#Get user input-------------------
def get_user_input():
    #get stock symbol
    stock_symbol = input("Enter the stock symbol: ")

    #get chart type, line or bar
    while True:
        print("\nChart Types\n ----------------\n 1) Bar \n 2) Line\n")
        chart_type = input("Enter 1 for Bar chart, 2 for Line chart: ")
        if chart_type in ["1", "2"]:
            break
        else:
            print("\nInvalid input\n")
            raise ValueError

    #get time series function, intraday, daily, weekly, or monthly
    while True:
        print("\nTime Series \n--------------------------------\n 1) Intraday\n 2) Daily\n 3) Weekly\n 4) Monthly\n")
        u_time_series = input("Enter time series (1,2,3,4): ")
        if u_time_series in ["1","2","3","4"]:
            break
        else: 
            print("\nInvalid input")
            raise ValueError


    if u_time_series == "1":
        time_series = "TIME_SERIES_INTRADAY"
        time_series_output = "Time Series (5min)"
    if u_time_series == "2":
        time_series = "TIME_SERIES_DAILY"
        time_series_output = "Time Series (Daily)"
    if u_time_series == "3":
        time_series = "TIME_SERIES_WEEKLY"
        time_series_output = "Weekly Time Series"
    if u_time_series == "4":
        time_series = "TIME_SERIES_MONTHLY"
        time_series_output = "Monthly Time Series"


    #get start date
    while True:
        start_date = input("\nEnter the start date (YYYY-MM-DD): ")
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            break
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD format.")


    #get end date
    while True:
        end_date = input("\nEnter the end date in YYYY-MM-DD format: ")
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
            if end_date >= start_date:
                break
            else:
                print("The end date should not be before the begin date.")
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD format.")


    return stock_symbol, chart_type, time_series, start_date, end_date

# Test class
class TestGetUserInput(unittest.TestCase):

    #test good input 
    @patch('builtins.input', side_effect=['AAPL', '1', '2', '2023-01-01', '2023-01-10'])
    def test_gather_user_input(self, mock_input):
        result = get_user_input()
        expected_result = ('AAPL', '1', 'TIME_SERIES_DAILY', '2023-01-01', '2023-01-10')
        self.assertEqual(result, expected_result)

    #test bad symbol stock symbol (this one should fail)
    @patch('builtins.input', side_effect=['aapl', '1', '2', '2023-01-01', '2023-01-10'])
    def test_bad_stock_symbol(self, mock_input):
        with self.assertRaises(ValueError) as context:
            get_user_input()

        expected_error_message = "Invalid input. Please enter up to 7 capital letters."
        self.assertEqual(str(context.exception), expected_error_message)

    #test bad chart type input
    def test_bad_chart_type(self):
        with patch('builtins.input', side_effect=['AAPL', '3', '2', '2023-01-01', '2023-01-10']):
            with self.assertRaises(ValueError) as context:
                get_user_input()

            expected_error_message = "Invalid input"
            self.assertEqual(str(context.exception), expected_error_message)


    #test bad time series input
    @patch('builtins.input', side_effect=['AAPL', '1', '5', '2023-01-01', '2023-01-10'])
    def test_bad_time_series(self, mock_input):
        with self.assertRaises(ValueError) as context:
            get_user_input()

        expected_error_message = "Invalid input"
        self.assertEqual(str(context.exception), expected_error_message)

    #test bad start date input
    @patch('builtins.input', side_effect=['AAPL', '1', '2', 'bad-date', '2023-01-10'])
    def test_bad_start_date(self, mock_input):
        with self.assertRaises(ValueError) as context:
            get_user_input()

        expected_error_message = "Invalid date format. Please use YYYY-MM-DD format."
        self.assertEqual(str(context.exception), expected_error_message)

    #test bad end date input
    @patch('builtins.input', side_effect=['AAPL', '1', '2', '2023-01-01', 'bad-date'])
    def test_bad_end_date(self, mock_input):
        with self.assertRaises(ValueError) as context:
            get_user_input()

        expected_error_message = "The end date should not be before the begin date."
        self.assertEqual(str(context.exception), expected_error_message)

if __name__ == '__main__':
    unittest.main()
