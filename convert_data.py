import re
import json

def parse_medicinal_plants(input_filepath, output_filepath):
    # Load the text file
    with open(input_filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the text into lines
    lines = content.split('\n')
    
    # Data structures to hold the parsed information
    disease_data = []
    current_disease = "General Medicinal Plants" # Default heading for the first block
    current_plants = []

    # Regex to identify disease headings (e.g., "1. BILHARZIA", "VIII. FEMALE CONDITIONS")
    heading_pattern = re.compile(r'^([IVXLCDM]+\.\s+|\d+\.\s+)[A-Z].*')
    
    # Lines to completely ignore (page headers, footers, column markers)
    ignore_patterns = [
        r'^\d+\s+Medicinal Plants of East Africa', # Page numbers
        r'^#*\s*Diseases and the Plant Species used for Treatment \d+', # Page footers
        r'^(Left|Right) Column:$', # Column markers
        r'^\d+$' # Standalone numbers
    ]

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines that match ignore patterns
        if any(re.match(pattern, line) for pattern in ignore_patterns):
            continue
            
        # Check if the line is a new disease heading
        if heading_pattern.match(line):
            # If we have accumulated plants for the previous disease, save them
            if current_plants:
                # Clean up duplicates and sort
                unique_plants = sorted(list(set(current_plants)))
                disease_data.append({
                    "disease": current_disease,
                    "plants": unique_plants
                })
            
            # Start a new disease section
            current_disease = line
            current_plants = []
            
        else:
            # It's a plant name. Remove any trailing commas or weird characters
            plant = line.rstrip(',').strip()
            
            # Avoid adding obvious noise or incomplete sentences
            if len(plant) > 2 and not plant.startswith('(') and not plant.startswith('See'):
                current_plants.append(plant)

    # Don't forget to save the very last section!
    if current_plants:
        unique_plants = sorted(list(set(current_plants)))
        disease_data.append({
            "disease": current_disease,
            "plants": unique_plants
        })

    # Save the final structured data to a JSON file
    with open(output_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(disease_data, json_file, indent=4)
        
    print(f"Success! Data converted and saved to {output_filepath}")
    print(f"Total diseases/conditions processed: {len(disease_data)}")

# Run the script
if __name__ == "__main__":
    # Make sure to change the filename if yours is slightly different
    input_txt = "Croton megalocarpus.txt" 
    output_json = "data.json"
    
    parse_medicinal_plants(input_txt, output_json)