#!/bin/bash

# Usage: ./script.sh INDIR NUMOFRUNS OUTFILE

# Check for required arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 INDIR NUMOFRUNS OUTFILE"
    exit 1
fi

# Assign the input arguments
INDIR="$1"
N="$2"
OUTFILE="${3:-output}"  # Default to 'output' if not provided

# Recursively find all .cnf files in the given directory
find "$INDIR" -type f -name "*.cnf" | while read -r cnf_file; do
    # Execute the Python script for each cnf file
    echo "Processing $cnf_file"
    python3 probsat-run-n-times.py "$N" "$cnf_file" "$OUTFILE"
done

echo "All files processed."
