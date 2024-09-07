#!/bin/bash

# Loop through all pcap files in the current directory and convert each to JSON
for pcap in *.pcap; do
    json_file="${pcap%.pcap}.json"
    tshark -r "$pcap" -T json > "$json_file"
    echo "Converted $pcap to $json_file"
done
