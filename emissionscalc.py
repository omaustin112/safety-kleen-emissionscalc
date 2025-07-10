import streamlit as st

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
        "Extreme Pressure Gear Oil (MD)": (10.7, 2.78),
        "Extreme Pressure Gear Oils (EHV)": (10.7, 2.78),
        "Extreme Pressure Gear Oils (HV)": (11, 3.5),
        "ISO Way Oils": (12.84, 2.78)
    },
    "Base Oils": {
        "Kleen+ RHT70 Base Oil": (12.84, 2.78),
        "Kleen+ RHT120 Base Oil": (12.84, 2.78),
        "Kleen+ RHT240 Base Oil": (12.84, 2.78)
    },
    "Motor Oils": {
        "Synthetic Blend Motor Oil": (12.84, 2.78),
        "Full Synthetic (SP/GF-6A) Motor Oil": (13.4, 1.6),
        "Full Synthetic (SP/GF-6B) Motor Oil": (13.4, 1.6),
        "Full Synthetic DEXOS1 Gen 3 Motor Oil": (13.4, 1.6),
        "Fully Synthetic Euro Spec Motor Oil": (13.4, 1.6),
        "Heavy Duty CK-4 Engine Oil": (12.8, 1.5),
        "Synthetic Blend Heavy Duty CK-4 Engine Oil": (13.2, 1.5),
        "Full Synthetic Heavy Duty CK-4 Engine Oil": (14, 1.6),
        "Natural Gas Engine Oil NGP-3": (13.8, 1.5)
    },
    "Driveline Fluids": {
        "Automatic Transmission Fluid (Dexron III/ Mercon)": (12.8, 1.4),
        "Full Synthetic Multi-Vehicle ATP": (13, 1.5),
        "Full Synthetic Heavy Duty SYN SSE": (13.5, 1.6),
        "Full Synthetic Heavy-Duty SYN EATON PS-386": (13.5, 1.6),
        "Full Synthetic Heavy Duty ATF (Allison TES-295 & TES-389)": (13.7, 1.7),
        "Full Synthetic Heavy Duty ATF (SAE 50)": (13.7, 1.7)
    },
     "Gear Oils": {
        "Conventional": (12.8, 1.5),
        "Full Synthetic": (14, 2),
    },
    "Greases": {
        "All Purpose Lithium (NLGI 1)": (13, 2),
        "All Purpose Lithium (NLGI 2)": (13, 2),
        "High Temp Lithium (NLGI 1)": (13.5, 2.1),
        "High Temp Lithium (NLGI 2)": (13.5, 2.1),
        "Moly Supreme (NLGI 1)": (14, 2.2),
        "Moly Supreme (NLGI 2)": (14, 2.2),
        "Construction Red (NLGI 1)": (14.5, 2.3),
        "Construction Red (NLGI 2)": (14.5, 2.3),
        "Ultra Calcium Sulfonate (NLGI 2)": (15, 2.5),
    },
    "Antifreeze & Coolants": {
        "HD Extended Life NAPS Free OAT": (7.2512, 5.514),
        "HD Extended Life NMOAT": (7.246, 5.512),
        "LD Extended Life NAPS Free OAT": (7.2512, 5.514),
        "LD/HD Conventional": (7.2537, 5.516),
        "LD/HD Extended Service Interval HOAT": (7.2512, 5.514),
        "LD Extended Life 2-EH OAT": (7.2512, 5.514)
    }
}

