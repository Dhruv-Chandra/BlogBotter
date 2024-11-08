import warnings, json, string

warnings.filterwarnings("ignore")
from modules.Extract_Content import get_most_common_keywords
import streamlit as st
from modules.Generate_Response import generate_response
from googlesearch import search

from wordpress_xmlrpc import WordPressPost, Client
from wordpress_xmlrpc.methods import posts
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

st.set_page_config(page_title="BlogBotter 💬 ", initial_sidebar_state="auto")

with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("BlogBotter 💬 ")

config_data = json.load(open("config.json"))
models = config_data["models"]
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


def get_tags_categories(title):
    title_for_tags = title.translate(str.maketrans("", "", string.punctuation))

    list_title_for_tags = title_for_tags.split()
    list_title_for_tags.extend([title_for_tags])

    tags = []
    stop_words = set(stopwords.words("english"))

    for word in list_title_for_tags:
        if word not in stop_words and len(word) > 1:
            tags.append(word)
            tags.append(lemmatizer.lemmatize(word))

    return tags, [title_for_tags]


def wordpress(action):
    wp_url = config_data["wordpress"]["wordpress_url"]
    wp_username = config_data["wordpress"]["wordpress_username"]
    wp_password = config_data["wordpress"]["wordpress_password"]

    client = Client(wp_url, wp_username, wp_password)

    # clean_title = title.replace(":", "-")
    tags, categories = get_tags_categories(title)

    post = WordPressPost()
    post.title, post.content = st.session_state.result.split("\n\n", 1)

    post.id = client.call(posts.NewPost(post))

    post.terms_names = {
        "post_tag": tags,
        "category": categories,
    }

    post.post_status = action
    try:
        client.call(posts.EditPost(post.id, post))
    except:
        wordpress()
    clear()

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

    selection = st.selectbox(
        "What model would you like to use?", models.keys(), on_change=clear
    )

    title = st.text_input(
        "Enter Title: ", placeholder="Title of the Blog goes here.", on_change=clear
    )

    blog = st.text_area(
        "Enter Blog: ", placeholder="Your Original Blog goes here.", on_change=clear
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

    with open("./Sample.html", "r") as sample:
        format = sample.read()

    if st.session_state.imp_run:
        promptVisible = f"Improving the SEO of the following blog: {title}"
        promptInVisible = f"""
        Improve SEO of the blog: "{blog}" and write an imporved blog in the format: {format}
        """
    else:
        promptVisible = f"Writing a blog on the following topic: {title}"
        promptInVisible = f"""
        Write a blog on {title} in the format: {format}
        """

    st.session_state.messages.append({"role": "user", "content": promptVisible})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(promptVisible)

    with st.spinner("Generating response..."):
        urls = []
        for j in search(title, tld="co.in", num=5, stop=5, pause=2):
            urls.append(j)
        keywords = get_most_common_keywords(urls)

        # print(promptInVisible + str(keywords))

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

        if st.session_state.result is not None:
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
                    "Publish to WordPress", on_click=wordpress, args=("publish",), use_container_width=True
                )
