import streamlit as st
import pandas as pd
import cbsodata
import seaborn as sns
import matplotlib.pyplot as plt

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

data = pd.DataFrame(
        cbsodata.get_data('70072ned',
                          filters="RegioS eq 'GM0363'",
                          select=['Perioden','TotaleBevolking_1','Mannen_2','Vrouwen_3','VestigingUitAndereGemeente_69', 'VertrekNaarAndereGemeente_70', 
                                 ]))
print(data.head(20))

# Checkbox to toggle male population
st.subheader("Population Data")
show_male_population = st.checkbox("Show Male Population")

# Scatter plot with Seaborn
fig, ax = plt.subplots()

# Plot total population
st.line_chart(data, x='Perioden', y='TotaleBevolking_1')

# Conditionally add male population to the plot
if show_male_population:
    sns.scatterplot(data, x='Perioden', y='Mannen_2', ax=ax, label='Male Population')

# Add labels
ax.set_title('Amsterdam Population Over Time')
ax.set_ylabel('Population')
ax.set_xlabel('Year')

# Set y-axis limit to include 0
ax.set_ylim(0, data['TotaleBevolking_1'].max() + 50000)

# Show only every 2nd x-axis tick
ax.set_xticks(data['Perioden'][::2])

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show the plot in the Streamlit app
st.pyplot(fig)

# Second plot: Immigration and Emigration Data
st.subheader("Migration Data")

# Dropdown menu to select between immigration and emigration
migration_type = st.selectbox(
    "Select change Type:",
    options=["Vestiging Gemeente", "Vertrek Gemeente"]
)

if migration_type == "Vestiging Gemeente":
    st.scatter_chart(data, x='Perioden', y='VestigingUitAndereGemeente_69')
else:
    st.scatter_chart(data, x='Perioden', y='VertrekNaarAndereGemeente_70')
