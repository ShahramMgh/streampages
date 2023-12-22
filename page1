import streamlit as st

# Title of the app
st.title("My Streamlit App")

# Add some text to the app
st.write("Welcome to my Streamlit app. You can add various elements here.")

# Add a sidebar
st.sidebar.title("Sidebar")
st.sidebar.write("You can put widgets and controls here.")

# Add a button widget
if st.button("Click Me"):
    st.write("Button clicked!")

# Add a text input widget
user_input = st.text_input("Enter your name", "Your name here")
st.write(f"Hello, {user_input}!")

# Add a selectbox widget
option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {option}")

# Add a slider widget
value = st.slider("Select a value", 0, 100, 50)
st.write(f"Selected value: {value}")

# Display an image
st.image("https://via.placeholder.com/150", caption="Placeholder Image", use_column_width=True)

# Display a DataFrame (using pandas)
import pandas as pd
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}
df = pd.DataFrame(data)
st.dataframe(df)

# Display a chart (e.g., line chart)
import matplotlib.pyplot as plt
chart_data = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]})
st.line_chart(chart_data.set_index('x'))

# Display a map
st.map()

# Add a progress bar
import time
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.05)
    progress_bar.progress(i + 1)

# Add a footer
st.write("This is the end of my Streamlit app!")

# Run the app with `streamlit run app.py` in your terminal
