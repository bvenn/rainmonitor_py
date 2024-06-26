import os
import pandas as pd
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
from io import StringIO
import streamlit as st
import plotly.express as px
import time
import plotly.graph_objs as plotly
from datetime import datetime, timedelta

# ------------ SETTINGS ------------
temp_dir = os.environ.get('TEMP', '/tmp')
page_title = "Rain Monitor"
page_icon = "cloud_with_rain"
# ----------------------------------

# hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Read the file into a DataFrame
stations_df = pd.read_csv('stations.csv',dtype={'stationID':str})

col1, col2 = st.columns(2)
with col1:
    # Allow the user to edit the DataFrame
    edited_df = st.data_editor(stations_df)

with col2:
    # If the user clicks the "Update" button
    if st.button('Update list of stations'):
        # Save the edited DataFrame to a CSV file
        edited_df.to_csv('stations.csv', index=False)
        st.success('File updated successfully.')

# Download the zip file from the FTP server
is_clicked01 = st.button("Download and extract data")
if is_clicked01:

    ## Read the number of stations from the file
    #with open('stations.txt', 'r') as f:
    #    lines = f.readlines()
#
    #entries = []
    #for line in lines:
    #    entry = line.strip().split(',')
    #    entries.append(entry)

    # Filter the first two occurrences of True
    filtered_df = edited_df[edited_df['Select_2'] == True]
    
    # Split the stationID at the hyphen
    split_df = filtered_df['stationID'].str.split(' - ', expand=True)
    split_df.columns = ['id', 'city']

    # Store the two parts in individual parameters      
    fstStation_no: str= split_df.iloc[0]['id']
    fstStation_city: str = split_df.iloc[0]['city']
    sndStation_no: str = split_df.iloc[1]['id']
    sndStation_city: str = split_df.iloc[1]['city']
    
    # Creating the DataFrame wi
    # Define the URL of the zip file and the target directory
    zip_urlKaiserslautern = "ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/recent/stundenwerte_RR_{}_akt.zip".format(fstStation_no)
    zip_urlNennig = "ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/recent/stundenwerte_RR_{}_akt.zip".format(sndStation_no)
    #
    # st.write("**FirstStation**:\r  - {}\r  - {}\r  - {}\r  - {}\r\r".format(fstStation_no,fstStation_city,zip_urlKaiserslautern,type(fstStation_no)),unsafe_allow_html=True)
    #
    # st.write("**SecondStation**:\r  - {}\r  - {}\r  - {}\r  - {}".format(sndStation_no,sndStation_city,zip_urlNennig,type(fstStation_no)),unsafe_allow_html=True)
    
    myProgress = st.progress(0., text="Downloading zip archive data...")
        

    # Open the zip file from the URL
    with urlopen(zip_urlKaiserslautern) as response:
        with ZipFile(BytesIO(response.read())) as zip_file:
            # Find the file that starts with 'produkt'
            matching_files = [file for file in zip_file.namelist() if file.startswith('produkt')]

            # Extract the matching file
            if matching_files:
                matching_file_content = zip_file.read(matching_files[0])
                (matching_file_content.decode('utf-8'))
            else:
                print("No file found that starts with 'produkt'")

    # Open the zip file from the URL
    responseF = urlopen(zip_urlKaiserslautern)
    zip_fileF = ZipFile(BytesIO(responseF.read())) 
    # Find the file that starts with 'produkt'
    matching_filesF = [file for file in zip_fileF.namelist() if file.startswith('produkt')]
    # Extract the matching file
    matching_file_contentF = zip_fileF.read(matching_filesF[0])
    fstStation = (matching_file_contentF.decode('utf-8'))

    # Open the zip file from the URL
    responseS = urlopen(zip_urlNennig)
    zip_fileS = ZipFile(BytesIO(responseS.read())) 
    # Find the file that starts with 'produkt'
    matching_filesS = [file for file in zip_fileS.namelist() if file.startswith('produkt')]
    # Extract the matching file
    matching_file_contentS = zip_fileS.read(matching_filesS[0])
    sndStation = (matching_file_contentS.decode('utf-8'))

    dfK = pd.read_csv(StringIO(fstStation), sep=';', skipinitialspace=True, encoding='latin1')
    dfN = pd.read_csv(StringIO(sndStation), sep=';', skipinitialspace=True, encoding='latin1')





    ##st.markdown("Downloading zip file...",unsafe_allow_html=True)
    #response = urlopen(zip_urlKaiserslautern)
    #zipfile = ZipFile(BytesIO(response.read()))
    #zipfile.extractall(temp_dir)
