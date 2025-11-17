# python/hcmut/iaslab/nlp/app/utils.py
import os, re
from .grammar import CFGrammar

APP_DIR = os.path.dirname(os.path.abspath(__file__))

NLP_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(NLP_DIR, 'data')


_iaslab_dir = os.path.dirname(NLP_DIR)
_hcmut_dir = os.path.dirname(_iaslab_dir)
PYTHON_DIR = os.path.dirname(_hcmut_dir)

ROOT_DIR = os.path.dirname(PYTHON_DIR)

SV_DIR = os.path.join(ROOT_DIR, "2311402")
OUTPUT_DIR = os.path.join(SV_DIR, 'output')
INPUT_DIR = os.path.join(ROOT_DIR, 'input')

LEXICON_CONFIG = {
    # Nhóm Đồ ăn
    '_DO_AN_': os.path.join(DATA_DIR, 'food_names.txt'),
    '_TUY_CHON_DO_AN_': os.path.join(DATA_DIR, 'food_opts.txt'),
    
    # Nhóm Đồ uống
    '_DO_UONG_': os.path.join(DATA_DIR, 'drink_names.txt'),
    '_TUY_CHON_DO_UONG_': os.path.join(DATA_DIR, 'drink_opts.txt'),
    
    # Nhóm Chung
    '_TUY_CHON_CHUNG_': os.path.join(DATA_DIR, 'common_opts.txt'),
    
    # Các từ khác giữ nguyên
    '_DON_VI_': os.path.join(DATA_DIR, 'units.txt'),
    '_TEN_QUAN_': os.path.join(DATA_DIR, 'restaurants.txt')
}
def simple_tokenizer(sentence: str) -> list:
    return re.findall(r'\w+', sentence.lower())
def load_grammar_with_lexicons(grammar_file: str, 
                               lexicon_config: dict) -> CFGrammar:

    grammar = CFGrammar(grammar_file)
    for non_terminal, lexicon_file in lexicon_config.items():
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    item = line.strip().lower() 
                    if item:
                        tokens = simple_tokenizer(item)
                        rhs = " ".join(tokens)
                        rule_str = f"{non_terminal} -> {rhs}"
                        grammar.add_rule(rule_str)
                        count += 1
                # print(f" -> Đã thêm {count} quy tắc cho {non_terminal}")
        except FileNotFoundError:
            print(f"  [LỖI] Không tìm thấy file {lexicon_file}")
        except Exception as e:
            print(f"  [LỖI] Không thể đọc file {lexicon_file}: {e}")
            
    print(grammar.get_stats())
    print("--- Nạp văn phạm hoàn tất ---")
    return grammar