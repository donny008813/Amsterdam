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
                          select=['Perioden','TotaleBevolking_1','Mannen_2','Vrouwen_3']))
print(data.head(20))

scatter = sns.scatterplot(data, x = 'Perioden', y = 'TotaleBevolking_1')

st.pyplot(scatter)
