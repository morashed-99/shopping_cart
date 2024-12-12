import streamlit as st
import plotly.express as px
import pandas as pd

# Set colors and page configuration
color1 = ['#330000','#252526','#0487D9','#F29F05','#F2E0DF']

st.set_page_config(
    layout='wide',
    page_title='Shopping Cart',
    page_icon='🛒'
)

x = st.sidebar.checkbox('Show Data', False, key=1)

df = pd.read_csv("shopping_cart.csv")

st.markdown('<h1 style="text-align: center; color: black;">Home Page For Dashboard</h1>', unsafe_allow_html=True)

if x:
    st.dataframe(df.copy(), height=500, width=1000)

tab1, tab2 = st.tabs(["📊 Univariate", "📈 Bivariate"])

with tab1:
    st.markdown('<h3 style="text-align: center; color: black;">Univariate Analysis</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([5, 1, 5])

    # Gender Distribution
    fig = px.histogram(
        df, 
        x='gender', 
        color_discrete_sequence=color1, 
        title='Distribution of Gender',text_auto=True
    )
    col1.plotly_chart(fig, use_container_width=True)

    fig = px.box(
        df, 
        x='differnce', 
        color_discrete_sequence=color1, 
        title='Difference Between Delivery and Order Date'
    )
    col3.plotly_chart(fig, use_container_width=True)
    
    state= col1.radio('Select state', df['state'].unique(),horizontal=True)
    new_df2 = df[df['state'] == state]
    fig = px.bar(new_df2, x='name_day_delivery', color_discrete_sequence=color1, title='Best Delivery Day')
    col1.plotly_chart(fig, use_container_width=True)
    
    
    top_5_df = new_df2.groupby(['country', 'city', 'payment']).size().reset_index(name='count')
    top_5_df = top_5_df.groupby('country').apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)
    top_5_df = top_5_df.groupby('city').apply(lambda x: x.nlargest(5, 'count')).reset_index(drop=True)

    fig = px.sunburst(top_5_df, path=['country', 'city', 'payment'],
                      title='Top 5 Counting Over Country, City, and Payment',height=600 ,
                      color_discrete_sequence=color1)
    col3.plotly_chart(fig, use_container_width=True)
    

with tab2:
    st.markdown('<h3 style="text-align: center; color: black;">Bivariate Analysis</h3>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([5, 1, 5])

    fig = px.scatter(
        df, 
        x='payment', 
        y='state', 
        title="Scatter Plot of State vs Payment", 
        color_discrete_sequence=color1
    )
    col1.plotly_chart(fig, use_container_width=True)

    fig = px.box(df, x="payment", y="delivery_date", title="Delivery Time by Payment",color_discrete_sequence=color1)
    col1.plotly_chart(fig, use_container_width=True)

    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['differnce'] = pd.to_numeric(df['differnce'], errors='coerce')
    df_1 = df.groupby('order_date').agg({'differnce': 'mean'}).reset_index()

    fig = px.line(
        df_1, 
        x="order_date", 
        y='differnce', 
        title="Mean Difference Over Order Dates", markers=dict(size=10, symbol='circle', color='navy'),
        color_discrete_sequence=color1
    )
    col3.plotly_chart(fig, use_container_width=True)
    
    numeric_df = df.select_dtypes(include=['number'])
    fig = px.imshow(numeric_df.corr(), title="Correlation Heatmap",color_continuous_scale='YlOrBr')
    col3.plotly_chart(fig, use_container_width=True)
