import streamlit as st

# Function to calculate brewhouse efficiency
def calculate_brewhouse_efficiency(grain_weight_kg, wort_volume_liters, original_gravity):
    max_potential_gravity = 1.080  # Example value; you may change this based on your grain bill
    max_potential_points = (max_potential_gravity - 1) * 1000

    actual_points = (original_gravity - 1) * 1000
    potential_yield = grain_weight_kg * max_potential_points * 1000  # converting kg to grams

    efficiency = (actual_points * wort_volume_liters) / potential_yield
    return efficiency * 100  # Convert to percentage

# Function to calculate yeast pitching rate
def calculate_yeast_pitching_rate(volume_liters, original_gravity, pitching_rate):
    degrees_plato = (original_gravity - 1) * 1000 / 4
    yeast_cells_needed = volume_liters * degrees_plato * pitching_rate
    yeast_cells_needed_billions = yeast_cells_needed / 1e9
    return yeast_cells_needed_billions

# Function to calculate extract yield and extract efficiency using SG method
def calculate_extract_yield_efficiency_SG(grain_weight_kg, wort_volume_liters, original_gravity, extract_per_kg):
    # Convert hectoliters to liters
    wort_volume_liters = wort_volume_liters * 100
    
    # Calculate potential available extract
    potential_available_extract = grain_weight_kg * extract_per_kg
    
    # Actual extract achieved
    actual_extract_achieved = wort_volume_liters * (original_gravity - 1) * 1000
    
    # Extract yield
    extract_yield = actual_extract_achieved / grain_weight_kg
    
    # Extract efficiency
    extract_efficiency = (actual_extract_achieved / potential_available_extract) * 100
    
    return extract_yield, extract_efficiency

# Function to calculate the grain weight needed for a brew
def calculate_grain_weight(wort_volume_liters, target_original_gravity, extract_efficiency):
    # Calculate the total extract needed in litre degrees
    total_extract_needed = wort_volume_liters * (target_original_gravity - 1) * 1000
    
    # Calculate the grain weight required
    grain_weight = total_extract_needed / (extract_efficiency / 100 * 300)
    
    return grain_weight

# Function to calculate hops utilization
def calculate_hops_utilization(alpha_acids, hop_weight_g, boil_time, wort_volume_liters):
    # Utilization factor based on boil time (simplified model)
    utilization_factor = 0.1 + (boil_time / 60) * 0.15
    ibu = (alpha_acids * hop_weight_g * utilization_factor * 1000) / wort_volume_liters
    return ibu

st.title('Brewing Calculators')

# Custom CSS to add a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1457382713369-161d1d986f54?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# About Section
st.sidebar.title('About Me')
st.sidebar.image("https://media.licdn.com/dms/image/C4D03AQFHBrqSoctkhg/profile-displayphoto-shrink_800_800/0/1657162810861?e=1693440000&v=beta&t=usR9Ti1AWTjv9O7GVnH9Q_eL8vZhM7ydkS1X9qlmLl8")  # Replace with your own image URL
st.sidebar.markdown("""
## Ankur Napa

I'm Ankur Napa, a professional with extensive experience in the brewing industry, specializing in AI, ML, and data analytics solutions for breweries. I have worked with several renowned breweries, including Kingfisher, Budweiser, Carlsberg, and SABMiller. I hold a Master of Science in Data Science from Liverpool John Moores University and a PG Diploma in Business Analytics from IIIT Bengaluru. I am passionate about leveraging technology to optimize brewing processes and improve product quality.

[LinkedIn Profile](https://www.linkedin.com/in/ankur-napa/)
""")

# Create tiles for different calculators
tile = st.selectbox("Choose a calculator:", ["Brewhouse Efficiency", "Yeast Pitching Rate", "Extract Yield and Efficiency", "Grain Weight", "Hops Utilization"])

