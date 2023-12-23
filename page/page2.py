import streamlit as st
import requests
import folium
from pyproj import Proj, transform
import warnings
from streamlit_folium import folium_static

# Suppress FutureWarnings from pyproj
warnings.filterwarnings("ignore", category=FutureWarning)

st.markdown(
    """
    <style>
    .main {
       background-color: #f0f2f6;
    }
    .stRadio > div{flex-direction:row;}
    input[type="text"] {
        border: 2px solid #0a8fdb;  /* Blue border */
        border-radius: 5px;         /* Rounded border edges */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def utm_to_latlon(x, y):
    in_proj = Proj(init='epsg:2154')  
    out_proj = Proj(init='epsg:4326')  
    lon, lat = transform(in_proj, out_proj, x, y)
    return lat, lon


def search_address(query):
    base_url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": query}
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None


# Function to display map
def display_map(latitude, longitude):
    map_address = folium.Map(location=[latitude, longitude], zoom_start=16, tiles=None)


    # Adding tile layers
    folium.TileLayer('openstreetmap').add_to(map_address)
    # folium.TileLayer('Stamen Terrain').add_to(map_address)
    # folium.TileLayer('Stamen Toner').add_to(map_address)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite',
        overlay= False,
        control=True
    ).add_to(map_address)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri WorldStreetMap',
        overlay=False,
        control=True
    ).add_to(map_address)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri TopoWorld',
        overlay=False,
        control=True
    ).add_to(map_address)
    folium.TileLayer(
        tiles='https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png',
        attr='Wikimedia',
        name='Wikimedia Map',
        overlay=False
    ).add_to(map_address)
    folium.TileLayer('CartoDB Positron').add_to(map_address)
    folium.TileLayer('CartoDB Dark_Matter').add_to(map_address)

    # Adding OpenTopoMap
    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='OpenTopoMap',
        overlay=False,
        control=True
    ).add_to(map_address)

    folium.CircleMarker(
        location=[latitude, longitude],
        radius=15,  # Size of the circle marker
        color='red',  # Border color of the marker
        fill=True,
        fill_color=None,  # Fill color of the marker
        weight=1  # Thickness of the border
    ).add_to(map_address)

    # Add layer control to switch between layers
    folium.LayerControl().add_to(map_address)

    folium_static(map_address)
    
def display_address_details(data):
    # French translations for the fields
    translations = {
        'score': 'Score de similarité',
        'id': 'Identifiant',
        'name': 'Nom',
        'postcode': 'Code postal',
        'citycode': 'Code de ville',
        'city': 'Ville',
        'context': 'Contexte',
        'type': 'Type',
        'importance': 'Importance',
        'street': 'Rue'
        # Note: 'x' and 'y' are handled separately
    }

    # Convert UTM to geographical coordinates
    if 'x' in data and 'y' in data:
        lat, lon = utm_to_latlon(float(data['x']), float(data['y']))
        data['latitude'] = lat  # Changed to 'latitude'
        data['longitude'] = lon # Changed to 'longitude'

    with st.expander("Détails de l'Adresse"):  # Accordion/Expander
        col1, col2 = st.columns(2)
        for key, value in data.items():
            if key.lower() in ['x', 'y']:
                continue  # Skip raw UTM coordinates

            translated_key = translations.get(key.lower(), key.capitalize())
            col1.markdown(f"<p style='margin-bottom:1px;'>{translated_key}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='margin-bottom:1px;'>{value}</p>", unsafe_allow_html=True)


# Streamlit user interface
st.title("Localisateur d'Adresse")
st.markdown("Entrez une adresse pour voir sa localisation sur une carte et obtenir des détails supplémentaires.")

# Layout adjustments
col1, col2 = st.columns([1, 2])

with col1:
    address_query = st.text_input("Entrez l'adresse:", placeholder="4 Place du Louvre, 75001 Paris")
    if address_query:
        with st.spinner('Recherche de l\'adresse...'):
            result = search_address(address_query)
        if result and result['features']:
            addresses = [feature['properties']['label'] for feature in result['features']]
            data = {feature['properties']['label']: feature['properties'] for feature in result['features']}
            selected_address = st.radio("Sélectionnez une adresse", addresses)
        else:
            st.error("Aucun résultat trouvé pour l'adresse donnée.")
    else:
        st.info("Veuillez entrer une adresse pour la recherche.")

with col2:

    if address_query and result and result['features']:
        selected_data = data[selected_address]
        latitude, longitude = utm_to_latlon(selected_data['x'], selected_data['y'])
        display_map(latitude, longitude)
        display_address_details(selected_data)
