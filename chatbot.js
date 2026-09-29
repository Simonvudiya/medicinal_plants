// Native JavaScript Chatbot for Medicinal Plants of East Africa
// Loads data from JSON files and provides search functionality

(function() {
    let chatData = null;
    let chatHistory = [];

    function loadData() {
        const data = {};
        
        // Load from inline script data if available
        if (window.MEDICINAL_PLANTS_DATA) {
            data.plants = window.MEDICINAL_PLANTS_DATA;
        }
        if (window.DISEASE_DATA) {
            data.diseases = window.DISEASE_DATA;
        }
        if (window.VERNACULAR_DATA) {
            data.vernacular = window.VERNACULAR_DATA;
        }
        if (window.COMPOUNDS_DATA) {
            data.compounds = window.COMPOUNDS_DATA;
        }
        
        return data;
    }

    function searchPlants(query, data) {
        const q = query.toLowerCase().trim();
        const results = [];

        // Search plant species
        if (data.plants) {
            data.plants.forEach(plant => {
                if (plant.toLowerCase().includes(q)) {
                    results.push({ type: 'plant', name: plant });
                }
            });
        }

        // Search diseases
        if (data.diseases) {
            data.diseases.forEach(item => {
                if (item.disease.toLowerCase().includes(q)) {
                    results.push({ type: 'disease', name: item.disease, plants: item.plants });
                }
                item.plants.forEach(plant => {
                    if (plant.toLowerCase().includes(q)) {
                        results.push({ type: 'plant_use', name: plant, treats: item.disease });
                    }
                });
            });
        }

        // Search vernacular names
        if (data.vernacular) {
            data.vernacular.forEach(item => {
                if (item.vernacular_name.toLowerCase().includes(q) ||
                    item.botanical_equivalent.toLowerCase().includes(q) ||
                    item.language_tribe.toLowerCase().includes(q)) {
                    results.push({ type: 'vernacular', name: item.vernacular_name, 
                                   language: item.language_tribe, botanical: item.botanical_equivalent });
                }
            });
        }

        // Search compounds
        if (data.compounds) {
            data.compounds.forEach(c => {
                if ((c.molecularFormula || '').toLowerCase().includes(q) ||
                    (c.species || '').toLowerCase().includes(q) ||
                    (c.family || '').toLowerCase().includes(q)) {
                    results.push({ type: 'compound', formula: c.molecularFormula,
                                   species: c.species, family: c.family, novelty: c.novelty });
                }
            });
        }

        return results.slice(0, 10);
    }

    function formatResults(results, query) {
        if (results.length === 0) {
            return `I couldn't find exact matches for "<strong>${query}</strong>". Try searching by plant name, disease, vernacular name, language, family, or molecular formula.`;
        }

        let html = `Found <strong>${results.length}</strong> result(s) for "<strong>${query}</strong>":\n\n`;
        
        results.forEach(r => {
            switch(r.type) {
                case 'plant':
                    html += `🌱 <strong>${r.name}</strong> - Medicinal plant species\n`;
                    break;
                case 'disease':
                    const plants = r.plants.slice(0, 5).join(', ');
                    html += `🏥 <strong>${r.name}</strong>: Treated with ${plants}${r.plants.length > 5 ? '...' : ''}\n`;
                    break;
                case 'plant_use':
                    html += `🌿 <strong>${r.name}</strong> is used to treat ${r.treats}\n`;
                    break;
                case 'vernacular':
                    html += `🗣️ <strong>${r.name}</strong> (${r.language}) = ${r.botanical}\n`;
                    break;
                case 'compound':
                    html += `🧪 <strong>${r.formula}</strong> (MW: ${r.molecularWeight || 'N/A'}) from ${r.species} [${r.family}] - Novel: ${r.novelty}\n`;
                    break;
            }
        });

        if (results.length === 10) html += `\n...and more results. Try refining your search.`;
        return html;
    }

    // Expose chatbot globally
    window.MedicinalChatbot = {
        search: function(query) {
            if (!chatData) chatData = loadData();
            const results = searchPlants(query, chatData);
            return formatResults(results, query);
        },
        loadData: loadData
    };
})();