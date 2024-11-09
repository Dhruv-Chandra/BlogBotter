from modules.Rewrite_Content import rewrite_content
import json
import streamlit as st

# from numba import jit
# @jit

# @st.cache_data
def generate_response(selection, promptInVisible):
    config_data = st.secrets

    if config_data["models"][selection]["api"] != "":
        llm_response = rewrite_content(selection, promptInVisible)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("Choose a different Model.")

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(llm_response)

    st.session_state.messages.append({"role": "assistant", "content": llm_response})

    last_response = st.session_state.messages[len(st.session_state.messages) - 1][
        "content"
    ]

    if str(last_response) != str(llm_response):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(llm_response)

    return llm_response
