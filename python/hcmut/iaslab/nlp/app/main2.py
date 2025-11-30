# python/hcmut/iaslab/nlp/app/main2.py
import sys
import os

# Thêm đường dẫn hiện tại vào path để import được package 'models'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import các module
from models.maltparser import malt_parse
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.database import RestaurantDatabase
from models.answer_generator import AnswerGenerator
from models.data import tokenize

def process_query(sentence: str, generator: AnswerGenerator):
    print(f"\nKhách iu: {sentence}")
    print("=" * 60)
    
    # Tokenization
    tokens = tokenize(sentence)
    print(f"1️⃣  Tokens:       {tokens}")

    # Dependency parsing
    dependencies = malt_parse(sentence)
    dep_str = ', '.join([f"{d.relation}({d.head}->{d.tail})" for d in dependencies])
    print(f"2️⃣  Dependencies: [{dep_str}]")

    # Semantic relations
    relations = relationalize(dependencies)
    rel_str = ', '.join([str(r) for r in relations])
    print(f"3️⃣  Relations:    [{rel_str}]")

    # Logical form
    logical_form = logicalize(relations)
    print(f"4️⃣  Logical Form: {logical_form}")
    
    # Procedural semantics
    procedure = proceduralize(logical_form)
    print(f"5️⃣  Procedure:    \033[92m{procedure}\033[0m")
    
    # Execution & answer
    response = generator.execute_and_answer(procedure)
    print("-" * 60)
    print(f"KelvinCook Server: {response}")
    print("=" * 60)

def main():
    print("\nHỆ THỐNG ĐẶT MÓN ĂN CỦA NHÀ HÀNG KELVINCOOK")
    
    db = RestaurantDatabase(reset_order=True)
    # db = RestaurantDatabase()
    print(f"Database loaded: {len(db.get_all_items())} items.")
    generator = AnswerGenerator(db)

    test_queries = [
        "Tôi muốn đặt một tô phở bò tái",
        "Có những món gì trong menu ?",
        "Phở bò giá bao nhiêu ?",
        "Có món gà rán không ?",
        "Thêm 2 ly trà sữa vào đơn .",
        "Tôi đã đặt những món gì ?"
    ]
    
    for query in test_queries:
        process_query(query, generator)

if __name__ == "__main__":
    main()