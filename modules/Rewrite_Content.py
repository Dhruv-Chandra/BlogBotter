# import google.generativeai as genai
import json
import streamlit as st
from openai import OpenAI

# @st.cache_data
def rewrite_content(selection, prompt):

    # config_data = json.load(open("config.json"))
    config_data = st.secrets

    model = config_data["models"][selection]["model_name"]
    api = config_data["models"][selection]["api"]

    # print(model)
    # print(api)

    if (selection.lower() == "gpt-4") or (selection.lower() == "llama"):
        return rewrite_content_gpt(model, api, prompt)
    elif selection.lower() == "gemini":
        return rewrite_content_gemini(model, api, prompt)

# @st.cache_data
def rewrite_content_gemini(model, api, prompt):

    genai.configure(api_key=api)

    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    return response.text

# @st.cache_data
def rewrite_content_gpt(model, api, prompt):

    if api.startswith("nvapi"):
        baseurl = "https://integrate.api.nvidia.com/v1"
        client = OpenAI(api_key=api, base_url=baseurl)
    else:
        # baseurl = ''
        client = OpenAI(
            api_key=api,
            # base_url=baseurl
        )

    # client = OpenAI(
    #     api_key = api,
    #     base_url=baseurl
    # )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0]
    return answer.message.content
