import datetime
import argparse
import numpy as np
from tabulate import tabulate
import glob
import sys

def delta_time(time1, time2):
    # split time and take up to seconds, discard microseconds
    t1 = ':'.join(time1.split(':')[:3])
    t2 = ':'.join(time2.split(':')[:3])
    time_i = datetime.datetime.strptime(t1, '%H:%M:%S') 
    time_j = datetime.datetime.strptime(t2, '%H:%M:%S')
    delta = time_j - time_i
    return delta


def main():
    '''
    Generates a report of any discontinuities and time gaps
    in accelerometer data.
    '''
    parser = argparse.ArgumentParser("plot accelerometer data")
    parser.add_argument("input_files", metavar='file', type=str, nargs='+', help="file containing acc data")
    parser.add_argument("-o", "--output_file", type=str, help="file name for saving the generated plot.", default=None)
    parser.add_argument("-d", "--delimiter", type=str, help="delimiter used in file, default is , (csv)", default = ',')
    parser.add_argument("-v", help="verbose", action='store_true')
    
    args = parser.parse_args()
    input_files = args.input_files
    output_file = args.output_file
    delimiter = args.delimiter
    verbose = args.v

    stats = []
    for fname in input_files:
        time = np.genfromtxt(fname, dtype=str, skip_header=1, skip_footer=1, delimiter=delimiter, usecols=(0))

        seconds = [int(line.split(':')[2]) for line in time]

        gap_count = 0
        gaps = [] 
        gaps_time = [] 

        print('-' * 30)
        print fname
        for i in range(len(seconds) - 1):
            # if gap found, i.e. seconds in consecutive terms don't have a +1 difference
            if not(
                (seconds[i] + 1 == seconds[i+1]) or 
                (seconds[i] == 59 and seconds[i+1] == 0) or 
                (seconds[i] == seconds[i+1]) ):

                gap_count += 1

                delta = delta_time(time[i], time[i+1])
                gaps.append(delta.seconds)
                gaps_time.append(delta)

                if verbose:
                    print("Line {}: {} to {}, time gap: {}".format(i+2, time[i], time[i+1], delta))


        total_gap =  sum(gaps_time, datetime.timedelta())
        total_time = delta_time(time[0], time[-1])

        labels = ['gaps', 'longest gap', 
                  'shortest gap', 'total gaps', 
                  'total time', 'diff', 
                  '%']
        if gap_count == 0:
            data = [0, 0, 0, 0] 
        else:
            data = [gap_count, max(gaps), 
                    min(gaps), sum(gaps_time, datetime.timedelta())]

        data.extend([total_time, total_time - total_gap,
                    '%.2f' % (float(total_gap.seconds) / total_time.seconds)])

        stats.append([fname] + data)

        if verbose:
            table = [[label, d] for label, d in zip(labels, data)]

            print 'Report: {}'.format(fname)
            print tabulate(table, tablefmt='grid')

    if output_file:
        np.savetxt(output_file, stats, delimiter=',', fmt='%s')
        

if __name__ == "__main__":
    main()
