import json
from datetime import datetime, timedelta
#files to analyze 
file_paths = [
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_app\\o2\\1st\\2_1.json'
]
# packets that are of type udp will be stored, the key will be the packet load 
categorized_packets = {}
time_format = "%b %d, %Y %H:%M:%S.%f000 %Z"

def parse_frame_time(packet):
    frame_protocols = packet["_source"]["layers"]["frame"]["frame.protocols"]
    if frame_protocols == "eth:ethertype:ip:udp:data":                       #the packets we are interested in
        frame_time = packet["_source"]["layers"]["frame"]["frame.time"]
        data_field = packet["_source"]["layers"]["data"]["data.data"]
        destination = packet["_source"]["layers"]["ip"]["ip.dst"]
        print("Frame time:", frame_time)
        print("Data:", data_field)
        print(file_path)
        print("Destination", destination)
        return frame_time, data_field, destination
    return None, None, None

for file_path in file_paths:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)    
    # Process each packet in the file
    for packet in data:
        frame_time, data_field, destination = parse_frame_time(packet)
        if frame_time and destination == '10.0.0.17':
            time = datetime.strptime(frame_time, time_format)
            #print(time)
            # Categorize packets by data field
            if data_field not in categorized_packets:
                categorized_packets[data_field] = [time]
            else:
                categorized_packets[data_field].append(time)     

    for packet in data:
        frame_time, data_field, destination = parse_frame_time(packet)
        if frame_time and destination != "10.0.0.17":
            time = datetime.strptime(frame_time, time_format)
            #print(time)
            # Categorize packets by data field
            if data_field not in categorized_packets:
                categorized_packets[data_field] = [time]
            else:
                categorized_packets[data_field].append(time)                   
  
print(categorized_packets)
print(len(categorized_packets))
time_differences = []

for data_field in categorized_packets:
    for i in range(1, len(categorized_packets[data_field])):
        time_differences.append(categorized_packets[data_field][i] - categorized_packets[data_field][0]) 
        print("Time difference:", categorized_packets[data_field][i] - categorized_packets[data_field][0])
    print("Next batch")

print(time_differences)
sum = timedelta()
for time in time_differences:
    sum = sum + time

avg = sum / len(time_differences)
minimum = min(time_differences)
maximum = max(time_differences)

print(minimum, maximum, avg)
