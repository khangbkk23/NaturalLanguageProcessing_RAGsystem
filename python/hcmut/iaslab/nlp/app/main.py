# python/hcmut/iaslab/nlp/app/main.py
import os
from .grammar import CFGrammar
from .earley_parser import EarleyParser

APP_DIR = os.path.dirname(os.path.abspath(__file__))
NLP_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(NLP_DIR, 'data')
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(NLP_DIR)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# Cấu hình các file "token mở"
LEXICON_CONFIG = {
    '_MON_AN_': os.path.join(DATA_DIR, 'dishes.txt'),
    '_DON_VI_': os.path.join(DATA_DIR, 'units.txt'),
    '_TUY_CHON_MON_': os.path.join(DATA_DIR, 'food_options.txt'),
    '_TEN_QUAN_': os.path.join(DATA_DIR, 'restaurants.txt')
}

def load_grammar_with_lexicons(grammar_file: str, 
                               lexicon_config: dict) -> CFGrammar:
    """
    Nạp văn phạm cấu trúc VÀ "tiêm" các quy tắc từ vựng.
    Đây chính là code "cầu nối".
    """
    print("--- Bắt đầu nạp văn phạm ---")
    grammar = CFGrammar(grammar_file)
    
    # Bắt đầu "tiêm"
    for non_terminal, lexicon_file in lexicon_config.items():
        print(f"[Loader] Nạp từ vựng cho '{non_terminal}' từ {lexicon_file}...")
        try:
            with open(lexicon_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    item = line.strip()
                    if item:
                        # Tạo quy tắc: _MON_AN_ -> phở bò
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
    """
    Tokenizer đơn giản (sẽ cần cải thiện sau).
    Tách câu thành các từ.
    """
    return sentence.lower().split()

def run_parser_task():
    """
    Hàm chính thực thi Task 2.3
    """
    # 1. Nạp văn phạm
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    # 2. Khởi tạo Parser
    parser = EarleyParser(grammar)
    
    # 3. Chuẩn bị file input/output (Theo yêu cầu đề bài)
    input_file = os.path.join(PROJECT_ROOT, 'input', 'sentences.txt')
    output_file = os.path.join(OUTPUT_DIR, 'parse-results.txt')
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Tạo file input mẫu nếu chưa có
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
            
    print("\n--- Hoàn tất Phần I ---")

if __name__ == "__main__":
    run_parser_task()