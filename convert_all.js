const XLSX = require('xlsx');
const fs = require('fs');

// 1. Convert medicinal_plant.xlsx -> medicinal_plant.json
function convertMedicinalPlant() {
    const wb = XLSX.readFile('medicinal_plant.xlsx');
    const ws = wb.Sheets[wb.SheetNames[0]];
    const data = XLSX.utils.sheet_to_json(ws, { header: 1 });

    // First row is header "Botanical name"
    const plants = [];
    for (let i = 1; i < data.length; i++) {
        const row = data[i];
        if (row && row[0]) {
            const name = String(row[0]).trim();
            if (name && name !== 'Botanical name') {
                plants.push(name);
            }
        }
    }

    fs.writeFileSync('medicinal_plant.json', JSON.stringify(plants, null, 2));
    console.log(`medicinal_plant.json: ${plants.length} plants`);
}

// 2. Convert condition_medicinal_plants.xlsx -> disease_plants.json
function convertConditionData() {
    const wb = XLSX.readFile('condition_medicinal_plants.xlsx');
    const ws = wb.Sheets[wb.SheetNames[0]];
    const data = XLSX.utils.sheet_to_json(ws, { header: 1 });

    const structured = [];
    for (let i = 1; i < data.length; i++) {
        const row = data[i];
        if (!row || row.length < 2) continue;

        const disease = String(row[0]).trim();
        const plantsString = String(row[1]).trim();

        if (!disease || disease === 'Disease / Condition') continue;

        // Split plants by comma
        const plants = plantsString.split(',').map(p => p.trim()).filter(p => p);
        // Remove duplicates and sort
        const uniquePlants = [...new Set(plants)].sort((a, b) => a.localeCompare(b));

        structured.push({ disease, plants: uniquePlants });
    }

    fs.writeFileSync('disease_plants.json', JSON.stringify(structured, null, 2));
    console.log(`disease_plants.json: ${structured.length} conditions`);
}

// 3. Convert vernacular_botanical_name.xlsx -> vernacular_data.json
function convertVernacularData() {
    const wb = XLSX.readFile('vernacular_botanical_name.xlsx');
    const ws = wb.Sheets[wb.SheetNames[0]];
    const data = XLSX.utils.sheet_to_json(ws, { header: 1 });

    const structured = [];
    for (let i = 1; i < data.length; i++) {
        const row = data[i];
        if (!row || row.length < 3) continue;

        const vernacular = String(row[0]).trim();
        const language = String(row[1]).trim();
        const botanical = String(row[2]).trim();

        if (!vernacular || vernacular === 'Vernacular name') continue;

        structured.push({
            vernacular_name: vernacular,
            language_tribe: language,
            botanical_equivalent: botanical
        });
    }

    fs.writeFileSync('vernacular_data.json', JSON.stringify(structured, null, 2));
    console.log(`vernacular_data.json: ${structured.length} entries`);
}

// Run all conversions
convertMedicinalPlant();
convertConditionData();
convertVernacularData();
console.log('All conversions complete!');