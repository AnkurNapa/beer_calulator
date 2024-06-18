import math
import streamlit as st

# Placeholder functions for the missing acan module
def sg_to_plato(sg):
    return (sg - 1) * 1000 / 4  # Simplified conversion

def plato_to_sg(plato):
    return 1 + (plato * 4) / 1000  # Simplified conversion

def brix_to_sg(brix):
    return 1 + (brix / (258.6 - ((brix / 258.2) * 227.1)))  # Simplified conversion

def sg_to_gu(sg):
    return (sg - 1) * 1000  # Gravity units

def litre_to_gallon(liters):
    return liters * 0.264172  # Convert liters to gallons

def gram_to_pound(grams):
    return grams * 0.00220462  # Convert grams to pounds

def gram_to_ounce(grams):
    return grams * 0.035274  # Convert grams to ounces

# Wort class
class Wort:
    def __init__(self, original, final, unit='sg', grains=None, volume=None):
        if unit == 'sg':
            self.og = original
            self.fg = final
            self.oe = sg_to_plato(self.og)
            self.ae = sg_to_plato(self.fg)
        elif unit == 'plato':
            self.oe = original
            self.ae = final
            self.og = plato_to_sg(self.oe)
            self.fg = plato_to_sg(self.ae)
        elif unit == 'brix':
            self.og = brix_to_sg(original)
            self.fg = brix_to_sg(final)
            self.oe = sg_to_plato(self.og)
            self.ae = sg_to_plato(self.fg)
        else:
            raise ValueError('unit must be sg, plato, or brix')

        if grains:
            if volume:
                self.volume = float(volume)
                total_weight = sum(grain[0] for grain in grains)
                gallons = litre_to_gallon(self.volume)
                self.points_pound_gallon = (gallons * sg_to_gu(self.og) / gram_to_pound(total_weight))
                self.mash_efficiency = sg_to_gu(self.og) / sum(g[1] * gram_to_pound(g[0]) / gallons for g in grains) * 100
            else:
                raise ValueError('wort\'s volume must be informed')
        else:
            self.points_pound_gallon = self.volume = -1.0
            self.brewhouse_efficiency = self.mash_efficiency = self.volume

        self.real_extract = (0.1808 * self.oe) + (0.8192 * self.ae)
        self.apparent_attenuation = (self.og - self.fg) / (self.og - 1) * 100
        self.real_attenuation = ((self.oe - self.real_extract) / (self.oe - 1) * 100)
        self.alcohol_by_volume = ((self.og - self.fg) / 0.75) * 100
        self.alcohol_by_weight = (((0.79 * (self.alcohol_by_volume / 100)) / self.fg) * 100)
        self.calories = (((6.9 * self.alcohol_by_weight) + (4 * (self.real_extract - 0.1))) * self.fg * 3.55)

    def __str__(self):
        return 'Original gravity.....[SG]: {0:7.3f}\n'\
            'Final gravity........[SG]: {1:7.3f}\n'\
            'Original extract..[Plato]: {2:7.3f}\n'\
            'Apparent extract..[Plato]: {3:7.3f}\n'\
            'Real extract......[Plato]: {4:7.3f}\n'\
            'Volume................[L]: {5:7.3f}\n'\
            'Points/Pound/Gallon.[PPG]: {6:7.3f}\n'\
            'Mash efficiency.......[%]: {7:7.3f}\n'\
            'Apparent attenuation..[%]: {8:7.3f}\n'\
            'Real attenuation......[%]: {9:7.3f}\n'\
            'Alcohol by weight.....[%]: {10:7.3f}\n'\
            'Alcohol by volume.....[%]: {11:7.3f}\n'\
            'Calories in 355 mL..[Cal]: {12:7.3f}\n'.format(self.og, self.fg,
            self.oe, self.ae, self.real_extract, self.volume,
            self.points_pound_gallon, self.mash_efficiency,
            self.apparent_attenuation, self.real_attenuation,
            self.alcohol_by_weight, self.alcohol_by_volume, self.calories)

