import cv2
import json
import csv

data = json.load(open("input.json", "r"))

# total number of wafers
wafers = data["die"]["rows"] * data["die"]["columns"]

with open("defects.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(["Wafer Number", "X-coordinate", "Y-coordinate"])

    for wafer_num in range(1, wafers + 1):
     
        wafer_imag = cv2.imread(f"wafer_image_{wafer_num}.png")

        #empty list to store defect coordinates
        defect_coordinates = []

        
        for row_index in range(len(wafer_imag)):
            # dictionary to store pixel counts and coordinates
            count = {}

            
            for column_index in range(len(wafer_imag[row_index])):
                # Convert the pixel value to a string
                pixel_value = str(wafer_imag[row_index][column_index])

                if pixel_value in count:
                    # If the pixel value exists in the dictionary, increment the count and append coordinates
                    count[pixel_value]["count"] += 1
                    count[pixel_value]["id"].append([row_index, column_index])
                else:
                    # If the pixel value is not in the dictionary, create a new entry
                    count[pixel_value] = {
                        "count": 1,
                        "id": [[column_index, row_index]],
                    }

            # Find the pixel value with the maximum count
            max_count_pixel = max(count, key=lambda k: count[k]["count"])

            # Remove the key with the maximum count from the dictionary
            del count[max_count_pixel]

            # Write defect coordinates to the CSV file
            for pixel_key in count:
                defect_coordinates.extend(count[pixel_key]["id"])
                csv_writer.writerow(
                    [
                        wafer_num,
                        count[pixel_key]["id"][0][0],
                        count[pixel_key]["id"][0][1],
                    ]
                )



print("Defect coordinates saved in defects.csv")

#the program may take a couple of time to run :) pls wait
