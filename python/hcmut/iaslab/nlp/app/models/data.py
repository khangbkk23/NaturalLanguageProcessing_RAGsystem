# python/hcmut/iaslab/nlp/app/models/data.py
from collections import OrderedDict
import re
from unicodedata import normalize

# --- CONSTANTS ---
ROOT = "ROOT"
N = "NOUN"; V = "VERB"; PP = "PREPOSITION"; Q = "QUERY"; NAME = "NAME"
PUNC = "PUNC"; YN = "YESNO"; ADV = "ADVERB"; P = "PRONOUN"; DET = "DETERMINER"; NUM = "NUMBER"

# --- TỪ VỰNG TOKENIZE (Hardcode) ---
TOKENIZE_DICT = OrderedDict({
    "bao nhiêu": "bao_nhiêu", "món nào": "món_nào", "những món gì": "những_món_gì", 
    "món gì": "món_gì", "vào đơn": "vào_đơn", "đơn hàng": "đơn_hàng", "thực đơn": "menu",
    # Tên món
    "phở bò": "phở_bò", "gà rán": "gà_rán", "trà sữa": "trà_sữa", 
    "bún chả": "bún_chả", "cơm tấm": "cơm_tấm", "cà phê sữa": "cà_phê_sữa", "nước cam": "nước_cam",
    # Option
    "ít đường": "ít_đường", "nhiều đá": "nhiều_đá"
})

# --- POS TAGS ---
POS = {
    "có": V, "những": DET, "món": N, "nào": Q, "gì": Q, "trong": PP,
    "menu": N, "thực_đơn": N, "giá": N, "bao_nhiêu": Q, "không": YN,
    "tôi": P, "đã": ADV, "đặt": V, "thêm": V, "cho": V, "lấy": V, "mua": V,
    "1": NUM, "2": NUM, "3": NUM, "ly": N, "phần": N, "vào_đơn": PP, 
    "?": PUNC, ".": PUNC,
    # Món ăn
    "phở_bò": NAME, "gà_rán": NAME, "trà_sữa": NAME, "bún_chả": NAME, 
    "cơm_tấm": NAME, "cà_phê_sữa": NAME, "nước_cam": NAME
}

def tokenize(text: str) -> "list[str]":
    if not text: return []
    text = normalize("NFC", text).lower()
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(.)\?", r"\1 ?", text)
    text = re.sub(r"(.)\.", r"\1 .", text)

    for k, v in TOKENIZE_DICT.items():
        if k in text: text = text.replace(k, v)

    return [t for t in text.split(" ") if t in POS or t.isdigit()]