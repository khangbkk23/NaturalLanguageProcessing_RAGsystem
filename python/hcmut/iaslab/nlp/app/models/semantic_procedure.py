# python/hcmut/iaslab/nlp/app/models/semantic_procedure.py
from models.grammar_relation import SEM

class Procedure:
    def __init__(self, name:str, args:list):
        self.name = name
        self.args = args
    def __str__(self): return f"{self.name}({', '.join(self.args)})"

def proceduralize(sem: SEM) -> Procedure:
    """
    Chuyển đổi Logical form thành Procedural semantics.
    """
    intent = sem.predicate
    pred = ""
    theme = ""
    location = ""
    attr_item = ""
    quantity = "1"
    
    # Trích xuất thông tin từ cây SEM
    for child in sem.relations:
        if child.predicate == "PRED": 
            pred = child.variable
        elif child.predicate == "THEME": 
            theme = child.variable
            for sub in child.relations:
                if sub.predicate == "QUANT": 
                    quantity = sub.variable
        elif child.predicate == "LOCATION":
            location = child.variable
        elif child.predicate == "HAS-ATTR":
            attr_item = child.variable

    
    # 1. Câu hỏi liệt kê menu
    # "Có những món nào?" -> (EXIST-QUERY, PRED có, THEME món)
    if intent == "EXIST-QUERY" and theme in ["menu", "món", "thực_đơn", "trong"]:
        return Procedure("LIST_ALL_ITEMS", [])

    # 2. Câu hỏi giá
    # "Phở bò giá bao nhiêu?" -> (PRICE-QUERY, ...)
    if intent == "PRICE-QUERY":
        # item nằm ở attribute (giá CỦA phở_bò) hoặc theme
        target = attr_item if attr_item else theme
        return Procedure("GET_PRICE", [target])

    # 3. Câu hỏi tồn tại món (Yes/No)
    # "Có món gà rán không?" -> (EXIST-QUERY, PRED có, THEME gà_rán)
    if intent == "EXIST-QUERY" or intent == "YN-QUERY":
        return Procedure("CHECK_AVAILABILITY", [theme])

    # 4. Câu hỏi lịch sử đặt hàng
    # "Tôi đã đặt món gì?" -> (WH-QUERY, PRED đặt)
    if intent == "WH-QUERY" and pred == "đặt":
        return Procedure("GET_ORDER_HISTORY", ["user_current"])

    # 5. Hành động thêm vào giỏ
    # "Thêm 1 trà sữa" -> (STATEMENT, PRED thêm, THEME trà_sữa, QUANT 1)
    if intent == "STATEMENT" and pred in ["thêm", "đặt"]:
        return Procedure("ADD_TO_CART", [theme, quantity])

    return Procedure("UNKNOWN_PROCEDURE", [])