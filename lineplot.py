import argparse
import numpy as np
import matplotlib.pyplot as plt


def main():
    '''
    Creates a line plot of accelerometer data vs time.
    '''
    parser = argparse.ArgumentParser("plot accelerometer data")
    parser.add_argument("input_file", type=str, help="file containing acc data")
    parser.add_argument("-o", "--output_file", type=str, help="file name for saving the generated plot.")
    parser.add_argument("-d", "--delimiter", type=str, help="delimiter used in file, default is , (csv)", default = ',')
    parser.add_argument("-r", "--dpi", type=int, help="resolution of image", default = 300)
    parser.add_argument("-lw", "--line_width", type=float, help="line_width", default = 1.0)

    args = parser.parse_args()
    delimiter = args.delimiter
    linewidth = args.line_width

    data = np.genfromtxt(args.input_file, skip_header=2, skip_footer=1, delimiter=delimiter, usecols=(1,2,3))

    dpi = args.dpi
    out_name = None
    if args.output_file:
        out_name = args.output_file

    plt.figure()

    # data[:,0] -> gens
    plt.plot(data[:,0], label='x', color='r', linewidth=linewidth)
    plt.plot(data[:,1], label='y', color='b', linewidth=linewidth)
    plt.plot(data[:,2], label='z', color='g', linewidth=linewidth)

    plt.xlabel('Time')
    plt.ylabel('Acceleration')

    plt.legend()
    plt.tight_layout()
    plt.show()

    if out_name:
        plt.savefig(out_name + '.png', bbox_inches='tight')

if __name__ == "__main__":
    main()
