import json

def convert_vernacular_to_json(input_filepath, output_filepath):
    # Create an empty list to hold our structured data
    structured_data = []
    
    # Read the text file
    with open(input_filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip the header row
        if line.startswith("Vernacular name"):
            continue
            
        # Split the line into parts by the Tab character
        parts = line.split('\t')
        
        # We expect exactly 3 parts: Vernacular, Language, Botanical
        if len(parts) >= 3:
            vernacular = parts[0].strip()
            language = parts[1].strip()
            botanical = parts[2].strip()
            
            # Add to our structured data list
            structured_data.append({
                "vernacular_name": vernacular,
                "language_tribe": language,
                "botanical_equivalent": botanical
            })
        elif len(parts) == 2:
            # Fallback for lines that might only have 2 columns
            vernacular = parts[0].strip()
            language = parts[1].strip()
            structured_data.append({
                "vernacular_name": vernacular,
                "language_tribe": language,
                "botanical_equivalent": ""
            })

    # Save the structured data to a JSON file
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, indent=4)
        
    print(f"Success! Converted {len(structured_data)} entries to {output_filepath}")

# Run the conversion
if __name__ == "__main__":
    # Change this to match the exact name of your text file
    input_txt = "vernacular_data.txt" 
    output_json = "vernacular_data.json"
    
    convert_vernacular_to_json(input_txt, output_json)