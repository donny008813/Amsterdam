import streamlit as st
import pandas as pd
import cbsodata
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Inladen van de data met behulp van een fuctie en cache_data zodat deze geladen blijft
@st.cache_data
def load_data():
    data = pd.DataFrame(cbsodata.get_data('70072ned', 
                                          filters="RegioS eq 'GM0363'", 
                                          select=['Perioden','TotaleBevolking_1','Mannen_2',
                                                  'Vrouwen_3','VestigingUitAndereGemeente_69', 
                                                  'VertrekNaarAndereGemeente_70', 'Immigratie_74', 'Emigratie_75',
                                                 'LevendGeborenKinderen_58', 'Overledenen_60', 'TotaalBanen_111', 'Werkloosheid_154']))
    return data

# Laad de data
data = load_data()


# Titel en inleidende tekst voor de app
st.title("Voorspellen van de populatie van Amsterdam")
st.write("De woningcrisis is een actueel probleem. Alleen om erachter te komen hoeveel woningen er nodig zijn in Amsterdam, moet er een beeld zijn hoeveel inwoners erbij zullen komen en er weggaan.")
st.write("Er zijn nog meer problemen te bedenken die voort komen uit de toename van de populatie. Is dit aantal te beinvloeden? Hier zal naar gekeken worden.")
st.write("Eerst zal er worden gekeken naar de totale populatie van Amsterdam en verdeeld over mannen en vrouwen. Vervolgens wordt er gekeken naar hoeveel mensen er bij zijn gekomen en hoeveel mensen er weg zijn gegaan.")
st.write("Tot slot zal er gekeken worden of er aan de hand van andere gegevens over de jaren heen een lineair regressie model opgesteld kan worden waarmee de populatie voorspeld zou kunnen worden.")
st.write("De gekozen variabelen worden verklaard en het model zal worden getoond.")

# Eerste scatter plot: Populatie
st.subheader("Populatie Data")
st.write('Populatie van Amsterdam over de jaren.')
show_male_population = st.checkbox("Toon mannelijke populatie")
show_female_population = st.checkbox("Toon vrouwelijke populatie")

# Maak de eerste plot
fig1, ax1 = plt.subplots()

# Plot de totale populatie
sns.scatterplot(data=data, x='Perioden', y='TotaleBevolking_1', ax=ax1, label='Totale Populatie')

# If statements voor de checkbox
if show_male_population:
    sns.scatterplot(data=data, x='Perioden', y='Mannen_2', ax=ax1, label='Mannelijke Populatie')

if show_female_population:
    sns.scatterplot(data=data, x='Perioden', y='Vrouwen_3', ax=ax1, label='Vrouwelijke Populatie')

# Labels en titel
ax1.set_title('Populatie van Amsterdam over de jaren')
ax1.set_ylabel('Populatie')
ax1.set_xlabel('Jaar')

# Voeg nul toe aan de y-as
ax1.set_ylim(0, data['TotaleBevolking_1'].max() + 50000)

# x-as labels draaien
plt.xticks(fontsize=10, rotation=90)

# Plot de eerste plot
st.pyplot(fig1)

# Tweede plot inkomende en vertrekkende bewoners
st.subheader("Inkomende en vertrekkende bewoners")
st.write('De verschillende aantallen inkomende of vertrekkende bewoners van Amsterdam. Selecteer in het dropdown menu welke vorm van inkomend of uitgaand getoond wordt.')

# Dropdown menu om soort te selecteren
migration_type = st.selectbox(
    "Selecteer type ingaand of vertrekkende:",
    options=["Vestiging", "Vertrek", "Immigratie", "Emigratie", "Geboren", "Overleden"]
)

# Maak de tweede plot
fig2, ax2 = plt.subplots()

# Plot de soort op basis van de checkbox
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

# Labels
ax2.set_ylabel('Aantal mensen')
ax2.set_xlabel('Jaar')

# x-as labels draaien en formaat
plt.xticks(fontsize=10, rotation=90)

# x-as toon elk tweede jaar
ax2.set_xticks(data['Perioden'][::2])

# Plot de tweede plot
st.pyplot(fig2)

# Derde grafiek
st.subheader('Totaal inkomend of vertrekkende populatie Amsterdam')
st.write('Toont het totaal van de inkomende en uitgaande bewoners van Amsterdam. Hierin zijn de uitgaande en ingaande cijfers dus samengenomen om te tonen hoeveel mensen er per jaar afgaan of bijkomen.')

