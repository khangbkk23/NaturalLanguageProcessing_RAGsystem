from collections import OrderedDict
import re
from unicodedata import normalize

# --- CONSTANTS ---
ROOT = "ROOT"
N = "NOUN"; V = "VERB"; PP = "PREPOSITION"; Q = "QUERY"; NAME = "NAME"
PUNC = "PUNC"; YN = "YESNO"; ADV = "ADVERB"; P = "PRONOUN"; DET = "DETERMINER"; NUM = "NUMBER"
ADJ = "ADJECTIVE" 

TOKENIZE_DICT = OrderedDict({
    "có bán": "có",
    
    "sốt phô mai": "sốt_phô_mai",
    "sốt cay": "sốt_cay",
    "phô mai": "phô_mai",
    "cay": "cay",

    "thêm sầu riêng": "thêm_sầu_riêng",
    "trân châu đen": "trân_châu_đen", 
    "trân châu trắng": "trân_châu_trắng",
    "thạch dừa": "thạch_dừa",
    "kem cheese": "kem_cheese",
    "cam sả": "cam_sả", 
    "thêm đào": "thêm_đào",
    
    "trứng ốp la": "trứng_ốp_la",
    "ốp la": "ốp_la",
    "thịt nướng": "thịt_nướng",
    "chả lụa": "chả_lụa",
    "chả cua": "chả_cua",
    "giò heo": "giò_heo",
    "tôm thịt": "tôm_thịt",
    "tai heo": "tai_heo",
    "tương đen": "tương_đen",
    "mắm nêm": "mắm_nêm",
    "hải sản": "hải_sản",
    "xúc xích": "xúc_xích",
    
    "thêm bò": "thêm_bò", 
    "thêm bánh": "thêm_bánh",
    "thêm thịt": "thêm_thịt", 
    "thêm bún": "thêm_bún",
    "thêm cơm": "thêm_cơm",
    "thêm gà": "thêm_gà",

    "ít đường": "ít_đường", "nhiều đường": "nhiều_đường", "không đường": "không_đường",
    "ít sữa": "ít_sữa", "nhiều sữa": "nhiều_sữa",
    "ít đá": "ít_đá", "nhiều đá": "nhiều_đá", "không đá": "không_đá",
    "ít ngọt": "ít_ngọt", "ít muối": "ít_muối", "ít dầu": "ít_dầu",
    "không hành": "không_hành", "không rau": "không_rau", "thêm ớt": "thêm_ớt",
    
    "size lớn": "size_lớn", "size nhỏ": "size_nhỏ",
    "đế dày": "đế_dày", "đế mỏng": "đế_mỏng",
    "đặc biệt": "đặc_biệt", "bạc xỉu": "bạc_xỉu",
    "gói mang đi": "gói_mang_đi", "ăn tại chỗ": "ăn_tại_chỗ", "giao nhanh": "giao_nhanh",

    "phở bò": "phở_bò", "gà rán": "gà_rán", "trà sữa": "trà_sữa", 
    "bún chả": "bún_chả", "cơm tấm": "cơm_tấm", "cà phê sữa": "cà_phê_sữa", 
    "nước cam": "nước_cam", "bánh mì": "bánh_mì", "pizza": "pizza",
    "bún bò huế": "bún_bò_huế", "mì xào": "mì_xào", "gỏi cuốn": "gỏi_cuốn",
    "trà đào": "trà_đào", "sinh tố bơ": "sinh_tố_bơ",

    "bao nhiêu": "bao_nhiêu", "món nào": "món_nào", "những món gì": "những_món_gì", 
    "món gì": "món_gì", "vào đơn": "vào_đơn", "đơn hàng": "đơn_hàng", "thực đơn": "menu",
    "hết hàng": "hết_hàng", "là gì": "là_gì", "giỏ hàng": "giỏ_hàng",
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
    "món_nào": Q, "những_món_nào": Q, "là_gì": Q,
    
    "những": DET, "trong": PP, "vào_đơn": PP, "không": YN, "đã": ADV, 
    "nhé": PUNC, "?": PUNC, ".": PUNC,
    
    # Tên món ăn
    "phở_bò": NAME, "gà_rán": NAME, "trà_sữa": NAME, "bún_chả": NAME, 
    "cơm_tấm": NAME, "cà_phê_sữa": NAME, "nước_cam": NAME, "bánh_mì": NAME, "pizza": NAME,
    "bún_bò_huế": NAME, "mì_xào": NAME, "gỏi_cuốn": NAME, "trà_đào": NAME, "sinh_tố_bơ": NAME,
    
    # Phở/Bún
    "tái": ADJ, "nạm": ADJ, "gầu": ADJ, "viên": ADJ, "gân": ADJ,
    "đặc_biệt": ADJ, "thêm_bò": ADJ, "thêm_bánh": ADJ, "thêm_thịt": ADJ, "thêm_bún": ADJ,
    "không_hành": ADJ, "ít_muối": ADJ, "thêm_ớt": ADJ, "giò_heo": ADJ, "chả_cua": ADJ,
    
    # Cơm/Bánh mì
    "sườn": ADJ, "bì": ADJ, "chả": ADJ, "trứng_ốp_la": ADJ, "thịt_nướng": ADJ, 
    "chả_lụa": ADJ, "pate": ADJ, "ốp_la": ADJ, "không_rau": ADJ,
    
    # Gà/Pizza/Mì
    "cay": ADJ, "không_cay": ADJ, "giòn": ADJ, "sốt_phô_mai": ADJ, "sốt_cay": ADJ,
    "đùi": ADJ, "cánh": ADJ, "ức": ADJ, "hải_sản": ADJ, "xúc_xích": ADJ, "nhiều_phô_mai": ADJ,
    "đế_dày": ADJ, "đế_mỏng": ADJ, "ít_dầu": ADJ,
    
    # Gỏi cuốn
    "tôm_thịt": ADJ, "tai_heo": ADJ, "tương_đen": ADJ, "mắm_nêm": ADJ,
    
    # Đồ uống
    "size_lớn": ADJ, "size_nhỏ": ADJ, "bạc_xỉu": ADJ,
    "ít_đường": ADJ, "nhiều_đường": ADJ, "không_đường": ADJ, "ít_ngọt": ADJ,
    "trân_châu_đen": ADJ, "thạch_dừa": ADJ, "cam_sả": ADJ, "thêm_đào": ADJ, "thêm_sầu_riêng": ADJ,
    "nóng": ADJ, "đá": ADJ, "ít_sữa": ADJ, "nhiều_sữa": ADJ,
    "ít_đá": ADJ, "nhiều_đá": ADJ, "không_đá": ADJ,
    
    # Dịch vụ
    "gói_mang_đi": ADJ, "ăn_tại_chỗ": ADJ, "giao_nhanh": ADJ
}

# Add numbers 0-999
for i in range(1000): POS[str(i)] = NUM
for t in ["một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười", "chục", "trăm"]:
    POS[t] = NUM

def tokenize(text: str) -> "list[str]":
    if not text: return []
    text = normalize("NFC", text).lower()
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(.)\?", r"\1 ?", text)
    text = re.sub(r"(.)\.", r"\1 .", text)
    
    for k, v in TOKENIZE_DICT.items():
        if k in text: text = text.replace(k, v)
    
    tokens = []
    for t in text.split(" "):
        if not t.strip(): continue
        tokens.append(t)
        
    return tokens