#
#
#
    #responseN = urlopen(zip_urlNennig)
    #zipfileN = ZipFile(BytesIO(responseN.read()))
    #zipfileN.extractall(temp_dir)
#
    #myProgress.progress(0.5, text="Download and extraction finished!")
    #time.sleep(0.5)
    ##st.markdown("download finished",unsafe_allow_html=True)    
    #myProgress.progress(0.6, text="Loading data...")
    #time.sleep(0.5)
    #
    #st.write("-----------------------------")
    ## Find the csv file in the subfolder "ftpRainDataRecent"
    #file_pathK = None
    #file_pathN = None
    #for root, dirs, files in os.walk(temp_dir):
    #    #st.write("dirs -----------------------------")
    #    #for dir in dirs: st.write(dir)
    #    #st.write("-----------------------------")
    #    for file in files:
    #        if file.startswith("produkt"): st.write(file)
    #        
    #        if file.startswith('produkt_rr_stunde') & file.endswith('.txt') & file.__contains__(fstStation_no):
    #            file_pathK = os.path.join(root, file)
    #            st.write(file_pathK)
    #        if file.startswith('produkt_rr_stunde') & file.endswith('.txt') & file.__contains__(sndStation_no):
    #            file_pathN = os.path.join(root, file)
    #            st.write(file_pathN)
    #            break
#
    #st.write("-----------------------------")
#
    ## Check if the file was found
    #if file_pathK is None :
    #    st.markdown("The fst file could not be found: {}".format(file_pathK))
    #    
#
    #if file_pathN is None:
    #    st.markdown("The snd file could not be found: {}".format(file_pathN))
    #    
