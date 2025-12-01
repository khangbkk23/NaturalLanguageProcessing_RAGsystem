# python/hcmut/iaslab/nlp/app/models/semantic_procedure.py
from models.grammar_relation import SEM
import models.data as dt

class Procedure:
    def __init__(self, name:str, args:list):
        self.name = name; self.args = args
    def __str__(self): return f"{self.name}({', '.join(map(str, self.args))})"

def proceduralize(sem: SEM) -> Procedure:
    intent = sem.predicate
    pred = ""
    theme = ""
    agent = "" 
    location = ""
    options = [] 
    quantity = "1"
    query_word = ""
    has_location_context = False
    
    # 1. Flatten Tree
    for child in sem.relations:
        val = str(child.variable) if child.variable else ""
        
        if child.predicate == "PRED": 
            pred = val
        elif child.predicate == "THEME": 
            theme = val
            if hasattr(child, 'relations'):
                for sub in child.relations:
                    if sub.predicate == "QUANT": 
                        quantity = str(sub.variable)
        elif child.predicate == "AGENT": 
            agent = val
        elif child.predicate == "LOCATION": 
            location = val
            has_location_context = True
        elif child.predicate == "HAS-ATTR": 
            options.append(val)
        elif child.predicate == "QUERY":
            query_word = val
        elif child.predicate == "FOCUS":
            query_word = val

    # --- MAPPING RULES ---
    
    # 2. ADD TO CART
    if intent == "STATEMENT" and pred in ["thêm", "cho", "lấy", "đặt", "mua"]:
        if theme and dt.POS.get(theme) == dt.NAME:
            return Procedure("ADD_TO_CART", [theme, quantity, options])
    
    # 3. HISTORY
    if intent in ["WH-QUERY", "STATEMENT"]:
        is_asking_what = query_word in ["những_món_gì", "món_gì", "gì"]
        if (is_asking_what and not has_location_context) or \
           (pred in ["xem", "gọi"]) or \
           (theme == "đơn_hàng") or \
           (pred == "đặt" and not theme):
            return Procedure("GET_ORDER_HISTORY", [])
    
    # 4. LIST MENU
    if (intent in ["EXIST-QUERY", "WH-QUERY"]) and \
       (theme in ["menu", "thực_đơn"] or 
        location in ["menu", "thực_đơn", "trong"] or
        (query_word == "những_món_gì" and has_location_context)):
        return Procedure("LIST_ALL_ITEMS", [])

    # 5. ASK PRICE
    if intent == "PRICE-QUERY":
        # Ưu tiên lấy Option đầu tiên làm target hỏi giá
        target = options[0] if options else theme 
        if not target: target = agent
        if target == "giá": target = theme
        if not target and dt.POS.get(pred) == dt.NAME: target = pred
        
        return Procedure("GET_PRICE", [target])

    # 6. CHECK AVAILABILITY
    if intent in ["EXIST-QUERY", "YN-QUERY"]:
        target = theme if theme else agent
        if target and target not in ["menu", "món", "gì", "những_món_gì"]:
            return Procedure("CHECK_AVAILABILITY", [target])

    return Procedure("UNKNOWN_PROCEDURE", [])