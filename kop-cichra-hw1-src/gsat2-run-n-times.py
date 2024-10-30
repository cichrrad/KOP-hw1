import subprocess
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the GSAT algorithm with specified parameters.")
    parser.add_argument('n_runs', type=int, help="Number of randomized runs")
    parser.add_argument('max_flips', type=int, help="Maximum number of flips per run")
    parser.add_argument('in_file', type=str, help="Path to the CNF input file")
    parser.add_argument('out_file', type=str, help="Path to save the log of results. Raw output log file with the same name with .raw extension will be saved as well")
    return parser.parse_args()

def run_gsat(n_runs, max_flips, cnf_file, log_file):
    gsat_script_path = subprocess.check_output(["pwd"]).decode('utf-8').strip() + "/gsat2"
    cnf_file_short = cnf_file.split('/')[-1]
    # Run the GSAT algorithm n times
    with open(log_file, 'a') as log:
        with open(log_file+'.raw', 'a') as raw_log:
            for i in range(n_runs):

                gsat_command = f"{gsat_script_path} -r time -p 0.4 -i {max_flips} {cnf_file}"

                # capture the output
                result = subprocess.run(gsat_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Parse the result 
                output = result.stderr.decode('utf-8').strip()
                raw_log.write(cnf_file_short + '; run ' + str(i) + ';' + output + '\n')
                try:
                    steps, max_steps, satisfied_clauses, total_clauses = map(int, output.split())

                    if satisfied_clauses == total_clauses:
                        log.write(f"{cnf_file_short};run {i};S;{steps}\n")
                    else:
                        log.write(f"{cnf_file_short};run {i};F;{steps}\n")
                except ValueError:
                    log.write(f"{cnf_file_short};run {i}: Error parsing result: {output}\n")
        # Close the raw log file
            raw_log.close()
    # Close the log file
        log.close()

def main():
    args = parse_arguments()
    run_gsat(args.n_runs, args.max_flips, args.in_file, args.out_file)

if __name__ == "__main__":
    main()
