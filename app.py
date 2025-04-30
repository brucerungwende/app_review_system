import streamlit as st

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

if st.session_state.page == 'welcome':
    st.title("Welcome to App Review Analyzer")
    st.write("This system helps you decide if you should download an app by analyzing real user reviews!")
    if st.button('Next'):
        st.session_state.page = 'input'

elif st.session_state.page == 'input':
    st.title("Search for an App")
    app_name = st.text_input('Enter the app name')
    if st.button('Search App'):
        if app_name:
            st.session_state.page = 'results'
            st.session_state.app_name = app_name
        else:
            st.warning('Please enter an app name!')

elif st.session_state.page == 'results':
    st.title(f"Results for {st.session_state.app_name}")
    st.write("Coming soon... We will analyze the reviews!")


































