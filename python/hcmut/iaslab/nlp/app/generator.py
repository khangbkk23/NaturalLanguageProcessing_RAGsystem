# python/hcmut/iaslab/nlp/app/generator.py
import os
import random
import sys
from .grammar import CFGrammar
from .utils import load_grammar_with_lexicons, LEXICON_CONFIG, DATA_DIR, OUTPUT_DIR
def generate_from_symbol(grammar: CFGrammar, symbol: str) -> str:
    MAX_DEPTH = 20
    
    def _generate_recursive(sym, depth):
        if depth > MAX_DEPTH:
            return ""
            
        if not grammar.is_non_terminal(sym):
            return sym

        if sym not in grammar.rules or not grammar.rules[sym]:
            return "" 

        production = random.choice(grammar.rules[sym])

        if not production:
            return ""

        parts = []
        for s in production:
            parts.append(_generate_recursive(s, depth + 1))
        
        return " ".join(filter(None, parts))
    return _generate_recursive(symbol, 0)


def run_generation_task(limit=10000):

    print("--- Sinh câu ngẫu nhiên ---")
    
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    output_file = os.path.join(OUTPUT_DIR, 'samples.txt')
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    generated_sentences = set()
    start_symbol = grammar.start_symbol
    
    print(f"Đang sinh câu... (tối đa {limit})")
    try:
        for _ in range(limit * 5):
            if len(generated_sentences) >= limit:
                break
                
            sentence = generate_from_symbol(grammar, start_symbol)
            cleaned_sentence = " ".join(sentence.split())
            
            if cleaned_sentence:
                generated_sentences.add(cleaned_sentence)

    except KeyboardInterrupt:
        print("\nĐã dừng sinh câu.")
        
    # 4. Ghi kết quả
    print(f"Đã sinh tổng cộng {len(generated_sentences)} câu.")
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for s in generated_sentences:
            f_out.write(s + "\n")
            
    print(f"Đã lưu kết quả vào: {output_file}")