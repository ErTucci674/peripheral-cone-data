# Peripheral Cone Data
#
# Copyright (c) 2024, Alessandro Amatucci Girlanda
#
# This module is free software; you can redistribute it and/or modify it under
# the terms of the MIT license. See LICENSE for details.


import csv
import math
import matplotlib.pyplot as plot
import sys


values_types = {
    "point": 0,
    "angle": 1,
    "distance": 2
}

directions = {
    "North": math.pi / 2,
    "West": math.pi,
    "South": math.pi * 3 / 2,
    "East": 0
}


def main():  
    # --- Data Reading ---
    # Read user input
    len_argv = len(sys.argv)
    if len_argv != 2:
        print("Usage: python main.py data.csv")
        sys.exit(1)

    # Check that the file exists
    try:
        data_file = open(sys.argv[1], "r")
    except:
        print(f"Error: {sys.argv[1]} file not found")
        sys.exit(404)

    data_reader = csv.DictReader(data_file)

    # Inserting file data in a Dictionary
    data_dict = list()
    for row in data_reader:
        data_dict.append(row)
    
    # Sorting order based on 'X' values
    data_sorted_x = sorted(data_dict, key=lambda k: (float(k['X']), float(k['Y'])))

    # Store values for the plotting
    x_list = list()
    y_list = list()
    data_labels = list()
    for data in data_sorted_x:
        x_list.append(float(data['X']))
        y_list.append(float(data['Y']))
        data_labels.append(data['Number'])

    Plot(x_list, y_list, data_labels)
            
    # Get user input
    values = promptValues(data_dict)
    points = sorted(visiblePoints(data_dict, values), key=lambda k: (float(k['X']), float(k['Y'])))

    if points:
        print("Visible Points:")
        for point in points:
            print(f"Number {point["Number"]}")
    else:
        print("No visible points")

    plot.show(block=True)

    data_file.close()
    return


def Plot(x_list, y_list, data_labels):
    # 'zorder' makes sure data is rendered on the top
    plot.xlim(0, max(x_list) + 10)
    plot.ylim(0, max(y_list) + 10)
    plot.scatter(x_list, y_list, zorder=2)
    plot.title("Points and Peripheral Vision")
    plot.xlabel("X")
    plot.ylabel("Y")
    plot.grid(True)

    # Add data point number
    for label, x, y in zip(data_labels, x_list, y_list):
        plot.text(x, y, label, ha="right", va="bottom")

    plot.show(block=False)


def validInput(value):
    try:
        return float(value) >= 0
    except ValueError:
        return False


def promptValues(data_dict):
    print("Type in the point number you want to observe, the angle in degrees from the data point towards one side and the distance:")
    print("You must leave a space between the values")

    while True:
        user_input = input("Input: ")
        values = user_input.split()

        # Check if correct number of elements are inserted
        if len(values) != len(values_types):
            print("Usage: point angle distance")
            continue

        # Check if all values are positive integers
        if not all(validInput(value) for value in values):
            print("Error: the inserted values must be positive integers")
            continue

        values = [float(value) for value in values]

        # Check if values stay in corresponding range
        if values[values_types["point"]] == 0 or values[values_types["point"]] > len(data_dict):
            print(f"Error: Data Point number must be between 1 and {str(len(data_dict))}")
            continue
        elif values[values_types["angle"]] > 180:
            print("Error: the maximum value for the angle is 180 degrees")
            continue

        break

    return values


def calculateDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculateAngle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def peripheralRange(startAngle, angleVision, angle):
    if angle < 0:
        angle += math.pi * 2
    
    return angle <= startAngle + angleVision and angle >= startAngle - angleVision


def visiblePoints(data_dict, values):
    point = int(values[values_types["point"]] - 1)
    angleVision = math.radians(values[values_types["angle"]])
    distance = values[values_types["distance"]]

    source = data_dict[point]
    x_source = float(source["X"])
    y_source = float(source["Y"])
    startAngle = float(directions[source["Direction"]])

    points = list()
    for data in data_dict:
        if data == data_dict[point]:
            continue

        x_point = float(data["X"])
        y_point = float(data["Y"])

        angle = calculateAngle(x_source, y_source, x_point, y_point)

        if calculateDistance(x_source, y_source, x_point, y_point) <= distance and peripheralRange(startAngle, angleVision, angle):
            points.append(data)

    return points


if __name__ == "__main__":
    main()