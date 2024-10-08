import streamlit as st
import pandas as pd
import plotly.express  as px

from time import time

# [TODO] 아래 summary를 참고하여 막대 그래프와 라인 그래프를 그리는 함수를 구성해봅니다.
# """_summary_
# fig = px.bar(bar_df, 
#                 title="",
#                 y='',
#                 color="",
#                 hover_data='')

# fig = px.line(line_df,x="일시",y="",
#             title="",
#             color='',
#             line_group='',
#             hover_name="")
# """

## *geo는 클릭이 된 지역구들이 들어있는 튜플이라고 생각하시면 됩니다.
# 여기서 *는 가변인자를 받을때 사용하는 것이다.(데이터 개수, 길이가 막 달라질 수 있는 경우)
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


# 체크 표시된 지역구만 뽑아서 리스트로 저장합니다.

# 오른쪽 column의 내용을 채워줍니다. (Tab 두개를 만들어줍니다. )

# streamlit run 19_public_app1.py