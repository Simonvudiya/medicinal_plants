import json

def convert_tsv_to_json(input_filepath, output_filepath):
    # Create an empty list to hold our structured data
    structured_data = []
    
    # Read the text file
    with open(input_filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Lines to completely ignore (page numbers, headers, column markers)
    ignore_phrases = [
        "Medicinal Plants of East Africa",
        "Diseases and the Plant Species used for Treatment",
        "Disease / Condition",
        "Left Column:",
        "Right Column:"
    ]

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines containing ignore phrases
        if any(phrase in line for phrase in ignore_phrases):
            continue

        # Split the line into two parts by the Tab character
        parts = line.split('\t', 1) 
        
        # Check if the line actually has a tab (Disease \t Plants)
        if len(parts) == 2:
            disease = parts[0].strip()
            plants_string = parts[1].strip()
            
            # Split the plants by comma
            plants_list = [plant.strip() for plant in plants_string.split(',')]
            
            # Clean up any empty strings or trailing periods
            plants_list = [plant.rstrip('.').strip() for plant in plants_list if plant.strip()]
            
            # Remove duplicates and sort alphabetically
            unique_plants = sorted(list(set(plants_list)))
            
            # Add to our structured data list
            structured_data.append({
                "disease": disease,
                "plants": unique_plants
            })

    # Save the structured data to a JSON file
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, indent=4)
        
    print(f"Success! Converted {len(structured_data)} conditions to {output_filepath}")

# Run the conversion
if __name__ == "__main__":
    # Make sure the input filename matches exactly what you have
    input_txt = "4. DISEASES OF THE EARAcacia brevispica, Acalypha.txt" 
    output_json = "data.json"
    
    convert_tsv_to_json(input_txt, output_json)