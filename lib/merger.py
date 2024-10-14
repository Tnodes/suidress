import json
import os

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_sui_addresses(data):
    return [wallet['sui_address'] for wallet in data.values()]

def merge_sui_addresses(path):
    merged_addresses = []
    
    if os.path.isfile(path):
        # If the path is a file, process only that file
        data = load_json_file(path)
        merged_addresses.extend(extract_sui_addresses(data))
    elif os.path.isdir(path):
        # If the path is a directory, process all JSON files in it
        json_files = [f for f in os.listdir(path) if f.endswith('.json')]
        for file_name in json_files:
            file_path = os.path.join(path, file_name)
            data = load_json_file(file_path)
            merged_addresses.extend(extract_sui_addresses(data))
    else:
        raise ValueError(f"Invalid path: {path}")
    
    return merged_addresses

def merge_addresses():
    path = input("Enter the directory containing JSON files or a specific JSON file: ")
    
    # If the user didn't specify .json, add it
    if not path.lower().endswith('.json') and not os.path.isdir(path):
        path += '.json'
    
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return None
    
    try:
        merged_addresses = merge_sui_addresses(path)
        print(f"Total addresses merged: {len(merged_addresses)}")
        return merged_addresses
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    merge_addresses()
