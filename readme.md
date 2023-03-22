# Locations Data Pipeline

This is a data pipeline that processes customer location data and merges it with a barangay masterlist to create a more accurate location data. Before running the pipeline, you must create a virtual environment and install the required dependencies listed in `requirements.txt`.

## Installation

To install the required dependencies, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the repository.
3. Create a virtual environment by running the following command:
    ```
    python3 -m venv env
    ```
4. Activate the virtual environment by running the following command:
    ```
    source env/bin/activate
    ```
5. Install the required dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```

## Usage

To run the pipeline, use the following command from the root directory:

 ```
 python src/main.py --filepath-to-barangay-masterlist-csv --filepath-to-customer-locations-csv --output-file
 ```

 - Replace the `--filepath-to-barangay-masterlist-csv` argument with the file path to the barangay masterlist CSV file 
 - Replace the `--filepath-to-customer-locations-csv` argument with the file path to the customer locations CSV file 
 - Replace the `--output-file` argument with the desired output file name and path.

For example:

 ```
 python src/main.py data/input/barangay_masterlist_all.csv data/input/customer_locations_iloilo.csv .data/output/output_iloilo.csv
 ```