# Bereken inkomend
data['inkomend'] = data['VestigingUitAndereGemeente_69'] + data['Immigratie_74'] + data['LevendGeborenKinderen_58']

# Bereken uitgaand
data['uitgaand'] = data['VertrekNaarAndereGemeente_70'] + data['Emigratie_75'] + data['Overledenen_60']

# Bereken net populatie
data['net populatie'] = data['inkomend'] - data['uitgaand']

# Jaartal naar int veranderen voor de slider
data['Perioden'] = data['Perioden'].astype('int')

# Slider maken voor de net grafiek
min_year = int(data['Perioden'].min())
max_year = int(data['Perioden'].max())
year_range = st.slider('Select het aantal jaren voor de inkomende of vertrekende populatie', min_year, max_year, (min_year, max_year))

# Data selecter op basis van de slider
data_slider = data[(data['Perioden'] >= year_range[0]) & (data['Perioden'] <= year_range[1])]

# Plot maken voor net grafiek
fig3, ax3 = plt.subplots()

# Plot de net grafiek als barplot
sns.barplot(data=data_slider, x='Perioden', y='net populatie', ax=ax3)

# Voeg titel en labels toe
ax3.set_title('Amsterdam totaal inkomend of vertrekende populatie')
ax3.set_ylabel('Aantal mensen')
ax3.set_xlabel('Jaar')

# x-as draaien
plt.xticks(fontsize=10, rotation=90)

# Plot de derde plot
st.pyplot(fig3)

#######
# Lineairiteit controleren
st.subheader('Het voorspellen van de populatie van Amsterdam')
st.write('Is het mogelijk om de populatie van Amsterdam te voorspellen aan de hand van andere variabelen zoals hierboven getoond. Deze variabelen geven direct aan of er mensen vertrekken of bijkomen. Er zijn meer gegevens beschikbaar over Amsterdam. Een van deze variabelen waar we eerst onderzoek naar doen is werkloosheid en aantal banen. Er zal gekeken worden of deze variabelen de populatie van Amsterdam kunnen voorspellen.')
st.write('Om een lineair model op te stellen moet er eerst gekeken worden of de totale populatie lineair afhankelijk lijkt van de variablen.')

st.subheader("Check Lineariteit: Voorspellende variabelen tegen populatie")

show_line = st.checkbox('Toon regressielijn')

# Twee scatterplots om te kijken of de totale populatie lineair afhankelijk lijkt voor het totaal aantal banen en werkloosheid
fig4, ax4 = plt.subplots()
sns.scatterplot(data=data, x='TotaalBanen_111', y='TotaleBevolking_1', ax=ax4, color='blue', label="Totaal aantal banen tegen populatie")
if show_line:
    sns.regplot(data=data, x='TotaalBanen_111', y='TotaleBevolking_1', ax=ax4, scatter=False, color='red', label="Regression Line", ci=None)

# Voeg titel en labels toe
ax4.set_title('Totaal aantal banen tegenover totale populatie')
ax4.set_xlabel('Totaal aantal banen (x1000)')
ax4.set_ylabel('Populatie')

# Plot de vierde plot
st.pyplot(fig4)

fig5, ax5 = plt.subplots()
sns.scatterplot(data=data, x='Werkloosheid_154', y='TotaleBevolking_1', ax=ax5, color='green', label="Werkloosheid tegen populatie")
if show_line:
    sns.regplot(data=data, x='Werkloosheid_154', y='TotaleBevolking_1', ax=ax5, scatter=False, color='red', label="Regression Line", ci=None)

# Voeg titel en labels toe 
ax5.set_title('Werkloosheid tegenover totale populatie')
ax5.set_xlabel('Werkloosheid')
ax5.set_ylabel('Populatie')

# Plot de vijfde plot
st.pyplot(fig5)

st.write('Zoals in de bovenste grafiek te zien is, die van het totaal aantal banen. Lijkt er een lineair verband te zijn met de totale populatie. Met de tweede grafiek lijkt dit niet zo te zijn. Dus wordt alleen het totaal aantal banen meegenomen in het opstellen van het model.')

#######
# Lineair model opstellen
st.subheader("Toepassen lineaire regressie: voorspellen van de totale populatie met het totale aantal banen.")

# Alleen gevulde data selecteren
data_gevuld = data[~data['TotaalBanen_111'].isna()]

# Bepaal de voorspellende en afhankelijke variabelen
X = data_gevuld[['TotaalBanen_111']]  # Predictor variables
y = data_gevuld['TotaleBevolking_1']  # Response variable

