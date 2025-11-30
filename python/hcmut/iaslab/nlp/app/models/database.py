# python/hcmut/iaslab/nlp/app/models/database.py
import json
import os
from datetime import datetime

class RestaurantDatabase:

    def __init__(self, menu_file='data/menu.json'):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.menu_file = os.path.join(base_dir, menu_file)
        
        self.data = self._load_database()

    # ==================== CORE: LOAD & SAVE ====================

    def _load_database(self):
        try:
            os.makedirs(os.path.dirname(self.menu_file), exist_ok=True)
            with open(self.menu_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self._validate_structure(data)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[DB] Không tìm thấy hoặc lỗi file {self.menu_file}, tạo database mẫu...")
            return self._create_sample_database()

    def save_database(self):
        try:
            with open(self.menu_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Lỗi lưu database: {e}")
            return False

    def _validate_structure(self, data):
        defaults = {
            'dishes': [],
            'order_history': [],
            'current_order': {
                'order_id': 'CURRENT', 'user': 'default_user', 
                'items': [], 'total': 0, 'status': 'draft'
            },
            'global_options': {
                'food_common': {'options': []},
                'drink_common': {'options': []},
                'all_common': {'options': []}
            }
        }
        for key, value in defaults.items():
            if key not in data:
                data[key] = value

    def _create_sample_database(self):
        return {
            'dishes': [
                # --- FOOD ---
                {'id': 1, 'name': 'phở bò', 'price': 50000, 'type': 'food', 'category': 'món nước', 'available': True, 'options': ['tái', 'nạm', 'gầu', 'viên']},
                {'id': 2, 'name': 'cơm tấm', 'price': 45000, 'type': 'food', 'category': 'cơm', 'available': True, 'options': ['sườn', 'bì', 'chả', 'trứng ốp la']},
                {'id': 3, 'name': 'bún chả', 'price': 55000, 'type': 'food', 'category': 'món nước', 'available': True, 'options': ['thêm thịt', 'thêm bún']},
                
                # --- DRINK ---
                {'id': 101, 'name': 'trà sữa', 'price': 25000, 'type': 'drink', 'category': 'trà', 'available': True, 'options': ['ít đường', 'nhiều đường', 'trân châu đen', 'thạch dừa']},
                {'id': 102, 'name': 'cà phê sữa', 'price': 20000, 'type': 'drink', 'category': 'cà phê', 'available': True, 'options': ['nóng', 'đá', 'ít sữa', 'nhiều sữa']},
                {'id': 103, 'name': 'nước cam', 'price': 30000, 'type': 'drink', 'category': 'nước ép', 'available': True, 'options': ['không đường', 'ít đá']}
            ],
            'global_options': {
                'food_common': {'options': ['cay', 'không cay', 'ít muối', 'thêm ớt', 'không hành']},
                'drink_common': {'options': ['ít đá', 'nhiều đá', 'không đá', 'ít đường', 'nhiều đường', 'nóng', 'lạnh']},
                'all_common': {'options': ['gói mang đi', 'ăn tại chỗ', 'giao nhanh']}
            },
            'order_history': [],
            'current_order': {
                'order_id': 'CURRENT', 'user': 'default_user', 
                'items': [], 'total': 0, 'status': 'draft'
            }
        }

    def get_all_items(self):
        return self.data['dishes']

    def get_food_items(self):
        return [d for d in self.data['dishes'] if d.get('type') == 'food']

    def get_drink_items(self):
        return [d for d in self.data['dishes'] if d.get('type') == 'drink']

    def find_item_by_name(self, name):
        name_lower = name.lower().replace("_", " ").strip()
    
        for item in self.data['dishes']:
            if item['name'].lower() == name_lower:
                return item
        
        for item in self.data['dishes']:
            if name_lower in item['name'].lower():
                return item
        return None
    
    def find_item_by_id(self, item_id):
        for item in self.data['dishes']:
            if item['id'] == item_id:
                return item
        return None

    def get_valid_options(self, item_id):
        item = self.find_item_by_id(item_id)
        if not item: return None

        valid_opts = item.get('options', []).copy()
        item_type = item.get('type', 'food')
        if item_type == 'food':
            valid_opts += self.data['global_options']['food_common']['options']
        elif item_type == 'drink':
            valid_opts += self.data['global_options']['drink_common']['options']
        
        valid_opts += self.data['global_options']['all_common']['options']
        
        return list(set(valid_opts))

    def validate_options(self, item_id, requested_options):
        """Validate list options người dùng nhập vào"""
        valid_list = self.get_valid_options(item_id)
        if not valid_list:
            return {'valid': [], 'invalid': requested_options, 'all_valid': False}

        validated = {'valid': [], 'invalid': [], 'all_valid': True}
        
        for req in requested_options:
            req_clean = req.lower().strip()
            # Check fuzzy
            match = next((v for v in valid_list if req_clean in v.lower() or v.lower() in req_clean), None)
            if match:
                validated['valid'].append(match)
            else:
                validated['invalid'].append(req)
                validated['all_valid'] = False
        
        return validated

    # ==================== ORDER LOGIC (TRANSACTION) ====================

    def get_current_order(self):
        return self.data['current_order']

    def get_order_history(self):
        return self.data['order_history']

    def add_to_cart(self, item_name, quantity=1, options=None):
        if options is None: options = []
        
        # 1. Tìm món
        item = self.find_item_by_name(item_name)
        if not item:
            return {'success': False, 'message': f'Không tìm thấy món "{item_name}"'}
        
        if not item.get('available', True):
            return {'success': False, 'message': f'Món "{item["name"]}" đang tạm hết'}

        # 2. Validate Options
        val_result = self.validate_options(item['id'], options)
        final_options = val_result['valid']
        warnings = [f"Bỏ qua '{opt}' do không hợp lệ" for opt in val_result['invalid']]

        # 3. Logic thêm vào giỏ hàng
        current = self.data['current_order']

        existing_entry = next((i for i in current['items'] if i['dish_id'] == item['id'] and set(i.get('options',[])) == set(final_options)), None)

        if existing_entry:
            existing_entry['quantity'] += quantity
            existing_entry['subtotal'] = existing_entry['quantity'] * existing_entry['price']
            msg = f"Đã cập nhật số lượng {item['name']}"
        else:
            new_entry = {
                'dish_id': item['id'],
                'dish_name': item['name'],
                'type': item.get('type', 'food'),
                'quantity': quantity,
                'price': item['price'],
                'options': final_options,
                'subtotal': quantity * item['price']
            }
            current['items'].append(new_entry)
            msg = f"Đã thêm {quantity} {item['name']}"

        # Recalculate Total
        current['total'] = sum(i['subtotal'] for i in current['items'])
        
        self.save_database()
        
        return {
            'success': True, 
            'message': msg, 
            'option_warnings': warnings,
            'item': existing_entry or new_entry
        }

    def remove_from_cart(self, item_name):
        current = self.data['current_order']

        for i in range(len(current['items']) - 1, -1, -1):
            item = current['items'][i]
            if item_name.lower() in item['dish_name'].lower():
                removed = current['items'].pop(i)
                current['total'] = sum(x['subtotal'] for x in current['items'])
                self.save_database()
                return {'success': True, 'message': f"Đã xóa {removed['dish_name']} khỏi giỏ"}
        
        return {'success': False, 'message': f"Không thấy món {item_name} trong giỏ"}

    def place_order(self):
        current = self.data['current_order']
        if not current['items']:
            return {'success': False, 'message': "Giỏ hàng đang trống"}
        
        new_order = current.copy()
        new_order['order_id'] = f"ORD-{datetime.now().strftime('%Y%m%d')}-{len(self.data['order_history'])+1:03d}"
        new_order['status'] = 'pending'
        new_order['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.data['order_history'].append(new_order)
        
        # Reset Cart
        self.data['current_order'] = {
            'order_id': 'CURRENT', 'user': 'default_user', 
            'items': [], 'total': 0, 'status': 'draft'
        }
        self.save_database()
        
        return {'success': True, 'message': f"Đã đặt hàng thành công! Mã đơn: {new_order['order_id']}", 'order': new_order}