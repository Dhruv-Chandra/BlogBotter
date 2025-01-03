from modules.Rewrite_Content import rewrite_content
import streamlit as st

# from numba import jit
# @jit

# @st.cache_data
def generate_response(promptInVisible, to_add_in_chat = True):
    user = st.session_state.user

    if user["Models"]["API"] != "":
        llm_response = rewrite_content(promptInVisible)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown("Choose a different Model.")

    if to_add_in_chat:
        with st.chat_message("assistant", avatar="🤖"):
            # st.markdown(stream_parser(llm_response))
            st.markdown(llm_response)

        st.session_state.messages.append({"role": "assistant", "content": llm_response})

        last_response = st.session_state.messages[len(st.session_state.messages) - 1][
            "content"
        ]

        if str(last_response) != str(llm_response):
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(llm_response)

    return llm_response
