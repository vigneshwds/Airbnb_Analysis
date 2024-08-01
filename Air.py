import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from PIL import Image


def mainfile():
    file=pd.read_csv("C:/Capstone files/Airbnb_trend_analysis.csv")
    return file

air_df1=mainfile()

def geoGraph():
  
  st.subheader(":blue[Geospatial Distribution of Listings across world]")
  fig=px.scatter_mapbox(air_df1, lon='Longitude', lat='Latitude', color='Price', size='Accommodates', color_continuous_scale='rainbow', hover_name='City', range_color=(0, 200), mapbox_style='carto-positron', zoom=0.4)
  fig.update_layout(width=1200,height=600,title='Airbnb Listings across the world')
  st.plotly_chart(fig)

def country_filter(country):
  country_df=air_df1[air_df1['Country']==country]
  country_df.reset_index(drop=True, inplace=True)

  #Plot
  fig=px.scatter_mapbox(country_df, lon='Longitude', lat='Latitude', color='Price', size='Accommodates', color_continuous_scale='rainbow', hover_name='Listing Name', range_color=(0, 200), mapbox_style='carto-positron', zoom=11)
  fig.update_layout(width=1150,height=800,title=f'Airbnb Listings across {country}')
  st.plotly_chart(fig)

  st.markdown("**:red[Note :] Above Map shows our available listings across the country with the filtered options for the  overall price range and maximum accommodation details.**")

  return country_df

def price_analysis(df):
  #Removing outliers
  Q1=df['Price'].quantile(0.25)
  Q3=df['Price'].quantile(0.75)

  #Calculate interquartile range (IQR)
  IQR= Q3-Q1

  #Defining outlier thereholds
  lower_bound= Q1 - 1.5*IQR
  upper_bound= Q3 + 1.5*IQR

  #Create new datafram without outliers
  clear_price=df[(df['Price']>=lower_bound) & (df['Price']<=upper_bound)]

  filter_avg=clear_price[clear_price['Host Neighbourhood']!='Not Mentioned'].reset_index()
  avg_price_analy=filter_avg.groupby('Host Neighbourhood')[['Price']].mean().reset_index().rename(columns={'Price':'Average Price', 'Host Neighbourhood':'Neighbourhoods'})
  avg_price_analy=avg_price_analy.sort_values('Average Price', ascending=False)

  #plot
  fig=px.bar(avg_price_analy, x='Neighbourhoods', y='Average Price', title=f'Average Airbnb Price by Neighborhoods in {country}', color_discrete_sequence=px.colors.sequential.Blues_r)
  st.plotly_chart(fig)

  st.markdown("**:red[Note :] Average price analysis bar graph of Neighborhoods.**")
  st.markdown("**:red[Interpretation :] Bar graph represent the average price range of Neighborhoods from high to low and this bar chart helps to choose a right neighbourhood based on your budget.**")

  #Plots
  col1, col2=st.columns(2)

  with col1:  
    fig=px.bar(clear_price, x='Room Type', y='Price', hover_name='Listing Name', title=f'Price Analysis and Commonly Preferred Room Type in {country}', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig)

  with col2:   
    fig=px.pie(values=clear_price['Price'], names=clear_price['Room Type'], hole=0.7, title=f'Commonly Preferred Room Type in {country}', color_discrete_sequence=px.colors.sequential.Emrld_r)
    st.plotly_chart(fig)
  st.markdown("**:red[Note :] Bar and Donut chart of Room type price analysis**")
  st.markdown("**:red[Interpretation :] The bar and donut charts help to illustrate how price listings vary by room type. Entire home/apartment listings are comparatively higher than private and shared rooms.**")  

  return clear_price

def responds_time(df):
    df_res_time=pd.DataFrame(df.groupby('Host Response Time')[['Price', 'Bedrooms']].sum()).reset_index().rename(columns={'Bedrooms' : 'Number of Rooms booked'})
    filt_res_time=df_res_time[df_res_time['Host Response Time']!='Not Mentioned']

    #Plot
    fig=px.bar(filt_res_time, x="Number of Rooms booked", y="Host Response Time", hover_data='Price', title='Listings booking based on host response time', color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig) 

    st.markdown("**:red[Note :] Booking analysis bar chart based on Host Response time**")
    st.markdown("**:red[Interpretation :] In this bar graph clearly shows whenever the host's response times is quick, number of booking listings is high**")

