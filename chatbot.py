import streamlit as st
import json
import os

# Prevent redirect loop - critical for iframe embedding
st.markdown("""
    <meta http-equiv="Content-Security-Policy" content="frame-ancestors *">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
        // Prevent Streamlit's automatic redirect loop
        if (window.top !== window) {
            // We are in an iframe - prevent redirects
            const originalReplace = window.location.replace;
            window.location.replace = function(url) {
                if (url && url.indexOf('streamlit') !== -1) {
                    return;
                }
                return originalReplace.call(this, url);
            };
        }
    </script>
    <style>
        .stApp { margin: 0; padding: 0; }
        header[data-testid="stHeader"] { display: none; }
        .stDeployButton { display: none; }
        div[data-testid="stStatusWidget"] { display: none; }
        .block-container { padding-top: 0 !important; }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    data = {}
    for fname in ['medicinal_plant.json', 'disease_plants.json', 'vernacular_data.json', 'present_compounds.txt']:
        if os.path.exists(fname):
            with open(fname, 'r', encoding='utf-8') as f:
                data[fname] = json.load(f)
    return data

data = load_data()

# Title (compact for iframe)
st.title("🌿 Medicinal Plants Chatbot")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I can help you find information about East African medicinal plants, their traditional uses, chemical compounds, and more. What would you like to know?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about a plant, disease, compound, or use..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            response = search_plants(prompt, data)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

def search_plants(query, data):
    """Search across all datasets and return relevant information."""
    query_lower = query.lower()
    results = []
    
    if 'medicinal_plant.json' in data:
        for plant in data['medicinal_plant.json']:
            if query_lower in plant.lower():
                results.append(f"🌱 **{plant}** - Found in medicinal plant database")
    
    if 'disease_plants.json' in data:
        for item in data['disease_plants.json']:
            if query_lower in item['disease'].lower():
                plants = ', '.join(item['plants'][:5])
                results.append(f"🏥 **{item['disease']}**: Treated with {plants}{'...' if len(item['plants']) > 5 else ''}")
            for plant in item['plants']:
                if query_lower in plant.lower():
                    results.append(f"🌿 {plant} is used to treat {item['disease']}")
    
    if 'vernacular_data.json' in data:
        for item in data['vernacular_data.json']:
            if (query_lower in item['vernacular_name'].lower() or 
                query_lower in item['botanical_equivalent'].lower() or
                query_lower in item['language_tribe'].lower()):
                results.append(f"🗣️ {item['vernacular_name']} ({item['language_tribe']}) = {item['botanical_equivalent']}")
    
    if 'present_compounds.txt' in data:
        compounds = data['present_compounds.txt'].get('compounds', [])
        for c in compounds:
            if (query_lower in c.get('molecularFormula', '').lower() or
                query_lower in c.get('family', '').lower() or
                query_lower in c.get('species', '').lower()):
                results.append(f"🧪 {c.get('molecularFormula')} (MW: {c.get('molecularWeight')}) from {c.get('species')} [{c.get('family')}] - Novel: {c.get('novelty')}")
    
    if not results:
        return ("I couldn't find exact matches. Try searching by plant name, disease, "
                "vernacular name, language, family, or molecular formula. "
                "Examples: 'Croton megalocarpus', 'diabetes', 'Luo', 'Rutaceae', or 'C18H32O4'")
    
    unique_results = list(dict.fromkeys(results))[:10]
    
    response = f"Found {len(unique_results)} result(s) for '{query}':\n\n"
    response += "\n\n".join(unique_results)
    
    if len(unique_results) == 10:
        response += "\n\n...and more results available. Try refining your search."
    
    return response

# Sidebar with stats
with st.sidebar:
    st.header("📊 Database Stats")
    if 'medicinal_plant.json' in data:
        st.metric("Plant Species", len(data['medicinal_plant.json']))
    if 'disease_plants.json' in data:
        st.metric("Disease Conditions", len(data['disease_plants.json']))
    if 'vernacular_data.json' in data:
        st.metric("Vernacular Names", len(data['vernacular_data.json']))
    if 'present_compounds.txt' in data:
        st.metric("Chemical Compounds", len(data['present_compounds.txt'].get('compounds', [])))
    
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    examples = [
        "Croton megalocarpus",
        "diabetes",
        "Luo language",
        "Rutaceae family",
        "C18H32O4",
        "Acokanthera schimperi"
    ]
    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state.messages.append({"role": "user", "content": ex})
            st.rerun()