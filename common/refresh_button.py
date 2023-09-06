import subprocess
import streamlit as st  # pip install streamlit

# Define the function to be triggered by the button
def run_script():
    try:
        result = subprocess.run(["python3", "data.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        st.write("Successfully refreshed coin data!!")
    except subprocess.CalledProcessError as e:
        st.error("Error refreshing coing data.")
        st.code(e.stderr)

def display_data_refresh_button():
    if st.sidebar.button("Refresh Coin Data"):
        run_script()
    #st.sidebar.divider() 


