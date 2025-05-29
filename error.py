import streamlit as st

st.write("Streamlit rerun 테스트")

if st.button("재실행 테스트"):
    st.experimental_rerun()