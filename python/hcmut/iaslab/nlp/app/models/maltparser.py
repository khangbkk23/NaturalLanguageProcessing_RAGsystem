import models.data as dt
from models.data import ROOT, N, V, NAME, Q, PP, YN, NUM, PUNC, DET, ADV, P

RIGHT_ARC = {
    ROOT: {V: "root", N: "root", NAME: "root"},
    V: {N: "dobj", Q: "query", PP: "loc", YN: "yesno", NAME: "dobj", PUNC: "punc", P: "subj"},
    N: {Q: "attr", PP: "nmod", NAME: "nmod", PUNC: "punc", N: "subj"},
    NAME: {Q: "attr", N: "attr", V: "acl", YN: "yesno", PUNC: "punc"},
    PP: {N: "pobj", NAME: "pobj"},
}

LEFT_ARC = {
    NUM: {NAME: "quan", N: "quan"}, 
    N: {DET: "det", NAME: "subj", PP: "nmod"},
    NAME: {},  # Xóa N: "subj" ở đây
    V: {ADV: "adv", P: "subj", NAME: "subj"},
    Q: {},
    PP: {V: "vmod"},
}

class Dependency:
    def __init__(self, relation: str, head: str, tail: str):
        self.relation = relation; self.head = head; self.tail = tail 
    def __str__(self) -> str: return f"\"{self.head}\" --{self.relation} -> \"{self.tail}\""

def malt_parse_helper(tokens: "list[str]") -> "list[Dependency]":
    buffer = tokens.copy()
    stack = [ROOT]
    dependencies = []
    
    while buffer:
        if len(stack) < 1:
            stack.append(buffer.pop(0))
            continue
            
        stack_item = stack[-1]
        buffer_item = buffer[0]
        stack_pos = dt.POS.get(stack_item, ROOT)
        buffer_pos = NUM if buffer_item.isdigit() else dt.POS.get(buffer_item, N)

        dependency = None
        
        # ← FIX: Ưu tiên tạo root cho VERB
        if stack_pos == ROOT and buffer_pos == dt.V:
            dependency = Dependency("root", ROOT, buffer_item)
            stack.append(buffer.pop(0))
            dependencies.append(dependency)
            continue
        
        # ← FIX: Ưu tiên LEFT_ARC cho V <- P (subj)
        if stack_pos == dt.V and buffer_pos == dt.P:
            dependency = Dependency("subj", buffer_item, stack_item)
            stack.pop()
            dependencies.append(dependency)
            continue
        
        # RIGHT_ARC
        if stack_pos in RIGHT_ARC and buffer_pos in RIGHT_ARC[stack_pos]:
            rel = RIGHT_ARC[stack_pos][buffer_pos]
            dependency = Dependency(rel, stack_item, buffer_item)
            stack.append(buffer.pop(0))
            
        # LEFT_ARC
        elif (stack_pos in LEFT_ARC and buffer_pos in LEFT_ARC[stack_pos] 
              and (len(buffer) == 1 or not _has_right_child(stack_pos, dt.POS.get(buffer[1], dt.N)))):
            rel = LEFT_ARC[stack_pos][buffer_pos]
            dependency = Dependency(rel, buffer_item, stack_item)
            stack.pop()
            
        else:
            stack.append(buffer.pop(0))

        if dependency: 
            dependencies.append(dependency)
        
    return dependencies

def _has_right_child(pos, next_pos):
    return pos in RIGHT_ARC and next_pos in RIGHT_ARC[pos]

def malt_parse(sentence: str) -> "list[Dependency]":
    tokens = dt.tokenize(sentence)
    return malt_parse_helper(tokens)