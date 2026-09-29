import streamlit as st
import json
import os

# Page config
st.set_page_config(
    page_title="Medicinal Plants Chatbot",
    page_icon="🌿",
    layout="wide"
)

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

# Custom CSS
st.markdown("""
    <style>
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌿 Medicinal Plants of East Africa - Chatbot")
st.markdown("Ask me about medicinal plants, their uses, compounds, or diseases!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm the Medicinal Plants Chatbot. I can help you find information about East African medicinal plants, their traditional uses, chemical compounds, and more. What would you like to know?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about a plant, disease, compound, or use..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching plant database..."):
            response = search_plants(prompt, data)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

def search_plants(query, data):
    """Search across all datasets and return relevant information."""
    query_lower = query.lower()
    results = []
    
    # Search medicinal plant list
    if 'medicinal_plant.json' in data:
        for plant in data['medicinal_plant.json']:
            if query_lower in plant.lower():
                results.append(f"🌱 **{plant}** - Found in medicinal plant database")
    
    # Search disease data
    if 'disease_plants.json' in data:
        for item in data['disease_plants.json']:
            if query_lower in item['disease'].lower():
                plants = ', '.join(item['plants'][:5])
                results.append(f"🏥 **{item['disease']}**: Treated with {plants}{'...' if len(item['plants']) > 5 else ''}")
            for plant in item['plants']:
                if query_lower in plant.lower():
                    results.append(f"🌿 {plant} is used to treat {item['disease']}")
    
    # Search vernacular names
    if 'vernacular_data.json' in data:
        for item in data['vernacular_data.json']:
            if (query_lower in item['vernacular_name'].lower() or 
                query_lower in item['botanical_equivalent'].lower() or
                query_lower in item['language_tribe'].lower()):
                results.append(f"🗣️ {item['vernacular_name']} ({item['language_tribe']}) = {item['botanical_equivalent']}")
    
    # Search compounds
    if 'present_compounds.txt' in data:
        compounds = data['present_compounds.txt'].get('compounds', [])
        for c in compounds:
            if (query_lower in c.get('molecularFormula', '').lower() or
                query_lower in c.get('family', '').lower() or
                query_lower in c.get('species', '').lower()):
                results.append(f"🧪 {c.get('molecularFormula')} (MW: {c.get('molecularWeight')}) from {c.get('species']} [{c.get('family')}] - Novel: {c.get('novelty')}")
    
    if not results:
        return ("I couldn't find exact matches for your query. Try searching by plant name, "
                "disease, vernacular name, language, family, or molecular formula. "
                "For example: 'Croton megalocarpus', 'diabetes', 'Luo', 'Rutaceae', or 'C18H32O4'")
    
    # Deduplicate and limit
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