# Hops class
class Hops:
    def __init__(self, w, a, v, sg, t):
        self.hops_weight = w
        self.hops_alpha = a
        self.wort_volume = v
        self.wort_sg = sg
        self.hops_boil_time = t
        self.wort_bitterness = self.tinseth(self.hops_weight, self.hops_alpha, self.wort_volume, self.wort_sg, self.hops_boil_time)

    def tinseth(self, w, a, v, sg, t):
        return ((1.65 * 0.000125 ** (sg - 1)) * ((1 - math.e ** (-0.04 * t)) / 4.15) * ((a / 100) * w * 1000 / v))

    def __str__(self):
        return 'Hops weight.......[g]: {0:6.2f}\n'\
            'Hops alpha acids..[%]: {1:6.2f}\n'\
            'Wort volume.......[L]: {2:6.2f}\n'\
            'Wort SG...........[L]: {3:7.3f}\n'\
            'Hops boil time....[m]: {4:3.0f}\n'\
            'Wort bitterness.[IBU]: {5:7.3f}'.format(self.hops_weight,
            self.hops_alpha, self.wort_volume, self.wort_sg,
            self.hops_boil_time, self.wort_bitterness)

# Custom CSS to add a background image and style buttons
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1457382713369-161d1d986f54?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
        background-size: cover;
        color: white;
    }
    .sidebar-content {
        background-color: #000;
    }
    .sidebar .sidebar-content {
        background-color: #000;
        color: white;
    }
    .stButton>button {
        background-color: #444;
        color: white;
        border: 1px solid #888;
        border-radius: 5px;
        padding: 10px 20px;
        margin: 5px;
    }
    .stButton>button:hover {
        background-color: #888;
        color: black;
        border: 1px solid #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('🍺 Brewing Calculators')

# About Section
st.sidebar.title('About Me')
st.sidebar.image("https://media.licdn.com/dms/image/C5603AQGcCco8w8XjOA/profile-displayphoto-shrink_400_400/0/1600255517459?e=1724284800&v=beta&t=ssZTKMh1D9GJ_tvB6ED_cAdk3cuKQ1eRCxAais2s-WE", use_column_width=True, caption="Ankur Napa")  # Your provided image URL
st.sidebar.markdown("""
## Ankur Napa

I'm Ankur Napa, a professional with extensive experience in the brewing industry, specializing in AI, ML, and data analytics solutions for breweries. I have worked with several renowned breweries, including Kingfisher, Budweiser, Carlsberg, and SABMiller. I hold a Master of Science in Data Science from Liverpool John Moores University and a PG Diploma in Business Analytics from IIIT Bengaluru. I am passionate about leveraging technology to optimize brewing processes and improve product quality.

[LinkedIn Profile](https://www.linkedin.com/in/ankur-napa/)
""")

# Create buttons for different calculators
st.write("## Choose a Calculator")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button('Brewhouse Efficiency 🔧'):
        tile = 'Brewhouse Efficiency'
with col2:
    if st.button('Yeast Pitching Rate 🍶'):
        tile = 'Yeast Pitching Rate'
with col3:
    if st.button('Extract Yield and Efficiency 🧮'):
        tile = 'Extract Yield and Efficiency'
with col4:
    if st.button('Grain Weight ⚖️'):
        tile = 'Grain Weight'
with col5:
    if st.button('Hops Utilization 🌿'):
        tile = 'Hops Utilization'

# Initialize tile if not set
if 'tile' not in locals():
    tile = 'Brewhouse Efficiency'

if tile == 'Brewhouse Efficiency':
    st.header('Brewhouse Efficiency Calculator (Metric) 🔧')
    
    # Input fields for brewhouse efficiency
    grain_weight_kg = st.number_input('Enter grain weight (in kilograms)', min_value=0.0, format="%.2f")
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")

    if st.button('Calculate Brewhouse Efficiency'):
        if grain_weight_kg > 0 and wort_volume_liters > 0 and original_gravity > 1.000:
            wort = Wort(original_gravity, 1.000, unit='sg', grains=[(grain_weight_kg, 36)], volume=wort_volume_liters)
            efficiency = wort.mash_efficiency
            st.success(f'Brewhouse Efficiency: {efficiency:.2f}%')
        else:
            st.error('Please enter valid input values')

elif tile == 'Yeast Pitching Rate':
    st.header('Yeast Pitching Rate Calculator 🍶')
    
    # Input fields for yeast pitching rate
    volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")
    pitching_rate = st.number_input('Enter desired pitching rate (cells/mL/°P)', min_value=0.0, format="%.2f", value=0.75)

    if st.button('Calculate Yeast Pitching Rate'):
        if volume_liters > 0 and original_gravity > 1.000 and pitching_rate > 0:
            yeast_cells_needed = (volume_liters * ((original_gravity - 1) * 1000 / 4) * pitching_rate) / 1e9
            st.success(f'Yeast Cells Needed: {yeast_cells_needed:.2f} billion cells')
        else:
            st.error('Please enter valid input values')

elif tile == 'Extract Yield and Efficiency':
    st.header('Extract Yield and Efficiency Calculator (SG Method) 🧮')
    
    # Input fields for extract yield and efficiency
    grain_weight_kg = st.number_input('Enter grain weight (in kilograms)', min_value=0.0, format="%.2f")
    wort_volume_hl = st.number_input('Enter wort volume (in hectoliters)', min_value=0.0, format="%.2f")
    original_gravity = st.number_input('Enter original gravity', min_value=1.000, format="%.3f")
    extract_per_kg = st.number_input('Enter extract per kg of malt (in litre degrees per kg)', min_value=0.0, format="%.2f", value=300.0)

    if st.button('Calculate Extract Yield and Efficiency'):
        if grain_weight_kg > 0 and wort_volume_hl > 0 and original_gravity > 1.000:
            potential_available_extract = grain_weight_kg * extract_per_kg
            actual_extract_achieved = wort_volume_hl * 100 * (original_gravity - 1) * 1000
            extract_yield = actual_extract_achieved / grain_weight_kg
            extract_efficiency = (actual_extract_achieved / potential_available_extract) * 100
            st.success(f'Extract Yield: {extract_yield:.2f} litre degrees per kg')
            st.success(f'Extract Efficiency: {extract_efficiency:.2f}%')
        else:
            st.error('Please enter valid input values')

elif tile == 'Grain Weight':
    st.header('Grain Weight Calculator ⚖️')
    
    # Input fields for grain weight calculation
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")
    target_original_gravity = st.number_input('Enter target original gravity', min_value=1.000, format="%.3f")
    extract_efficiency = st.number_input('Enter extract efficiency (in percentage)', min_value=0.0, max_value=100.0, format="%.2f", value=75.0)

    if st.button('Calculate Grain Weight'):
        if wort_volume_liters > 0 and target_original_gravity > 1.000 and extract_efficiency > 0:
            total_extract_needed = wort_volume_liters * (target_original_gravity - 1) * 1000
            grain_weight = total_extract_needed / (extract_efficiency / 100 * 300)
            st.success(f'Grain Weight Needed: {grain_weight:.2f} kg')
        else:
            st.error('Please enter valid input values')

elif tile == 'Hops Utilization':
    st.header('Hops Utilization Calculator 🌿')
    
    # Input fields for hops utilization
    alpha_acids = st.number_input('Enter alpha acids percentage', min_value=0.0, max_value=100.0, format="%.2f")
    hop_weight_g = st.number_input('Enter hop weight (in grams)', min_value=0.0, format="%.2f")
    boil_time = st.number_input('Enter boil time (in minutes)', min_value=0, format="%d")
    wort_volume_liters = st.number_input('Enter wort volume (in liters)', min_value=0.0, format="%.2f")

    if st.button('Calculate Hops Utilization'):
        if alpha_acids > 0 and hop_weight_g > 0 and boil_time > 0 and wort_volume_liters > 0:
            hops = Hops(hop_weight_g, alpha_acids, wort_volume_liters, 1.050, boil_time)  # Assuming a default wort SG
            ibu = hops.wort_bitterness
            st.success(f'IBU: {ibu:.2f}')
        else:
            st.error('Please enter valid input values')
