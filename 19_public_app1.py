import streamlit as st
import pandas as pd
import plotly.express as px
from time import time


@st.cache_data
def bar_chart(*geo):
    bar_df = edited_df[edited_df['선택']]
    fig = px.bar(bar_df, y='미세먼지', color='지역구')
    return fig

@st.cache_data    
def line_chart(*geo):
    line_df = df[df['구분'].apply(lambda x: x in geo)]
    fig = px.line(line_df, x='일시', y='초미세먼지(PM2.5)', color='구분')
    return fig


# 페이지 구성
df = pd.read_csv("seoul.csv")
st.title("서울시 미세먼지 분포")


## 각 지역별 미세먼지, 초미세먼지 평균을 알아보기 위해 pivot_table을 활용해봅시다. 
pivot_table = pd.pivot_table(df, index= '구분', values=['미세먼지(PM10)', '초미세먼지(PM2.5)'],aggfunc='mean')
pivot_table['선택'] = pivot_table['미세먼지(PM10)'].apply(lambda x : False)
pivot_table = pivot_table.rename(columns={'미세먼지(PM10)':'미세먼지', '초미세먼지(PM2.5)':'초미세먼지'})


##  column으로 구역을 나눠줍니다 
col1, col2 = st.columns(2)


# 왼쪽 column의 내용을 채워줍니다. 
with col1:
    edited_df = st.data_editor(pivot_table)

edited_df['지역구'] = edited_df.index
select = list(edited_df[edited_df['선택']]['지역구'])

with col2:
    tab1, tab2 = st.tabs(['Bar chart', 'Line chart'])

    t1 = time()
    with tab1:
        st.plotly_chart(bar_chart(*select))

    with tab2:
         st.plotly_chart(line_chart(*select))
    t2 = time()
    st.write(t2-t1)
