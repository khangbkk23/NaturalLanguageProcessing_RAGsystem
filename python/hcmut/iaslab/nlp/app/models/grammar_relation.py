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
    
    # Mapping
    classifier_to_item = {} 
    quantity_map = {} 
    for dep in dependencies:
        if dep.relation == "nmod" and dt.POS.get(dep.tail) == dt.NAME:
            classifier_to_item[dep.head] = dep.tail
        elif dep.relation in ["quan", "clf"]:
            quantity_map[dep.head] = dep.tail
    
    for dep in dependencies:
        # ROOT / SUBJ / DOBJ
        if dep.relation == "root": 
            relations.append(Relation("PRED", "s1", dep.tail))
        elif dep.relation == "subj": 
            relations.append(Relation("AGENT", "s1", dep.tail))
        elif dep.relation == "dobj": 
            actual_item = classifier_to_item.get(dep.tail, dep.tail)
            relations.append(Relation("THEME", "s1", actual_item))
            if dep.tail in quantity_map:
                relations.append(Relation("QUANTITY", actual_item, quantity_map[dep.tail]))
            if not any(r.type == "PRED" for r in relations):
                if dt.POS.get(dep.head) == dt.V:
                    relations.insert(0, Relation("PRED", "s1", dep.head))
        
        elif dep.relation == "query": 
            relations.append(Relation("QUERY", "s1", dep.tail))
        
        # NMOD
        elif dep.relation == "nmod":
            if dep.head in classifier_to_item: continue 
            head_pos = dt.POS.get(dep.head)
            tail_pos = dt.POS.get(dep.tail)
            
            if head_pos == dt.N and tail_pos == dt.NAME:
                found = False
                for r in relations:
                    if r.type == "THEME" and r.right == dep.head:
                        r.right = dep.tail
                        found = True
                        break
                if not found: relations.append(Relation("THEME", "s1", dep.tail))
            elif tail_pos == dt.Q:
                relations.append(Relation("QUERY", "s1", dep.tail))
            else:
                relations.append(Relation("MOD", dep.head, dep.tail))
        
        elif dep.relation == "attr":
            if dep.tail == "giá":
                relations.append(Relation("PRED", "s1", "giá"))
                relations.append(Relation("THEME", "s1", dep.head))
            else:
                if dt.POS.get(dep.head) == dt.ADJ or dt.POS.get(dep.head) == dt.N:
                     relations.append(Relation("ATTR-LINK", dep.head, dep.tail))

                relations.append(Relation("OF-ITEM", dep.head, dep.tail))
             
        elif dep.relation == "yesno": 
            relations.append(Relation("YESNO", "s1", dep.tail))
        elif dep.relation in ["loc", "pobj"]: 
            relations.append(Relation("LOCATION", "s1", dep.tail))
    
    return relations