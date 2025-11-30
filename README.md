# BÁO CÁO KẾT QUẢ THỰC HIỆN BÀI TẬP LỚN  
**Môn**: Xử lý ngôn ngữ tự nhiên (NLP)  
**Chủ đề hệ thống**: Đặt món ăn nhà hàng trực tuyến (ONLINE RESTAURANT FOOD BOOKING)

---

## 1. Thông tin sinh viên

- **Họ và tên**: Bùi Trần Duy Khang  
- **MSSV**: 2311402  
- **Đơn vị**: Khoa Khoa học và Kỹ thuật Máy tính – Trường Đại học Bách khoa – ĐHQG TP.HCM  

---

## 2. Mục tiêu & Phạm vi BTL phần II

Hệ thống này là phần mở rộng nâng cao tiếp theo của bài tập lớn, tập trung vào việc hiểu ngữ nghĩa sâu sắc của câu lệnh tiếng Việt và thực thi các hành động tương ứng trên cơ sở dữ liệu giả lập. Không chỉ dừng lại ở việc nhận diện từ khóa, hệ thống hướng tới việc mô phỏng khả năng hiểu ngôn ngữ của con người trong miền ứng dụng cụ thể là đặt món ăn nhà hàng.

Mục tiêu cốt lõi của hệ thống không chỉ dừng lại ở việc phân tích cú pháp để xác định cấu trúc ngữ pháp của câu, mà còn chuyển đổi cây cú pháp đó thành các biểu diễn ngữ nghĩa trừu tượng. Nhờ đó, máy tính có thể thực sự hiểu ý định và các thông tin chi tiết trong câu hỏi hoặc yêu cầu của người dùng, từ đó đưa ra phản hồi chính xác và thực hiện các tác vụ nghiệp vụ như tra cứu giá, kiểm tra món, hay cập nhật giỏ hàng.

## 3. Cấu trúc thư mục & Môi trường thực thi

### 3.1. Yêu cầu môi trường

- **Python**: phiên bản >= 3.8  
- Thư viện chuẩn Python:
  - `os`, `re`, `random`, `collections`, `itertools`, `sys`

### 3.2. Cấu trúc thư mục

```text
2311402/                        
├── input/
│   └── sentences.txt           # File chứa các câu truy vấn mẫu
├── output/                     # Thư mục chứa kết quả đầu ra
│   ├── qhnn.txt                # Quan hệ ngữ nghĩa
│   ├── qhvp.txt                # Quan hệ văn phạm
│   ├── ll.txt                  # Dạng luận lý & Ngữ nghĩa thủ tục
│   └── answer.txt              # Câu trả lời cuối cùng của hệ thống
├── python/                     # Source code chính
│   ├── hcmut/iaslab/nlp/app/   # Package code
│   │   ├── models/             # Chứa các module xử lý NLP
│   │   │   ├── data.py             # Dữ liệu từ vựng & POS Tagging
│   │   │   ├── maltparser.py       # Bộ phân tích cú pháp phụ thuộc
│   │   │   ├── grammar_relation.py # Chuyển đổi Parse Tree -> Semantic Relations
│   │   │   ├── logical_form.py     # Chuyển đổi Relations -> Logical Form
│   │   │   ├── semantic_procedure.py # Chuyển đổi Logical Form -> Procedure
│   │   │   ├── database.py         # Quản lý Menu & Giỏ hàng
│   │   │   └── answer_generator.py # Sinh câu trả lời tự nhiên
│   │   ├── main.py             # File chạy chính
│   │   └── output_writer.py    # Ghi log ra file output
│   ├── data/                   # Dữ liệu tĩnh
│   │   ├── grammar.txt         # Tập luật văn phạm phụ thuộc (Dependency Grammar Rules)
│   │   └── menu.json           # Dữ liệu Menu & Lịch sử đặt hàng
│   ├── Dockerfile              # Cấu hình Docker image
│   └── requirements.txt        # Các thư viện Python cần thiết
├── util.sh                     # Script tiện ích để chạy, test và đóng gói
└── README.md                   # Hướng dẫn sử dụng

```

## 4. Chức năng chính của hệ thống

### 4.1. Quy trình xử lý (Pipeline)

Hệ thống hoạt động theo mô hình đường ống (pipeline) gồm 5 bước:

1.  **Tokenization & POS Tagging (`data.py`):**
    
    *   Tách câu thành các tokens.
        
    *   Gán nhãn từ loại (POS tags) như NOUN, VERB, NAME dựa trên từ điển.
        
2.  **Dependency Parsing (`maltparser.py`):**
    
    *   Sử dụng thuật toán MaltParser.
        
    *   Đọc tập luật từ `data/grammar.txt` để xác định quan hệ phụ thuộc giữa các từ.
        
    *   **Output:** Cây cú pháp phụ thuộc (ghi vào `qhvp.txt`).
        
