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
    def __str__(self):
        return f"({self.predicate} '{self.variable}' {list(map(str, self.relations))})"

def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    relations = []
    for dep in dependencies:
        # 1. ROOT & PREDICATE
        if dep.relation == "root":
            relations.append(Relation("PRED", "s1", dep.tail))
        # 2. AGENT / SUBJECT
        elif dep.relation == "subj":
            relations.append(Relation("AGENT", "s1", dep.tail))
        # 3. THEME / OBJECT
        elif dep.relation == "dobj":
            relations.append(Relation("THEME", "s1", dep.tail))
        # 4. QUERY
        elif dep.relation == "query":
            relations.append(Relation("QUERY", "s1", dep.tail))
        # 5. MODIFIER (Quan trọng: Xử lý thông minh hơn)
        elif dep.relation == "nmod":
            # Nếu từ phụ thuộc là từ để hỏi (gì, nào...), coi là QUERY
            if dt.POS.get(dep.tail) == dt.Q:
                relations.append(Relation("QUERY", "s1", dep.tail))
            # Nếu từ phụ thuộc là Tên món ăn -> OF-ITEM (giá CỦA phở_bò)
            elif dt.POS.get(dep.tail) == dt.NAME:
                relations.append(Relation("OF-ITEM", dep.head, dep.tail))
            else:
                relations.append(Relation("MOD", dep.head, dep.tail))
        # 6. QUANTITY
        elif dep.relation == "quan" or dep.relation == "clf":
            relations.append(Relation("QUANTITY", dep.head, dep.tail))
        # 7. LOCATION
        elif dep.relation == "loc" or dep.relation == "pobj":
            relations.append(Relation("LOCATION", "s1", dep.tail))

    return relations