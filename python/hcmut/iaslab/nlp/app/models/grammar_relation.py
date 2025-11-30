import models.data as dt
from models.maltparser import Dependency

class Relation:
    def __init__(self, type: str, left: str, right: str):
        self.type = type; self.left = left; self.right = right
    def __str__(self): return f"({self.left} {self.type} {self.right})"

class SEM:
    def __init__(self, predicate: str, variable, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    def __str__(self): return f"({self.predicate} '{self.variable}' {len(self.relations)})"

def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    relations = []
    
    # Extract động từ từ dependencies
    verbs_in_deps = set()
    for dep in dependencies:
        if dt.POS.get(dep.head) == dt.V:
            verbs_in_deps.add(dep.head)
        if dt.POS.get(dep.tail) == dt.V:
            verbs_in_deps.add(dep.tail)
    
    # ← THÊM: Map để track classifier -> actual item
    classifier_to_item = {}  # {"ly": "trà_sữa"}
    quantity_map = {}        # {"ly": "2"}
    
    # First pass: Build mappings
    for dep in dependencies:
        if dep.relation == "nmod":
            # ly -> trà_sữa
            if dt.POS.get(dep.tail) == dt.NAME:
                classifier_to_item[dep.head] = dep.tail
        elif dep.relation in ["quan", "clf"]:
            # ly -> 2
            quantity_map[dep.head] = dep.tail
    
    # Second pass: Create relations
    for dep in dependencies:
        if dep.relation == "root": 
            relations.append(Relation("PRED", "s1", dep.tail))
            
        elif dep.relation == "subj": 
            relations.append(Relation("AGENT", "s1", dep.tail))
            
        elif dep.relation == "dobj": 
            # ← FIX: Nếu dobj là classifier (ly, tô), thay bằng actual item
            actual_item = classifier_to_item.get(dep.tail, dep.tail)
            relations.append(Relation("THEME", "s1", actual_item))
            
            # ← FIX: Gắn QUANTITY vào actual item
            if dep.tail in quantity_map:
                qty = quantity_map[dep.tail]
                relations.append(Relation("QUANTITY", actual_item, qty))
            
            # Infer PRED từ head của dobj
            if not any(r.type == "PRED" for r in relations):
                if dt.POS.get(dep.head) == dt.V:
                    relations.insert(0, Relation("PRED", "s1", dep.head))
        
        elif dep.relation == "query": 
            relations.append(Relation("QUERY", "s1", dep.tail))
        
        elif dep.relation == "nmod":
            head_pos = dt.POS.get(dep.head)
            tail_pos = dt.POS.get(dep.tail)
            
            # ← FIX: Bỏ qua nmod nếu head là classifier
            if dep.head in classifier_to_item:
                continue  # Đã xử lý ở trên
            
            if head_pos == dt.N and tail_pos == dt.NAME:
                for r in relations:
                    if r.type == "THEME" and r.right == dep.head:
                        r.right = dep.tail
                        break
                else:
                    relations.append(Relation("THEME", "s1", dep.tail))
            
            elif tail_pos == dt.Q:
                relations.append(Relation("QUERY", "s1", dep.tail))
            else:
                relations.append(Relation("MOD", dep.head, dep.tail))
        
        elif dep.relation == "attr":
            head_pos = dt.POS.get(dep.head)
            tail_pos = dt.POS.get(dep.tail)
            
            if head_pos == dt.NAME and tail_pos == dt.N and dep.tail == "giá":
                for r in relations:
                    if r.type == "PRED" and r.right == dep.head:
                        relations.remove(r)
                        break
                relations.append(Relation("PRED", "s1", "giá"))
                relations.append(Relation("THEME", "s1", dep.head))
            
            elif head_pos == dt.N and tail_pos == dt.Q:
                relations.append(Relation("QUERY", "s1", dep.tail))
            
            else:
                relations.append(Relation("OF-ITEM", dep.head, dep.tail))
             
        elif dep.relation == "yesno": 
            relations.append(Relation("YESNO", "s1", dep.tail))
            
        elif dep.relation in ["quan", "clf"]:
            continue
            
        elif dep.relation in ["loc", "pobj"]: 
            relations.append(Relation("LOCATION", "s1", dep.tail))
    
    return relations