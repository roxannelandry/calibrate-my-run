import argparse
from datetime import datetime, timedelta
from lxml import etree


def adjust_distance(trackpoints, nsmap, actual_distance_km):
    """Adjust the distance in the TCX file to match the actual distance."""
    last_distance_element = trackpoints[-1].find("tcx:DistanceMeters", nsmap)
    if last_distance_element is None or not last_distance_element.text:
        print("No distance data found in the last trackpoint.")
        return

    current_distance_m = float(last_distance_element.text)
    actual_distance_m = actual_distance_km * 1000
    distance_scaling_factor = actual_distance_m / current_distance_m

    for trackpoint in trackpoints:
        distance_element = trackpoint.find("tcx:DistanceMeters", nsmap)
        if distance_element is not None and distance_element.text:
            original_distance = float(distance_element.text)
            scaled_distance = original_distance * distance_scaling_factor
            distance_element.text = f"{scaled_distance:.2f}"

    last_distance_element.text = f"{actual_distance_m:.2f}"


def adjust_time(trackpoints, nsmap, actual_time_minutes):
    """Adjust the time in the TCX file to match the actual time."""
    first_time_element = trackpoints[0].find("tcx:Time", nsmap)
    last_time_element = trackpoints[-1].find("tcx:Time", nsmap)

    if first_time_element is None or last_time_element is None:
        print("No time data found in the trackpoints.")
        return

    start_time = datetime.fromisoformat(first_time_element.text.replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(last_time_element.text.replace("Z", "+00:00"))
    current_duration_seconds = (end_time - start_time).total_seconds()
    actual_duration_seconds = actual_time_minutes * 60
    time_scaling_factor = actual_duration_seconds / current_duration_seconds

    for trackpoint in trackpoints:
        time_element = trackpoint.find("tcx:Time", nsmap)
        if time_element is not None and time_element.text:
            original_time = datetime.fromisoformat(
                time_element.text.replace("Z", "+00:00")
            )
            adjusted_time = start_time + timedelta(
                seconds=(original_time - start_time).total_seconds()
                * time_scaling_factor
            )
            time_element.text = (
                adjusted_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            )


def adjust_distance_and_time(
    file_path, output_path, actual_distance_km, actual_time_minutes
):
    """Adjust the distance and time in a Garmin TCX file."""
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return
    except etree.XMLSyntaxError:
        print("There was an error parsing the XML file.")
        return

    namespaces = {
        "": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2",
        "ns3": "http://www.garmin.com/xmlschemas/ActivityExtension/v2",
        "ns2": "http://www.garmin.com/xmlschemas/UserProfile/v2",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    nsmap = {"tcx": namespaces[""], "ns3": namespaces["ns3"]}

    trackpoints = root.xpath("//tcx:Trackpoint", namespaces=nsmap)
    if not trackpoints:
        print("No trackpoints found in the file.")
        return

    # Adjust distance and time
    adjust_distance(trackpoints, nsmap, actual_distance_km)
    adjust_time(trackpoints, nsmap, actual_time_minutes)

    # Write the updated file
    try:
        tree.write(
            output_path, pretty_print=True, xml_declaration=True, encoding="UTF-8"
        )
        print(f"Updated file written to {output_path}")
    except IOError:
        print(f"An error occurred while writing to {output_path}")


def main():
    """Main function to parse arguments and adjust the TCX file."""
    parser = argparse.ArgumentParser(
        description="Adjust the distance and time in a Garmin TCX file."
    )
    parser.add_argument("input_file", help="Path to the input TCX file")
    parser.add_argument(
        "actual_distance_km", type=float, help="Desired total distance in km"
    )
    parser.add_argument(
        "actual_time_minutes", type=float, help="Desired total time in minutes"
    )

    args = parser.parse_args()

    output_file = "run.tcx"

    adjust_distance_and_time(
        args.input_file, output_file, args.actual_distance_km, args.actual_time_minutes
    )


if __name__ == "__main__":
    main()
