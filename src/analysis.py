import pandas as pd
import argparse
import os
import csv

def main(data_path):
    data = []
    bad_data = []

    try:
        with open(data_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None) # avoid double read of header

            for row in reader:
                # Clean up any carriage return characters in the row
                row = [col.replace('\r\n', '').strip() for col in row]
                print(row)

                if len(row) >= 3:
                    if any(col == '' for col in row[:3]):  # Check for empty columns
                        bad_data.append(row[:3])  # Collect bad data
                    else:
                        data.append(row[:3])  # Append the first three columns

        products_df = pd.DataFrame(data, columns=['product_name', 'our_price', 'category'])
        bad_data_df = pd.DataFrame(bad_data, columns=['product_name', 'our_price', 'category'])

        print(products_df.head())

        with open('report.md', 'w', encoding='utf-8') as report_file:
            report_file.write("\n\n## Bad Data\n")
            report_file.write("The following rows were missing required information:\n")
            report_file.write(bad_data_df.to_markdown(index=False))

            report_file.write("\n\n## Good Data\n")
            report_file.write(products_df.to_markdown(index=False))

        print("Report written to 'report.md'.")

    except Exception as e:
        print(f"Error reading the CSV file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read a CSV file.')
    parser.add_argument('data_path', type=str, help='Path to the CSV file')
    args = parser.parse_args()
    
    main(args.data_path)
  
