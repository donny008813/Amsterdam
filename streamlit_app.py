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
    options=["Vestiging Gemeente", "Vertrek Gemeente", "Immigratie", "Emigratie", "Geboren", "Overleden"]
)

# Create the second plot
fig2, ax2 = plt.subplots()

# Plot immigration or emigration based on the dropdown selection
if migration_type == "Vestiging Gemeente":
    sns.barplot(data=data, x='Perioden', y='VestigingUitAndereGemeente_69', ax=ax2)
    ax2.set_title('Amsterdam Vestiging in gemeente Over Time')
elif migration_type == "Vertrek Gemeente":
    sns.barplot(data=data, x='Perioden', y='VertrekNaarAndereGemeente_70', ax=ax2)
    ax2.set_title('Amsterdam vertrek gemeente Over Time')
elif migration_type == "Immigratie":
    sns.barplot(data=data, x='Perioden', y='Immigratie_74', ax=ax2)
    ax2.set_title('Amsterdam immigratie Over Time')
elif migration_type == "Emigratie":
    sns.barplot(data=data, x='Perioden', y='Emigratie_75', ax=ax2)
    ax2.set_title('Amsterdam emigratie Over Time')
elif migration_tyep == "Geboren":
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
