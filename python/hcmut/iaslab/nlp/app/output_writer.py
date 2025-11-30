# python/hcmut/iaslab/nlp/app/output_writer.py
import os
from datetime import datetime

class OutputWriter:
    def __init__(self, output_dir='output'):
        self.output_dir = os.path.abspath(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.qhnn_file = os.path.join(self.output_dir, 'qhnn.txt')
        self.qhvp_file = os.path.join(self.output_dir, 'qhvp.txt')
        self.ll_file = os.path.join(self.output_dir, 'll.txt')
        self.answer_file = os.path.join(self.output_dir, 'answer.txt')
        self._init_files()
    
    def _init_files(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = f"{'='*60}\n"
        header += f"HỆ THỐNG ĐẶT MÓN ĂN - KELVINCOOK\n"
        header += f"Thời gian: {timestamp}\n"
        
        with open(self.qhnn_file, 'w', encoding='utf-8') as f:
            f.write(header + "Quan hệ ngữ nghĩa\n" + "="*60 + "\n\n")
        
        with open(self.qhvp_file, 'w', encoding='utf-8') as f:
            f.write(header + "Quan hệ văn phạm\n" + "="*60 + "\n\n")
        
        with open(self.ll_file, 'w', encoding='utf-8') as f:
            f.write(header + "Dạng luận lý và ngữ nghĩa thủ tục\n" + "="*60 + "\n\n")
        
        with open(self.answer_file, 'w', encoding='utf-8') as f:
            f.write(header + "Câu trả lời\n" + "="*60 + "\n\n")
    
    def write_query(self, query_num, user_input, tokens, dependencies, relations, logical_form, procedure, answer):
        
        # 1. QHNN.txt - Quan hệ ngữ nghĩa
        with open(self.qhnn_file, 'a', encoding='utf-8') as f:
            f.write(f"Câu {query_num}: {user_input}\n")
            f.write(f"Tokens: {tokens}\n")
            f.write(f"Relations:\n")
            for rel in relations:
                f.write(f"  - {rel}\n")
            f.write("\n" + "-"*60 + "\n\n")
        
        # 2. QHVP.txt - Quan hệ văn phạm
        with open(self.qhvp_file, 'a', encoding='utf-8') as f:
            f.write(f"Câu {query_num}: {user_input}\n")
            f.write(f"Dependencies:\n")
            for dep in dependencies:
                f.write(f"  - {dep}\n")
            f.write("\n" + "-"*60 + "\n\n")
        
        # 3. ll.txt - Dạng luận lý và ngữ nghĩa thủ tục
        with open(self.ll_file, 'a', encoding='utf-8') as f:
            f.write(f"Câu {query_num}: {user_input}\n")
            f.write(f"Logical Form: {logical_form}\n")
            f.write(f"Procedure: {procedure}\n")
            f.write("\n" + "-"*60 + "\n\n")
        
        # 4. Answer.txt - Câu trả lời
        with open(self.answer_file, 'a', encoding='utf-8') as f:
            f.write(f"Câu {query_num}: {user_input}\n")
            f.write(f"Trả lời: {answer}\n")
            f.write("\n" + "-"*60 + "\n\n")
    
    def get_summary(self):
        """Trả về thông tin tổng kết"""
        return f"""
Đã xuất output thành công!
Thư mục: {self.output_dir}
"""