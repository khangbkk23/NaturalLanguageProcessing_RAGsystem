# python/hcmut/iaslab/nlp/app/earley_parser.py
from collections import namedtuple
from .grammar import CFGrammar
State = namedtuple('State', ['rule', 'dot_pos', 'start_pos', 'back_pointers'])

class ParseTree:
    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children

    def __repr__(self):
        if not self.children:
            return f"'{self.symbol}'"
        return f"({self.symbol} {' '.join(map(str, self.children))})"

class EarleyParser:
    def __init__(self, grammar: CFGrammar):
        self.grammar = grammar
        self.chart = []

    def parse(self, tokens: list):
        self.chart = [[] for _ in range(len(tokens) + 1)]
        self.tokens = tokens
        
        start_symbol = self.grammar.start_symbol
        for prod in self.grammar.rules[start_symbol]:
            self._add_to_chart(State(rule=(start_symbol, prod), 
                                     dot_pos=0, 
                                     start_pos=0,
                                     back_pointers=[]), 0)
        
        for k in range(len(tokens) + 1):
            i = 0
            while i < len(self.chart[k]):
                state = self.chart[k][i]
                i += 1
                
                if not self.is_state_complete(state):
                    symbol_after_dot = self.get_next_symbol(state)
                    
                    if self.grammar.is_non_terminal(symbol_after_dot):
                        # 1. PREDICTOR
                        self._predictor(symbol_after_dot, k)
                    
                    elif k < len(tokens) and tokens[k] == symbol_after_dot:
                        # 2. SCANNER
                        self._scanner(state, k)
                else:
                    # 3. COMPLETER
                    self._completer(state, k)

        return self.build_parse_tree(start_symbol, len(tokens))

    def _add_to_chart(self, state: State, k: int):
        if state not in self.chart[k]:
            self.chart[k].append(state)

    def is_state_complete(self, state: State):
        return state.dot_pos == len(state.rule[1])

    def get_next_symbol(self, state: State):
        if not self.is_state_complete(state):
            return state.rule[1][state.dot_pos]
        return None

    def _predictor(self, non_terminal: str, k: int):
        for prod in self.grammar.rules[non_terminal]:
            self._add_to_chart(State(rule=(non_terminal, prod), 
                                     dot_pos=0, 
                                     start_pos=k,
                                     back_pointers=[]), k)

    def _scanner(self, state: State, k: int):
        new_back_pointers = state.back_pointers + [ParseTree(self.tokens[k], [])]
        
        new_state = State(rule=state.rule, 
                          dot_pos=state.dot_pos + 1, 
                          start_pos=state.start_pos,
                          back_pointers=new_back_pointers)
        self._add_to_chart(new_state, k + 1)

    def _completer(self, completed_state: State, k: int):
        start_pos = completed_state.start_pos
        completed_non_terminal = completed_state.rule[0]
        
        completed_tree_node = ParseTree(completed_non_terminal, 
                                        completed_state.back_pointers)
        
        for state in self.chart[start_pos]:
            next_sym = self.get_next_symbol(state)
            if next_sym == completed_non_terminal:
                new_back_pointers = state.back_pointers + [completed_tree_node]
                
                new_state = State(rule=state.rule,
                                  dot_pos=state.dot_pos + 1,
                                  start_pos=state.start_pos,
                                  back_pointers=new_back_pointers)
                self._add_to_chart(new_state, k)

    def build_parse_tree(self, start_symbol: str, end_pos: int):
        for state in self.chart[end_pos]:
            if (state.rule[0] == start_symbol and 
                state.start_pos == 0 and 
                self.is_state_complete(state)):
                return ParseTree(start_symbol, state.back_pointers)
        
        return None