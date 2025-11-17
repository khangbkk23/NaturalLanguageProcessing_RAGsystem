# python/hcmut/iaslab/nlp/app/parser.py
import os
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
    print("--- [Task 2.3] Đang phân tích cú pháp... ---")
    
    grammar_file = os.path.join(DATA_DIR, 'grammar.txt')
    grammar = load_grammar_with_lexicons(grammar_file, LEXICON_CONFIG)
    
    # Khởi tạo parser
    parser = EarleyParser(grammar)
    
    input_file = os.path.join(INPUT_DIR, 'sentences.txt')
    output_file = os.path.join(OUTPUT_DIR, 'parse-results.txt')
    
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(input_file):
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("Tôi muốn đặt 2 phần phở bò\n")

    output_lines = []
    with open(input_file, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            sentence = line.strip()
            if not sentence: continue
            
            tokens = simple_tokenizer(sentence)
            parse_tree = parser.parse(tokens)
            
            output_lines.append(f"The sentence: {sentence}")
            output_lines.append("Parsed rule:")
            if parse_tree:
                output_lines.append(str(parse_tree))
            else:
                output_lines.append("()")
            output_lines.append("\n ====================================================================== \n")

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for line in output_lines:
            f_out.write(line + "\n")
            
    print(f"Đã lưu kết quả vào: {output_file}")