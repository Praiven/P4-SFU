import json
from datetime import datetime, timedelta
#files to analyze 
file_paths = [
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth1_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth2_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth3_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth4_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth5_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth6_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth7_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth8_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth9_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth10_in.json',     
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth11_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth12_in.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth1_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth2_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth3_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth4_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth5_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth6_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth7_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth8_out.json',  
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth9_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth10_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth11_out.json',
    'C:\\Users\\tsikr\\OneDrive\\Desktop\\Building\\Wireshark\\A_p4\\o12\\5th\\s1-eth12_out.json'                                                
]
# packets that are of type udp will be stored, the key will be the packet load 
categorized_packets = {}
time_format = "%b %d, %Y %H:%M:%S.%f000 %Z"

def parse_frame_time(packet):
    frame_protocols = packet["_source"]["layers"]["frame"]["frame.protocols"]
    if frame_protocols == "eth:ethertype:ip:udp:data":                       #the packets we are interested in
        frame_time = packet["_source"]["layers"]["frame"]["frame.time"]
        data_field = packet["_source"]["layers"]["data"]["data.data"]
        print("Frame time:", frame_time)
        print("Data:", data_field)
        print(file_path)
        return frame_time, data_field
    return None, None

for file_path in file_paths:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)    
    # Process each packet in the file
    for packet in data:
        frame_time, data_field = parse_frame_time(packet)
        if frame_time:
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

