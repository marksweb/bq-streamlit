import asyncio

import streamlit as st

from agent import run_agent

st.set_page_config(page_title="AI Research Assistant", page_icon=" ")
st.title(" AI Research Dashboard")
st.write(
    "Enter your research question below. Your personal research agent will scour the web and"
)

query = st.text_input(
    "What would you like to research today?", "How does reinforcement"
)

if st.button("Run Research"):
    with st.spinner("Consulting your research agent. Please wait..."):
        results, main_content = asyncio.run(run_agent(query))

if "main_content" in locals():
    st.subheader(" Summary")
    st.markdown(main_content, unsafe_allow_html=True)
    st.subheader(" Top Search Results")
    for idx, result in enumerate(results, 1):
        with st.container():
            st.markdown(f"**{idx}. [{result.title}]({result.url})**")
            st.markdown(result.snippet)
            st.markdown("---")