def rev_filt(df):
    filter_rev=df[df['Host Neighbourhood']!='Not Mentioned'].reset_index()
    top_review=filter_rev.groupby('Host Neighbourhood')[['Number of Reviews']].sum()

    top_review=top_review.sort_values('Number of Reviews', ascending=False).reset_index()[:15]
    top_review=top_review.rename(columns={'Host Neighbourhood':'Neighborhood'})
    top_review

    #Plot
    fig=px.line(x=top_review['Neighborhood'], y=top_review['Number of Reviews'], markers=True, title=f'Top Reviewed Neighborhood in {country}')
    fig.update_layout(xaxis_title='Neighborhood', yaxis_title='Number of Reviews')
    st.plotly_chart(fig)

    st.markdown("**:red[Note :] Trend analysis of top places in the selected country based on reviews**")
    st.markdown("**:red[Interpretation :]  By using the trend analysis we can easily identify the top Neighborhood's in the selected country, based on that we can book the listings accordingly!!**")

#Creating a new Dataframe that displaying number of listing count by each type of rooms
def r_type(df):
    room_types=df['Room Type'].value_counts().reset_index()
    room_types.columns=['Room Type', 'Total Count']


    #PLot
    col1, col2=st.columns(2)
    with col1:
      fig=px.pie(room_types, values='Total Count', names='Room Type', hole=0.7, title=f'Types of Home/Room availability in {country}')
      st.plotly_chart(fig)
      
    with col2:  
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
      st.write('')
     
      st.dataframe(room_types) 

    st.markdown("**:red[Note :] Types of Room in the selected country and their availability counts**")
    st.markdown("**:red[Interpretation :]  The majority of listings on Airbnb are for entire homes or apartments, followed by private rooms and shared rooms with the respective listings.**")

    return room_types

def min_nig(df):
    min_night_count=df.groupby('Minimum Nights').size().reset_index(name='Counts')
    filt=min_night_count[:11]

    #Plot
    fig=px.bar(filt, x='Minimum Nights', y='Counts', title=f'Stay Requirments by Minimum nights in {country}')
    st.plotly_chart(fig)

    st.markdown("**:red[Note :] Stay requirments by minimum nights in the selected country**")
    st.markdown("**:red[Interpretation :]  The majority of listings on Airbnb have a minimum stay requirement of 1 to 3 nights, with the given listings, respectively.**")
    

def top_citys(df):
    filtered_neigh=df[df['Host Neighbourhood']!='Not Mentioned']
    top_neighborhoods=filtered_neigh['Host Neighbourhood'].value_counts().nlargest(10).reset_index()
    top_neighborhoods

    #Plot
    fig=px.bar(top_neighborhoods, x='Host Neighbourhood', y='count', title=f'Top Neighborhoods by listing counts in {country}', color_discrete_sequence=px.colors.sequential.Bluyl_r)
    fig.update_layout(xaxis_title="Top Neighborhood", yaxis_title='Listing Counts')
    st.plotly_chart(fig)

    st.markdown("**:red[Note :] Bar graph represents the top neighborhood based on the number of listing counts**")
    st.markdown("**:red[Interpretation :]  By using this graph we can identify where the majority of listings available in Neighborhoods wise**")

