from transformers import MarianMTModel, MarianTokenizer

model_cache = {}

def get_model_name(src: str, tgt: str) -> str:
    return f"Helsinki-NLP/opus-mt-{src}-{tgt}"

def get_translation_model(src: str, tgt: str):
    key = f"{src}-{tgt}"

    if key in model_cache:
        return model_cache[key]

    model_name = get_model_name(src, tgt)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    model_cache[key] = (tokenizer, model)
    return tokenizer, model


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    tokenizer, model = get_translation_model(source_lang, target_lang)

    inputs = tokenizer([text], return_tensors="pt")
    translated_tokens = model.generate(**inputs)

    output = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return output
