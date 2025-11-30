# python/hcmut/iaslab/nlp/app/dependency_parser.py
"""
Output: qhnn.txt
"""

import os
import re

class DependencyParser:

    def __init__(self):
        self.relations = {
            'PRED': 'Predicate',
            'LSUBJ': 'Logical Subject',
            'LOBJ': 'Logical Object',
            'MOD': 'Modifier',
            'TIME': 'Time Expression'
        }
        self.event_counter = 0
    
    def parse_to_dependencies(self, parse_tree_str):
        """
        Parse tree string → Dependencies list
        
        Input: "(Sentence (Subject tôi) (Predicate (Verb đặt) ...))"
        Output: [('e1', 'PRED', 'đặt'), ('e1', 'LSUBJ', 'tôi'), ...]
        """
        if not parse_tree_str or parse_tree_str == "()":
            return []
        
        self.event_counter = 0
        dependencies = []
        
        components = self._extract_from_string(parse_tree_str)
        
        if components:
            event_id = f"e{self._next_event_id()}"
            
            # PRED
            if 'verb' in components:
                dependencies.append((event_id, 'PRED', components['verb']))
            
            # LSUBJ
            if 'subject' in components:
                dependencies.append((event_id, 'LSUBJ', components['subject']))
            
            # LOBJ
            if 'object' in components:
                dependencies.append((event_id, 'LOBJ', components['object']))
            
            # TIME
            if 'time' in components:
                dependencies.append((event_id, 'TIME', components['time']))
            
            # MOD
            if 'modifiers' in components:
                for mod in components['modifiers']:
                    dependencies.append((event_id, 'MOD', mod))
        
        return dependencies
    
    def _next_event_id(self):
        """Generate event ID"""
        self.event_counter += 1
        return self.event_counter
    
    def _extract_from_string(self, tree_str):
        """Extract semantic components from parse tree string"""
        components = {}
        tree_str = tree_str.lower()
        
        # Extract verb (modal + main verb)
        verbs = self._find_verbs(tree_str)
        if verbs:
            components['verb'] = ' '.join(verbs) if len(verbs) > 1 else verbs[0]
        
        # Extract subject
        subjects = self._find_pattern(tree_str, ['tôi', 'mình', 'em', 'anh', 'chị'])
        if subjects:
            components['subject'] = subjects[0]
        
        # Extract object (noun phrase)
        obj = self._extract_object(tree_str)
        if obj:
            components['object'] = obj
        
        # Extract time
        time = self._extract_time(tree_str)
        if time:
            components['time'] = time
        
        # Extract modifiers
        mods = self._extract_modifiers(tree_str)
        if mods:
            components['modifiers'] = mods
        
        return components
    
    def _find_verbs(self, text):
        """Extract verbs (modal + main)"""
        verbs = []
        
        # Modal verbs
        modals = ['muốn', 'cần', 'phải', 'nên', 'có thể']
        for modal in modals:
            if modal in text:
                verbs.append(modal)
        
        # Main verbs
        main_verbs = ['đặt', 'có', 'xem', 'thêm', 'hủy', 'sửa', 'đổi', 'kiểm tra', 'hỏi', 'giao']
        for verb in main_verbs:
            if verb in text and verb not in verbs:
                verbs.append(verb)
        
        return verbs
    
    def _find_pattern(self, text, patterns):
        """Find patterns in text"""
        found = []
        for pattern in patterns:
            if pattern in text:
                found.append(pattern)
        return found
    
    def _extract_object(self, text):
        """Extract object (food/drink + quantity)"""
        patterns = [
            r'(\d+)\s+(\w+)\s+([\w\s]+)',
            r'(món)\s+([\w\s]+)',
            r'([\w\s]{4,})',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    obj = ' '.join([str(x) for x in matches[0] if x]).strip()
                else:
                    obj = matches[0].strip()
                
                # Filter out common words
                if obj and len(obj) > 2:
                    exclude = ['trong', 'menu', 'đơn', 'hàng', 'những', 'nào']
                    if not any(word in obj for word in exclude):
                        return obj
        
        return None
    
    def _extract_time(self, text):
        time_patterns = [
            r'(lúc\s+\d+\s+giờ(?:\s+\d+\s+phút)?)',
            r'(\d+\s+giờ(?:\s+\d+\s+phút)?)',
            r'(hôm nay|hôm qua|ngày mai|bây giờ)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_modifiers(self, text):
        modifiers = []
        
        mod_list = [
            'đặc biệt', 'ít đường', 'ít đá', 'nhiều đá', 
            'nóng', 'lạnh', 'cay', 'không cay',
            'trong menu', 'tại chỗ', 'mang đi'
        ]
        
        for mod in mod_list:
            if mod in text:
                modifiers.append(mod)
        
        return modifiers
    
    def format_output(self, all_results, filename=None):
        if filename is None:
            from .utils import OUTPUT_DIR
            filename = os.path.join(OUTPUT_DIR, 'qhnn.txt')
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Quan hệ ngữ nghĩa\n")
            f.write("# Format: (event_id, relation, value)\n\n")
            
            for i, (sentence, dependencies) in enumerate(all_results, 1):
                f.write(f"## Câu {i}: {sentence}\n")
                
                if dependencies:
                    for head, relation, dependent in dependencies:
                        f.write(f"({head}, {relation}, {dependent})\n")
                else:
                    f.write("(Không phân tích được)\n")
                
                f.write("\n")
        
        print(f"[Bước 1] Đã xuất quan hệ ngữ nghĩa ra {filename}")
        return filename