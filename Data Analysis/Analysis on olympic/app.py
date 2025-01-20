import streamlit as st
import pandas as pd

st.slidebar.radio(
    'Select an option',
    ('Medal Tally','overall Analysis','Country-Wise Analysis','Athlete-wise Analysis')
    
)
git push -u origin master