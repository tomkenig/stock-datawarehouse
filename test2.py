from datetime import datetime, timedelta

DAILY_HISTORY_DAYS = 3

# todo: filenames to download # daily first in dev. Max Last 62 days
def get_filenames_to_download():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.strptime(str(datetime.now() - timedelta(days=DAILY_HISTORY_DAYS))[0:10], "%Y-%m-%d")
    end_date = datetime.strptime(str(datetime.now() - timedelta(days=1))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, str(day)[0:10])
        # print(day)
    return (l)


print(get_filenames_to_download())


1