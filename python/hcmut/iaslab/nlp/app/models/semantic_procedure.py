# python/hcmut/iaslab/nlp/app/models/semantic_procedure.py
from models.grammar_relation import SEM
import models.data as dt

class Procedure:
    def __init__(self, name:str, args:list):
        self.name = name; self.args = args
    def __str__(self): return f"{self.name}({', '.join(map(str, self.args))})"

# Hàm đệ quy để lấy hết option nối tiếp (A -> B -> C)
def collect_linked_options(sem_node, collected_list):
    if hasattr(sem_node, 'relations'):
        for child in sem_node.relations:
            if child.predicate == "ATTR-LINK" or child.predicate == "OF-ITEM":
                val = str(child.variable)
                if val not in collected_list:
                    collected_list.append(val)
                collect_linked_options(child, collected_list)

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
    
    for child in sem.relations:
        val = str(child.variable) if child.variable else ""
        if child.predicate == "PRED": pred = val
        elif child.predicate == "THEME": 
            theme = val
            if hasattr(child, 'relations'):
                mods = []
                for sub in child.relations:
                    if sub.predicate == "QUANT": quantity = str(sub.variable)
                    elif sub.predicate == "MOD": mods.append(str(sub.variable))
                if mods: theme = f"{theme} {' '.join(mods)}"
        elif child.predicate == "AGENT": agent = val
        elif child.predicate == "LOCATION": location = val; has_location_context = True
        
        elif child.predicate == "HAS-ATTR": 
            if val not in options: options.append(val)
            # Tìm các option con nối vào option này
            collect_linked_options(child, options)
            
        elif child.predicate in ["QUERY", "FOCUS"]: query_word = val

    if intent == "STATEMENT" and pred in ["thêm", "cho", "lấy", "đặt", "mua"]:
        if theme: return Procedure("ADD_TO_CART", [theme, quantity, options])
    
    if intent in ["WH-QUERY", "STATEMENT"]:
        is_asking_what = query_word in ["những_món_gì", "món_gì", "gì"]
        if (is_asking_what and not has_location_context) or \
           (pred in ["xem", "gọi"] or theme == "đơn_hàng" or (pred == "đặt" and not theme)):
            return Procedure("GET_ORDER_HISTORY", [])
    
    if (intent in ["EXIST-QUERY", "WH-QUERY"]) and \
       (theme in ["menu", "thực_đơn"] or location in ["menu", "thực_đơn", "trong"]):
        return Procedure("LIST_ALL_ITEMS", [])

    if intent == "PRICE-QUERY":
        target = options[0] if options else theme 
        if not target: target = agent
        if target == "giá": target = theme
        if not target and dt.POS.get(pred) == dt.NAME: target = pred
        return Procedure("GET_PRICE", [target])

    if intent in ["EXIST-QUERY", "YN-QUERY"]:
        target = theme if theme else agent
        if target and target not in ["menu", "món", "gì", "những_món_gì", "món_nào"]:
            return Procedure("CHECK_AVAILABILITY", [target])
            
    if pred == "có" and theme and theme not in ["menu", "món", "gì"]:
         return Procedure("CHECK_AVAILABILITY", [theme])

    return Procedure("UNKNOWN_PROCEDURE", [])