import os
import models.data as dt
from models.data import ROOT, N, V, NAME, Q, PP, YN, NUM, PUNC, DET, ADV, P

class Dependency:
    def __init__(self, relation: str, head: str, tail: str):
        self.relation = relation; self.head = head; self.tail = tail 
    def __str__(self) -> str: return f"\"{self.head}\" --{self.relation} -> \"{self.tail}\""

RIGHT_ARC = {}
LEFT_ARC = {}
GRAMMAR_LOADED = False

def load_grammar():
    global RIGHT_ARC, LEFT_ARC, GRAMMAR_LOADED
    
    if GRAMMAR_LOADED: return
    RIGHT_ARC = {}
    LEFT_ARC = {}

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    grammar_path = os.path.join(base_dir, 'data', 'grammar.txt')
    
    if not os.path.exists(grammar_path):
        grammar_path = os.path.join(base_dir, '../data/grammar.txt')

    if not os.path.exists(grammar_path):
        grammar_path = os.path.join(os.getcwd(), 'python/hcmut/iaslab/nlp/data/grammar.txt')

    if not os.path.exists(grammar_path):
        print(f"Không tìm thấy grammar.txt tại: {grammar_path}")
        return

    print(f"Đang tải văn phạm từ: {grammar_path}")
    
    try:
        with open(grammar_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split()
                if len(parts) < 4: continue
                
                head_str, rel, dep_str, direction = parts
                head_pos = getattr(dt, head_str, head_str)
                dep_pos = getattr(dt, dep_str, dep_str)
                
                if direction == 'RIGHT':
                    if head_pos not in RIGHT_ARC: RIGHT_ARC[head_pos] = {}
                    RIGHT_ARC[head_pos][dep_pos] = rel
                elif direction == 'LEFT':
                    if dep_pos not in LEFT_ARC: LEFT_ARC[dep_pos] = {}
                    LEFT_ARC[dep_pos][head_pos] = rel
        
        GRAMMAR_LOADED = True
        print(f"Đã tải xong văn phạm.")
        
    except Exception as e:
        print(f"Lỗi khi đọc file grammar: {e}")

def malt_parse_helper(tokens: "list[str]") -> "list[Dependency]":
    if not GRAMMAR_LOADED:
        load_grammar()
        
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
        
        if stack_pos == ROOT and buffer_pos == dt.V:
            dependency = Dependency("root", ROOT, buffer_item)
            stack.append(buffer.pop(0))
            dependencies.append(dependency)
            continue

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