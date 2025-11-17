# python/hcmut/iaslab/nlp/app/grammar.py
import os
from collections import defaultdict
from typing import Dict, List, Set


class CFGrammar:
    def __init__(self, grammar_file: str = None):
        self.rules = defaultdict(list)
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = 'Sentences'
        
        if grammar_file and os.path.exists(grammar_file):
            self.load_from_file(grammar_file)
        else:
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data',
                'grammar.txt'
            )
            if os.path.exists(default_path):
                self.load_from_file(default_path)
            else:
                print("[Warning] Không tìm thấy grammar.txt, sử dụng grammar tối thiểu")
                self._load_minimal_grammar()
    
    def load_from_file(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # Handle comment in grammar file
                line = line.split('#')[0].strip()
                if not line:
                    continue
                
                if '->' in line:
                    try:
                        self.add_rule(line)
                    except Exception as e:
                        print(f"[Warning] Lỗi ở dòng {line_num}: {e}")
    
    def add_rule(self, rule_str: str):
        parts = rule_str.split('->')
        if len(parts) != 2:
            return
        
        lhs = parts[0].strip()
        rhs_options = parts[1].split('|')
        
        self.non_terminals.add(lhs)
        
        for rhs in rhs_options:
            rhs = rhs.strip()
            
            if not rhs or rhs == 'ε':
                symbols = []
            else:
                symbols = rhs.split()
            
            self.rules[lhs].append(symbols)
            for symbol in symbols:
                if not symbol:
                    continue
                if symbol[0].isupper() or '_' in symbol:
                    self.non_terminals.add(symbol)
                else:
                    self.terminals.add(symbol)
    
    def _load_minimal_grammar(self):
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
        result = []
        result.append("# Văn phạm CFG cho hệ thống đặt món ăn online\n")
        result.append(f"# Start symbol: {self.start_symbol}\n")
        result.append(f"# Số non-terminals: {len(self.non_terminals)}\n")
        result.append(f"# Số terminals: {len(self.terminals)}\n\n")
        
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
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_string())
        print(f"[Grammar] Đã lưu văn phạm vào {filename}")
    
    def get_stats(self) -> Dict:
        return {
            'non_terminals': len(self.non_terminals),
            'terminals': len(self.terminals),
            'rules': sum(len(prods) for prods in self.rules.values()),
            'start_symbol': self.start_symbol
        }
    
    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.terminals or (
            symbol and symbol[0].islower() and symbol not in self.non_terminals
        )
    
    def is_non_terminal(self, symbol: str) -> bool:
        return symbol in self.non_terminals