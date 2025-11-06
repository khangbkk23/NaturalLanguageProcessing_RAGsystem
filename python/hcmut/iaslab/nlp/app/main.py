# python/hcmut/iaslab/nlp/app/main.py
import os
from .grammar import CFGrammar
from .earley_parser import EarleyParser

APP_DIR = os.path.dirname(os.path.abspath(__file__))
NLP_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(NLP_DIR, 'data')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(NLP_DIR)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

LEXICON_CONFIG = {
    '_MON_AN_': os.path.join(DATA_DIR, 'dishes.txt'),
    '_DON_VI_': os.path.join(DATA_DIR, 'units.txt'),
    '_TUY_CHON_MON_': os.path.join(DATA_DIR, 'food_options.txt'),
    '_TEN_QUAN_': os.path.join(DATA_DIR, 'restaurants.txt')
}

def load_grammar_with_lexicons(grammar_file: str, 
                               lexicon_config: dict) -> CFGrammar:
    grammar = CFGrammar(grammar_file)
    print("--- Bắt đầu nạp văn phạm ---")
    for non_terminal, lexicon_file in lexicon_config.items():
        print(f"[Loader] Nạp từ vựng cho '{non_terminal}' từ {lexicon_file}...")
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    item = line.strip()
                    if item:
                        rule_str = f"{non_terminal} -> {item}"
                        grammar.add_rule(rule_str)
                        count += 1
                print(f"  -> Đã thêm {count} quy tắc cho {non_terminal}")
        except FileNotFoundError:
            print(f"[LỖI] Không tìm thấy file {lexicon_file}")
        except Exception as e:
            print(f"[LỖI] Không thể đọc file {lexicon_file}: {e}")
            
    print(grammar.get_stats())
    print("--- Nạp văn phạm hoàn tất ---")
    return grammar

def simple_tokenizer(sentence: str) -> list:
    return sentence.lower().split()

def run_parser_task():
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    parser = EarleyParser(grammar)
    
    input_file = os.path.join(PROJECT_ROOT, 'input', 'sentences.txt')
    output_file = os.path.join(OUTPUT_DIR, 'parse-results.txt')
    
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    if not os.path.exists(input_file):
        print(f"Tạo file input mẫu: {input_file}")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("tôi muốn đặt 2 phần phở bò\n")
            f.write("có bún chả không\n")
            f.write("câu này sai ngữ pháp\n")

    print(f"\n--- Bắt đầu phân tích (Task 2.3) ---")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    
    results = []
    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            sentence = line.strip()
            if not sentence:
                continue
            
            tokens = simple_tokenizer(sentence)
            print(f"\nPhân tích câu: '{sentence}'")
            print(f"Tokens: {tokens}")
            
            # Chạy parser
            parse_tree = parser.parse(tokens)
            
            if parse_tree:
                tree_str = str(parse_tree)
                print(f"Kết quả: {tree_str}")
                results.append(tree_str)
            else:
                print("Kết quả: ()")
                results.append("()")

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for res in results:
            f_out.write(res + "\n")

if __name__ == "__main__":
    run_parser_task()