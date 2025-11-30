import models.data as dt
from models.data import ROOT, N, V, NAME, Q, PP, YN, NUM, PUNC, DET, ADV, P
RIGHT_ARC = {
    ROOT: {V: "root", N: "root"}, 
    V: {N: "dobj", Q: "query", PP: "loc", YN: "yesno", NAME: "dobj", NUM: "quan", PUNC: "punc"},
    N: {Q: "nmod", PP: "nmod", NAME: "nmod", PUNC: "punc"}, 
    NAME: {Q: "query", N: "attr", V: "acl", YN: "yesno", PUNC: "punc"},
    PP: {N: "pobj"},
    NUM: {N: "clf"}, 
}

LEFT_ARC = {
    N: {DET: "det", NAME: "nmod", PP: "nmod"}, 
    NAME: {N: "subj"}, 
    V: {ADV: "adv", P: "subj"},
    Q: {},
    PP: {V: "vmod"},
}

class Dependency:
    def __init__(self, relation: str, head: str, tail: str):
        self.relation = relation 
        self.head = head 
        self.tail = tail 
    
    def __str__(self) -> str:
        return f"\"{self.head}\" --{self.relation} -> \"{self.tail}\""

def malt_parse_helper(tokens: "list[str]") -> "list[Dependency]":
    buffer = tokens.copy()
    stack = [ROOT]
    dependencies: "list[Dependency]" = []
    
    while buffer:
        stack_item = stack[-1]
        buffer_item = buffer[0]
        
        stack_pos = dt.POS.get(stack_item, ROOT)
        
        if buffer_item.isdigit():
            buffer_pos = NUM
        else:
            buffer_pos = dt.POS.get(buffer_item, N)

        dependency = None
        
        # Thử RIGHT ARC
        if stack_pos in RIGHT_ARC and buffer_pos in RIGHT_ARC[stack_pos]:
            rel = RIGHT_ARC[stack_pos][buffer_pos]
            dependency = Dependency(rel, stack_item, buffer_item)
            stack.append(buffer.pop(0))
        # Thử LEFT ARC
        elif stack_pos in LEFT_ARC and buffer_pos in LEFT_ARC[stack_pos]:
            rel = LEFT_ARC[stack_pos][buffer_pos]
            dependency = Dependency(rel, buffer_item, stack_item)
            stack.pop()
        # SHIFT
        else:
            stack.append(buffer.pop(0))

        if dependency: dependencies.append(dependency)
        
    return dependencies

def malt_parse(sentence: str) -> "list[Dependency]":
    tokens = dt.tokenize(sentence)
    return malt_parse_helper(tokens)