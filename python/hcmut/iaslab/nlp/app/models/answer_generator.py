# python/hcmut/iaslab/nlp/app/models/answer_generator.py
from models.database import RestaurantDatabase
from models.semantic_procedure import Procedure

text2num = {
    "một": 1, "hai": 2, "ba": 3, "bốn": 4, "năm": 5,
    "sáu": 6, "bảy": 7, "tám": 8, "chín": 9, "mười": 10,
    "chục": 10, "trăm": 100,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10
}

class AnswerGenerator:
    def __init__(self, db: RestaurantDatabase):
        self.db = db

    def execute_and_answer(self, procedure: Procedure) -> str:
        cmd = procedure.name
        args = procedure.args

        # 1. LIST_ALL_ITEMS
        if cmd == "LIST_ALL_ITEMS":
            items = self.db.get_all_items()
            if not items: return "Menu hiện chưa có món nào."
            
            # Phân loại để hiển thị đẹp
            food = [i['name'] for i in items if i['type'] == 'food']
            drink = [i['name'] for i in items if i['type'] == 'drink']
            
            msg = "Thực đơn của quán gồm:\n"
            if food: msg += f"- Món ăn: {', '.join(food)}\n"
            if drink: msg += f"- Đồ uống: {', '.join(drink)}"
            return msg

        # 2. GET_PRICE
        elif cmd == "GET_PRICE":
            if not args: return "Bạn muốn hỏi giá món nào?"
            item_name = args[0]
            item = self.db.find_item_by_name(item_name)
            
            if item:
                return f"Món {item['name']} có giá {item['price']:,} VNĐ."
            return f"Xin lỗi, quán không phục vụ món '{item_name}'."

        # 3. CHECK_AVAILABILITY
        elif cmd == "CHECK_AVAILABILITY":
            if not args: return "Bạn muốn kiểm tra món nào?"
            item_name = args[0]
            item = self.db.find_item_by_name(item_name)
            
            if item and item['available']:
                return f"Dạ có, quán có phục vụ món {item['name']} ạ."
            return f"Dạ không, hiện quán không có món '{item_name}'."

        # 4. GET_ORDER_HISTORY
        elif cmd == "GET_ORDER_HISTORY":
            current_order = self.db.get_current_order()
            if not current_order['items']:
                return "Bạn chưa đặt món nào trong đơn hiện tại."
            
            msg = "Đơn hàng của bạn gồm:\n"
            for item in current_order['items']:
                opts = f" ({', '.join(item['options'])})" if item['options'] else ""
                msg += f"- {item['quantity']} {item['dish_name']}{opts}: {item['subtotal']:,}đ\n"
            msg += f"Tổng cộng: {current_order['total']:,}đ"
            return msg

        # 5. ADD_TO_CART
        elif cmd == "ADD_TO_CART":
            if not args or not args[0]: 
                return "Không rõ món cần thêm."
            
            item_name = args[0]
            raw_qty = args[1] if len(args) > 1 else "1"
            qty = 1
            raw_str = str(raw_qty).lower().strip()

            if raw_str.isdigit():
                qty = int(raw_str)
            elif raw_str in text2num:
                qty = text2num[raw_str]
            else:
                qty = 1 
            
            result = self.db.add_to_cart(item_name, qty, options=[])
            
            if result['success']:
                return f"Đã thêm {qty} phần {result['item']['dish_name']} vào đơn."
            return f"Không thể thêm món: {result['message']}"
        return "Xin lỗi, tôi chưa hiểu ý định của bạn."