#!/bin/bash

# Check if the folder is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <folder>"
    exit 1
fi

# Get the folder from the command-line argument
FOLDER=$1

# # cdf and hist gen
# # Loop over all files in the specified folder
for file in "$FOLDER"/*; do
    # Extract the filename without extension
    filename=$(basename "$file")
    base="${filename%.*}"

    # Define the output file
    output_file_cdf="${base}_cdf.pdf"
    output_file_hist="${base}_hist.pdf"
    
    # Call the Python script with the current file and the corresponding output file
    echo "Processing file: $base"
    python3 make-cdf.py "$file" "$output_file_cdf"
    python3 make-hist.py "$file" --bin_count=115 "$output_file_hist"
    echo "Output files: $output_file_cdf and $output_file_hist"
done
 
# Set the directory containing the files
directory="$FOLDER"
#merged gen
# Loop over all gsat2 files in the specified directory
for gsat2_file in "$directory"/gsat2_*; do
  # Extract the filename without the path
  gsat2_filename="${gsat2_file##*/}"
  
  # Extract the X part of the filename
  X="${gsat2_filename#gsat2_}"

  # Define the corresponding probsat file path
  probsat_file="$directory/probsat_${X}"
  
  # Check if the corresponding probsat file exists
  if [[ -f "$probsat_file" ]]; then
    # Run the Python command with the paired files
    echo "Processing pair: $gsat2_filename and probsat_${X}"
    python3 make-merged-cdfs.py "$gsat2_file" "$probsat_file" --label1=gsat2 --label2=probsat "comparison_cdf_${X}.pdf"
    python3 make-merged-hists.py "$gsat2_file" "$probsat_file" --label1=gsat2 --label2=probsat --bin_count=115 "comparison_hist_${X}.pdf"
  else
    echo "No matching probsat file for $gsat2_filename"
  fi
done

