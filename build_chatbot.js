const fs = require('fs');

// Load all data
const medicinalPlants = JSON.parse(fs.readFileSync('medicinal_plant.json', 'utf8'));
const diseaseData = JSON.parse(fs.readFileSync('disease_plants.json', 'utf8'));
const vernacularData = JSON.parse(fs.readFileSync('vernacular_data.json', 'utf8'));
const compoundsData = JSON.parse(fs.readFileSync('present_compounds.txt', 'utf8'));

// Generate chatbot.js with embedded data
const chatbotJS = `// Medicinal Plants Chatbot - Native JavaScript
// Auto-generated with embedded data

const MEDICINAL_PLANTS_DATA = ${JSON.stringify(medicinalPlants)};
const DISEASE_DATA = ${JSON.stringify(diseaseData)};
const VERNACULAR_DATA = ${JSON.stringify(vernacularData)};
const COMPOUNDS_DATA = ${JSON.stringify(compoundsData.compounds)};

function chatbotSearch(query) {
    const q = query.toLowerCase().trim();
    const results = [];

    // Search plant species
    MEDICINAL_PLANTS_DATA.forEach(plant => {
        if (plant.toLowerCase().includes(q)) {
            results.push({ type: 'plant', name: plant });
        }
    });

    // Search diseases
    DISEASE_DATA.forEach(item => {
        if (item.disease.toLowerCase().includes(q)) {
            results.push({ type: 'disease', name: item.disease, plants: item.plants });
        }
        item.plants.forEach(plant => {
            if (plant.toLowerCase().includes(q)) {
                results.push({ type: 'plant_use', name: plant, treats: item.disease });
            }
        });
    });

    // Search vernacular names
    VERNACULAR_DATA.forEach(item => {
        if (item.vernacular_name.toLowerCase().includes(q) ||
            item.botanical_equivalent.toLowerCase().includes(q) ||
            item.language_tribe.toLowerCase().includes(q)) {
            results.push({ type: 'vernacular', name: item.vernacular_name,
                           language: item.language_tribe, botanical: item.botanical_equivalent });
        }
    });

    // Search compounds
    COMPOUNDS_DATA.forEach(c => {
        if ((c.molecularFormula || '').toLowerCase().includes(q) ||
            (c.species || '').toLowerCase().includes(q) ||
            (c.family || '').toLowerCase().includes(q)) {
            results.push({ type: 'compound', formula: c.molecularFormula,
                           species: c.species, family: c.family, novelty: c.novelty,
                           molecularWeight: c.molecularWeight });
        }
    });

    return results.slice(0, 10);
}

function chatbotFormat(results, query) {
    if (results.length === 0) {
        return 'I couldn\\'t find exact matches for "' + query + '". Try searching by plant name, disease, vernacular name, language, family, or molecular formula.';
    }

    let html = 'Found <strong>' + results.length + '</strong> result(s) for "<strong>' + query + '</strong>":\\n\\n';
    
    results.forEach(r => {
        switch(r.type) {
            case 'plant':
                html += '🌱 <strong>' + r.name + '</strong> - Medicinal plant species\\n';
                break;
            case 'disease':
                const plants = r.plants.slice(0, 5).join(', ');
                html += '🏥 <strong>' + r.name + '</strong>: Treated with ' + plants + (r.plants.length > 5 ? '...' : '') + '\\n';
                break;
            case 'plant_use':
                html += '🌿 <strong>' + r.name + '</strong> is used to treat ' + r.treats + '\\n';
                break;
            case 'vernacular':
                html += '🗣️ <strong>' + r.name + '</strong> (' + r.language + ') = ' + r.botanical + '\\n';
                break;
            case 'compound':
                html += '🧪 <strong>' + r.formula + '</strong> (MW: ' + (r.molecularWeight || 'N/A') + ') from ' + r.species + ' [' + r.family + '] - Novel: ' + r.novelty + '\\n';
                break;
        }
    });

    if (results.length === 10) html += '\\n...and more results. Try refining your search.';
    return html;
}
`;

fs.writeFileSync('chatbot_data.js', chatbotJS);
console.log('Created chatbot_data.js with embedded data');