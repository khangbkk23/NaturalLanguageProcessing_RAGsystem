import os
import random
from .grammar import CFGrammar
from .utils import load_grammar_with_lexicons, LEXICON_CONFIG, DATA_DIR, OUTPUT_DIR

def generate_from_symbol_random(grammar: CFGrammar, symbol: str, max_depth=15) -> str:
    if max_depth <= 0: return ""
    
    if not grammar.is_non_terminal(symbol):
        return symbol

    if symbol not in grammar.rules or not grammar.rules[symbol]:
        return ""

    production = random.choice(grammar.rules[symbol])
    if not production: return ""

    parts = []
    for s in production:
        generated_part = generate_from_symbol_random(grammar, s, max_depth - 1)
        if generated_part:
            parts.append(generated_part)
    
    return " ".join(parts)

def generate_batch(grammar: CFGrammar, symbol: str, count: int) -> set:
    batch_results = set()
    attempts = 0
    max_attempts = count * 5
    
    while len(batch_results) < count and attempts < max_attempts:
        s = generate_from_symbol_random(grammar, symbol)
        clean_s = " ".join(s.split())
        if clean_s:
            batch_results.add(clean_s)
        attempts += 1
        
    return batch_results

def generate_structure_focused(grammar: CFGrammar, limit=10000) -> set:
    generated = set()
    target_per_group = limit // 4
    
    if 'VerbPhrase' in grammar.rules:
        items = generate_batch(grammar, 'VerbPhrase', target_per_group)
        generated.update(items)
        
    if 'Predicate' in grammar.rules and 'Wh' in grammar.rules:
        for _ in range(target_per_group * 2):
            p = generate_from_symbol_random(grammar, 'Predicate', max_depth=5)
            w = generate_from_symbol_random(grammar, 'Wh', max_depth=2)
            if p and w:
                generated.add(f"{p} {w}")
            if len(generated) > target_per_group * 2: break

    if 'VerbPhrase' in grammar.rules and 'DeliveryTimePhrase' in grammar.rules:
        for _ in range(target_per_group * 2):
            v = generate_from_symbol_random(grammar, 'VerbPhrase', max_depth=6)
            d = generate_from_symbol_random(grammar, 'DeliveryTimePhrase', max_depth=5)
            if v and d:
                generated.add(f"{v} {d}")
            if len(generated) > target_per_group * 3: break
            
    return generated

def run_generation_task(limit=10000):
    print(f"--- [Task 2.2] Đang sinh {limit} câu mẫu... ---")
    
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    output_file = os.path.join(OUTPUT_DIR, 'samples.txt')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    final_sentences = set()

    focused_set = generate_structure_focused(grammar, limit=int(limit * 0.4))
    final_sentences.update(focused_set)
    print(f"   -> Đã sinh {len(final_sentences)} câu theo cấu trúc tập trung.")

    retries = 0
    max_retries = limit * 5
    
    while len(final_sentences) < limit and retries < max_retries:
        s = generate_from_symbol_random(grammar, grammar.start_symbol)
        clean_s = " ".join(s.split())
        
        if clean_s and clean_s not in final_sentences:
            final_sentences.add(clean_s)
            if retries > 100: retries = 0 
        else:
            retries += 1
            
    sorted_list = sorted(list(final_sentences))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in sorted_list:
            f.write(s + "\n")
            
    print(f"Hoàn tất! Đã lưu {len(sorted_list)} câu vào: {output_file}")