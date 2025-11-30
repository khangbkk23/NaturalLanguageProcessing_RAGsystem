from collections import OrderedDict
import re
from unicodedata import normalize

# --- CONSTANTS ---
ROOT = "ROOT"
N = "NOUN"; V = "VERB"; PP = "PREPOSITION"; Q = "QUERY"; NAME = "NAME"
PUNC = "PUNC"; YN = "YESNO"; ADV = "ADVERB"; P = "PRONOUN"; DET = "DETERMINER"; NUM = "NUMBER"

# --- TỪ VỰNG TOKENIZE ---
TOKENIZE_DICT = OrderedDict({
    "bao nhiêu": "bao_nhiêu", "món nào": "món_nào", "những món gì": "những_món_gì", 
    "món gì": "món_gì", "vào đơn": "vào_đơn", "đơn hàng": "đơn_hàng", "thực đơn": "menu",
    "hết hàng": "hết_hàng", "là gì": "là_gì",
    
    "phở bò": "phở_bò", "gà rán": "gà_rán", "trà sữa": "trà_sữa", 
    "bún chả": "bún_chả", "cơm tấm": "cơm_tấm", "cà phê sữa": "cà_phê_sữa", 
    "nước cam": "nước_cam", "bánh mì": "bánh_mì",
    
    "ít đường": "ít_đường", "nhiều đá": "nhiều_đá", "không hành": "không_hành"
})

# --- POS TAGS ---
POS = {
    # Động từ
    "có": V, "đặt": V, "thêm": V, "cho": V, "lấy": V, "mua": V, "xem": V, "hủy": V, 
    "muốn": V, "ăn": V, "uống": V,
    # Danh từ & Đơn vị
    "món": N, "menu": N, "thực_đơn": N, "giá": N, "tôi": P, "đơn_hàng": N,
    # "ly": N, "phần": N, "tô": N, "chén": N, "dĩa": N, "cốc": N, "chai": N,
    # Từ hỏi
    "nào": Q, "gì": Q, "bao_nhiêu": Q, "những_món_gì": Q, "món_gì": Q, 
    "món_nào": Q, "những_món_nào": Q,
    # Khác
    "những": DET, "trong": PP, "vào_đơn": PP, "không": YN, "đã": ADV, 
    "nhé": PUNC, "?": PUNC, ".": PUNC,
    # Món ăn
    "phở_bò": NAME, "gà_rán": NAME, "trà_sữa": NAME, "bún_chả": NAME, 
    "cơm_tấm": NAME, "cà_phê_sữa": NAME, "nước_cam": NAME, "bánh_mì": NAME
}

for i in range(1000):
    POS[str(i)] = NUM

text_nums = ["một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười", "chục", "trăm"]
for t in text_nums:
    POS[t] = NUM

def tokenize(text: str) -> "list[str]":
    if not text: return []
    text = normalize("NFC", text).lower()
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(.)\?", r"\1 ?", text)
    text = re.sub(r"(.)\.", r"\1 .", text)
    
    for k, v in TOKENIZE_DICT.items():
        if k in text: text = text.replace(k, v)
    
    return [t for t in text.split(" ") if t in POS or t.isdigit()]