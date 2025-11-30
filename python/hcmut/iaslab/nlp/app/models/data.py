from collections import OrderedDict
import re
from unicodedata import normalize

# --- CONSTANTS ---
ROOT = "ROOT"
N = "NOUN"; V = "VERB"; PP = "PREPOSITION"; Q = "QUERY"; NAME = "NAME"
PUNC = "PUNC"; YN = "YESNO"; ADV = "ADVERB"; P = "PRONOUN"; DET = "DETERMINER"; NUM = "NUMBER"
ADJ = "ADJECTIVE"

TOKENIZE_DICT = OrderedDict({
    "bao nhiêu": "bao_nhiêu", "món nào": "món_nào", "những món gì": "những_món_gì", 
    "món gì": "món_gì", "vào đơn": "vào_đơn", "đơn hàng": "đơn_hàng", "thực đơn": "menu",
    "hết hàng": "hết_hàng", "là gì": "là_gì",
    "giỏ hàng": "giỏ_hàng",
    # Món ăn
    "phở bò": "phở_bò", "gà rán": "gà_rán", "trà sữa": "trà_sữa", 
    "bún chả": "bún_chả", "cơm tấm": "cơm_tấm", "cà phê sữa": "cà_phê_sữa", 
    "nước cam": "nước_cam", "bánh mì": "bánh_mì",
    
    # Option - Mới thêm
    "trứng ốp la": "trứng_ốp_la", "thêm thịt": "thêm_thịt", "thêm bún": "thêm_bún",
    "không cay": "không_cay", "ít đường": "ít_đường", "nhiều đường": "nhiều_đường",
    "trân châu đen": "trân_châu_đen", "thạch dừa": "thạch_dừa",
    "ít sữa": "ít_sữa", "nhiều sữa": "nhiều_sữa", "không đường": "không_đường",
    "ít đá": "ít_đá", "nhiều đá": "nhiều_đá", "không đá": "không_đá",
    "ít muối": "ít_muối", "thêm ớt": "thêm_ớt", "không hành": "không_hành",
    "gói mang đi": "gói_mang_đi", "ăn tại chỗ": "ăn_tại_chỗ", "giao nhanh": "giao_nhanh"
})


POS = {
    # Động từ
    "có": V, "đặt": V, "thêm": V, "cho": V, "lấy": V, "mua": V, "xem": V, "hủy": V, 
    "muốn": V, "ăn": V, "uống": V, "reset": V, "xóa": V,
    
    # Danh từ
    "món": N, "menu": N, "thực_đơn": N, "giá": N, "tôi": P, "đơn_hàng": N, 
    "giỏ_hàng": N,
    
    # Từ hỏi
    "nào": Q, "gì": Q, "bao_nhiêu": Q, "những_món_gì": Q, "món_gì": Q, 
    "món_nào": Q, "những_món_nào": Q,
    
    # Khác
    "những": DET, "trong": PP, "vào_đơn": PP, "không": YN, "đã": ADV, 
    "nhé": PUNC, "?": PUNC, ".": PUNC,
    
    # Món ăn
    "phở_bò": NAME, "gà_rán": NAME, "trà_sữa": NAME, "bún_chả": NAME, 
    "cơm_tấm": NAME, "cà_phê_sữa": NAME, "nước_cam": NAME, "bánh_mì": NAME,
    
    # Options
    "tái": ADJ, "nạm": ADJ, "gầu": ADJ, "viên": ADJ,
    "sườn": ADJ, "bì": ADJ, "chả": ADJ, "trứng_ốp_la": ADJ,
    "thêm_thịt": ADJ, "thêm_bún": ADJ,
    "cay": ADJ, "không_cay": ADJ, "giòn": ADJ,
    "ít_đường": ADJ, "nhiều_đường": ADJ, "trân_châu_đen": ADJ, "thạch_dừa": ADJ,
    "nóng": ADJ, "đá": ADJ, "ít_sữa": ADJ, "nhiều_sữa": ADJ,
    "không_đường": ADJ, "ít_đá": ADJ, "nhiều_đá": ADJ, "không_đá": ADJ,
    "ít_muối": ADJ, "thêm_ớt": ADJ, "không_hành": ADJ,
    "gói_mang_đi": ADJ, "ăn_tại_chỗ": ADJ, "giao_nhanh": ADJ
}

# Add numbers 0-999
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