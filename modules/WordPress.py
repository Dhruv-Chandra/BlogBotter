from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost, Client
from modules.Generate_Response import generate_response
from modules.Get_Tags_Categories import get_tags_categories
import re, os, datetime
import streamlit as st
from bs4 import BeautifulSoup


def check_or_create_folder(x):
    folder = f"./{x}"
    if os.path.isdir(folder):
        pass
    else:
        os.mkdir(folder)


def wordpress(action):
    user = st.session_state.user
    base = "blogs"
    check_or_create_folder(base)

    today = datetime.date.today().strftime("%d-%m-%Y")
    check_or_create_folder(f"{base}/{today}")

    prompt = f"""
    convert the output to html file: {st.session_state.result}"""

    result_to_wordpress = generate_response(
        promptInVisible=prompt, to_add_in_chat=False
    )

    wp_url = user["Wordpress"]["WP_URL"]
    wp_username = user["Wordpress"]["WP_USER"]
    wp_password = user["Wordpress"]["WP_PASS"]

    client = Client(wp_url, wp_username, wp_password)

    post = WordPressPost()

    title_pattern = r"<title>(.+?)</title>"
    post.title = re.findall(title_pattern, result_to_wordpress)[0]
    clean_title = post.title.replace(":", "-")

    tags, categories = get_tags_categories(clean_title)

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


def remove_h1_from_body(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    for h1_tag in soup.body.find_all("h1"):
        h1_tag.decompose()
    return str(soup)


def clear():
    st.session_state.result = None
