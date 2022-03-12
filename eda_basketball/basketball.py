#Importing Libraries
import streamlit as stl
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

stl.title('NBA Player Stats Explorer')

stl.markdown("""
    App Performs Webscraping of NBA Player stats data!
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [basketball-reference.com](https://www.basketball-reference.com/).
""")

stl.sidebar.header('User Input Features')
selected_year = stl.sidebar.selectbox('Year', list(reversed(range(1950,2021))))

#Web scraping of NBA Players
@stl.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url,header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) #Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'],axis=1)
    return playerstats
playerstats = load_data(selected_year)

#SideBar-Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = stl.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team) # options,default option values

#Sidebar position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = stl.sidebar.multiselect('Position',unique_pos,unique_pos)


#Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

stl.header('Display Player Stats of Selected Team(s)')
stl.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
df_selected_team['FG%'] = df_selected_team['FG%'].astype(bytes)
df_selected_team['3P%'] = df_selected_team['3P%'].astype(bytes)
df_selected_team['2P%'] = df_selected_team['2P%'].astype(bytes)
df_selected_team['eFG%'] = df_selected_team['eFG%'].astype(bytes)
df_selected_team['FT%'] = df_selected_team['FT%'].astype(bytes)
stl.dataframe(df_selected_team)

#Download NBA Player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()   #Strings <--> Bytes conversion
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

stl.markdown(filedownload(df_selected_team),unsafe_allow_html=True)

#HeatMap
if stl.button('Intercorrelation HeatMap'):
    stl.header('Intercorrelation Matrix HeatMap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f,ax = plt.subplots(figsize=(7,5))
        ax = sns.heatmap(corr,mask=mask,vmax=1,square=True)
    stl.pyplot(f)
