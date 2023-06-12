# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 21:22:41 2023

@author: Yinon Biran
"""
import pandas as pd # this will have the tools of handaling data sets
from matplotlib import pyplot as plt # this we will need for plot display
from IPython.display import display_html #handaling display html style
import seaborn as sns
import sidetable as stb
import os
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
import streamlit as st
import sidetable as std
import altair as alt

##set display of the whole columns -without trimming
sns.set_theme(style="whitegrid")

pd.set_option ('display.max_columns', None)

#using try except due to local files
try:
    #loading the files
    os.chdir(r"E:/YinonBiran/Practicum100/How_to_tell_a_story_based_on_Data_Project/Datasets/")
    
    rest_data_us_df = pd.read_csv(r"E:/YinonBiran/Practicum100/How_to_tell_a_story_based_on_Data_Project/Datasets/rest_data_us.csv")
    
except:
    rest_data_us_df = pd.read_csv(r"/datasets/rest_data_us.csv")

st.title(':blue[Resturants Chains in the LA district Analises]')
st.title('**The main goal of this project is to attract investors, for the possibility of oppening a robo-caffe chain in the LA district.**')
st.title('**This based on data gathered on resturants across town.**')


#drop missing values - they consist only 0.03% they will not effect our goal in this project
rest_data_us_df = rest_data_us_df.dropna()

#Eliminamte " " in the column names 
rest_data_us_df.columns = rest_data_us_df.columns.str.lower().str.replace(' ', '')
#change the name of 'number' column to no_of_seats -fro clarify.
rest_data_us_df.columns = rest_data_us_df.columns.str.lower().str.replace('number', 'no_of_seats')

#change cahin True / false values to - yes / no - more areable to the name of the data. 
rest_data_us_df['chain']=rest_data_us_df['chain'].apply(lambda x: 'yes' if x==True else 'no')

st.markdown("## :blue[The Data frame we have]")
st.write(rest_data_us_df)

st.markdown("## :blue[Data Analysis]")

st.markdown("###  Prprortions of different establishments")
st.markdown("**Lets see how many different types of resturants we have and how much they take from the general size of food establishments.**")

#Group all under the same establishment type counting those Id that are part of these types
rest_type_est = rest_data_us_df.groupby(['object_type'])['id'].nunique().reset_index()

st.markdown("### Prprortions of different establishments Graph")

fig3 = px.pie(rest_type_est, values=rest_type_est.id, names=rest_type_est.object_type,
              color=rest_type_est.object_type,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> Resturant in LA Split by establishment Type </b>")
#fig3.show()
st.plotly_chart(fig3)

st.markdown(":green[**We see that the Resturants in the LA area have dominance over all other establishments.**]")

st.markdown("### Prprortions of Chain / Non-Chain establishments")
st.markdown("**Lets devide all as thos who are considred chains and those which are not chins.**")

#Group all under the same chain / non-chaine type counting those Id that are part of these types
rest_type_chain = rest_data_us_df.groupby(['chain'])['id'].nunique().reset_index()

st.markdown("### Prprortions of Chain / Non-Chain establishments")
#Graph preper and display
fig3 = px.pie(rest_type_chain, values=rest_type_chain.id, names=rest_type_chain.chain,
              color=rest_type_chain.chain,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> Resturant in LA Split by Chain(yes) / Non-Chain(no) Type </b>")
#fig3.show()
st.plotly_chart(fig3)

st.markdown(":green[**We see that the over all Resturants in the LA area are Non-Chain like.**]")

st.markdown("### Prprortions of Chain / Non-Chain establishments number of seats")
#Group all under the same chain / non-chaine type counting those Id that are part of these types
rest_type_chain_seats = rest_data_us_df.groupby(['chain'])['no_of_seats'].sum().reset_index()
st.write(rest_type_chain_seats)
#Proportion graph for seats
fig3 = px.pie(rest_type_chain_seats, values=rest_type_chain_seats.no_of_seats, names=rest_type_chain_seats.chain,
              color=rest_type_chain_seats.no_of_seats,
color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> Resturant in LA Split by Chain(yes) / Non-Chain(no) Type By seats sum</b>")
#fig3.show()
st.plotly_chart(fig3)

st.markdown("### What is the prorportions of each type of resturant from the chain / non-chain types?")
#Chains proportion os rest types
rest_type_chain_est = rest_data_us_df.loc[(rest_data_us_df['chain']=='yes')].groupby(['chain','object_type'])['id'].nunique().reset_index()

#Non-Chains proportion os rest types
rest_type_non_chain_est = rest_data_us_df.loc[(rest_data_us_df['chain']=='no')].groupby(['chain','object_type'])['id'].nunique().reset_index()

#Merge  the two tbles
merged_rest_type_of_chain_est = pd.merge(rest_type_chain_est,rest_type_non_chain_est , how="left", on='object_type').fillna(0).reset_index(drop=True)

#rename the columns and drop thos we dont need
merged_rest_type_of_chain_est.rename(columns={'id_x':'chain_type','id_y':'non_chain_type'},inplace=True)
#drop the columns we do not need
merged_rest_type_of_chain_est.drop(columns=['chain_x','chain_y'], inplace=True)

#plot a bar chart
fig = px.bar(merged_rest_type_of_chain_est, x="object_type", y=["chain_type","non_chain_type"],
             barmode='group')
#fig.show() #
st.plotly_chart(fig)

st.markdown("### What is considred as chain ?")
st.markdown("**Is it large number of establishments with small amount of seats? Or a small number of establishments with high number of seats?**")

#group by type and number of seat getting the avarage of seats
rest_chains_grouped=rest_data_us_df[rest_data_us_df.chain=='yes'].groupby(['object_name'])['no_of_seats'].agg(['count','median']).reset_index()
rest_chains_grouped.columns=['name','no_of_est','average_seating']

st.markdown("### What is considred as chain? - Graph")
##scatter plot graph - seaborn
#fig = sns.scatterplot(data=rest_chains_grouped, x="average_seating", y="no_of_est")
#plt.show()
#st.plotly_chart(fig)    

c = alt.Chart(rest_chains_grouped).mark_circle(size=60).encode(
    x='average_seating',
    y='no_of_est',
    tooltip=['name', 'average_seating', 'no_of_est']
).interactive()

st.markdown("### What is considred as chain?")
st.altair_chart(c, use_container_width=True)       


st.markdown("**We can see that a chain has fewer seats and have more establishments(resturants).**")
st.markdown("**You can see that the most of establishments tha are considered as chain, have around 50 seats.**")
st.markdown("**There are branches that have more but they are not the majority.**")


st.markdown("### What is the Avarage number of seats in LA resturants")

#st.markdown("**We can see that a chain has fewer seats and have more establishments(resturants).**")
#st.markdown("**You can see that the most of establishments tha are considered as chain, have around 50 seats.**")
#st.markdown("**There are branches that have more but they are not the majority.**")

overall_seats_avg = rest_data_us_df.no_of_seats.median()
chain_no_seats_avg = rest_chains_grouped.average_seating.median()
non_chain_temp = rest_data_us_df[rest_data_us_df.chain=='no'].groupby(['object_name'])['no_of_seats'].agg(['count','median']).reset_index()
non_chain_temp.columns=['name','no_of_est','average_seating']
non_chain_no_seats_avg = non_chain_temp['average_seating'].median()

st.write('''The overall avarage of seats in resturants is:''',overall_seats_avg)
st.write('''The avarage of seats in chains resturants is:''',chain_no_seats_avg)
st.write('''The avarage of seats in non-chains resturants is:''',non_chain_no_seats_avg)

st.markdown("### What type of resturant has the most seat?")
st.markdown("**Lets check the number of seats by resturant type**")

#aggragate all resturant by type. count them and sum theire no. of seats
rest_seat_data_by_type = rest_data_us_df.groupby(['object_type']).agg({'id':'count','no_of_seats':'sum'}).reset_index()
#calculate theire avarage no. of seats
rest_seat_data_by_type['average_seating'] = (rest_seat_data_by_type['no_of_seats'] / rest_seat_data_by_type['id']).round(0)
#retrieve the type that has the max no of seats
rest_type = rest_seat_data_by_type.loc[(rest_seat_data_by_type['average_seating'] == rest_seat_data_by_type['average_seating'].max())].reset_index(drop=True)
rest_type_val = rest_type['object_type'].values[0]
rest_type_val_seats = rest_type['average_seating'].values[0]
#print the resault
st.write('''The avarage of most seats in resturants is: ''',rest_type_val,''' type of resturant''')
st.write('''With avarage  number of seats a : ''',rest_type_val_seats , '''seats per resturant''')

#plot a bar chart
fig = px.bar(rest_seat_data_by_type.sort_values(by='average_seating',ascending=False), x="object_type", y="average_seating",
             barmode='group', title = "<b>What type of resturant has the most seat  - Greaph by seats avarage</b>")
#fig.show() #
st.plotly_chart(fig)

st.markdown("### What Street  has the most resturant?")

#return a strin with street name only
def street_name(address):
    #split the string to list
    split_st = address.split(" ")
    #remove all numbers and strings with only 1 charachter
    street = ' ' .join((z for z in split_st if not z.isdigit() and len(z)!=1))
    #return the streat name as upper case string
    return(street.upper())

#Check if the function works 
address = "3708 N Eagle Rock BLVD"
print(street_name(address))

#apply the function on the  address column - creating a street column
rest_data_us_df['street'] = rest_data_us_df['address'].apply(street_name)
           
#Group all resturaunst by street name
rest_data_street_rest = rest_data_us_df.groupby(['street']).agg({'id':'count'}).sort_values(by="id",ascending=False).reset_index()
rest_data_street_rest.rename(columns={"id":"no_of_rest"}, inplace= True)

#get the first top 10 streets
top_ten_streets = rest_data_street_rest.head(10).reset_index(drop=True)
top_ten_streets.rename(columns={"id":"no_of_rest"}, inplace= True)
st.markdown("#### The top ten streets with most restaurants are:")
st.write(top_ten_streets)

st.markdown("### Top 10 Streets that have the most resturant  - Greaph by street name")

#plot a bar chart
fig = px.bar(top_ten_streets , x="street", y="no_of_rest",
             barmode='group',title="Top 10 Street with most resturants - LA")
fig.update_xaxes(tickangle= -90)  
#fig.show() #
st.plotly_chart(fig)


st.markdown("### What  is the distribution of seats in the streets we have a lot of resturants in them ?")

#xtract the names of the streets in the top 10
st_list = list(top_ten_streets['street'].unique())
#extract the data on those resturants that in these streets
st_lot_of_rests = rest_data_us_df[rest_data_us_df['street'].isin(st_list)].reset_index(drop=True)


st.markdown("##### Checking distribution of seats by street")
#Graph seats by streats
fig3 = px.pie(st_lot_of_rests, values=st_lot_of_rests.no_of_seats, names=st_lot_of_rests.street,
              color=st_lot_of_rests.street,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> No. of Seats split by Top 10 streets with most Resturants in LA </b>")
#fig3.show()
st.plotly_chart(fig3)


st.markdown("##### Checking distribution of seats by type")
#Graph seats by streats
fig3 = px.pie(st_lot_of_rests, values=st_lot_of_rests.no_of_seats, names=st_lot_of_rests.object_type,
              color=st_lot_of_rests.object_type,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> No. of Seats split by resturant type in Top 10 streets with most Resturants in LA </b>")
#fig3.show()
st.plotly_chart(fig3)

st.markdown("##### Checking distribution of seats by Chain/Non Chain")
#Graph seats by streats
fig3 = px.pie(st_lot_of_rests, values=st_lot_of_rests.no_of_seats, names=st_lot_of_rests.chain,
              color=st_lot_of_rests.chain,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> No. of Seats split by chain / non chain type in Top 10 streets with most Resturants in LA </b>")
#fig3.show()
st.plotly_chart(fig3)

st.markdown("##### Checking distribution of seats by Chain/Non Chain criteria - distribution By type")
st.markdown("**What is the distribution by type when we enter the Chain criteria?**")

#group all by chain \ non chain criteria
st_top_rest_data_chains_grouped = st_lot_of_rests.groupby(['object_type','chain']).agg({'id':'count','no_of_seats':'mean'}).reset_index()
st_top_rest_data_chains_grouped.rename(columns={'object_type':'resturant_type','id':'rest_count'},inplace=True)

#plot a bar chart
fig = px.bar(st_top_rest_data_chains_grouped, x="resturant_type", y="rest_count",
           color='chain', barmode='group',
            title="<b>Distribution by Chain \ Non Chain Criteria for Top 10 streets</b>")
fig.update_xaxes(tickangle= -45)  
#fig.show() #
st.plotly_chart(fig)

st.markdown("**Lets draw an avarage of seets in aresturant per street**")

#calculate the numner of resturant types in each streat and the over all no. of seats of these resturants
st_avg_rest_seat = st_lot_of_rests.groupby(["street","object_type"]).agg({"id":"count","no_of_seats":"sum"}).reset_index()

#Calculate avarage seats per street per type
st_avg_rest_seat["avg_type_seats"] = (st_avg_rest_seat["no_of_seats"] / st_avg_rest_seat["id"]).round(0)

#plot a bar chart
fig = px.bar(st_avg_rest_seat, x="street", y="avg_type_seats",
           color='object_type', barmode='group', 
            title = "<b>Distribution of firts top 10 streets by resturant type</b>")
fig.update_xaxes(tickangle= -45)  
#fig.show() #
st.plotly_chart(fig)

st.markdown("##### Data by type of restauran criteria - avarage seat number")


#Gether all the data by type of resturant
st_avg_rest_seat_type = st_avg_rest_seat.groupby('object_type').agg({"id":"sum" , "avg_type_seats":"mean"}).reset_index()
st_avg_rest_seat_type['avg_type_seats'] =st_avg_rest_seat_type['avg_type_seats'].round(0)
st_avg_rest_seat_type.rename(columns={'object_type':'resturant_type','id':'rest_count'},inplace=True)

#plot a bar chart
fig = px.bar(st_avg_rest_seat_type, x="resturant_type", y="avg_type_seats",
           color="rest_count", barmode='group',
            title = "<b>Resturants types avarage no. of seets - with number of establishments for top 10 streets</b>")
fig.update_xaxes(tickangle= 0)  
#fig.show() #
st.plotly_chart(fig)

st.markdown("##### Checking distribution of resturans type in all other streets where  have only small number of resturants")
st.markdown("**Lets check the other streets, How does restaurants distributes there**")

#retrieve all records that the street namr is not part of the first 10 streets from before
st_min_rest_data_df = rest_data_us_df.query("street not in @st_list")
#Group all streets that have under less resturants
st_min_rest_data_df_grouped = st_min_rest_data_df.groupby(["street","object_type"]).agg({'id':'count','no_of_seats':'mean'}).reset_index()

#Calculate avarage seats per street per type
st_min_rest_data_df_grouped["avg_type_seats"] = (st_min_rest_data_df_grouped["no_of_seats"] / st_min_rest_data_df_grouped["id"]).round(0)

#group all by type of resturant
st_min_rest_data_df_grouped.rename(columns={'object_type':'resturant_type','id':'rest_count'},inplace=True)
st_min_rest_data_grouped = st_min_rest_data_df_grouped.groupby('resturant_type').agg({'rest_count':'sum','avg_type_seats':'mean'}).reset_index()
st_min_rest_data_grouped['avg_type_seats'] = st_min_rest_data_grouped['avg_type_seats'].round(0)


#plot a bar chart for 
fig = px.bar(st_min_rest_data_grouped, x="resturant_type", y="avg_type_seats",
            color='rest_count', barmode='group',
            title="<b>Avarage setats per resturant type per street</b>")
fig.update_xaxes(tickangle= -90)  
#fig.show() #
st.plotly_chart(fig)


st.markdown("##### Checking distribution of resturans type in all other streets where  have only small number of resturants - By chain criterua")
st.markdown("**How does restaurants distributed there by chain criteria?**")

#group all by chain \ non chain criteria
st_min_rest_data_chains_grouped = st_min_rest_data_df.groupby('chain').agg({'id':'count','no_of_seats':'mean'}).reset_index()
st_min_rest_data_chains_grouped.rename(columns={'object_type':'resturant_type','id':'rest_count'},inplace=True)

#Graph seats by chain/non chain
fig3 = px.pie(st_min_rest_data_chains_grouped, values=st_min_rest_data_chains_grouped.rest_count, names=st_min_rest_data_chains_grouped.chain,
              color=st_min_rest_data_chains_grouped.chain,
              color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
fig3.update_layout(
title="<b> No. of Resaturants split by chain / non chain type in all other streets in LA </b>")
#fig3.show()
st.plotly_chart(fig3)

#group all by chain \ non chain criteria
st_min_rest_data_chains_grouped_type = st_min_rest_data_df.groupby(['object_type','chain']).agg({'id':'count','no_of_seats':'mean'}).reset_index()
st_min_rest_data_chains_grouped_type.rename(columns={'object_type':'resturant_type','id':'rest_count'},inplace=True)

#plot a bar chart
fig = px.bar(st_min_rest_data_chains_grouped_type, x="resturant_type", y="rest_count",
           color='chain', barmode='group',
            title="<b>Distribution by Chain \ Non Chain Criteria for rest of the streets</b>")
fig.update_xaxes(tickangle= -45)  
#fig.show() #
st.plotly_chart(fig)


st.markdown("## Conclusions and Recommandations")
st.markdown("### Conclusions ")
st.markdown("**We see a definate tendancy to open resturans in the LA area.**")
st.markdown("* The most number of seats is the resturants type")
st.markdown("* The most type of esatablishments are resturants, with over 6000 resturants.")
st.markdown("* The bakaryes are just a small part, so are bars and cafe.(cafa about 600 and Bar about 290)")
st.markdown("* The preferance is for those establishments that are no a chain type ones.")
st.markdown("* The resturants are distributed with most differ up to 5% and dominate each street.")
st.markdown("* Most cafe are of the chains stores. ")


st.markdown("### Recommandations")
st.markdown("**The recommendations are as follows:**")
st.markdown("* Try to distribute the branches to the streets near those streets in tje list bellow:")
st.markdown(" * SUNSET BLVD,")
st.markdown(" * PICO BLVD,")
st.markdown(" * WESTERN AVE,")
st.markdown(" * FIGUEROA ST,")
st.markdown(" * VERMONT AVE,")
st.markdown(" * WILSHIRE BLVD,")
st.markdown(" * OLYMPIC BLVD,")
st.markdown(" * HOLLYWOOD BLVD,")
st.markdown(" * SANTA MONICA BLVD,")
st.markdown(" * 3RD ST")
st.markdown("* The traffic on these streets is emmence and have a potential to create a surge of customers that would like a 'fresh' chine of cafe stores to go to.")
st.markdown("* since there are many resturants the menu should take more of a snack type and not meals.(like toast, sandwiched etc.)")
st.markdown("* The potential of attracting custommers near thos street is great. I would not try to open on the streets i have listed. There are a lot of establishments and a new one will be lost in this 'jungle' , and compattition will be great.Moving to naighbouring streets make competition easier, and still accesible to the potential croud(not far from the main streets)")










