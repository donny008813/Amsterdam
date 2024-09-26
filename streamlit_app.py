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

data = load_data()
print(data.head(20))

# Title for the app
st.title("Voorspellen van de populatie van Amsterdam")
st.write("De woningcrisis is een actueel probleem. Alleen om erachter te komen hoeveel woningen er nodig zijn in Amsterdam, moet er een beeld zijn hoeveel inwoners erbij zullen komen en er weggaan.")
st.write("Eerst zal er worden gekeken naar de totale populatie van Amsterdam en verdeeld over mannen en vrouwen. Daarna naar hoeveel er bij zijn gekomen en hoeveel er weg zijn gegaan.")
st.write("Daarna zal er gekeken worden of er aan de hand van andere gegevens over de jaren heen een lineair regressie model opgesteld kan worden waarmee de populatie voorspeld zou kunnen worden.")
st.write("De gekozen variabelen worden verklaard en het model wordt getoond.")

# First scatter plot: Population
st.subheader("Populatie Data")
st.write('Populatie van Amsterdam over de jaren.')
show_male_population = st.checkbox("Toon mannelijke populatie")
show_female_population = st.checkbox("Toon vrouwelijke populatie")

# Create the first plot for population
fig1, ax1 = plt.subplots()

# Plot total population
sns.scatterplot(data=data, x='Perioden', y='TotaleBevolking_1', ax=ax1, label='Totale Populatie')

# Conditionally add male population to the plot
if show_male_population:
    sns.scatterplot(data=data, x='Perioden', y='Mannen_2', ax=ax1, label='Mannelijke Populatie')

if show_female_population:
    sns.scatterplot(data=data, x='Perioden', y='Vrouwen_3', ax=ax1, label='Vrouwelijke Populatie')

# Add labels and title
ax1.set_title('Populatie van Amsterdam over de jaren')
ax1.set_ylabel('Populatie')
ax1.set_xlabel('Jaar')

# Set y-axis limit to include 0
ax1.set_ylim(0, data['TotaleBevolking_1'].max() + 50000)

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show only every 2nd x-axis tick
ax1.set_xticks(data['Perioden'][::2])

# Show the first plot in the Streamlit app
st.pyplot(fig1)

# Second plot: Immigration and Emigration Data
st.subheader("Inkomende en vertrekkende bewoners")
st.write('De verschillende aantallen inkomende of vertrekkende bewoners van Amsterdam. Selecteer in de dropdown menu welke vorm van inkomend of uitgaand getoond wordt.')

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
    ax2.set_title('Amsterdam vestiging over de jaren')
elif migration_type == "Vertrek":
    sns.barplot(data=data, x='Perioden', y='VertrekNaarAndereGemeente_70', ax=ax2)
    ax2.set_title('Amsterdam vertrek over de jaren')
elif migration_type == "Immigratie":
    sns.barplot(data=data, x='Perioden', y='Immigratie_74', ax=ax2)
    ax2.set_title('Amsterdam immigratie over de jaren')
elif migration_type == "Emigratie":
    sns.barplot(data=data, x='Perioden', y='Emigratie_75', ax=ax2)
    ax2.set_title('Amsterdam emigratie over de jaren')
elif migration_type == "Geboren":
    sns.barplot(data=data, x='Perioden', y='LevendGeborenKinderen_58', ax=ax2)
    ax2.set_title('Amsterdam geboren over de jaren')
else:
    sns.barplot(data=data, x='Perioden', y='Overledenen_60', ax=ax2)
    ax2.set_title('Amsterdam overledenen over de jaren')

# Add labels
ax2.set_ylabel('Aantal mensen')
ax2.set_xlabel('Jaar')

# Modify x-axis ticks: rotate and set font size
plt.xticks(fontsize=10, rotation=45)

# Show only every 2nd x-axis tick
ax2.set_xticks(data['Perioden'][::2])

# Show the second plot in the Streamlit app
st.pyplot(fig2)

# Derde grafiek
st.subheader('Totaal inkomend of vertrekende populatie Amsterdam')

# Calculate inkomend
data['inkomend'] = data['VestigingUitAndereGemeente_69'] + data['Immigratie_74'] + data['LevendGeborenKinderen_58']

# Calculate uitgaand
data['uitgaand'] = data['VertrekNaarAndereGemeente_70'] + data['Emigratie_75'] + data['Overledenen_60']

# Calculate net populatie
data['net populatie'] = data['inkomend'] - data['uitgaand']

# Jaartal naar int veranderen voor de slider
data['Perioden'] = data['Perioden'].astype('int')

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
ax3.set_title('Amsterdam totaal inkomend of vertrekende populatie')
ax3.set_ylabel('Aantal mensen')
ax3.set_xlabel('Jaar')


# Rotate the x-ticks for better readability
plt.xticks(rotation=90)  # Adjust the rotation angle as needed

# Show the third plot in the Streamlit app
st.pyplot(fig3)
