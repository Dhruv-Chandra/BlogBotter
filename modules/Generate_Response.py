from modules.Rewrite_Content import rewrite_content
import json, time
import streamlit as st

# from numba import jit
# @jit

# @st.cache_data
def generate_response(selection, promptInVisible):

    t21 = time.time()
    if json.load(open("config.json"))[selection]["api"] != "":
        llm_response = rewrite_content(selection, promptInVisible)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("Choose a different Model.")

    t22 = time.time()
    print("After Response", t22-t21)
    # llm_response = 'Response is here'

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(llm_response)

    st.session_state.messages.append({"role": "assistant", "content": llm_response})

    last_response = st.session_state.messages[len(st.session_state.messages) - 1][
        "content"
    ]

    if str(last_response) != str(llm_response):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(llm_response)

    t23 = time.time()
    print("Appending Response", t23-t22)

    return llm_response
