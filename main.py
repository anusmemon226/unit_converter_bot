import streamlit as st
from pint import UnitRegistry
from google import genai

API_KEY = st.secrets["GOOGLE_GEMINI_API_KEY"]
# Initialize unit registry
ureg = UnitRegistry()
Q = ureg.Quantity

# Title
st.title("Unit Converter")

# Define unit categories and their corresponding units
unit_categories = {
    "Area": ["square meter", "square kilometer","square mile","square yard","square foot","square inch","hectare","acre"],
    "Data Transfer Rate": [
    "bit_per_second", "kilobit_per_second", "megabit_per_second", "gigabit_per_second",
    "terabit_per_second", "byte_per_second", "kilobyte_per_second", "megabyte_per_second",
    "gigabyte_per_second", "terabyte_per_second"
]   ,
    "Digital Storage": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
    "Energy": ["joule", "calorie", "kilocalorie", "kilojoule", "watt-hour"],
    "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
    "Fuel Economy": ["kilometers per liter", "miles per gallon"],
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch", "centimeter", "millimeter"],
    "Mass": ["gram", "kilogram", "pound", "ounce", "milligram", "ton"],
    "Plane Angle": ["degree", "radian"],
    "Pressure": ["pascal", "bar", "atmosphere", "psi", "torr"],
    "Speed": ["meter per second", "kilometer per hour", "mile per hour", "foot per second"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day"],
    "Volume": ["liter", "milliliter", "cubic meter", "gallon", "cup"]
}


category = st.selectbox("🔹 Select Unit Category", list(unit_categories.keys()))

col1,col2 = st.columns(2)

with col1:
    input_unit = st.selectbox("Convert From:", unit_categories[category])

with col2:
    output_unit = st.selectbox("Convert To:", unit_categories[category])

value = st.number_input("Enter Value:", min_value=0.0)

if category:
    if st.button("Convert"):
        if input_unit == output_unit:
            st.write("Please Select Different Unit..")
        else:
            try:
                fromVal = float(value)
                client = genai.Client(api_key=API_KEY)
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[{"text": f"Convert {fromVal} {input_unit} to {output_unit}"}])
                ai_response = response.candidates[0].content.parts[0].text
                st.success(f"AI Bot Response: {ai_response}")
                if category == "Temperature":
                    input_quantity = Q(value, ureg(input_unit))
                    converted_quantity = input_quantity.to(ureg(output_unit))
                else:
                    input_quantity = value * ureg(input_unit)
                    converted_quantity = input_quantity.to(output_unit)
                result = f"{value} {input_unit.replace('_', ' ')} = {converted_quantity.magnitude} {output_unit.replace('_', ' ')}"
                st.success(f"PInt Library Response : {result}")
            except Exception as e:
                st.error(f"⚠️ Conversion Error: {e}")