from models.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    mapping = {r.type: r for r in relations}
    
    # Lấy Predicate
    pred_relation = mapping.get("PRED")
    pred_word = pred_relation.right if pred_relation else "UNKNOWN"
    
    sem_relations = []
    intent = "STATEMENT"
    
    # 1. Xử lý QUERY (Intent Detection)
    q_relation = mapping.get("QUERY")
    if q_relation:
        q_word = q_relation.right
        sem_relations.append(SEM("FOCUS", q_word))
        intent = "WH-QUERY"
        
        # Logic phát hiện hỏi giá: Từ hỏi là 'bao_nhiêu' VÀ có từ 'giá' xuất hiện bất cứ đâu
        has_price_keyword = any("giá" in [r.left, r.right] for r in relations)
        
        if q_word == "bao_nhiêu" and has_price_keyword:
            intent = "PRICE-QUERY"
        elif pred_word == "có":
            intent = "EXIST-QUERY"
            
    elif any(x.right == "không" for x in relations):
        intent = "YN-QUERY"

    # 2. Xử lý THEME (Món ăn) & QUANTITY (Số lượng)
    if "THEME" in mapping:
        theme_word = mapping["THEME"].right
        theme_node = SEM("THEME", theme_word) # [FIX] Lưu theme_word vào variable
        
        for r in relations:
            # Tìm số lượng gắn vào Theme hoặc gắn vào Động từ (như "Thêm 2 trà sữa")
            if r.type == "QUANTITY":
                if r.left == theme_word or r.left == pred_word:
                    theme_node.relations.append(SEM("QUANT", r.right))
        
        sem_relations.append(theme_node)

    # 3. Xử lý LOCATION & ATTRIBUTE
    if "LOCATION" in mapping:
        sem_relations.append(SEM("LOCATION", mapping["LOCATION"].right))

    for r in relations:
        if r.type == "OF-ITEM": # Attribute (tên món trong câu hỏi giá)
            sem_relations.append(SEM("HAS-ATTR", r.right))

    return SEM(intent, "s1", [SEM("PRED", pred_word)] + sem_relations)