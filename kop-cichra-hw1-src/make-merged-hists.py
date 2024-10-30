import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Overlay histograms from two log files of successful GSAT steps with outlier trimming.")
    parser.add_argument('input_file1', type=str, help="Path to the first input log file")
    parser.add_argument('input_file2', type=str, help="Path to the second input log file")
    parser.add_argument('output_file', type=str, help="Path to save the output plot image (e.g., output.png)")
    parser.add_argument('--label1', type=str, default="Algorithm 1", help="Label for the first algorithm")
    parser.add_argument('--label2', type=str, default="Algorithm 2", help="Label for the second algorithm")
    parser.add_argument('--bin_count', type=str, default='auto', help="Number of bins for the histogram (default: 'auto'). Can be an integer or a valid string.")
    return parser.parse_args()

def process_log_file(input_file):
    steps_success = []
    with open(input_file, 'r') as log:
        for line in log:
            if "S" in line:
                steps = int(line.split(";")[-1])
                steps_success.append(steps)
    #steps_success = steps_success[:850000]
    return steps_success

def filter_outliers(steps_success):
    Q1 = np.percentile(steps_success, 25)
    Q3 = np.percentile(steps_success, 75)
    IQR = Q3 - Q1
    lower_bound = max(0, Q1 - 2 * IQR)
    upper_bound = min(10000, Q3 + 2 * IQR)
    filtered_steps = [x for x in steps_success if lower_bound <= x <= upper_bound]
    return filtered_steps, lower_bound, upper_bound

def plot_overlayed_histogram(steps_success1, steps_success2, output_file, label1, label2, bin_count, common_name):
    filtered_steps1, lower_bound1, upper_bound1 = filter_outliers(steps_success1)
    filtered_steps2, lower_bound2, upper_bound2 = filter_outliers(steps_success2)
    upper_bound = max(upper_bound1, upper_bound2)
    
    filtered_steps1 = steps_success1
    filtered_steps2 = steps_success2
    
    plt.figure(figsize=(10, 6))
    plt.xlim([0, upper_bound])
    
    plt.hist(filtered_steps1, bins=int(bin_count), color='blue', alpha=0.5, label=label1, edgecolor='black')
    plt.hist(filtered_steps2, bins=int(bin_count), color='green', alpha=0.5, label=label2, edgecolor='black')

    percentile_50_1 = np.percentile(filtered_steps1, 50)
    percentile_90_1 = np.percentile(filtered_steps1, 90)
    percentile_50_2 = np.percentile(filtered_steps2, 50)
    percentile_90_2 = np.percentile(filtered_steps2, 90)

    plt.axvline(percentile_50_1, color='blue', linestyle='--', label=f'{label1} - 50th Percentile ({percentile_50_1:.2f})')
    plt.axvline(percentile_90_1, color='blue', linestyle=':', label=f'{label1} - 90th Percentile ({percentile_90_1:.2f})')
    plt.axvline(percentile_50_2, color='green', linestyle='--', label=f'{label2} - 50th Percentile ({percentile_50_2:.2f})')
    plt.axvline(percentile_90_2, color='green', linestyle=':', label=f'{label2} - 90th Percentile ({percentile_90_2:.2f})')

    plt.title(f'Overlayed Histogram - \'{common_name}\'')
    plt.xlabel('Number of Steps')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)

    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def main():
    args = parse_arguments()
    steps_success1 = process_log_file(args.input_file1)
    steps_success2 = process_log_file(args.input_file2)
    common_name = args.input_file1.replace("gsat2_", "").replace("probsat_", "").split("/")[-1]
    plot_overlayed_histogram(steps_success1, steps_success2, args.output_file, args.label1, args.label2, args.bin_count, common_name)

if __name__ == "__main__":
    main()