3.  **Semantic Analysis (`grammar\_relation.py`, `logical\_form.py`):**
    
    *   **Relationalize:** Chuyển đổi cây cú pháp thành danh sách các quan hệ ngữ nghĩa (ví dụ: (s1 AGENT phở\_bò)). **Output:** `qhnn.txt`.
        
    *   **Logicalize:** Tổng hợp các quan hệ thành biểu diễn Logic (Logical Form) có cấu trúc (ví dụ: `(PRICE-QUERY 's1' ...)`).
        
4.  **Procedural Semantics (`semantic\_procedure.py`):**
    
    *   Ánh xạ Logical Form sang thủ tục thực thi cụ thể.
        
    *   Ví dụ: `GET\_PRICE(phở\_bò)`, `ADD\_TO\_CART(trà\_sữa, 2)`.
        
    *   **Output:** `ll.txt`.
        
5.  **Execution & Response (answer\_generator.py):**
    
    *   Thực thi thủ tục trên Database.
        
    *   Sinh câu trả lời tiếng Việt tự nhiên.
        
    *   **Output:** answer.txt.
        

### 4.2. Các truy vấn hỗ trợ

Hệ thống hỗ trợ 5 loại câu hỏi theo yêu cầu đề bài:

1.  **Hỏi Menu:** "Có những món nào trong menu?", "Quán có món gì?"
    
2.  **Hỏi Giá:** "Phở bò giá bao nhiêu?", "Giá trà sữa là bao nhiêu?"
    
3.  **Kiểm tra món:** "Có món gà rán không?", "Còn trà sữa không?"
    
4.  **Xem lịch sử / Giỏ hàng:** "Tôi đã đặt những món gì?", "Kiểm tra đơn hàng."
    
5.  **Đặt món:** "Thêm 1 ly trà sữa vào đơn.", "Cho 2 phần phở bò."
    

## 5. Hướng dẫn sử dụng
----------------------------------

Hệ thống cung cấp script util.sh để đơn giản hóa việc chạy và kiểm thử.

**Trước khi chạy, cấp quyền thực thi:**

```bash
chmod +x util.sh
```

### A. Chế độ Tự động (Batch Mode) - Dùng để chấm bài

Hệ thống sẽ đọc các câu mẫu trong input/sentences.txt, xử lý lần lượt và xuất toàn bộ kết quả ra thư mục output/.

**Lệnh chạy:**

```bash
./util.sh batch
```

**Kết quả:** Kiểm tra thư mục output/ sau khi chạy xong. Sẽ có đầy đủ 4 file:

*   `qhvp.txt`: Quan hệ văn phạm.
    
*   `qhnn.txt`: Quan hệ ngữ nghĩa.
    
*   `ll.txt`: Dạng luận lý & Thủ tục.
    
*   `answer.txt`: Câu trả lời của hệ thống.
    

### B. Chế độ Tương tác (Interactive Mode) - Dùng để Test/Chat

Cho phép người dùng nhập câu hỏi trực tiếp từ bàn phím để kiểm tra khả năng phản hồi của hệ thống.

**Lệnh chạy:**

```bash
./util.sh interactive
```

*   Sau khi container khởi động, chọn chế độ **Interactive Mode**.
    
*   Nhập câu hỏi (ví dụ: "`Phở bò giá bao nhiêu?`").
    
*   Gõ reset để xóa giỏ hàng hiện tại.
    
*   Gõ quit hoặc exit để thoát chương trình.
    

### C. Đóng gói nộp bài

Lệnh này sẽ tự động chạy Batch Mode một lần để sinh kết quả mới nhất, sau đó nén toàn bộ source code và output vào file .zip.

```bash
 ./util.sh submit
 ```

*   **Kết quả:** File 2311402.zip sẽ được tạo tại thư mục gốc.
    

## 5. Các truy vấn hỗ trợ (Supported Queries)

Hệ thống hỗ trợ các loại câu hỏi sau (tương ứng với yêu cầu đề bài):

1.  **Hỏi Menu:**
    
    *   "Có những món nào trong menu?"
        
    *   "Quán có món gì?"
        
2.  **Hỏi giá:**
    
    *   "Phở bò giá bao nhiêu?"
        
    *   "Giá trà sữa là bao nhiêu?"
        
3.  **Kiểm tra món:**
    
    *   "Có món gà rán không?"
        
    *   "Còn trà sữa không?"
        
4.  **Xem lịch sử / Giỏ hàng:**
    
    *   "Tôi đã đặt những món gì?"
        
    *   "Kiểm tra đơn hàng."
        
5.  **Đặt món (Thêm vào giỏ):**
    
    *   "Thêm 1 ly trà sữa vào đơn."
        
    *   "Cho 2 phần phở bò."
        
    *   "Lấy tôi ba tô bún chả."
        

## 6. Thông tin liên hệ

*   **Sinh viên:** Bùi Trần Duy Khang
    
*   **MSSV:** 2311402
    
*   **Email:** khang.buitranduycse@hcmut.edu.vn