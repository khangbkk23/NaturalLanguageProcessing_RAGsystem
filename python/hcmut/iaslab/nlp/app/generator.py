import os
import random
import sys
from itertools import product
from .grammar import CFGrammar
from .utils import load_grammar_with_lexicons, LEXICON_CONFIG, DATA_DIR, OUTPUT_DIR

def generate_from_symbol_random(grammar: CFGrammar, symbol: str) -> str:
    MAX_DEPTH = 20
    
    def _generate_recursive(sym, depth):
        if depth > MAX_DEPTH: return ""
        if not grammar.is_non_terminal(sym): return sym

        if sym not in grammar.rules or not grammar.rules[sym]: return ""

        production = random.choice(grammar.rules[sym])
        if not production: return ""

        parts = []
        for s in production:
            parts.append(_generate_recursive(s, depth + 1))
        
        return " ".join(filter(None, parts))
        
    return _generate_recursive(symbol, 0)

def get_all_terminals(grammar: CFGrammar, symbol: str, max_depth=6) -> list:
    if max_depth <= 0: return []
    
    if not grammar.is_non_terminal(symbol):
        return [symbol]

    if symbol not in grammar.rules or not grammar.rules[symbol]:
        return []

    all_results = []
    
    for production in grammar.rules[symbol]:
        if not production: continue
        
        parts_options = []
        for sym in production:
            variants = get_all_terminals(grammar, sym, max_depth - 1)
            if not variants: variants = [""]
            parts_options.append(variants)
        
        for combination in product(*parts_options):
            result = " ".join(filter(None, combination))
            if result:
                all_results.append(result)
    
    return all_results

def generate_focused(grammar: CFGrammar, limit=10000) -> set:
    generated = set()
    target_per_structure = limit // 4
    
    if 'VerbPhrase' in grammar.rules:
        verbs = get_all_terminals(grammar, 'VerbPhrase', max_depth=6)
        random.shuffle(verbs)
        for v in verbs[:target_per_structure]:
            generated.add(v)
        
    if 'Predicate' in grammar.rules and 'Wh' in grammar.rules:
        predicates = get_all_terminals(grammar, 'Predicate', max_depth=5)
        wh_words = get_all_terminals(grammar, 'Wh', max_depth=2)
        
        count = 0
        for p in predicates:
            for w in wh_words:
                if count >= target_per_structure: break
                generated.add(f"{p} {w}")
                count += 1
    
    if 'VerbPhrase' in grammar.rules and 'DeliveryTimePhrase' in grammar.rules:
        verbs = get_all_terminals(grammar, 'VerbPhrase', max_depth=6)
        deliveries = get_all_terminals(grammar, 'DeliveryTimePhrase', max_depth=5)
        random.shuffle(verbs)
        
        count = 0
        for v in verbs[:200]:
            for d in deliveries:
                if count >= target_per_structure: break
                generated.add(f"{v} {d}")
                count += 1
            
    return generated

def run_generation_task(limit=10000):
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    output_file = os.path.join(OUTPUT_DIR, 'samples.txt')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    final_sentences = set()

    focused_set = generate_focused(grammar, limit=limit//2)
    final_sentences.update(focused_set)
        
    retries = 0
    while len(final_sentences) < limit and retries < limit * 10:
        s = generate_from_symbol_random(grammar, grammar.start_symbol)
        clean_s = " ".join(s.split())
        if clean_s and clean_s not in final_sentences:
            final_sentences.add(clean_s)
        retries += 1

    sorted_list = sorted(list(final_sentences))
    with open(output_file, 'w', encoding='utf-8') as f:
        for s in sorted_list:
            f.write(s + "\n")
            
    print(f"-> Generated {len(sorted_list)} sentences to {output_file}")