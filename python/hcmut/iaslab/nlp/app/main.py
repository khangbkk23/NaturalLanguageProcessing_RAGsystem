# python/hcmut/iaslab/nlp/app/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import models.data as dt
from models.maltparser import malt_parse
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.database import RestaurantDatabase
from models.answer_generator import AnswerGenerator
from output_writer import OutputWriter

def process_pipeline(user_input, query_id, generator, writer):
    print(f"\n[{query_id}] Khách: {user_input}")
    print("-" * 60)
    
    # 1. Tokenization
    tokens = dt.tokenize(user_input)
    print(f" - 1. Tokens:       {tokens}")
    
    # 2. Parse
    dependencies = malt_parse(user_input)
    dep_str = [str(d) for d in dependencies]
    print(f" - 2. Dependencies: {dep_str}")
    
    # 3. Relationalize
    relations = relationalize(dependencies)
    rel_str = [str(r) for r in relations]
    print(f" - 3. Relations:    {rel_str}")
    
    # 4. Logicalize
    logical_form = logicalize(relations)
    print(f" - 4. Logical Form: {logical_form}")
    
    # 5. Proceduralize
    procedure = proceduralize(logical_form)
    print(f" - 5. Procedure:    \033[92m{procedure}\033[0m")
    
    # 6. Execute
    print("-" * 60)
    answer = generator.execute_and_answer(procedure)
    print(f"KelvinCook Take Order: {answer}")
    print("=" * 60)

    writer.write_query(
        query_num=query_id,
        user_input=user_input,
        tokens=tokens,
        dependencies=dependencies,
        relations=relations,
        logical_form=logical_form,
        procedure=procedure,
        answer=answer
    )

default_queries = [
    "Có những món gì trong menu ?",
    "Phở bò giá bao nhiêu ?",
    "Có món gà rán không ?",
    "Thêm 2 trà sữa vào đơn .",
    "Tôi đã đặt những món gì ?"
]

def main():
    db = RestaurantDatabase()
    generator = AnswerGenerator(db)
    writer = OutputWriter()
    
    print("\nHỆ THỐNG ĐẶT MÓN ĂN ONLINE CỦA NHÀ HÀNG KELVINCOOK")
    print(f"Database loaded: {len(db.get_all_items())} items.")
    
    print("\nCHỌN CHẾ ĐỘ CHẠY:")
    print("  [1] Interactive Mode")
    print("  [2] Batch Mode")
    
    choice = input(">> Nhập lựa chọn (1/2): ").strip()

    # CHẾ ĐỘ 2: BATCH MODE
    if choice == '2':
        cwd = os.getcwd()
        input_path = os.path.join(cwd, 'input', 'sentences.txt')
        
        queries = []
        if os.path.exists(input_path):
            print(f"\nĐang đọc file: {input_path}")
            with open(input_path, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
        else:
            print(f"\nKhông tìm thấy {input_path}, sử dụng danh sách mặc định.")
            queries = default_queries

        print(f"Bắt đầu xử lý {len(queries)} câu truy vấn...\n")
        
        for i, query in enumerate(queries, 1):
            if 'reset' in query.lower() or 'xóa giỏ' in query.lower():
                db.data['current_order'] = {
                    'order_id': 'CURRENT', 'user': 'default_user', 
                    'items': [], 'total': 0, 'status': 'draft'
                }
                db.save_database()
                
                print(f"\n[{i}] Khách: {query}")
                print("=" * 60)
                print("SYSTEM COMMAND DETECTED: RESET CART")
                print("-" * 60)
                print("KelvinCook Take Order: Đã xóa sạch giỏ hàng.")
                print("=" * 60)

                writer.write_query(
                    query_num=i,
                    user_input=query,
                    tokens=["reset", "giỏ_hàng", "."],
                    dependencies=['"reset" --dobj -> "giỏ_hàng"'],
                    relations=['(s1 PRED reset)', '(s1 THEME giỏ_hàng)'],
                    logical_form="(COMMAND RESET)",
                    procedure="RESET_CART()",
                    answer="Đã xóa sạch giỏ hàng."
                )
                continue
            # -------------------------------------

            process_pipeline(query, i, generator, writer)
        print(writer.get_summary())

    # CHẾ ĐỘ 1: INTERACTIVE MODE
    else:
        print("\nĐã vào chế độ nhập tay. Gõ 'quit' để thoát, 'reset' để xóa giỏ hàng.")
        query_count = 0
        while True:
            user_input = input("\nKhách iu: ").strip()
            
            if not user_input: continue
            
            if user_input.lower() in ['quit', 'exit', 'thoát']:
                print(writer.get_summary())
                print("Cảm ơn quý khách!")
                break
            
            if user_input.lower() == 'reset':
                db.data['current_order'] = {
                    'order_id': 'CURRENT', 'user': 'default_user', 
                    'items': [], 'total': 0, 'status': 'draft'
                }
                db.save_database()
                print("Đã xóa sạch giỏ hàng!")
                continue
            
            query_count += 1
            process_pipeline(user_input, query_count, generator, writer)

if __name__ == "__main__":
    main()