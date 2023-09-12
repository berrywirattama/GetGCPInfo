#!/bin/bash

# Initialize the CSV file with headers
echo "PROJECT NAME,INSTANCE NAME,ZONE,MACHINE-TYPE,OPERATING SYSTEM,CPU,MEMORY,DISK SIZE" > compute-engine-details.csv

# Get a list of project IDs
prjs=( $(gcloud projects list --format="value(projectId)") )

# Loop through projects
for i in "${prjs[@]}"
do
    echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" >> list.txt
    echo "Setting Project: $i" >> list.txt
    gcloud config set project "$i"

    if gcloud services list --enabled --filter="NAME:compute.googleapis.com" --format="value(NAME)" | grep -q "compute.googleapis.com"; then
        echo "Compute API is enabled in project - $i"
        gcloud compute instances list --format="table[no-heading](name,zone)" | tail -n +2 | while read -r name zone; do
            python3 retrieve-compute-engine-details.py "$i" "$name" "$zone" >> compute-engine-details.csv
        done
    else
        echo "Compute API is not enabled in project - $i"
    fi
done
