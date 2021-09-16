
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from wordcloud import WordCloud
from matplotlib import pyplot as plt
import re

path="/content/gdrive/MyDrive/visualization_challenge_1_analyze_and_visualize_the_food_delivery_time_for_different_cuisines/new_data.csv"


def load_data():
  data=pd.read_csv(path)
  return data

data=load_data()

# -- Set page config
apptitle = 'food_delivery'


# Title the app
st.title('Location Wise Food Delivery Time For Different Cuisines')


select = st.sidebar.selectbox('Select a State',data['state'].unique())


state_loc = data[data['state']==select]['Rest_area'].unique()

loc=st.sidebar.selectbox("Select Restaurant Location",state_loc)


@st.cache
def cuisi_list(col):
  cuisines=[]
  cuisines_list=set()
  for i in col:
    cuisines.append(i.split(","))
    for i in cuisines:
      for j in i:
        cuisines_list.add(j)
  return cuisines_list

@st.cache
def group_cuis():
  li=cuisi_list(data[(data['state']==select)&(data['Rest_area']==loc)]['Cuisines'])
  return li

lis=group_cuis()


cuisines_sel=st.sidebar.selectbox("Select Cuisines",lis)


data['Average_Cost']=data['Average_Cost'].str.extract("(\d+)")


@st.cache
def av_price():
  pri=data[(data['state']==select)&(data['Rest_area']==loc)&(data['Cuisines'].str.contains(re.compile(cuisines_sel)))]['Average_Cost'].unique()
  return pri

prices=av_price()



avg_price = st.sidebar.radio("Average Price",prices)

import plotly.express as px

data['Delivery_Time']=data['Delivery_Time'].str.extract('(\d+)')

@st.cache
def cuisi_list1(col):
  cuisines=[]
  cuisines_list=list()
  for i in col:
    cuisines.append(i.split(","))
    for i in cuisines:
      for j in i:
        cuisines_list.append(j)
  return cuisines_list


#list_cuis=cuisi_list1(data[(data['state']==select)&(data['Rest_area']==loc)]['Cuisines'])

#st.write(list_cuis.to_string())
@st.cache
def all_str():
  text=""
  list_cuis=cuisi_list1(data[(data['state']==select)&(data['Rest_area']==loc)]['Cuisines'])
  for i in list_cuis:
    text+=" "+i
  return text  

txt=all_str()






@st.cache
def word_cloud():
  plt.figure(figsize = (8, 8), facecolor = None)
  plt.axis("off")
  wordcloud = WordCloud(width = 500, height = 500,
                background_color ='white',
                min_font_size = 10).generate(txt)
  plt.imshow(wordcloud)
  plt.show()

word_cloud_plot=word_cloud()
st.set_option('deprecation.showPyplotGlobalUse', False)


col1, col2 = st.columns(2)

col1.subheader("Famous Cuisines in "+loc+", "+select)
col1.pyplot(word_cloud_plot)


@st.cache
def top_rest():
  temp=(data[(data['Rating'].str.contains("(\d+.\d+)"))&(data['state']==select)&
            (data['Rest_area']==loc)].astype({'Rating':'float'}))
  temp['rank_data']=temp.groupby(['state','Rest_area'])['Rating'].rank(method='max')
  temp2=temp[(temp['rank_data']<6)][['Restaurant','rank_data']]
  temp2['Restaurant']=temp2['Restaurant'].str.extract("(\d+)")
  temp2['Restaurant']=temp2['Restaurant'].astype('category')
  temp2['rank_data']=temp2['rank_data'].astype('float')
  temp2=temp2.sort_values('rank_data',ascending=True)
  return temp2






col2.subheader(f"Top Restaurants in "+loc)


@st.cache
def top_ten():
  rank_res=top_rest()
  #x, y = rank_res['Restaurant'].values,rank_res['rank_data'].values
  #fig = go.Figure(data=[go.Bar(x=x, y=y)])
  fig = px.bar(rank_res, x='Restaurant', y="rank_data",color="Restaurant")
  fig.update_xaxes(type='category')
  fig.update(layout_showlegend=False)
  fig.update_layout(autosize=False,width=600,height=400,)
  fig.show()
  return fig


top_ten_plot=top_ten()

col2.plotly_chart(top_ten_plot)