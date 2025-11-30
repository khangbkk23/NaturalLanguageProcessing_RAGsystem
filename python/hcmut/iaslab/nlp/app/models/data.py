from collections import OrderedDict
import re
from unicodedata import normalize

# Import Database để lấy dữ liệu động
# Lưu ý: Import bên trong hoặc xử lý khéo để tránh Circular Import nếu cấu trúc dự án phức tạp
# Ở đây ta giả định data.py là tầng thấp nhất, có thể import database wrapper
try:
    from models.database import RestaurantDatabase
except ImportError:
    # Fallback cho trường hợp chạy unit test riêng lẻ
    RestaurantDatabase = None

# ==================== 1. ĐỊNH NGHĨA HẰNG SỐ (CONSTANTS) ====================
N = "NOUN"
V = "VERB"
PP = "PREPOSITION"
Q = "QUERY"
NAME = "NAME"
PUNC = "PUNC"
YN = "YESNO"
ADV = "ADVERB"
P = "PRONOUN"
DET = "DETERMINER"
NUM = "NUMBER"

# ==================== 2. TỪ VỰNG CỐ ĐỊNH (STATIC LEXICON) ====================
# Chỉ chứa các từ chức năng, ngữ pháp, không chứa tên món ăn cụ thể
STATIC_TOKENIZE = OrderedDict({
    "bao nhiêu": "bao_nhiêu",
    "món nào": "món_nào",
    "những món gì": "những_món_gì",
    "món gì": "món_gì",
    "vào đơn": "vào_đơn",
    "đơn hàng": "đơn_hàng",
    "thực đơn": "menu",
    "hết hàng": "hết_hàng"
})

STATIC_POS = {
    "có": V,
    "những": DET,
    "món": N,
    "nào": Q,
    "trong": PP,
    "menu": N,
    "thực_đơn": N,
    "giá": N,
    "bao_nhiêu": Q,
    "không": YN,
    "tôi": P,
    "đã": ADV,
    "đặt": V,
    "những_món_gì": Q,
    "món_gì": Q,
    "thêm": V,
    "bớt": V,
    "hủy": V,
    "xóa": V,
    "lấy": V,
    "cho": V,
    "1": NUM, "2": NUM, "3": NUM, "4": NUM, "5": NUM,
    "ly": N,
    "phần": N,
    "tô": N,
    "dĩa": N,
    "chén": N,
    "cốc": N,
    "suất": N,
    "vào_đơn": PP,
    "?": PUNC,
    ".": PUNC,
    "nhé": PUNC,
    "gì": Q,
    "ạ": PUNC,
}

PRONOUN = ["tôi", "em", "anh", "bạn", "mình", "shop", "quán"]

# ==================== 3. HÀM KHỞI TẠO DỮ LIỆU ĐỘNG ====================

def load_dynamic_data():

    final_tokenize = STATIC_TOKENIZE.copy()
    final_pos = STATIC_POS.copy()
    if RestaurantDatabase:
        try:
            db = RestaurantDatabase()
            items = db.get_all_items()
            
            for item in items:
                raw_name = item['name'].lower().strip()
                token_name = raw_name.replace(" ", "_")
                final_tokenize[raw_name] = token_name
                final_pos[token_name] = NAME
                
                if 'options' in item:
                    for opt in item['options']:
                        opt_raw = opt.lower().strip()
                        opt_token = opt_raw.replace(" ", "_")
                        final_tokenize[opt_raw] = opt_token
                        if opt_token not in final_pos:
                            final_pos[opt_token] = N

        except Exception as e:
            print(f"Warning: Không thể load dữ liệu động từ DB: {e}")
    
    sorted_tokenize = OrderedDict(
        sorted(final_tokenize.items(), key=lambda x: len(x[0]), reverse=True)
    )
    
    return sorted_tokenize, final_pos


TOKENIZE_DICT, POS = load_dynamic_data()