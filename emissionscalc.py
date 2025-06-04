import streamlit as st

# Page config
st.set_page_config(
    page_title="Safety-Kleen Product Emissions Calculator",
    layout="wide",
)

# Custom styles
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f7fa;
            font-family: 'Arial', sans-serif;
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #004b87;
        }
        .block-container {
            padding: 2rem 3rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        }
        .css-1v0mbdj p {
            font-size: 16px;
        }
        .stDownloadButton > button {
            background-color: #004b87;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Emissions data (kg CO2e per gallon)
emissions_data = {
    "Industrial Fluids": {
        "Extreme Pressure Gear Oil (MD)": (3.4, 1.5),
        "Extreme Pressure Gear Oils (EHV)": (3.5, 1.6),
        "Extreme Pressure Gear Oils (HV)": (3.5, 1.6),
        "ISO Way Oils": (3.3, 1.4)
    },
    "Base Oils": {
        "Kleen+ RHT70 Base Oil": (3.6, 1.7),
        "Kleen+ RHT120 Base Oil": (3.6, 1.7),
        "Kleen+ RHT240 Base Oil": (3.6, 1.7)
    },
    "Motor Oils": {
        "Synthetic Blend Motor Oil": (3.4, 1.5),
        "Full Synthetic (SP/GF-6A) Motor Oil": (3.5, 1.6),
        "Full Synthetic (SP/GF-6B) Motor Oil": (3.5, 1.6),
        "Full Synthetic DEXOS1 Gen 3 Motor Oil": (3.5, 1.6),
        "Fully Synthetic Euro Spec Motor Oil": (3.5, 1.6),
        "Heavy Duty CK-4 Engine Oil": (3.4, 1.5),
        "Synthetic Blend Heavy Duty CK-4 Engine Oil": (3.4, 1.5),
        "Full Synthetic Heavy Duty CK-4 Engine Oil": (3.5, 1.6),
        "Natural Gas Engine Oil NGP-3": (3.4, 1.5)
    },
    "Driveline Fluids": {
        "Automatic Transmission Fluid (Dexron III/ Mercon)": (3.2, 1.4),
        "Full Synthetic Multi-Vehicle ATP": (3.4, 1.5),
        "Full Synthetic Heavy Duty SYN SSE": (3.5, 1.6),
        "Full Synthetic Heavy-Duty SYN EATON PS-386": (3.5, 1.6),
        "Full Synthetic Heavy Duty ATF (Allison TES-295 & TES-389)": (3.6, 1.7),
        "Full Synthetic Heavy Duty ATF (SAE 50)": (3.6, 1.7)
    },
    "Greases": {
        "All Purpose Lithium (NLGI 1)": (2.8, 1.3),
        "All Purpose Lithium (NLGI 2)": (2.8, 1.3),
        "High Temp Lithium (NLGI 1)": (2.9, 1.4),
        "High Temp Lithium (NLGI 2)": (2.9, 1.4),
        "Moly Supreme (NLGI 1)": (3.0, 1.4),
        "Moly Supreme (NLGI 2)": (3.0, 1.4),
        "Construction Red (NLGI 1)": (3.1, 1.5),
        "Construction Red (NLGI 2)": (3.1, 1.5),
        "Ultra Calcium Sulfonate (NLGI 2)": (3.2, 1.6)
    }
}

volume_conversion = {
    "Quart": 0.25,
    "Gallon": 1,
    "Drum (55G)": 55,
    "Tote (330G)": 330,
    "10 x 14 oz Case": 1.09375,
    "35lb Pail": 4.375,
    "120lb Keg": 15,
    "400lb Drum": 50
}

# App UI
st.title("Safety-Kleen Product Emissions Calculator")

# Product Selection
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Product field:", list(emissions_data.keys()))
with col2:
    product = st.selectbox("Product:", list(emissions_data[category].keys()))

# Volume selection
col3, col4 = st.columns(2)
with col3:
    volume_type = st.selectbox(
        "Select volume:",
        list(volume_conversion.keys()),
        help="Example: Drum (55G) means a 55-gallon drum"
    )
with col4:
    volume_count = st.number_input("Number of units:", min_value=0.0, value=1.0)

is_loop = st.radio("Are you using Safety-Kleen closed-loop system?", ("Yes", "No"))

# Emissions calculations
virgin_emission, loop_emission = emissions_data[category][product]
total_gallons = volume_conversion[volume_type] * volume_count

virgin_emissions = virgin_emission * total_gallons
loop_emissions = loop_emission * total_gallons
co2_saved = virgin_emissions - loop_emissions

total_emissions = loop_emissions if is_loop == "Yes" else virgin_emissions

# Output results
st.subheader("Results")
st.write(f"**Product:** {product}")
st.write(f"**Volume:** {total_gallons:.2f} gallons")
st.write(f"**System Used:** {'Safety-Kleen LOOP' if is_loop == 'Yes' else 'Virgin Oil'}")

if is_loop == "Yes":
    st.markdown(f"<h2 style='color:green; font-size:28px;'>Estimated CO₂ Emissions: {total_emissions:.2f} kg CO₂</h2>", unsafe_allow_html=True)
    st.success(f"You saved approximately {co2_saved:.2f} kg CO₂ by using the Safety-Kleen LOOP system.")
else:
    st.markdown(f"<h2 style='color:red; font-size:28px;'>Estimated CO₂ Emissions: {total_emissions:.2f} kg CO₂</h2>", unsafe_allow_html=True)
    st.info(f"Using Safety-Kleen's LOOP system, you could have saved {co2_saved:.2f} kg CO₂.")

# Virgin oil baseline reminder
if is_loop=="Yes":
    st.write("\n")
    st.markdown(f"<h4>Compared to virgin crude oil emissions:</h4>", unsafe_allow_html=True)
    st.write(f"Using {total_gallons:.2f} gallons of {product} with virgin oil would generate approximately {virgin_emissions:.2f} kg CO₂.")

# Downloadable summary
summary = f"""Product: {product}
Volume: {total_gallons:.2f} gallons
System Used: {is_loop}
Emissions: {total_emissions:.2f} kg CO₂
CO₂ Saved: {co2_saved:.2f} kg
"""
st.download_button(
    label="📥 Download results as .txt",
    data=summary,
    file_name="safety-kleen_emissions_summary.txt"
)

st.markdown("---")
st.markdown("🚛 **Want to learn more about closed-loop sustainability?** [Visit Safety-Kleen](https://www.safety-kleen.com)", unsafe_allow_html=True)

