from datetime import datetime, timedelta

def calculate_dates(last_period_date, period_length, cycle_length):
    # Calculate the next period date
    next_period_date = last_period_date + timedelta(days=cycle_length)

    # Period end date
    period_end_date = last_period_date + timedelta(days=period_length)

    # The fertile window starts 3 to 5 days after the period ends and lasts for about 6 days.
    # We'll calculate the start and end dates of this ovulation period.
    ovulation_start_date = period_end_date + timedelta(days=3)  # Start of the fertile window
    ovulation_end_date = period_end_date + timedelta(days=5) + timedelta(days=6)  # End of the fertile window

    return next_period_date, ovulation_start_date, ovulation_end_date

def date_input(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


def integer_input(num):
    return int(num)

