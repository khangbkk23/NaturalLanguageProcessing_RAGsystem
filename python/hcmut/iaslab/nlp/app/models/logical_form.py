from models.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    mapping = {r.type: r for r in relations}
    
    # 1. PREDICATE
    pred_rel = mapping.get("PRED")
    pred_word = pred_rel.right if pred_rel else "UNKNOWN"
    
    sem_relations = []
    intent = "STATEMENT"
    
    # 2. INTENT DETECTION
    if "QUERY" in mapping:
        intent = "WH-QUERY"
        q_word = mapping["QUERY"].right
        sem_relations.append(SEM("FOCUS", q_word))
        
        # Logic phát hiện câu hỏi giá hoặc tồn tại
        has_price = any("giá" in [r.left, r.right] for r in relations)
        if q_word == "bao_nhiêu" and has_price: intent = "PRICE-QUERY"
        elif pred_word == "có": intent = "EXIST-QUERY"
    elif any(x.right == "không" for x in relations):
        intent = "YN-QUERY"

    # 3. THEME & QUANTITY
    if "THEME" in mapping:
        theme_word = mapping["THEME"].right
        theme_node = SEM("THEME", theme_word) 
        
        for r in relations:
            if r.type == "QUANTITY":
                if r.left == theme_word or r.left == pred_word:
                    theme_node.relations.append(SEM("QUANT", r.right))
        sem_relations.append(theme_node)

    # 4. LOCATION & ATTRIBUTE
    if "LOCATION" in mapping:
        sem_relations.append(SEM("LOCATION", mapping["LOCATION"].right))

    for r in relations:
        if r.type == "OF-ITEM":
            sem_relations.append(SEM("HAS-ATTR", r.right))

    return SEM(intent, "s1", [SEM("PRED", pred_word)] + sem_relations)