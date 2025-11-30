# python/hcmut/iaslab/nlp/app/main.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import các module
from models.maltparser import malt_parse
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.database import RestaurantDatabase
from models.answer_generator import AnswerGenerator
from models.data import tokenize # Chỉ cần import tokenize

def process_query(sentence: str, generator: AnswerGenerator):
    print(f"\n🗣️  USER: {sentence}")
    print("-" * 60)
    
    # Debug Tokenize
    # tokens = tokenize(sentence)
    # print(f"Tokens: {tokens}")

    dependencies = malt_parse(sentence)
    relations = relationalize(dependencies)
    logical_form = logicalize(relations)
    
    # [Lưu ý] Đảm bảo bạn đang dùng file semantic_procedure.py phiên bản ROBUST tôi gửi ở câu trước
    procedure = proceduralize(logical_form)
    print(f"⚙️  Procedure: {procedure}")
    
    response = generator.execute_and_answer(procedure)
    print(f"🤖 BOT: {response}")
    print("-" * 60)

def main():
    print("=== 🍜 HỆ THỐNG ĐẶT MÓN ĂN (SIMPLE MODE) 🍜 ===")
    
    # 1. Khởi tạo Database (Chỉ để lấy giá tiền, không dùng để load từ vựng nữa)
    db = RestaurantDatabase()
    
    # 2. Khởi tạo Generator
    generator = AnswerGenerator(db)

    test_queries = [
        "Có những món gì trong menu ?",
        "Phở bò giá bao nhiêu ?",
        "Có món gà rán không ?",
        "Thêm 2 trà sữa vào đơn .",
        "Tôi đã đặt những món gì ?"
    ]
    
    for query in test_queries:
        process_query(query, generator)

if __name__ == "__main__":
    main()