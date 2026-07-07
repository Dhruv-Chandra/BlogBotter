import streamlit as st
import warnings, json
from modules.Generate_Response import generate_response
from modules.WordPress import wordpress, clear

st.set_page_config(page_title="BlogBotter 💬 ", initial_sidebar_state="auto")
st.title("BlogBotter 💬 ")

warnings.filterwarnings("ignore")


def imp_run():
    st.session_state.imp_run = True


def gen_run():
    st.session_state.gen_run = True


with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "gen_run" not in st.session_state:
    st.session_state.gen_run = False
    st.session_state.result = None
if "imp_run" not in st.session_state:
    st.session_state.imp_run = False
    st.session_state.result = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"], avatar="🧑‍💻"):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar="🤖"):
            st.markdown(message["content"])

with st.sidebar:
    st.markdown("# Chat Options")
    word_press_col_1, word_press_col_2 = st.columns(2)

    title = st.text_input(
        "Enter Topic on which you want the blog written: ",
        placeholder="Topic of the Blog goes here.",
        on_change=clear,
    )
    title = title.title()

    c6, c7 = st.columns(2)

    with c6:
        language = st.selectbox("Language for Code examples?", ["Python", "R"])

    with c7:
        depth = st.selectbox("Depth?", ["General", "In-Depth"])

    blog = st.text_area(
        f"Enter your Blog to improve:",
        placeholder="Your Original Blog goes here.",
        on_change=clear,
    )

    imp_lock = (
        st.session_state.imp_run
        or st.session_state.gen_run
        or st.session_state.result is not None
        or title == ""
        or blog == ""
    )
    gen_lock = (
        st.session_state.gen_run
        or st.session_state.imp_run
        or st.session_state.result is not None
        or title == ""
    )

    c1, c2 = st.columns(2)

    with c1:
        st.button(
            "Generate a Fresh Blog",
            on_click=gen_run,
            disabled=gen_lock,
            use_container_width=True,
        )
    with c2:
        st.button(
            "Improve the Above Blog",
            on_click=imp_run,
            disabled=imp_lock,
            use_container_width=True,
        )

if st.session_state.gen_run or st.session_state.imp_run:
    if st.session_state.imp_run:
        promptVisible = f"Improving the SEO of the following blog: {title}"
        first = f"Write a {depth} blog improving the SEO of: {blog}, using latest up-to date information"
        code = f"citing some coding examples of {language} as code snippets."
        promptInVisible = f"{first}, {code}"
    else:
        promptVisible = f"Writing a blog on the following topic: {title}"
        first = f"Write a {depth} blog titled '{title}'"
        code = f"citing some coding examples of {language} as code snippets."
        promptInVisible = f"{first}, {code}"

    st.session_state.messages.append({"role": "user", "content": promptVisible})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(promptVisible)

    with st.spinner("Generating response..."):

        if st.session_state.imp_run:
            st.session_state.result = generate_response(
                promptInVisible, title=title
            )
            st.session_state.imp_run = False

        if st.session_state.gen_run:
            st.session_state.result = generate_response(
                promptInVisible, title=title
            )
            st.session_state.gen_run = False

        if st.session_state.result is not None:
            # Display the generated blog content
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(st.session_state.result)
            st.session_state.messages.append(
                {"role": "assistant", "content": st.session_state.result}
            )

            c3, c4, c5 = st.columns(3)
            with c3:
                st.button("Clear", on_click=clear, use_container_width=True)

            with c4:
                st.button(
                    "Add Draft to WordPress",
                    on_click=wordpress,
                    args=("draft",),
                    use_container_width=True,
                )
            with c5:
                st.button(
                    "Publish to WordPress",
                    on_click=wordpress,
                    args=("publish",),
                    use_container_width=True,
                )
