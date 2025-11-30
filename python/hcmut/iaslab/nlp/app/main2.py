# python/hcmut/iaslab/nlp/app/main.py
import sys
import os

# Setup đường dẫn
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.maltparser import malt_parse
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.database import RestaurantDatabase
from models.answer_generator import AnswerGenerator

def process_query(sentence: str, generator: AnswerGenerator):
    print(f"\n🗣️  USER: {sentence}")
    print("-" * 60)

    # B1: Phân tích cú pháp
    dependencies = malt_parse(sentence)
    # Debug in ra cây phụ thuộc
    # print(f"1. Dependency Parse: {', '.join([str(d) for d in dependencies])}")

    # B2: Quan hệ ngữ nghĩa
    relations = relationalize(dependencies)
    # print(f"2. Relations: {', '.join([str(r) for r in relations])}")

    # B3: Dạng luận lý
    logical_form = logicalize(relations)
    # print(f"3. Logical Form: {logical_form}")

    # B4: Thủ tục
    procedure = proceduralize(logical_form)
    print(f"⚙️  Procedure: {procedure}")

    # B5: Thực thi & Trả lời
    response = generator.execute_and_answer(procedure)
    print(f"🤖 BOT: {response}")
    print("-" * 60)

def main():
    # Khởi tạo DB & Generator
    db = RestaurantDatabase()
    generator = AnswerGenerator(db)

    # Các câu test case
    test_queries = [
        "Có những món gì trong menu ?",       # Test LIST_ALL
        "Phở bò giá bao nhiêu ?",             # Test GET_PRICE
        "Có món gà rán không ?",              # Test CHECK_AVAILABILITY
        "Thêm 2 trà sữa vào đơn .",           # Test ADD_TO_CART (Số lượng > 1)
        "Tôi đã đặt những món gì ?"           # Test GET_ORDER_HISTORY
    ]

    print("=== 🍜 HỆ THỐNG ĐẶT MÓN ĂN THÔNG MINH 🍜 ===")
    
    for query in test_queries:
        process_query(query, generator)

if __name__ == "__main__":
    main()