import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import re 

st.set_page_config(layout="wide")

st.title('International Union for Conservation of Nature (IUCN) Red-List species in Utah ')
st.write("This is an enhanced alternative to the ICUN Red-list advanced search section (https://www.iucnredlist.org/search) for endangered species in Utah." )

df = pd.read_csv('iucn_species_scraped2.csv')
iucn_order = ["Critically Endangered","Endangered","Vulnerable","Near Threatened","Least Concern","Data Deficient","Not Evaluated"]
present_statuses = [status for status in iucn_order if status in df['Conservation Status'].unique()]

#summary stats 
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Species", len(df))
with col2:  
    st.metric("Unique Classes", df['Class'].nunique())
with col3: 
    st.metric("Animals", len(df[df['Kingdom'] == 'animalia']))
with col4:
    st.metric("Plants", len(df[df['Kingdom'] == 'plantae']))

#sidebar
#filter by conservation status
st.sidebar.header("Filter Species")
status_options = ['All'] + present_statuses
selected_status = st.sidebar.selectbox("Select a Conservation Status", options=status_options)
if selected_status != "All":
    df = df[df['Conservation Status'] == selected_status]
#filter by kingdom 
selected_kingdoms = st.sidebar.multiselect("Filter by Kingdom", options=df['Kingdom'].dropna().unique())
if selected_kingdoms:
    df = df[df['Kingdom'].isin(selected_kingdoms)]
#filter by population trend
selected_trend = st.sidebar.multiselect("Filter by Population Trend", options=df['Population Trend'].dropna().unique())
if selected_trend:
    df = df[df['Population Trend'].isin(selected_trend)]

#searh bar
search_term = st.text_input("Search for a species by name")
if search_term:
    df = df[df['Common Name'].str.contains(search_term, case=False, na=False) |
            df['Scientific Name'].str.contains(search_term, case=False, na=False)]

col1, col2 = st.columns(2)
with col1:
# visualization
    st.subheader("Species Count by Class")
    st.bar_chart(df['Class'].value_counts())
    st.caption("Most species belong to class *magnoliopsida* (flowering plants), followed by *insecta*.")  
with col2:  
#popoulation trend
    st.subheader("Population Trend Distribution")
    pop_counts = df['Population Trend'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(pop_counts, labels=pop_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.caption("Over 60% of tracked species have a stable population trend, while 8% are still decreasing. The smallest proportion of animals have increasing populations.")
#pivot table 
st.markdown("### Species Count by Class and Conservation Status")
pivot_table = df.pivot_table(index='Class', columns='Conservation Status', aggfunc='size', fill_value=0)
pivot_table = pivot_table.reindex(columns=present_statuses)
pivot_table = pivot_table.fillna("-") 
st.dataframe(pivot_table)

#table with new hyperlink 
st.markdown("---") 
st.markdown("### Species Table")
df['IUCN Link'] = df['IUCN Link'].apply(lambda url: f"[Link]({url})")
df = df.fillna("—")
columns_to_show = ['Common Name', 'Scientific Name', 'Conservation Status', 'Population Trend', 'Classification', 'Kingdom', 'Class', 'IUCN Link']
st.dataframe(df[columns_to_show], hide_index=True)

#st.dataframe(df, hide_index=True)

