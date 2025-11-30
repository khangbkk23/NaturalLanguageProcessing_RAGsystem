from models.grammar_relation import SEM

class Procedure:
    def __init__(self, name:str, args:list):
        self.name = name; self.args = args
    def __str__(self): return f"{self.name}({', '.join(map(str, self.args))})"

def proceduralize(sem: SEM) -> Procedure:
    intent = sem.predicate
    pred = ""
    theme = ""
    location = ""
    attr_item = ""
    quantity = "1"
    
    # Flatten Tree
    for child in sem.relations:
        # [QUAN TRỌNG] Lấy dữ liệu từ variable (đã được fix ở logical_form.py)
        val = str(child.variable) if child.variable else ""
        
        if child.predicate == "PRED": pred = val
        elif child.predicate == "THEME": 
            theme = val
            for sub in child.relations:
                if sub.predicate == "QUANT": quantity = str(sub.variable)
        elif child.predicate == "LOCATION": location = val
        elif child.predicate == "HAS-ATTR": attr_item = val

    # --- RULES MAPPING ---

    # 1. LIST MENU: (Hỏi 'có món gì' hoặc 'trong menu')
    if (intent in ["EXIST-QUERY", "WH-QUERY"]) and \
       (theme in ["menu", "thực_đơn", "món"] or location in ["menu", "thực_đơn", "trong"]):
        return Procedure("LIST_ALL_ITEMS", [])

    # 2. ASK PRICE: (Hỏi giá)
    if intent == "PRICE-QUERY":
        target = attr_item if attr_item else theme # Ưu tiên attribute (giá của X)
        if not target and dt.POS.get(pred) == dt.NAME: target = pred # Fallback nếu parser nhận tên món là root
        return Procedure("GET_PRICE", [target])

    # 3. CHECK AVAILABILITY: (Hỏi có món X không)
    if intent in ["EXIST-QUERY", "YN-QUERY"]:
        if theme and theme not in ["menu", "món", "gì"]:
             return Procedure("CHECK_AVAILABILITY", [theme])

    # 4. ORDER HISTORY: (Hỏi lịch sử)
    if (intent in ["WH-QUERY", "STATEMENT"]) and \
       (pred in ["đặt", "gọi", "xem"] or theme in ["đơn_hàng", "những_món_gì"]):
        return Procedure("GET_ORDER_HISTORY", [])

    # 5. ADD TO CART: (Thêm món)
    if intent == "STATEMENT" and pred in ["thêm", "cho", "lấy", "đặt"]:
        return Procedure("ADD_TO_CART", [theme, quantity])

    return Procedure("UNKNOWN_PROCEDURE", [])
# Cần import models.data để dùng dt.POS trong case Ask Price
import models.data as dt