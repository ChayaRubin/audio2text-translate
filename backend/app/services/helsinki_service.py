from transformers import MarianTokenizer, MarianMTModel

def load_translation_model(source_lang="en", target_lang="he"):
    name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    tok = MarianTokenizer.from_pretrained(name)
    model = MarianMTModel.from_pretrained(name)
    return tok, model

def translate(text, source="en", target="he"):
    tok, model = load_translation_model(source, target)
    tokens = tok(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokens)
    return tok.decode(translated[0], skip_special_tokens=True)
