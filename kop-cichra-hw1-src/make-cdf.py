import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process log file to create CDF of successful GSAT steps.")
    parser.add_argument('input_file', type=str, help="Path to the input log file")
    parser.add_argument('output_file', type=str, help="Path to save the output plot image (e.g., output.png)")
    return parser.parse_args()

def process_log_file(input_file):
    steps_success = []
    with open(input_file, 'r') as log:
        for line in log:
            if "S" in line:
                # Extract the number of steps from the line
                steps = int(line.split(";")[-1])
                steps_success.append(steps)

    # Sort and select the first 850,000 successful runs
    return steps_success

def plot_cdf(steps_success, output_file,input_file):
    if len(steps_success) == 0:
        print("No successful runs found in the log.")
    else:
        # Calculate IQR and bounds
        Q1 = np.percentile(steps_success, 25)
        Q3 = np.percentile(steps_success, 75)
        IQR = Q3 - Q1
        lower_bound = max(0, Q1 - 2 * IQR)
        upper_bound = min(10000, Q3 + 2 * IQR)

        # Filter steps to exclude outliers
        filtered_steps = [x for x in steps_success if lower_bound <= x <= upper_bound]
        # Create the cumulative distribution function (CDF)
        sorted_steps = np.sort(filtered_steps)
        cdf = np.arange(1, len(sorted_steps) + 1) / len(sorted_steps)

        # Plot the CDF with connected points
        plt.plot(sorted_steps, cdf, marker=' ', linestyle='-', color='cyan', linewidth=2)

        plt.xlim([0, upper_bound])
        plt.ylim([0, 1])

        # Set title and labels
        plt.title(f'CDF -\'{input_file.split("/")[-1]}\'')
        plt.xlabel('Steps')
        plt.ylabel('Cumulative Probability')
        plt.grid(True)
        

        # Save the plot to the output file
        plt.savefig(output_file)
        # plt.show()

def main():
    args = parse_arguments()
    steps_success = process_log_file(args.input_file)
    plot_cdf(steps_success, args.output_file, args.input_file)

if __name__ == "__main__":
    main()