# Volume options by product
product_volumes = {
    # Industrial Fluids
    "Extreme Pressure Gear Oil (MD)": ["5G Pail", "55G Drum", "330G Tote", "Bulk"],
    "Extreme Pressure Gear Oils (EHV)": ["55G Drum", "330G Tote", "Bulk"],
    "Extreme Pressure Gear Oils (HV)": ["55G Drum", "330G Tote", "Bulk"],
    "ISO Way Oils": ["5G Pail", "55G Drum", "330G Tote", "Bulk"],
    # Base Oils
    "Kleen+ RHT70 Base Oil": ["Gallon"],
    "Kleen+ RHT120 Base Oil": ["Gallon"],
    "Kleen+ RHT240 Base Oil": ["Gallon"],
    # Motor Oils
    "Synthetic Blend Motor Oil": ["12x1 Qt. Case", "4x5 Qt. Case", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic (SP/GF-6A) Motor Oil": ["12x1 Qt. Case", "4x5 Qt. Case", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic (SP/GF-6B) Motor Oil": ["55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic DEXOS1 Gen 3 Motor Oil": ["12x1 Qt. Case", "4x5 Qt. Case", "55G Drum", "330G Tote", "Bulk"],
    "Fully Synthetic Euro Spec Motor Oil": ["55G Drum", "330G Tote", "Bulk"],
    "Heavy Duty CK-4 Engine Oil": ["4x1G Case", "5G Pail", "55G Drum", "330G Tote", "Bulk"],
    "Synthetic Blend Heavy Duty CK-4 Engine Oil": ["55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic Heavy Duty CK-4 Engine Oil": ["4x1G Case", "5G Pail", "55G Drum", "330G Tote", "Bulk"],
    "Natural Gas Engine Oil NGP-3": ["55G Drum", "330G Tote", "Bulk"],
    # Driveline Fluids
    "Automatic Transmission Fluid (Dexron III/ Mercon)": ["12x1 Qt. Case", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic Multi-Vehicle ATP": ["12x1 Qt. Case", "4x5 Qt. Case", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic Heavy Duty SYN SSE": ["5G Pail", "55G Drum", "275G Tote", "Bulk"],
    "Full Synthetic Heavy-Duty SYN EATON PS-386": ["5G Pail", "55G Drum", "275G Tote", "Bulk"],
    "Full Synthetic Heavy Duty ATF (Allison TES-295 & TES-389)": ["5G Pail", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic Heavy Duty ATF (SAE 50)": ["5G Pail", "16G Keg", "330G Tote", "Bulk"],
    # Gear Oils
    "Conventional": ["5G Pail", "16G Keg", "55G Drum", "330G Tote", "Bulk"],
    "Full Synthetic": ["5G Pail", "16G Keg", "55G Drum", "330G Tote", "Bulk"],
    # Greases
    "All Purpose Lithium (NLGI 1)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "All Purpose Lithium (NLGI 2)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "High Temp Lithium (NLGI 1)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "High Temp Lithium (NLGI 2)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "Moly Supreme (NLGI 1)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "Moly Supreme (NLGI 2)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "Construction Red (NLGI 1)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "Construction Red (NLGI 2)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    "Ultra Calcium Sulfonate (NLGI 2)": ["10 x 14 oz Case", "35lb Pail", "120lb Keg", "400lb Drum"],
    # Antifreeze & Coolants
    "HD Extended Life NAPS Free OAT": ["55G Drum", "Bulk"],
    "HD Extended Life NMOAT": ["55G Drum", "Bulk"],
    "LD Extended Life NAPS Free OAT": ["55G Drum", "Bulk"],
    "LD/HD Conventional": ["55G Drum", "Bulk"],
    "LD/HD Extended Service Interval HOAT": ["55G Drum", "Bulk'],
    "LD Extended Life 2-EH OAT": ["55G Drum", "Bulk"],
}
}

volume_conversion = {
    "12x1 Qt. Case": 3,
    "4x5 Qt. Case": 5,
    "5G Pail": 5,
    "16G Keg": 16,
    "35lb Pail": 4.375,
    "55G Drum": 55,
    "120lb Keg": 15,
    "275G Tote": 275,
    "330G Tote": 330,
    "400lb Drum": 50,
    "Bulk": 1,  # Bulk assumed 1 gallon per unit; handle accordingly if different
    "10 x 14 oz Case": 1.09375,
}

# App UI
st.title("Safety-Kleen Product Emissions Calculator")

# Product Selection
col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("Product field:", list(emissions_data.keys()))
with col2:
    product = st.selectbox("Product:", list(emissions_data[category].keys()))

# Get volume options for selected product, fallback to empty list if not found
available_volumes = product_volumes.get(product, [])

# Volume selection with dynamic filtering
col3, col4 = st.columns(2)
with col3:
    if available_volumes:
        volume_type = st.selectbox(
            "Select volume:",
            available_volumes,
            help="Select the volume offered for the product"
        )
    else:
        st.write("No volume options available for this product.")
        volume_type = None
with col4:
    volume_count = st.number_input("Number of units:", min_value=0.0, value=1.0)

is_loop = st.radio("Are you using Safety-Kleen closed-loop system?", ("Yes", "No"))

if volume_type:
    # Emissions calculations
    virgin_emission, loop_emission = emissions_data[category][product]
    total_gallons = volume_conversion.get(volume_type, 1) * volume_count

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

else:
    st.warning("Please select a volume option to calculate emissions.")

st.markdown("---")
st.markdown("🚛 **Want to learn more about closed-loop sustainability?** [Visit Safety-Kleen](https://www.safety-kleen.com)", unsafe_allow_html=True)