#
#
    ## Load the semicolon-separated file
    ##st.markdown("Loading data...",unsafe_allow_html=True) # end=""
    ##dfK = pd.read_csv(file_pathK, sep=';', encoding='latin1')
    ##dfN = pd.read_csv(file_pathN, sep=';', encoding='latin1')
    

    myProgress.progress(1.0, text="Data loaded!")
    # Parse the datetime and select the precipitation column
    dfK['MESS_DATUM'] = pd.to_datetime(dfK['MESS_DATUM'], format='%Y%m%d%H', utc=True).dt.tz_convert('Europe/Berlin')#'%Y%m%d%H%M')
    dfN['MESS_DATUM'] = pd.to_datetime(dfN['MESS_DATUM'], format='%Y%m%d%H', utc=True).dt.tz_convert('Europe/Berlin')#'%Y%m%d%H%M')
    
    now = pd.Timestamp.now(tz='Europe/Berlin')

    # Filter rows that are within the last two weeks
    two_months_ago = now - pd.Timedelta(weeks=8)
    two_weeks_ago = now - pd.Timedelta(weeks=2)

    filtered_dfK = dfK[dfK['MESS_DATUM'] >= two_months_ago]
    filtered_dfN = dfN[dfN['MESS_DATUM'] >= two_months_ago]
    filtered_dfK = filtered_dfK[filtered_dfK['R1'] >= 0]
    filtered_dfN = filtered_dfN[filtered_dfN['R1'] >= 0]


    # Plot the data
    figK = px.histogram(filtered_dfK, x='MESS_DATUM', y='R1', title='R1 vs Time', nbins=int(len(filtered_dfK)))
    figN = px.histogram(filtered_dfN, x='MESS_DATUM', y='R1', title='R1 vs Time', nbins=int(len(filtered_dfN)))
    
    figK.update_layout(title=fstStation_city)
    figN.update_layout(title=sndStation_city)

    figK.update_xaxes(
        title='Time',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True,
        range=[two_weeks_ago, now]
    )
    
    figK.update_yaxes(
        title='Regenmenge (mm)',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True
    )


    figN.update_xaxes(
        title='Time',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True,
        range=[two_weeks_ago, now]
    )
    
    figN.update_yaxes(
        title='Regenmenge (mm)',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True
    )
    
    myfigK = px.histogram(filtered_dfK, x='MESS_DATUM', y='R1',  nbins=int(len(filtered_dfK)),color_discrete_sequence=['#1f77b4'], opacity=0.5)
    myfigN = px.histogram(filtered_dfN, x='MESS_DATUM', y='R1',  nbins=int(len(filtered_dfN)),color_discrete_sequence=['#ff7f0e'], opacity=0.5)

    layoutC = plotly.Layout(
        title='Regenmengen der letzten 14 Tage in {} und {}'.format(fstStation_city, sndStation_city),
        xaxis=dict(title='Value',range=[two_weeks_ago, pd.Timestamp.now()]),
        yaxis=dict(title='Count'),
        barmode='overlay',
        legend=dict(x=0.7, y=1),
        width= 600,
        height=400
    )

    figXCX = plotly.Figure(data = myfigK.data + myfigN.data, layout=layoutC)

    figXCX.update_xaxes(
        title='Time',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True,
        range=[two_weeks_ago, now]
    )
    
    figXCX.update_yaxes(
        title='Regenmenge (mm)',
        mirror='all',
        ticks='inside',
        showgrid=False,
        showline=True,
        zeroline=True
    )
    
    st.plotly_chart(figXCX,use_container_width=True,theme=None)


    st.markdown("<i>Abbildung 1: Regenmengen sind angegeben als L / qm innerhalb einer Stunde</i>",unsafe_allow_html=True)

    tmpK = filtered_dfK[['MESS_DATUM','R1']].rename(columns={'R1': fstStation_city})
    tmpN = filtered_dfN[['MESS_DATUM','R1']].rename(columns={'R1': sndStation_city})

    daily_sumK = tmpK.groupby(tmpK['MESS_DATUM'].dt.date)[fstStation_city].sum()
    daily_sumN = tmpN.groupby(tmpN['MESS_DATUM'].dt.date)[sndStation_city].sum()
    daily_sums = pd.merge(daily_sumK, daily_sumN, on='MESS_DATUM', how='outer')


    weekly_sumK = tmpK.groupby(tmpK['MESS_DATUM'].dt.isocalendar().week)[fstStation_city].sum()
    weekly_sumN = tmpN.groupby(tmpN['MESS_DATUM'].dt.isocalendar().week)[sndStation_city].sum()
    weekly_sums = pd.merge(weekly_sumK, weekly_sumN, on='week', how='outer')


    weekly_sums.index.name = ('KW (aktuell: {})'.format(now.isocalendar()[1]))
    daily_sums.index.name = ('Datum')
    
    container = st.container()
    # Create content for the second column
    with container:
        col1, col2 = st.columns(2)
        col1.markdown('#### Tägliche Regenmengen in L/qm')
        col1.dataframe(daily_sums,height=800)

        col2.markdown('#### Wöchentliche Regenmengen in L/qm')
        col2.dataframe(weekly_sums)

    mylist = (daily_sums.index.tolist())
    peter = '<br>'.join([d.strftime('%Y-%m-%d') for d in mylist])

    concatenated_fst = '<br>'.join(daily_sums[fstStation_city].round(2).astype(str))
    concatenated_snd = '<br>'.join(daily_sums[sndStation_city].round(2).astype(str))
    tablestyle = "<style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 65%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style>"
    table ="""Columns at 21:00 indicate the precipitation between 20:00 and 21:00 MEZ <br><br>{}<table>
            <tr><td>{}</td><td>{}</td><td>{}</td></tr>
            <tr><td>{}</td><td>{}</td><td>{}</td></tr></table>""".format(tablestyle, 'Datum', fstStation_city, sndStation_city, peter, concatenated_fst, concatenated_snd)
    st.markdown(table,unsafe_allow_html=True)


    # works if local folder is defined, not if tmp folder is specified
    # Remove the downloaded files
    #for filename in os.listdir(temp_dir):
    #    file_path = os.path.join(temp_dir, filename)
    #    try:
    #        if os.path.isfile(file_path):
    #            os.remove(file_path)
    #            #st.write(f'Removed {file_path}')
    #    except Exception as e:
    #        st.write(f'Error deleting {file_path}: {e}')
    



# cd C:\Users\beve\source\repos\rainmonitor_py
## conda create –n rainmonitor python=3.12
# conda activate rainmonitor
## pip install –r requirements.txt
# streamlit run main.py

# oder einfach vs code terminal und streamlit run main.py

# dont forget to set:
# Azure Ressource -> settings -> configuration -> general -> startup command: run.sh

# DOCKERFILE
# FROM python:3
# WORKDIR /app
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# EXPOSE 8501	
# CMD [ "streamlit", "run", "app.py" ]