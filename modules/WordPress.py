from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import WordPressPost, Client
from modules.Generate_Response import generate_response
from modules.Get_Tags_Categories import get_tags_categories
import re, os, datetime
import streamlit as st
from bs4 import BeautifulSoup

MAX_RETRIES = 3


def check_or_create_folder(x):
    folder = f"./{x}"
    if not os.path.isdir(folder):
        os.makedirs(folder, exist_ok=True)


def wordpress(action):
    base = "blogs"
    check_or_create_folder(base)

    today = datetime.date.today().strftime("%d-%m-%Y")
    check_or_create_folder(f"{base}/{today}")

    prompt = f"""
    convert the output to html file: {st.session_state.result}"""

    result_to_wordpress = generate_response(
        promptInVisible=prompt, to_add_in_chat=False
    )

    wp_username = os.getenv("WORDPRESS_USERNAME")
    wp_password = os.getenv("WORDPRESS_PASSWORD")
    wp_url = os.getenv("WORDPRESS_URL")

    if not all([wp_username, wp_password, wp_url]):
        st.error("WordPress credentials not configured. Check your .env file.")
        return

    client = Client(wp_url, wp_username, wp_password)

    post = WordPressPost()

    # Safely extract title from generated HTML
    title_pattern = r"<title>(.+?)</title>"
    title_matches = re.findall(title_pattern, result_to_wordpress)
    if title_matches:
        post.title = title_matches[0]
    else:
        # Fallback: use the session topic or a default
        post.title = "Untitled Blog Post"

    clean_title = post.title.replace(":", "-")

    tags, categories = get_tags_categories(clean_title)

    post.content = result_to_wordpress

    content_pattern = r"</head>(.*?)</html>"
    match = re.search(content_pattern, result_to_wordpress, re.DOTALL)

    if match:
        body = match.group(1)
        try:
            post.content = remove_h1_from_body(body)
        except Exception:
            post.content = body

    with open(f"{base}/{today}/{clean_title}.html", "w", encoding="utf-8") as f:
        f.write(result_to_wordpress)

    post.terms_names = {
        "post_tag": tags,
        "category": categories,
    }

    post.post_status = action

    post.id = client.call(posts.NewPost(post))

    # Retry EditPost with a limit to avoid infinite recursion
    for attempt in range(MAX_RETRIES):
        try:
            client.call(posts.EditPost(post.id, post))
            break
        except Exception as e:
            print(f"EditPost attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                st.error(f"Failed to update WordPress post after {MAX_RETRIES} attempts.")

    clear()


def remove_h1_from_body(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    # soup.body may be None if the HTML fragment has no <body> tag
    container = soup.body if soup.body else soup
    for h1_tag in container.find_all("h1"):
        h1_tag.decompose()
    return str(soup)


def clear():
    st.session_state.result = None