def avail_days(df):
    col1, col2=st.columns(2)

    #Plot
    with col1:
      avail_90=px.sunburst(df, path=['Room Type', 'Bed Type', 'Bathrooms'], values='Availability_90', width=550, height=450, title='Available 90 days', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
      st.plotly_chart(avail_90)
    with col2:
      avail_365=px.sunburst(df, path=['Room Type', 'Bed Type', 'Bathrooms'], values='Availability_365', width=550, height=450, title='Available 365 days', color_discrete_sequence=px.colors.sequential.haline)
      st.plotly_chart(avail_365)

    st.write('')  
    st.write('')
    st.write('')
    st.write('')

    col1, col2=st.columns(2)

    #Plot
    with col1:
      avail_30=px.sunburst(df, path=['Room Type', 'Bed Type', 'Bathrooms'], values='Availability_30', width=550, height=450, title='Available 30 days', color_discrete_sequence=px.colors.sequential.Blues_r)
      st.plotly_chart(avail_30)

    with col2:
      avail_60=px.sunburst(df, path=['Room Type', 'Bed Type', 'Bathrooms'], values='Availability_60', width=550, height=450, title='Available 60 days', color_discrete_sequence=px.colors.sequential.Greens_r)
      st.plotly_chart(avail_60)    

    st.markdown("**:red[Note :] This is Sunburst graph helps to analysis multiple features, including Room Type, Bed Type, Number of Bathrooms**")
    st.markdown("**:red[Interpretation:]** \
             **<br>1. Based on these Sunburst graphs, the majority of listings are available for 365 days, followed by 90, 60, and 30 days. \
             <br>2. All three types of rooms use real beds. \
             <br>3. Multi-bathroom setups are highest in Home/Apartment type listings, with a maximum of 4.**", 
             unsafe_allow_html=True)



#Streamlit

st.title(":red[Airbnb Analysis]")

with st.sidebar:
    st.image(Image.open(r'C:/Capstone files/Airbnb_Analysis/slider.png'), width=90)

    user=option_menu("Menu", ["Home", "Data Exploration", "About"],icons=["house", "graph-up", "book"], menu_icon="cast")

if user=='Home':
    st.image(Image.open(r'C:/Capstone files/Airbnb_Analysis/download.png'))
    st.subheader(':red[Project Overview]')
    st.markdown('**The Airbnb project is focused on analyzing and visualizing Airbnb listings data to derive meaningful insights. The project involves data cleaning, exploration, and analysis using various Python libraries, culminating in a Streamlit dashboard to present the findings interactively**')
    st.markdown("**:blue[Domain :] Travel Industry, Property Managment and Tourism**")
    st.subheader(':red[Project Goal]')
    st.markdown('**1.Data Cleaning and Preprocessing**')
    st.markdown('**2.Explorator Data Analysis**')
    st.markdown('**3.Geospatial Analysis**')
    st.markdown('**4.Data Visualization**')
    st.markdown('**5.Streamlit Dashboard**')
    st.write('')

    st.markdown("**:blue[Technologies Used :] Pandas, Seaborn, Python Scripting, MongoDB, PowerBi, Streamlit and Plotly**")
    st.write('')

    st.markdown("**:blue[PowerBi Dashboard Display]**")
    #Add checkbox
    show_dashboard=st.checkbox(":red[Show the Dashboard image]")
    if show_dashboard:
       st.image(Image.open(r"C:/Capstone files/Airbnb_Analysis/PowerBi_Dashboard.PNG"))

    st.write('')   

    st.markdown("**:blue[Github link - ] https://github.com/vigneshwds/Airbnb_Analysis.git**")


elif user=='Data Exploration':
    st.markdown("**Hello, Folks! Please find the available listings across the world on our Airbnb**")

    geoGraph()

    st.markdown("**:red[Note :] Above Map shows our available listings across the world**")
    st.markdown("**:green[Please use the below drop down box to explore the listings, country wise!!]**")

    col1, col2=st.columns(2)
    with col1:
      country=st.selectbox("**:blue[Select the country you want to explore?]**", air_df1['Country'].unique())

    cf=country_filter(country)

    tab1, tab2, tab3, tab4 = st.tabs(['**Price Analysis**', '**Review Analysis**', '**Room Type Analysis**', '**Room Availabilities**'])

    with tab1:
       cp=price_analysis(cf)

       st.write('')
       st.write('')

       col1, col2=st.columns(2)
       
    
    with tab2:
       st.markdown('**Top Reviewed Neighborhood in the selected country**')

       rf=rev_filt(cf)

       col1, col2=st.columns(2)
       with col1:
        type=st.selectbox('**:blue[Select the Room type]**', cf['Room Type'].unique()) 
       
       rt=cf[cf['Room Type']==type] 

       responds_time(rt)

    with tab3:
       rt=r_type(cf)

       mn=min_nig(cf)


    with tab4:
       tc=top_citys(cf) 

       st.write('')
       st.write('')
       st.write('')

       avail_days(cf)

    #Price analysis, Room type analysis, review analysis, top neighborhood(tab mode)

elif user=='About':
    st.header("About this Project")

    st.subheader(":red[Data Cleaning and Preparation:]")

    st.write('***1. Load the Airbnb dataset and handle missing values and erroneous data.***')
    st.write('***2. Convert data types as necessary for analysis (e.g., converting price strings to numerical values).***')
    st.write('***3. Remove or correct outliers detected through exploratory data analysis.***')
    
    st.subheader(":red[Exploratory Data Analysis (EDA):]")

    st.write('***1. Analyze the distribution of listings across different locations and property types.***')
    st.write('***2. Investigate the relationship between variables such as price, number of reviews, and room types.***')
    st.write('***3. Use visualizations like box plots, scatter plots, and bar charts to identify trends and patterns.***')
    
    st.subheader(":red[Geospatial Analysis:]")

    st.write('***1. Visualize the geographical distribution of Airbnb listings using latitude and longitude data.***')
    st.write('***2. Utilize Plotlys scatter_mapbox to create an interactive map displaying the listings based on various attributes like price and neighborhood***')
    
    st.subheader(":red[Data Visualization:]")

    st.write('***1. Employ Plotly and Seaborn for creating insightful visualizations, including histograms, strip plots, and heatmaps.***')
    st.write('***2. Implement a Streamlit dashboard for interactive exploration and presentation of the data.***')
    
    st.subheader(":red[Streamlit Dashboard:]")

    st.write('***1. Create a user-friendly interface to showcase different analyses.***')
    st.write('***2. Provide features like sidebar navigation for exploring various sections of the analysis.***')
    st.write('***3. Display images, maps, and plots with adjustable parameters for an engaging user experience.***')

