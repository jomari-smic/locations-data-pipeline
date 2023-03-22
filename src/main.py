# main.py

import argparse
import logging
import datetime
from data_loader import load_csv_data
from data_preprocessor import normalize_selected_columns, filter_df_columns, filter_masterlist_by_province_and_region
from data_preprocessor import preprocess_address, create_is_found_in_column, make_column_title_case
from data_output import generate_output_csv_data


def main():
    now = datetime.datetime.now()

    parser = argparse.ArgumentParser()
    parser.add_argument("barangay_masterlist", help="Filepath for barangay masterlist CSV")
    parser.add_argument("customer_location_data", help="Filepath for customer location CSV")
    parser.add_argument("output_file", help="Output file for preprocessed data")
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=f"logs/pipeline_{now.strftime('%Y-%m-%d_%H-%M-%S')}.log",
    )

    # Load data
    logging.info(f"Loading barangay masterlist: {args.barangay_masterlist}")
    barangay_master_list = load_csv_data(args.barangay_masterlist)

    
    logging.info(f"Loading customer locations: {args.customer_location_data}")
    customer_loc = load_csv_data(args.customer_location_data)

    # Preprocess barangay master list
    barangay_master_list = normalize_selected_columns(barangay_master_list,['barangay','city','province','region'])

    # filter by province AND region
    # TODO, fidn out if need add input arg for province and region??
    barangays = filter_masterlist_by_province_and_region(barangay_master_list,'iloilo','region vi (western visayas)')
    
    bml_cleaned = filter_df_columns(barangays,['barangay','city', 'province','region'])

    
    # Preprocess customer locations
    cli_cleaned = preprocess_address(customer_loc)
    cli_cleaned = filter_df_columns(cli_cleaned, ['persistent_id', 'address_string_cleaned', 'City', 'Province'])

    make_column_title_case(cli_cleaned,"City", inplace=True)
    make_column_title_case(cli_cleaned,"Province", inplace=True)

    # store values in set
    barangay_set = set(bml_cleaned['barangay']) 
    city_set = set(bml_cleaned['city'])

    # TODO: find out if we should ask a user for this one, hardcoded for the meantime
    # added "iloilo" and "iloilo city" in set manually since it is not given and it is a city of iloilo province
    #city_set.add('iloilo city') #maybe di na need to since makikita na agad sa iloilo palang
    city_set.add('iloilo')

    cli_cleaned = create_is_found_in_column(cli_cleaned,'barangay_found',barangay_set)
    cli_cleaned = create_is_found_in_column(cli_cleaned,'city_found',city_set)


    # ask user for this one?
    PROVINCE = "Iloilo"
    REGION = "Region VI (Western Visayas)"

    # Output data
    generate_output_csv_data(cli_cleaned, PROVINCE, REGION, args.output_file, set(barangay_master_list['barangay']))


if __name__ == "__main__":
    main()