'''
Things to try:
    Combine two functions in extract content to reduce looping. - Not Effective
    Try to enable buttons after refresh. - Done
    Find a way to calculate seo score manually.
'''

import warnings, json, time

warnings.filterwarnings("ignore")
from modules.Extract_Content import get_most_common_keywords
import streamlit as st
from modules.Generate_Response import generate_response
from googlesearch import search
# from modules.Export_PDF import export_pdf
from modules.Export import export

st.set_page_config(page_title="BlogBotter 💬 ", initial_sidebar_state="auto")

with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("BlogBotter 💬 ")

models = json.load(open("config.json"))
keywords = []


def imp_run():
    st.session_state.imp_run = True


if "imp_run" not in st.session_state:
    st.session_state.imp_run = False
    st.session_state.result = None


def gen_run():
    st.session_state.gen_run = True


if "gen_run" not in st.session_state:
    st.session_state.gen_run = False
    st.session_state.result = None


def clear():
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

    selection = st.selectbox("What model would you like to use?", (models.keys()), on_change=clear)

    title = st.text_input("Enter Title: ", placeholder="Title of the Blog goes here.", on_change=clear)

    blog = st.text_area("Enter Blog: ", placeholder="Your Original Blog goes here.", on_change=clear)

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
        # or blog == ""
    )

    c1, c2 = st.columns(2)

    with c1:
        generate = st.button(
            "Generate a Fresh Blog",
            on_click=gen_run,
            disabled=gen_lock,
            use_container_width=True,
        )
    with c2:
        improve = st.button(
            "Improve the Above Blog",
            on_click=imp_run,
            disabled=imp_lock,
            use_container_width=True,
        )

if st.session_state.gen_run or st.session_state.imp_run:
    t1 = time.time()

    if st.session_state.imp_run:
        promptVisible = f"Improving the SEO of the following blog: {title}"
        promptInVisible = f"""
        Improve SEO of the blog: "{blog}" and write an imporved blog focusing mainly on the keywords:
        """
    else:
        promptVisible = f"Writing a blog on the following topic: {title}"
        promptInVisible = f"""
        Write a blog on {title} focusing mainly on the keywords:
        """

    st.session_state.messages.append({"role": "user", "content": promptVisible})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(promptVisible)

    t2 = time.time()
    print("Part 1:", t2-t1)

    with st.spinner("Generating response..."):
        urls = []
        for j in search(title, tld="co.in", num=5, stop=5, pause=2):
            urls.append(j)
        keywords = get_most_common_keywords(urls)
        
        t3 = time.time()
        print("Part 2:", t3-t1)

        print(promptInVisible + str(keywords))

        if st.session_state.imp_run:
            st.session_state.result = generate_response(
                selection, promptInVisible + str(keywords)
            )
            st.session_state.imp_run = False

        if st.session_state.gen_run:
            st.session_state.result = generate_response(
                selection, promptInVisible + str(keywords)
            )
            st.session_state.gen_run = False
        
        t3 = time.time()
        print("Part 3:", t3-t1)

        if st.session_state.result is not None:
            c3, c4 = st.columns(2)
            with c3:
                st.button("Clear", on_click=clear, use_container_width=True)

            with c4:
                # Export to PDF
                # st.download_button(
                #     label="Export",
                #     data=export_pdf(title, st.session_state.result),
                #     file_name="ImprovedContent.pdf",
                #     mime="application/octet-stream",
                #     use_container_width=True,
                #     on_click=clear,
                # )

                # Export to HTML
                st.download_button(
                    label="Export",
                    data=export(title, st.session_state.result),
                    file_name=f"{title}.html",
                    use_container_width=True,
                    on_click=clear,
                )