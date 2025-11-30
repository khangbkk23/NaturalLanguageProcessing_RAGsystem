# python/hcmut/iaslab/nlp/app/models/grammar_relation.py
from models.data import *
from models.maltparser import Dependency

class Relation:
    def __init__(self, type: str, left: str, right: str):
        self.type = type
        self.left = left
        self.right = right
    
    def __str__(self) -> str:
        return f"({self.left} {self.type} {self.right})"

class SEM:
    def __init__(self, predicate: str, variable, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable}" \
                + f"{' ' + ' '.join(map(str, self.relations)) if self.relations else ''})"

def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    """
    Chuyển đổi Dependency Parse thành Semantic Relations.
    """
    relations = []
  
    for dep in dependencies:
        # dep.head: từ cha, dep.tail: từ con, dep.relation: nhãn quan hệ
        
        # 1. Xác định Vị ngữ chính (PREDICATE)
        if dep.relation == "root":
            relations.append(Relation("PRED", "s1", dep.tail))

        # 2. Xác định Chủ thể hành động (AGENT)
        elif dep.relation == "subj":
            relations.append(Relation("AGENT", "s1", dep.tail))

        # 3. Xác định Đối tượng chịu tác động (THEME)
        elif dep.relation == "dobj":
            relations.append(Relation("THEME", "s1", dep.tail))

        # 4. Xác định Thông tin cần hỏi
        elif dep.relation == "query":
            relations.append(Relation("QUERY", "s1", dep.tail))

        # 5. Xác định Thuộc tính (ATTRIBUTE/MODIFIER)
        elif dep.relation == "nmod":
            if POS.get(dep.tail) == NAME:
                relations.append(Relation("OF-ITEM", dep.head, dep.tail)) # giá OF phở_bò
            else:
                relations.append(Relation("MOD", dep.head, dep.tail))

        # 6. Xác định Số lượng (QUANTITY)
        elif dep.relation == "quan":
            relations.append(Relation("QUANTITY", dep.head, dep.tail))

        # 7. Xác định Vị trí/Đích đến (LOCATION/GOAL)
        elif dep.relation == "loc":
            relations.append(Relation("LOCATION", "s1", dep.tail))

    return relations