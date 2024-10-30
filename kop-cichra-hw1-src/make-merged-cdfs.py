import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Overlay CDFs from two log files of successful GSAT steps with outlier trimming.")
    parser.add_argument('input_file1', type=str, help="Path to the first input log file")
    parser.add_argument('input_file2', type=str, help="Path to the second input log file")
    parser.add_argument('output_file', type=str, help="Path to save the output plot image (e.g., output.png)")
    parser.add_argument('--label1', type=str, default="Algorithm 1", help="Label for the first algorithm")
    parser.add_argument('--label2', type=str, default="Algorithm 2", help="Label for the second algorithm")
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
    return filtered_steps, upper_bound

def plot_overlayed_cdf(steps_success1, steps_success2, output_file, label1, label2, common_name):
    filtered_steps1, upper_bound1 = filter_outliers(steps_success1)
    filtered_steps2, upper_bound2 = filter_outliers(steps_success2)
    upper_bound = max(upper_bound1, upper_bound2)
    #filtered_steps1= steps_success1
    #filtered_steps2 = steps_success2
    sorted_steps1 = np.sort(filtered_steps1)
    sorted_steps2 = np.sort(filtered_steps2)
    
    cdf1 = np.arange(1, len(sorted_steps1) + 1) / len(sorted_steps1)
    cdf2 = np.arange(1, len(sorted_steps2) + 1) / len(sorted_steps2)

    plt.figure(figsize=(10, 6))
    plt.xlim([0, upper_bound])

    plt.plot(sorted_steps1, cdf1, label=label1, color='blue', linestyle='-')
    plt.plot(sorted_steps2, cdf2, label=label2, color='green', linestyle='-')

    #plt.text(x_at_50_1, 0.5, f' {x_at_50_1:.2f}', color='blue', verticalalignment='bottom')
    #plt.text(x_at_90_1, 0.9, f' {x_at_90_1:.2f}', color='blue', verticalalignment='bottom')
    #plt.text(x_at_50_2, 0.5, f' {x_at_50_2:.2f}', color='green', verticalalignment='bottom')
    #plt.text(x_at_90_2, 0.9, f' {x_at_90_2:.2f}', color='green', verticalalignment='bottom')

    plt.ylim([0, 1])
    plt.title(f'Overlayed CDF - \'{common_name}\'')
    plt.xlabel('Steps')
    plt.ylabel('Cumulative Probability')
    plt.legend()
    plt.grid(True)

    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def main():
    args = parse_arguments()
    steps_success1 = process_log_file(args.input_file1)
    steps_success2 = process_log_file(args.input_file2)
    common_name = args.input_file1.replace("gsat2_", "").replace("probsat_", "").split("/")[-1]
    plot_overlayed_cdf(steps_success1, steps_success2, args.output_file, args.label1, args.label2, common_name)

if __name__ == "__main__":
    main()
