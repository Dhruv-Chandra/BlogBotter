from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost, Client
from modules.Generate_Response import generate_response
import streamlit as st
import warnings
import datetime
import string, re, os
from bs4 import BeautifulSoup

nltk.download("stopwords")
nltk.download("wordnet")
warnings.filterwarnings("ignore")


def check_or_create_folder(x):
    folder = f"./{x}"
    if os.path.isdir(folder):
        pass
    else:
        os.mkdir(folder)


lemmatizer = WordNetLemmatizer()

st.set_page_config(page_title="BlogBotter 💬 ", initial_sidebar_state="auto")

with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("BlogBotter 💬 ")

config_data = st.secrets
models = config_data["models"]
keywords = []


def remove_h1_from_body(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    for h1_tag in soup.body.find_all("h1"):
        h1_tag.decompose()
    return str(soup)


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
    base = "blogs"
    check_or_create_folder(base)

    today = datetime.date.today().strftime("%d-%m-%Y")
    check_or_create_folder(f'{base}/{today}')

    prompt = f"""
    convert the output to html file: {st.session_state.result}"""

    result_to_wordpress = generate_response(
        selection, promptInVisible=prompt, to_add_in_chat=False
    )

    wp_url = config_data["wordpress"]["wordpress_url"]
    wp_username = config_data["wordpress"]["wordpress_username"]
    wp_password = config_data["wordpress"]["wordpress_password"]

    client = Client(wp_url, wp_username, wp_password)

    tags, categories = get_tags_categories(title)

    post = WordPressPost()

    title_pattern = r"<title>(.+?)</title>"
    post.title = re.findall(title_pattern, result_to_wordpress)[0]
    clean_title = post.title.replace(":", "-")

    post.content = result_to_wordpress

    content_pattern = r"</head>(.*?)</html>"
    match = re.search(content_pattern, result_to_wordpress, re.DOTALL)

    if match:
        body = match.group(1)
        try:
            post.content = remove_h1_from_body(body)
        except:
            post.content = body

    with open(f"{base}/{today}/{clean_title}.html", "w") as f:
        f.write(result_to_wordpress)

    post.id = client.call(posts.NewPost(post))

    post.terms_names = {
        "post_tag": tags,
        "category": categories,
    }

    post.post_status = action
    try:
        client.call(posts.EditPost(post.id, post))
    except:
        wordpress(action)
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
        "Enter Topic on which you want the blog written: ",
        placeholder="Topic of the Blog goes here.",
        on_change=clear,
    )
    title = title.title()

    c6, c7 = st.columns(2)
    language = None

    with c6:
        language = st.selectbox("Language for Code examples?", ["", "Python", "R"])

    with c7:
        depth = st.selectbox("Depth?", ["General", "In-Depth"])

    blog = st.text_area(
        f"Enter your Blog to improve it with: {selection}", placeholder="Your Original Blog goes here.", on_change=clear
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
    if st.session_state.imp_run:
        promptVisible = f"Improving the SEO of the following blog: {title}"
        first = f"Write a {depth} blog improving the SEO of: {blog}, using latest up-to date information"
        code = f"citing some coding examples of {language} as code snippets."

        if language:
            promptInVisible = f"""
            {first}, {code}
            """
        else:
            promptInVisible = first
    else:
        promptVisible = f"Writing a blog on the following topic: {title}"
        first = f"Write a {depth} blog titled {title}"
        code = f"citing some coding examples of {language} as code snippets."
        if language:
            promptInVisible = f"""
            {first}, {code}
            """
        else:
            promptInVisible = first

    st.session_state.messages.append({"role": "user", "content": promptVisible})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(promptVisible)

    with st.spinner("Generating response..."):

        if st.session_state.imp_run:
            st.session_state.result = generate_response(selection, promptInVisible)
            st.session_state.imp_run = False

        if st.session_state.gen_run:
            st.session_state.result = generate_response(selection, promptInVisible)
            st.session_state.gen_run = False

        # title, content = st.session_state.result.split()

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
                    "Publish to WordPress",
                    on_click=wordpress,
                    args=("publish",),
                    use_container_width=True,
                )