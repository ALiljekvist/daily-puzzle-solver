from datetime import datetime, timedelta
import time
import numpy as np
from main import run

def test_all():
    times = []
    today = datetime.today()
    day = datetime.strptime(f'Jan 1 {today.year}', '%b %d %Y')
    print('----- STARTING TEST -----')
    while day.year == today.year:
        day_time = time.time()
        for wd in range(7):
            start = time.time()
            solved = run(day, weekday=wd, plot=False)
            if not solved:
                print(f'COULD NOT FIND SOLUTION FOR {day.month}-{day.day}-{wd}')
                continue
            times.append(time.time()-start)
        day_time = time.time() - day_time
        print(day.strftime('%Y-%m-%d'), f' ({day_time} s)')
        day += timedelta(days=1)
    times = np.array(times)
    print('----- TEST DONE -----')
    print(f'total time: {np.sum(times)}')
    print(f'average time: {np.mean(times)}')
    print(f'standard deviation: {np.std(times)}')

if __name__ == '__main__':
    test_all()