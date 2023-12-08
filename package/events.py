from sqlalchemy import event

from sqlalchemy.orm import sessionmaker, scoped_session, mapper

from .models import CycleEntry, Ovulation
from .utils import calculate_dates, date_input, integer_input


def after_insert(mapper, connection, target):
    lastperioddate = date_input(target.lastperioddate)
    period_length = integer_input(target.period_length)
    cycle_length = integer_input(target.cycle_length)
    next_period, ovulation_start, ovulation_end = calculate_dates(lastperioddate, period_length, cycle_length)

    ov_table = Ovulation.__table__
    connection.execute(
        ov_table.insert().values(
            user_id=target.cyc_user_id,
            start_date=ovulation_start,
            end_date=ovulation_end,
            next_period_start_date=next_period,
            ovul_entry_id=target.entry_id,
        )
    )


def after_update(mapper, connection, target):
    lastperioddate = date_input(target.lastperioddate)
    period_length = integer_input(target.period_length)
    cycle_length = integer_input(target.cycle_length)
    next_period, ovulation_start, ovulation_end = calculate_dates(lastperioddate, period_length, cycle_length)


    ov_table = Ovulation.__table__
    connection.execute(
        ov_table.update()
        .where(ov_table.c.ovulation_id == target.cycovul[0].ovulation_id)
        .values(
            user_id=target.cyc_user_id,
            start_date=ovulation_start,
            end_date=ovulation_end,
            next_period_start_date=next_period,
            ovul_entry_id=target.entry_id,
        )
    )

    

event.listen(CycleEntry, "after_insert", after_insert)
event.listen(CycleEntry, "after_update", after_update)
