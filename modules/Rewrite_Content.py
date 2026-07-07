import os
from dotenv import load_dotenv
load_dotenv()

# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from google import genai
# import torch
# from peft import PeftModel

def rewrite_content_gemini(prompt):
    model_name = os.getenv("GEMINI_MODEL")
    api = os.getenv("GEMINI_API")

    client = genai.Client(api_key=api)
    response = client.models.generate_content(
        model=model_name, contents=prompt
    )
    return response.text

# def rewrite_content_finetuned(prompt, tokenizer, model):
    # os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")
    # base_model_id = os.getenv("HF_BASE_MODEL")
    # fine_tuned_model_id = os.getenv("HF_MODEL")

    # tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)

    # bnb_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_use_double_quant=True,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_compute_dtype="bfloat16"
    # )

    # base_model = AutoModelForCausalLM.from_pretrained(
    #     base_model_id,
    #     quantization_config=bnb_config,
    #     torch_dtype=torch.float16,
    #     device_map="auto",
    # )
    # base_model.config.use_cache = False

    # model = PeftModel.from_pretrained(base_model, fine_tuned_model_id)
    # # model = model.merge_and_unload()
    # torch.cuda.empty_cache()

    # tokenizer.pad_token = tokenizer.eos_token
    # tokenizer.padding_side = "right"

    # messages = [{ "role": "user", "content": prompt}]
    # model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")

    # if torch.cuda.is_available():
    #     model_inputs = model_inputs.to('cuda')

    # generated_ids = model.generate(
    #     model_inputs,
    #     max_new_tokens=500,
    #     do_sample=True,
    #     temperature=0.7,
    #     top_p=0.9
    # )

    # decoded = tokenizer.batch_decode(generated_ids)
    # # del model, base_model, tokenizer
    # raw_output = decoded[0]
    # if "[/INST] " in raw_output:
    #     result = raw_output.split("[/INST] ", 1)[1]
    #     # Strip trailing end-of-sequence token (e.g., "</s>")
    #     if result.endswith("</s>"):
    #         result = result[:-4]
    #     return result.strip()
    # else:
    #     # Fallback: return the full decoded output minus the input prompt
    #     return raw_output.strip()