# Maak en pas het model toe
model = LinearRegression()
model.fit(X, y)

# Verkrijg de waardes van de vergelijking
coefficients = model.coef_
intercept = model.intercept_

# Toon de vergelijking
st.write(f"Regressie vergelijking: Populatie = {coefficients[0]:.2f} * Totaal aantal banen + {intercept:.2f}, dit is de vergelijking die het model geeft")
st.write("Als het aantal banen groter wordt zal het aantal inwoners met 750 toenemen per 1000 banen.")
st.write("Hieronder is de grafiek te zien waarin de werkelijke populatie getoond wordt en de voorspelde populatie aan de hand van het model. En de grafiek van de werkelijke waarde en de lijn voor de voorspelde waarde van het model tegenover de tijd.")

# Voorspel de waardes
y_pred = model.predict(X)

# Voeg waardes toe om te kunnen plotten
data_gevuld['Population_Predicted'] = y_pred

# Plot voor de werkelijke en voorspelde populatie tegenover elkaar
fig8, ax8 = plt.subplots()
sns.scatterplot(data=data_gevuld, x='TotaalBanen_111', y='TotaleBevolking_1', ax=ax8, label='Werkelijke populatie', color='blue')
sns.lineplot(data=data_gevuld, x='TotaalBanen_111', y='Population_Predicted', ax=ax8, label='Voorspelde populatie', color='red')

# Voeg titel en labels toe
ax8.set_title('Totaal aantal banen tegenover werkelijke en voorspelde populatie')
ax8.set_xlabel('Total aantal banen (x1000)')
ax8.set_ylabel('Populatie')

# Plot de achtste plot
st.pyplot(fig8)

# Plot de voorspelde waarden tegenover de werkelijke waarden
fig6, ax6 = plt.subplots()
sns.scatterplot(data=data_gevuld, x='Perioden', y='TotaleBevolking_1', ax=ax6, label='Werkelijke populatie', color='blue')
sns.lineplot(data=data_gevuld, x='Perioden', y='Population_Predicted', ax=ax6, label='Voorspelde Populatie', color='red')

# Voeg titel en labels toe
ax6.set_title('Werkelijke tegen voorspelde Populatie over de tijd')
ax6.set_xlabel('Jaar')
ax6.set_ylabel('Populatie')

# Plot de zesde plot
st.pyplot(fig6)

# Knik uitleggen
st.write("Er lijkt een knik in het model te zitten voor het jaar 2020. Waarom is dit? Dit hebben wij verder onderzocht aan de hand van de volgende grafiek.")

# Maak de zevende plot van het totaal aantal banen
fig7, ax7 = plt.subplots()
sns.barplot(data=data_gevuld, x='Perioden', y='TotaalBanen_111', ax=ax7)

# Voeg titel en labels toe
ax7.set_title('Totaal aantal banen per jaar')
ax7.set_xlabel('Jaar')
ax7.set_ylabel('Totaal aantal banen (x1000)')

# x-as labels draaien
plt.xticks(fontsize=10, rotation=90)

# Plot de zevende plot
st.pyplot(fig7)

st.write("In 2020 neemt het totaal aantal banen niet toe, zoals in de jaren ervoor en erna. Een soort gelijk iets was ook te zien in de grafiek van de inkomende populatie. Dit heeft mogelijk met Covid-19 te maken gehad. Maar dit heeft dus zoals te zien in de grafiek van het model wel invloed op het model zelf.")

# Toon de R-squared waarde
r_squared = model.score(X, y)
st.write(f"R-squared: {r_squared:.4f}, dit is het voorspellend vermogen van het model. Dit percentage van de variantie wordt opgevangen door het model. Het aantal banen lijkt dus een goede voorspeller te zijn voor het bepalen van de totale populatie van Amsterdam.")
st.write('Het bepalen van de totale populatie kan dus gedaan worden met het aantal banen. Maar er zullen ook nog mogelijk andere variabelen zijn die hier invloed op kunnen hebben. Hier kan nog verder onderzoek naar gedaan worden. Er kan dan mogelijk een nieuw model opgesteld worden, die mogelijk beter de populatie kan voorspelen.')
st.write('Aan de hand van het vinden en toevoegen van extra variabelen kan er ook bepaald worden waarin juist naar gekeken kan of moet worden om eventueel invloed te hebben op de totale populatie van Amsterdam.')
st.write('Op deze manier kan door Amsterdam bepaald worden of zij groter of juist niet willen worden, om zo eventueel problemen zoals de woningcrisis te kunnen voorkomen of voor te zijn.')
