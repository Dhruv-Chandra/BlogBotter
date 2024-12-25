# import google.generativeai as genai
import json
import streamlit as st
from openai import OpenAI

# @st.cache_data
def rewrite_content(prompt):
    user = st.session_state.user

    model = user["Models"]["Model"]
    api = user["Models"]["API"]
    # print(model, api)

    if (model == "gpt-4") or (model == "llama"):
        return rewrite_content_gpt(model, api, prompt)
    # elif selection.lower() == "gemini":
    #     return rewrite_content_gemini(model, api, prompt)

# @st.cache_data
# def rewrite_content_gemini(model, api, prompt):

#     genai.configure(api_key=api)

#     model = genai.GenerativeModel(model)
#     response = model.generate_content(prompt)

#     return response.text

# @st.cache_data
def rewrite_content_gpt(model, api, prompt):

    # if api.startswith("nvapi"):
    #     baseurl = "https://integrate.api.nvidia.com/v1"
    #     client = OpenAI(api_key=api, base_url=baseurl)
    # else:
    #     # baseurl = ''
    #     client = OpenAI(
    #         api_key=api,
    #         # base_url=baseurl
    #     )

    client = OpenAI(
        api_key = api,
        # base_url=baseurl
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    answer = response.choices[0]
    return answer.message.content
