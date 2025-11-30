# python/hcmut/iaslab/nlp/app/models/logical_form.py
from models.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    mapping = {r.type: r for r in relations}
    
    # 1. Lấy vị ngữ chính
    pred_relation = mapping.get("PRED")
    pred_word = pred_relation.right if pred_relation else "UNKNOWN"
    
    sem_relations = []
    
    # 2. Xây dựng Intent
    intent = "STATEMENT"
    
    # Check QUERY
    q_relation = mapping.get("QUERY")
    if q_relation:
        q_word = q_relation.right
        sem_relations.append(SEM("FOCUS", q_word, []))
        intent = "WH-QUERY"
        
        rel_lefts = [r.left for r in relations]
        if q_word == "bao_nhiêu" and "giá" in rel_lefts:
            intent = "PRICE-QUERY"
        elif pred_word == "có":
            intent = "EXIST-QUERY"
            
    elif any(x.right == "không" for x in relations):
        intent = "YN-QUERY"

    if "THEME" in mapping:
        theme_word = mapping["THEME"].right
        theme_node = SEM("THEME", theme_word, []) 
        
        for r in relations:
            if r.type == "QUANTITY":
                if r.left == theme_word or r.left == pred_word:
                    theme_node.relations.append(SEM("QUANT", r.right, []))
        
        sem_relations.append(theme_node)

    # Thêm LOCATION
    if "LOCATION" in mapping:
        loc_word = mapping["LOCATION"].right
        sem_relations.append(SEM("LOCATION", loc_word, []))

    for r in relations:
        if r.type == "OF-ITEM":
            sem_relations.append(SEM("HAS-ATTR", r.right, []))

    return SEM(intent, "s1", [SEM("PRED", pred_word, [])] + sem_relations)