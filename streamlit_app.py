import streamlit as st
import pandas as pd
import cbsodata
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    data = pd.DataFrame(cbsodata.get_data('70072ned', 
                                          filters="RegioS eq 'GM0363'", 
                                          select=['Perioden','TotaleBevolking_1','Mannen_2',
                                                  'Vrouwen_3','VestigingUitAndereGemeente_69', 
                                                  'VertrekNaarAndereGemeente_70', 'Immigratie_74', 'Emigratie_75',
                                                 'LevendGeborenKinderen_58', 'Overledenen_60']))
    return data

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

data = load_data()
print(data.head(20))

# Title for the app
st.title("Amsterdam Population and Migration Data")

# First scatter plot: Population
st.subheader("Population Data")
show_male_population = st.checkbox("Show Male Population")
show_female_population = st.checkbox("Show Female Population")

# Create the first plot for population
fig1, ax1 = plt.subplots()

# Plot total population
sns.scatterplot(data=data, x='Perioden', y='TotaleBevolking_1', ax=ax1, label='Total Population')

# Conditionally add male population to the plot
if show_male_population:
    sns.scatterplot(data=data, x='Perioden', y='Mannen_2', ax=ax1, label='Male Population')

if show_female_population:
    sns.scatterplot(data=data, x='Perioden', y='Vrouwen_3', ax=ax1, label='Female Population')

# Add labels and title
ax1.set_title('Amsterdam Population Over Time')
ax1.set_ylabel('Population')
ax1.set_xlabel('Year')

# Set y-axis limit to include 0
ax1.set_ylim(0, data['TotaleBevolking_1'].max() + 50000)

# Show only every 2nd x-axis tick
ax1.set_xticks(data['Perioden'][::2])

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show the first plot in the Streamlit app
st.pyplot(fig1)

# Second plot: Immigration and Emigration Data
st.subheader("Migration Data")

# Dropdown menu to select between immigration and emigration
migration_type = st.selectbox(
    "Select Change Type:",
    options=["Vestiging", "Vertrek", "Immigratie", "Emigratie", "Geboren", "Overleden"]
)

# Create the second plot
fig2, ax2 = plt.subplots()

# Plot immigration or emigration based on the dropdown selection
if migration_type == "Vestiging":
    sns.barplot(data=data, x='Perioden', y='VestigingUitAndereGemeente_69', ax=ax2)
    ax2.set_title('Amsterdam Vestiging Over Time')
elif migration_type == "Vertrek":
    sns.barplot(data=data, x='Perioden', y='VertrekNaarAndereGemeente_70', ax=ax2)
    ax2.set_title('Amsterdam vertrek Over Time')
elif migration_type == "Immigratie":
    sns.barplot(data=data, x='Perioden', y='Immigratie_74', ax=ax2)
    ax2.set_title('Amsterdam immigratie Over Time')
elif migration_type == "Emigratie":
    sns.barplot(data=data, x='Perioden', y='Emigratie_75', ax=ax2)
    ax2.set_title('Amsterdam emigratie Over Time')
elif migration_type == "Geboren":
    sns.barplot(data=data, x='Perioden', y='LevendGeborenKinderen_58', ax=ax2)
    ax2.set_title('Amsterdam geboren Over Time')
else:
    sns.barplot(data=data, x='Perioden', y='Overledenen_60', ax=ax2)
    ax2.set_title('Amsterdam overledenen Over Time')

# Add labels
ax2.set_ylabel('Number of People')
ax2.set_xlabel('Year')

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show the second plot in the Streamlit app
st.pyplot(fig2)

# Derde grafiek
st.subheader('Net inkomend populatie Amsterdam')

# Calculate inkomend
data['inkomend'] = data['VestigingUitAndereGemeente_69'] + data['Immigratie_74'] + data['LevendGeborenKinderen_58']

# Calculate uitgaand
data['uitgaand'] = data['VertrekNaarAndereGemeente_70'] + data['Emigratie_75'] + data['Overledenen_60']

# Calculate net populatie
data['net populatie'] = data['inkomend'] - data['uitgaand']

# Slider maken voor de net grafiek
min_year = int(data['Perioden'].min())
max_year = int(data['Perioden'].max())
year_range = st.slider('Select year range for net inkomende populatie', min_year, max_year, (min_year, max_year))

# Data selecter op basis van de slider
data_slider = data[(data['Perioden'] >= year_range[0]) & (data['Perioden'] <= year_range[1])]

# Plot maken voor net grafiek
fig3, ax3 = plt.subplots()

# Plot de net grafiek als barplot
sns.barplot(data=data_slider, x='Perioden', y='net populatie', ax=ax3)

# Add title and labels
ax3.set_title('Amsterdam Net Migration Over Time')
ax3.set_ylabel('Net Migration (Immigration - Emigration)')
ax3.set_xlabel('Year')

# Show the third plot in the Streamlit app
st.pyplot(fig3)
