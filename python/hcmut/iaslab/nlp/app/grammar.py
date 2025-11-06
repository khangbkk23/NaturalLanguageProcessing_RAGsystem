#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from typing import Dict, List, Set


class CFGrammar:
    """Context-Free Grammar cho hệ thống đặt món"""
    
    def __init__(self, grammar_file: str = None):
        self.rules = defaultdict(list)  # non-terminal -> list of productions
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = 'Sentences'  # Đổi start symbol
        
        if grammar_file and os.path.exists(grammar_file):
            self.load_from_file(grammar_file)
        else:
            # Tìm file parser.txt trong thư mục rule
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'rule',
                'parser.txt'
            )
            if os.path.exists(default_path):
                self.load_from_file(default_path)
            else:
                print("[Warning] Không tìm thấy parser.txt, sử dụng grammar tối thiểu")
                self._load_minimal_grammar()
    
    def load_from_file(self, filename: str):
        """Đọc văn phạm từ file"""
        print(f"[Grammar] Đang đọc văn phạm từ {filename}...")
        
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Bỏ qua comment và dòng trống
                if not line or line.startswith('#'):
                    continue
                
                if '->' in line:
                    try:
                        self.add_rule(line)
                    except Exception as e:
                        print(f"[Warning] Lỗi dòng {line_num}: {e}")
        
        print(f"[Grammar] Đã load {len(self.rules)} non-terminals, "
              f"{len(self.terminals)} terminals")
    
    def add_rule(self, rule_str: str):
        """Thêm quy tắc vào văn phạm"""
        parts = rule_str.split('->')
        if len(parts) != 2:
            return
        
        lhs = parts[0].strip()
        rhs_options = parts[1].split('|')
        
        self.non_terminals.add(lhs)
        
        for rhs in rhs_options:
            rhs = rhs.strip()
            
            # Xử lý epsilon production
            if not rhs or rhs == 'ε':
                symbols = []
            else:
                symbols = rhs.split()
            
            self.rules[lhs].append(symbols)
            
            # Phân loại terminal và non-terminal
            for symbol in symbols:
                if not symbol:
                    continue
                
                # Non-terminal: bắt đầu bằng chữ HOA hoặc có gạch dưới
                if symbol[0].isupper() or '_' in symbol:
                    self.non_terminals.add(symbol)
                else:
                    # Terminal: từ tiếng Việt, số, ký tự đặc biệt
                    self.terminals.add(symbol)
    
    def _load_minimal_grammar(self):
        """Load grammar tối thiểu khi không có file"""
        minimal_rules = """
Sentences -> Sentence | Sentence Wh
Sentence -> Subject Predicate | Predicate
Subject -> Pronoun | Noun
Predicate -> Verb NounPhrase
Verb -> đặt | có | thêm | hủy | giao
Pronoun -> tôi | mình
Noun -> món | đơn
NounPhrase -> Quantifier Unit FoodName
Quantifier -> 1 | 2 | 3 | một | hai
Unit -> phần | ly | tô
FoodName -> phở bò | trà sữa | cà phê
Wh -> không
"""
        for line in minimal_rules.strip().split('\n'):
            if line and '->' in line:
                self.add_rule(line)
    
    def to_string(self) -> str:
        """Chuyển văn phạm thành string"""
        result = []
        result.append("# Văn phạm CFG cho hệ thống đặt món ăn online\n")
        result.append(f"# Start symbol: {self.start_symbol}\n")
        result.append(f"# Số non-terminals: {len(self.non_terminals)}\n")
        result.append(f"# Số terminals: {len(self.terminals)}\n\n")
        
        # Sắp xếp theo thứ tự: start symbol trước, sau đó alphabet
        sorted_keys = sorted(self.rules.keys(), 
                           key=lambda x: (x != self.start_symbol, x))
        
        for lhs in sorted_keys:
            productions = self.rules[lhs]
            for i, prod in enumerate(productions):
                if i == 0:
                    prod_str = ' '.join(prod) if prod else 'ε'
                    result.append(f"{lhs} -> {prod_str}\n")
                else:
                    prod_str = ' '.join(prod) if prod else 'ε'
                    result.append(f"{' ' * len(lhs)} | {prod_str}\n")
            result.append("\n")
        
        return ''.join(result)
    
    def save_to_file(self, filename: str):
        """Lưu văn phạm ra file"""
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_string())
        print(f"[Grammar] Đã lưu văn phạm vào {filename}")
    
    def get_stats(self) -> Dict:
        """Lấy thống kê về văn phạm"""
        return {
            'non_terminals': len(self.non_terminals),
            'terminals': len(self.terminals),
            'rules': sum(len(prods) for prods in self.rules.values()),
            'start_symbol': self.start_symbol
        }
    
    def is_terminal(self, symbol: str) -> bool:
        """Kiểm tra symbol có phải terminal không"""
        return symbol in self.terminals or (
            symbol and symbol[0].islower() and symbol not in self.non_terminals
        )
    
    def is_non_terminal(self, symbol: str) -> bool:
        """Kiểm tra symbol có phải non-terminal không"""
        return symbol in self.non_terminals