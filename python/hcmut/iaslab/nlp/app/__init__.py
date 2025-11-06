#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hệ thống xử lý đặt món ăn online - NLP Assignment
Phần I: Văn phạm, Sinh câu, và Parser

MSSV: 2311402
Họ và tên: Bùi Trần Duy Khang
Cách chạy: python __init__.py
"""

import os
import sys


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp.app import CFGrammar, SentenceGenerator, Parser


def setup():
    """Tạo các thư mục và file cần thiết"""
    # Tạo thư mục
    for dir_name in ['input', 'output']:
        os.makedirs(dir_name, exist_ok=True)
    
    input_file = 'input/sentences.txt'
    if not os.path.exists(input_file):
        print(f"[Setup] Tạo file input mẫu: {input_file}")
        samples = [
            "tôi muốn đặt 2 phần phở bò",
            "có món trà sữa không",
            "thêm 1 ly cà phê vào đơn nhé",
            "tôi muốn hủy món gà rán",
            "phở bò đắt không",
            "bây giờ tôi muốn đặt 3 tô bún chả",
            "anh đã đặt món rồi",
            "mình thích cơm gà lắm",
            "xem menu nhé",
            "câu này không hợp lệ xyz abc"
        ]
        with open(input_file, 'w', encoding='utf-8') as f:
            for s in samples:
                f.write(s + '\n')


def main():
    
    # Setup
    setup()
    
    # =========================================================================
    # BƯỚC 2.1: VIẾT VĂN PHẠM
    # =========================================================================
    print("[BƯỚC 2.1] VIẾT VĂN PHẠM")
    print("-" * 70)
    
    grammar_file = os.path.join('nlp', 'rule', 'parser.txt')
    grammar = CFGrammar(grammar_file)
    
    stats = grammar.get_stats()
    print(f"✓ Đã load: {stats['non_terminals']} non-terminals, "
          f"{stats['terminals']} terminals, {stats['rules']} rules")
    
    grammar.save_to_file('output/grammar.txt')
    print()
    
    # =========================================================================
    # BƯỚC 2.2: SINH CÂU
    # =========================================================================
    print("[BƯỚC 2.2] SINH CÂU")
    print("-" * 70)
    
    generator = SentenceGenerator(grammar)
    
    # Sinh 500 câu (có thể tăng lên 10000)
    n = 500
    print(f"Đang sinh {n} câu...")
    sentences = generator.generate_multiple(n, verbose=False)
    
    generator.save_to_file(sentences, 'output/samples.txt')
    print(f"✓ Đã sinh {len(sentences)} câu")
    
    # Hiển thị mẫu
    print("\nMột số câu ví dụ:")
    for i, s in enumerate(sentences[:8], 1):
        print(f"  {i}. {s}")
    print()
    
    # =========================================================================
    # BƯỚC 2.3: PARSE CÂU
    # =========================================================================
    print("[BƯỚC 2.3] PARSE CÂU")
    print("-" * 70)
    
    parser = Parser(grammar)
    total, valid = parser.parse_file('input/sentences.txt', 
                                     'output/parse-results.txt')
    print()
    
    # =========================================================================
    # TỔNG KẾT
    # =========================================================================
    print("=" * 70)
    print("✅ HOÀN THÀNH!")
    print("=" * 70)
    print(f"\n📊 Kết quả:")
    print(f"  • Văn phạm: {stats['non_terminals']} non-terminals")
    print(f"  • Sinh câu: {len(sentences)} câu")
    print(f"  • Parse: {valid}/{total} câu hợp lệ")
    print(f"\n📁 File output:")
    print(f"  • output/grammar.txt")
    print(f"  • output/samples.txt")
    print(f"  • output/parse-results.txt")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Đã dừng.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
