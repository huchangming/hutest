import datetime


def get_times():
    times = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return times