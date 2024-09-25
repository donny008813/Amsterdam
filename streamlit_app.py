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

# Title for the app
st.title("Amsterdam Population and Migration Data")

# First scatter plot: Population
st.subheader("Population Data")
show_male_population = st.checkbox("Show Male Population")

# Create the first plot for population
fig1, ax1 = plt.subplots()

# Plot total population
sns.scatterplot(data=data, x='Perioden', y='TotaleBevolking_1', ax=ax1, label='Total Population')

# Conditionally add male population to the plot
if show_male_population:
    sns.scatterplot(data=df, x='Perioden', y='Mannen_2', ax=ax1, label='Male Population')

# Add labels and title
ax1.set_title('Amsterdam Population Over Time')
ax1.set_ylabel('Population')
ax1.set_xlabel('Year')

# Set y-axis limit to include 0
ax1.set_ylim(0, data['Population'].max() + 50000)

# Show only every 2nd x-axis tick
ax1.set_xticks(data['Year'][::2])

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show the first plot in the Streamlit app
st.pyplot(fig1)

# Second plot: Immigration and Emigration Data
st.subheader("Migration Data")

# Dropdown menu to select between immigration and emigration
migration_type = st.selectbox(
    "Select Migration Type:",
    options=["Vestiging Gemeente", "Vertrek Gemeente"]
)

# Create the second plot
fig2, ax2 = plt.subplots()

# Plot immigration or emigration based on the dropdown selection
if migration_type == "Vestiging Gemeente":
    sns.barplot(data=data, x='Perioden', y='VestigingUitAndereGemeente_69', ax=ax2)
    ax2.set_title('Amsterdam Immigration Over Time')
else:
    sns.barplot(data=data, x='Perioden', y='VertrekNaarAndereGemeente_70', ax=ax2)
    ax2.set_title('Amsterdam Emigration Over Time')

# Add labels
ax2.set_ylabel('Number of People')
ax2.set_xlabel('Year')

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show the second plot in the Streamlit app
st.pyplot(fig2)
