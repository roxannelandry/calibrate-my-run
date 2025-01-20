import xml.etree.ElementTree as ET

try:
    tree = ET.parse('file.tcx')
    root = tree.getroot()
except FileNotFoundError:
    print("The file 'file.tcx' was not found.")
    exit(1)
except ET.ParseError:
    print("There was an error parsing the XML file.")
    exit(1)

namespaces = {
    '': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'ns2': 'http://www.garmin.com/xmlschemas/UserProfile/v2',
    'ns3': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2',
    'ns4': 'http://www.garmin.com/xmlschemas/ProfileExtension/v1',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

trackpoints = root.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint')

total_additional_distance = 1000.0  # Adding 1000 meters to the existing 200 meters
num_trackpoints = len(trackpoints)
additional_distance_per_trackpoint = total_additional_distance / num_trackpoints

for i, trackpoint in enumerate(trackpoints):
    distance_element = trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters')
    if distance_element is not None:
        current_distance = float(distance_element.text)
        updated_distance = current_distance + (i + 1) * additional_distance_per_trackpoint
        distance_element.text = str(updated_distance)

if trackpoints:
    last_trackpoint = trackpoints[-1]
    distance_element = last_trackpoint.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters')
    if distance_element is not None:
        distance_element.text = str(1200.0)  # Setting the last trackpoint distance to 1200 meters

output_file = 'updated_file.tcx'
try:
    tree.write(output_file, xml_declaration=True, encoding='UTF-8')
    print(f"Updated file written to {output_file}")
except IOError:
    print(f"An error occurred while writing to {output_file}")
