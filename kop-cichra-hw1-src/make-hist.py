import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate a histogram of successful GSAT steps with bin counts.")
    parser.add_argument('input_file', type=str, help="Path to the input log file")
    parser.add_argument('output_file', type=str, help="Path to save the output plot image (e.g., output.png)")
    parser.add_argument('--bin_count', type=str, default='auto', help="Number of bins for the histogram (default: 'auto'). Can be an integer or a valid string.")
    return parser.parse_args()

def process_log_file(input_file):
    steps_success = []
    with open(input_file, 'r') as log:
        for line in log:
            if "S" in line:
                steps = int(line.split(";")[-1])
                steps_success.append(steps)

    return steps_success

def plot_histogram(steps_success, bin_count, output_file, input_file):
    if len(steps_success) == 0:
        print("No successful runs found in the log.")
    else:
        try:
            bin_count = int(bin_count)
        except ValueError:
            pass

        Q1 = np.percentile(steps_success, 25)
        Q3 = np.percentile(steps_success, 75)
        IQR = Q3 - Q1
        lower_bound = max(0, Q1 - 2 * IQR)
        upper_bound = min(10000, Q3 + 2 * IQR)


        plt.xlim([0, upper_bound])
        filtered_steps = steps_success
        if bin_count == 'auto':
            counts, bins, _ = plt.hist(filtered_steps, edgecolor='black', alpha=0.7)
        else:
            counts, bins, _ = plt.hist(filtered_steps, bins=int(bin_count), edgecolor='black', alpha=0.7)


        percentile_50 = np.percentile(filtered_steps, 50)
        percentile_90 = np.percentile(filtered_steps, 90)
        plt.axvline(percentile_50, color='r', linestyle='--', linewidth=1, label=f'50th Percentile ({percentile_50:.2f})')
        plt.axvline(percentile_90, color='g', linestyle='--', linewidth=1, label=f'90th Percentile ({percentile_90:.2f})')

        plt.title(f'Histogram -\'{input_file.split("/")[-1]}\'')
        plt.xlabel('Steps')
        plt.ylabel('Frequency')
        plt.legend()
        # Print the number of elements in each bin
        total_entries = 0
        for i in range(len(bins) - 1):
            print(f"Bin range {bins[i]:.2f} - {bins[i+1]:.2f}: {int(counts[i])} entries")
            total_entries+=int(counts[i])
            if percentile_50 >= bins[i] and percentile_50 < bins[i+1]:
                print(f"50th Percentile: {percentile_50:.2f} ({int(counts[i])} entries, ~ {total_entries})")
            if percentile_90 >= bins[i] and percentile_90 < bins[i+1]:
                print(f"90th Percentile: {percentile_90:.2f} ({int(counts[i])} entries, ~ {total_entries})")
        print(f"Total entries: {total_entries}")

        plt.savefig(output_file)

def main():
    args = parse_arguments()
    steps_success = process_log_file(args.input_file)
    plot_histogram(steps_success, args.bin_count, args.output_file, args.input_file)

if __name__ == "__main__":
    main()
