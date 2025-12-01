# python/hcmut/iaslab/nlp/app/models/logical_form.py
from models.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    mapping = {r.type: r for r in relations}
    pred_rel = mapping.get("PRED")
    pred_word = pred_rel.right if pred_rel else "UNKNOWN"
    sem_relations = []
    intent = "STATEMENT"
    
    if "QUERY" in mapping:
        intent = "WH-QUERY"
        q_word = mapping["QUERY"].right
        sem_relations.append(SEM("FOCUS", q_word))
        if q_word == "bao_nhiêu" and any("giá" in [r.left, r.right] for r in relations):
            intent = "PRICE-QUERY"
        elif pred_word == "có": intent = "EXIST-QUERY"
    elif any(r.type == "YESNO" for r in relations) or any(x.right == "không" for x in relations):
        intent = "YN-QUERY"

    if "THEME" in mapping:
        theme_word = mapping["THEME"].right
        theme_node = SEM("THEME", theme_word) 
        for r in relations:
            if r.type == "QUANTITY" and (r.left == theme_word or r.left == pred_word):
                theme_node.relations.append(SEM("QUANT", r.right))
            if r.type == "MOD" and r.left == theme_word:
                theme_node.relations.append(SEM("MOD", r.right))
        sem_relations.append(theme_node)

    if "LOCATION" in mapping: sem_relations.append(SEM("LOCATION", mapping["LOCATION"].right))

    for r in relations:
        if r.type == "OF-ITEM":
            attr_node = SEM("HAS-ATTR", r.right)
            
            for sub_r in relations:
                if sub_r.type == "ATTR-LINK" and sub_r.left == r.right:
                     attr_node.relations.append(SEM("ATTR-LINK", sub_r.right))
            
            sem_relations.append(attr_node)

    return SEM(intent, "s1", [SEM("PRED", pred_word)] + sem_relations)