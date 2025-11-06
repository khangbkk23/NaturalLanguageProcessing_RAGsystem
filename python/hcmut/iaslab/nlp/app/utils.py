# python/hcmut/iaslab/nlp/app/utils.py
import os, re
from .grammar import CFGrammar

APP_DIR = os.path.dirname(os.path.abspath(__file__))
NLP_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(NLP_DIR, 'data')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(NLP_DIR)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output') # Đã di chuyển từ main.py
INPUT_DIR = os.path.join(PROJECT_ROOT, 'input')  # Thêm thư mục input

LEXICON_CONFIG = {
    '_MON_AN_': os.path.join(DATA_DIR, 'dishes.txt'),
    '_DON_VI_': os.path.join(DATA_DIR, 'units.txt'),
    '_TUY_CHON_MON_': os.path.join(DATA_DIR, 'food_options.txt'),
    '_TEN_QUAN_': os.path.join(DATA_DIR, 'restaurants.txt')
}

def load_grammar_with_lexicons(grammar_file: str, 
                               lexicon_config: dict) -> CFGrammar:

    print("--- Bắt đầu nạp văn phạm ---")
    grammar = CFGrammar(grammar_file)
    for non_terminal, lexicon_file in lexicon_config.items():
        print(f"[Loader] Nạp từ vựng cho '{non_terminal}' từ {lexicon_file}...")
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    item = line.strip().lower() 
                    if item:
                        rule_str = f"{non_terminal} -> {item}"
                        grammar.add_rule(rule_str)
                        count += 1
                print(f"  -> Đã thêm {count} quy tắc cho {non_terminal}")
        except FileNotFoundError:
            print(f"  [LỖI] Không tìm thấy file {lexicon_file}")
        except Exception as e:
            print(f"  [LỖI] Không thể đọc file {lexicon_file}: {e}")
            
    print("\n[Grammar Stats] Thống kê sau khi nạp từ vựng:")
    print(grammar.get_stats())
    print("--- Nạp văn phạm hoàn tất ---")
    return grammar

def simple_tokenizer(sentence: str) -> list:
    return re.findall(r'\w+|\S', sentence.lower())