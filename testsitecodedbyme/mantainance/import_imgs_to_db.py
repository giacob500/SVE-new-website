'''
The code program below is used to convert a series of file directories listed in a TXT (or other formats) file,
providing in output a CSV file that can be added to the database via "DB Browser for DQL Lite"

'''
import csv
import os

def get_category(file_name):
    # Check if the file name starts with a certain string
    if file_name.startswith('xtcu'):
        return 'terracotta'
    elif file_name.startswith('PLA'):
        return 'terracotta_3d'
    elif file_name.startswith('XQ'):
        return 'marble_hearts'
    elif file_name.startswith('B'):
        return 'slate'
    elif file_name.startswith('RV'):
        return 'books'
    else:
        lower_file_name = file_name.lower()
        if lower_file_name.startswith('cu') or lower_file_name.startswith('cn') or lower_file_name.startswith('cal'):
            return 'marble'
        else:
            return ''

def get_image_url(file_path):
    file_path = file_path.strip('"')
    base_path = r'C:\Users\giaco\Documents\GitHub\SVE-new-website\testsitecodedbyme'
    # Extract the path starting from the 'static' folder
    relative_path = os.path.relpath(file_path, base_path)
    # Replace backslashes with forward slashes for URL compatibility
    relative_path = relative_path.replace(os.path.sep, '/')
    return relative_path

def txt_to_csv(input_file, output_file):
    # Open the input text file in read mode and read lines from the text file
    with open(input_file, 'r') as txt_file:
        lines = txt_file.readlines()

    # Open the output CSV file in write mode
    with open(output_file, 'w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write header to the CSV file
        csv_writer.writerow(['id', 'name', 'category', 'image_url'])  # Header for the column

        # Write each file name to the CSV file
        for line in lines:
            # Genarate id
            line_id = lines.index(line) + 1
            
            # Extract file name without path and extension
            file_name = os.path.basename(line.strip()).split('.')[0]

            # Get the category based on the file name
            category = get_category(file_name)

            # Get the image URL based on the file path
            image_url = get_image_url(line.strip())
            
            # Write the file name, category and image_url to the CSV file
            csv_writer.writerow([line_id, file_name, category, image_url])

if __name__ == "__main__":
    # Specify the input and output file paths
    input_file_path = 'input.txt'
    output_file_path = 'products.csv'

    # Call the function to convert text to CSV
    txt_to_csv(input_file_path, output_file_path)

    print(f"Conversion completed. CSV file '{output_file_path}' generated.")
