from modules.Rewrite_Content import rewrite_content_gemini
import datetime, os, json, string, re
from azure.storage.blob import BlobClient


def upload_blob_with_sas_url(data):
    file_name = data["prompt"].translate(str.maketrans("", "", string.punctuation))
    azure_blob_name = f"{file_name}.txt"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    container_sas_url = os.getenv("AZURE_BLOB")

    if not container_sas_url:
        print("Warning: AZURE_BLOB env var not set, skipping blob upload.")
        return

    home_path = "."
    folder = "/data"
    place = "/eval"

    try:
        if "?" not in container_sas_url:
            print("Warning: AZURE_BLOB URL has no SAS token, skipping blob upload.")
            return

        base_url, sas_token = container_sas_url.split("?", 1)
        if not base_url.endswith("/"):
            base_url += "/"
        text_file_loc = f"{base_url}{place}/{date}/{azure_blob_name}?{sas_token}"

        blob_client = BlobClient.from_blob_url(text_file_loc)
        blob_client.upload_blob(data["response"], overwrite=True)

        local_blog_dir = f"{home_path}{folder}/blogs{place}/{date}"
        os.makedirs(local_blog_dir, exist_ok=True)
        with open(f"{local_blog_dir}/{azure_blob_name}", "w") as f:
            f.write(data["response"])

        json_file_loc = f"{base_url}{place}/result.json?{sas_token}"
        blob_json_client = BlobClient.from_blob_url(json_file_loc)

        try:
            exists = blob_json_client.exists()
            if exists:
                existing_data = blob_json_client.download_blob().readall()
                try:
                    json_list = json.loads(existing_data)
                    if not isinstance(json_list, list):
                        json_list = [json_list]
                except Exception:
                    json_list = []
                json_list.append(data)
            else:
                json_list = [data]
        except Exception as e:
            print(f"Error reading existing data: {e}")
            json_list = [data]
        blob_json_client.upload_blob(
            json.dumps(json_list, ensure_ascii=False, indent=4), overwrite=True
        )

        local_eval_dir = f"{home_path}{folder}/blogs{place}"
        os.makedirs(local_eval_dir, exist_ok=True)
        with open(f"{local_eval_dir}/result.json", "w") as f:
            f.write(json.dumps(json_list, ensure_ascii=False, indent=4))

        print("result.json uploaded/appended successfully.")

    except Exception as e:
        print(f"Error uploading file: {e}")


def save_output(query, res, score=0):
    result = dict()

    result["prompt"] = query
    result["response"] = res
    result["score"] = score

    upload_blob_with_sas_url(result)


def _parse_score(raw_text):
    """Safely extract an integer score from LLM output.

    Handles formats like '85', 'Score: 85', '85/100', or free-form text.
    Returns 0 if no integer can be parsed.
    """
    if not raw_text:
        return 0
    # Try direct int conversion first
    cleaned = raw_text.strip()
    try:
        return int(cleaned)
    except ValueError:
        pass
    # Try to find the first integer in the string
    match = re.search(r'\d+', cleaned)
    if match:
        return int(match.group())
    return 0


def get_output_score(query, response):
    prompt = f"""Given the title: {query}, the blog returned from my fine-tuned model is: {response}.
    Score the blog on a scale of 1 to 100. 
    **Answer in a single token**"""

    raw_score = rewrite_content_gemini(prompt)
    score = _parse_score(raw_score)
    print("LLM Score: ", score)
    return score


def generate_response(promptInVisible, title=None, to_add_in_chat=True):
    """Generate a blog response using the Gemini API.

    Args:
        promptInVisible: The full prompt to send to the model.
        title: The blog title (used for scoring/saving when to_add_in_chat=True).
        to_add_in_chat: If True, score and save the output. If False, just return raw output.
    """
    llm_response = rewrite_content_gemini(promptInVisible)

    if to_add_in_chat and title:
        score = get_output_score(title, llm_response)
        save_output(title, llm_response, score)

    return llm_response
