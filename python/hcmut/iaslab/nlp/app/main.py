# python/hcmut/iaslab/nlp/app/main.py
import os
import sys
from .earley_parser import EarleyParser
from .utils import (
    load_grammar_with_lexicons, 
    simple_tokenizer, 
    LEXICON_CONFIG, 
    DATA_DIR, 
    OUTPUT_DIR,
    INPUT_DIR
)

def run_parser_task():
    # 1. Nạp văn phạm
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    # 2. Khởi tạo Parser
    parser = EarleyParser(grammar)
    
    # 3. Chuẩn bị file input/output
    input_file = os.path.join(INPUT_DIR, 'sentences.txt')
    output_file = os.path.join(OUTPUT_DIR, 'parse-results.txt')
    
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(input_file):
        print(f"Tạo file input mẫu: {input_file}")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("tôi muốn đặt 2 phần phở bò\n")
            f.write("có bún chả không\n")
            f.write("giao lúc 7 giờ 30 phút\n")
            f.write("xem menu của KelvinCook\n")

    print(f"\n--- Bắt đầu phân tích---")
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

    # 4. Ghi kết quả
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for res in results:
            f_out.write(res + "\n")


if __name__ == "__main__":
    run_parser_task()