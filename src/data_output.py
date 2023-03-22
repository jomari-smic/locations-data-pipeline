# data_output.py

import logging
import csv


def generate_output_csv_data(df, province, region, csv_file,barangay_raw_set=None):
    # CSV output headers
    headers = ['Persistent ID', 'Address String', 'Barangay', 'City', 'Province', 'Region']

    # Empty list to store output data
    output_data = []

    # Loop through cli_cleaned dataframe
    for index, row in df.iterrows():

        if row['city_found'] == None:
            
            for word in row['address_string_cleaned']:
                if word.lower() in barangay_raw_set: # in barangay
                    row['barangay_found'] = word.title()
                    break

            output_data.append([row['persistent_id'], row['address_string_cleaned'], row['barangay_found'], row['City'], row['Province'], None])

        elif row['barangay_found']:
            output_data.append([row['persistent_id'], row['address_string_cleaned'], row['barangay_found'], row['city_found'],  province, region])
                            
            # TODO: what if you have same barangay names but under different city?
            #       first thought was to look at the address string to get the city    
            '''
            if loremipsum:
                # Multiple rows have the same barangay value
                # Need to figure out which city the barangay belongs to
                city = None

                # Code to figure out the city
                output_data.append([row['persistent_id'], row['address_string_cleaned'], row['barangay_found'], city,  province, region])
            
            else:
                # Only one row has the barangay value
                output_data.append([row['persistent_id'], row['address_string_cleaned'], row['barangay_found'], row['city_found'], province, region])
            '''
        elif row['city_found']:
            # This means no barangay was given
            output_data.append([row['persistent_id'], row['address_string_cleaned'], None, row['city_found'], province, region])

    
    output_csv_data(csv_file, headers, output_data)
    return csv_file

def output_csv_data(csv_file, headers, output_data):

    # open the file for writing
    with open(csv_file, mode='w', newline='') as file:

        logging.info(f"Outputting data to file: {csv_file}")

        # create the writer object
        writer = csv.writer(file)

        # write the header row first
        writer.writerow(headers)

        # loop through each row in the data array and write it to the CSV file
        for row in output_data:
            writer.writerow(row)