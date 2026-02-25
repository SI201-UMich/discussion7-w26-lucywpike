import unittest
import os
import csv

###############################################################################
##### TASK 1: CSV READER
###############################################################################
def load_listings(f):
    """
    Read the Airbnb listings CSV and return a list of records.

    Parameters:
        f : str
            Filename or path to a CSV file containing Airbnb listings.

    Expected CSV header: id, name, host_id, neighbourhood, neighbourhood_group, latitude,
        longitude, room_type, price, minimum_nights, ...

    Returns:
        list of dictionaries
            A list where each element is a dictionary representing one listing.
            Each dictionary has:
                - Keys (str): Column names from the CSV header 
                  (e.g., 'id', 'name', 'host_id', 'neighbourhood', 'price', etc.)
                - Values (str): Corresponding values from that row
                  (NOTE: All values are strings, including numbers, which means you will need to convert them in later functions)
    """
    # Do not modify this code
    # This opens the CSV and saves it as a list of lists
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    # TODO: Read the CSV using csv.reader and convert it to a list a dictionaries
    
    with open(full_path) as f:
        reader = csv.reader(f) # pass the file object to csv.reader

        header = next(reader) # read the header row

        all_listings = [] # empty list to store all the listings as dictionaries 

        for row in reader: # loop through each row in the CSV after the header
            item = {}
            for i, column in enumerate(header): # loop through each column in the header
                item[column] = row[i] # create a key-value pair in the item dictionary where the key is the column name and the value is the corresponding value from the row
            all_listings.append(item) # add the item dictionary to the list of listings

        return all_listings # return the list of dictionaries representing the listings
        
###############################################################################
##### TASK 2: CALCULATION FUNCTION (single calculation)
###############################################################################
def calculate_avg_price_by_neighbourhood_group_and_room(listings):
    """
    Calculate the average nightly price for each (neighbourhood_group, room_type) pair.

    Parameters:
        listings : list of dictionaries
            - Keys (str): Column names from the CSV header 
            (e.g., 'id', 'name', 'host_id', 'neighbourhood', 'price', etc.)
            - Values (str): Corresponding values from that row
            (NOTE: All values are strings, including numbers, which means you will need to convert them in this function)

    Returns:
        dict mapping (neighbourhood_group, room_type) -> average_price (float)
        e.g. { ('Downtown', 'Entire home/apt'): 123.45, ... }
    """
    price_sum = {}
    price_counts = {}

    for listing in listings:
        neighbourhood_group = listing["neighbourhood_group"] # get the neighbourhood group from the listing 
        room_type = listing["room_type"] # get the room type from the listing
        price = float(listing["price"]) # get the price from the listing and convert it to a float

        listing_key = (neighbourhood_group, room_type) # create a tuple key for the dictionary using the neighbourhood group and room type

        if listing_key not in price_sum: # if this key is not already in the price_sum dictionary, initialize it and the count for this key
            price_sum[listing_key] = 0 
            price_counts[listing_key] = 0
        price_sum[listing_key] += price # add the price to the sum for this key
        price_counts[listing_key] += 1 # increment the count for this key

    price_average = {} # create a new dictionary to store the average prices

    for listing_key in price_sum: # loop through each key in the price_sum dictionary
        price_average[listing_key] = price_sum[listing_key] / price_counts[listing_key] # calculate the average price for this key and store it in the averages dictionary

    return price_average # return the dictionary mapping (neighbourhood_group, room_type) to average price 

###############################################################################
##### TASK 3: CSV WRITER
###############################################################################
def write_summary_csv(out_filename, avg_prices):
    """
    Write the summary statistics to a CSV file.

    Parameters:
        out_filename : str
            Path to output CSV file.
        avg_prices : dictionary
            dict mapping (neighbourhood_group, room_type) -> average_price (float)
            e.g. { ('Manhattan', 'Entire home/apt'): 123.45, ... }

    Returns:
        None
            Writes a CSV file with header: neighbourhood_group, room_type, average_price
    """
    with open(out_filename, 'w') as fout: # open the output file for writing
        writer = csv.writer(fout) # create a csv writer object

        writer.writerow(["neighbourhood_group", "room_type", "average_price"]) # write the header row

        for key, value in avg_prices: # loop through each key in the avg_prices dictionary
            writer.writerow([key[0], key[1], value]) # write a row to the CSV with the neighborhood group, room type, and average price
    return 

###############################################################################
##### UNIT TESTS (Do not modify the code below!)
###############################################################################
class TestAirbnbListings(unittest.TestCase):
    def setUp(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        full_path = os.path.join(base_path, 'new_york_listings_2024.csv')
        self.listings = load_listings(full_path)

    def test_load_listings(self):
        # Test that listings were loaded successfully
        self.assertIsInstance(self.listings, list)
        self.assertGreater(len(self.listings), 0)
        # Check that each listing is a dictionary
        self.assertIsInstance(self.listings[0], dict)
        # Check for expected keys
        expected_keys = ['neighbourhood_group', 'room_type', 'price']
        for key in expected_keys:
            self.assertIn(key, self.listings[0])

    def test_calculate_avg_price_by_neighbourhood_group_and_room(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)
        
        # Test a few key combinations from the real data
        self.assertAlmostEqual(averages[('Manhattan', 'Entire home/apt')], 253.74735249621784, places=2)

        self.assertAlmostEqual(averages[('Brooklyn', 'Private room')], 161.65877598152426, places=2)

        self.assertAlmostEqual(averages[('Queens', 'Entire home/apt')], 179.92875157629257, places=2)

        self.assertAlmostEqual(averages[('Bronx', 'Private room')], 97.30147058823529, places=2)

        self.assertAlmostEqual(averages[('Staten Island', 'Entire home/apt')], 139.85256410256412, places=2)

    def test_write_and_read_summary(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)
        test_output = 'test_summary_output.csv'
        
        write_summary_csv(test_output, averages)
        
        with open(test_output, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            # Check that we have the expected number of rows
            self.assertEqual(len(rows), 18)
            
            # Verify header
            self.assertEqual(reader.fieldnames, ['neighbourhood_group', 'room_type', 'average_price'])
        

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