if tile == 'Brewhouse Efficiency':
    st.header('Brewhouse Efficiency Calculator (Metric)')
    
    # Input fields for brewhouse efficiency
    grain_weight_kg = st.number_input('Enter grain weight (in kilograms)', min_value=0.0, format="%.2f")
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")

    if st.button('Calculate Brewhouse Efficiency'):
        if grain_weight_kg > 0 and wort_volume_liters > 0 and original_gravity > 1.000:
            efficiency = calculate_brewhouse_efficiency(grain_weight_kg, wort_volume_liters, original_gravity)
            st.success(f'Brewhouse Efficiency: {efficiency:.2f}%')
        else:
            st.error('Please enter valid input values')

elif tile == 'Yeast Pitching Rate':
    st.header('Yeast Pitching Rate Calculator')
    
    # Input fields for yeast pitching rate
    volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")
    pitching_rate = st.number_input('Enter desired pitching rate (cells/mL/°P)', min_value=0.0, format="%.2f", value=0.75)

    if st.button('Calculate Yeast Pitching Rate'):
        if volume_liters > 0 and original_gravity > 1.000 and pitching_rate > 0:
            yeast_cells_needed = calculate_yeast_pitching_rate(volume_liters, original_gravity, pitching_rate)
            st.success(f'Yeast Cells Needed: {yeast_cells_needed:.2f} billion cells')
        else:
            st.error('Please enter valid input values')

elif tile == 'Extract Yield and Efficiency':
    st.header('Extract Yield and Efficiency Calculator (SG Method)')
    
    # Input fields for extract yield and efficiency
    grain_weight_kg = st.number_input('Enter grain weight (in kilograms)', min_value=0.0, format="%.2f")
    wort_volume_hl = st.number_input('Enter wort volume (in hectoliters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")
    extract_per_kg = st.number_input('Enter extract per kg of malt (in litre degrees per kg)', min_value=0.0, format="%.2f", value=300.0)

    if st.button('Calculate Extract Yield and Efficiency'):
        if grain_weight_kg > 0 and wort_volume_hl > 0 and original_gravity > 1.000:
            extract_yield, extract_efficiency = calculate_extract_yield_efficiency_SG(grain_weight_kg, wort_volume_hl, original_gravity, extract_per_kg)
            st.success(f'Extract Yield: {extract_yield:.2f} litre degrees per kg')
            st.success(f'Extract Efficiency: {extract_efficiency:.2f}%')
        else:
            st.error('Please enter valid input values')

elif tile == 'Grain Weight':
    st.header('Grain Weight Calculator')
    
    # Input fields for grain weight calculation
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    target_original_gravity = st.number_input('Enter target original gravity', min_value=1.000, format="%.3f")
    extract_efficiency = st.number_input('Enter extract efficiency (in percentage)', min_value=0.0, max_value=100.0, format="%.2f", value=75.0)

    if st.button('Calculate Grain Weight'):
        if wort_volume_liters > 0 and target_original_gravity > 1.000 and extract_efficiency > 0:
            grain_weight = calculate_grain_weight(wort_volume_liters, target_original_gravity, extract_efficiency)
            st.success(f'Grain Weight Needed: {grain_weight:.2f} kg')
        else:
            st.error('Please enter valid input values')

elif tile == 'Hops Utilization':
    st.header('Hops Utilization Calculator')
    
    # Input fields for hops utilization
    alpha_acids = st.number_input('Enter alpha acids percentage', min_value=0.0, max_value=100.0, format="%.2f")
    hop_weight_g = st.number_input('Enter hop weight (in grams)', min_value=0.0, format="%.2f")
    boil_time = st.number_input('Enter boil time (in minutes)', min_value=0, format="%d")
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")

    if st.button('Calculate Hops Utilization'):
        if alpha_acids > 0 and hop_weight_g > 0 and boil_time > 0 and wort_volume_liters > 0:
            ibu = calculate_hops_utilization(alpha_acids, hop_weight_g, boil_time, wort_volume_liters)
            st.success(f'IBU: {ibu:.2f}')
        else:
            st.error('Please enter valid input values')
