#!/bin/bash

# Usage: ./script.sh INDIR NUMOFRUNS MAXFLIPS OUTFILE

# Check for required arguments
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 INDIR NUMOFRUNS MAXFLIPS [OUTFILE]"
    exit 1
fi

# Assign the input arguments
INDIR="$1"
N="$2"
MAXF="$3"
OUTFILE="${4:-output}"  # Default to 'output' if not provided

# Recursively find all .cnf files in the given directory
find "$INDIR" -type f -name "*.cnf" | while read -r cnf_file; do
    # Execute the Python script for each cnf file
    echo "Processing $cnf_file"
    python3 gsat2-run-n-times.py "$N" "$MAXF" "$cnf_file" "$OUTFILE"
done

echo "All files processed."
