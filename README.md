# BÁO CÁO KẾT QUẢ THỰC HIỆN BÀI TẬP LỚN  
**Môn**: Xử lý ngôn ngữ tự nhiên (NLP)  
**Chủ đề hệ thống**: Đặt món ăn nhà hàng trực tuyến (ONLINE RESTAURANT FOOD BOOKING)

## 1. Thông tin sinh viên

- **Họ và tên**: Bùi Trần Duy Khang  
- **MSSV**: 2311402  
- **Đơn vị**: Khoa Khoa học và Kỹ thuật Máy tính – Trường Đại học Bách khoa – ĐHQG TP.HCM  

## 2. Mục tiêu & Phạm vi BTL phần II

### 2.1. Tổng quan
Hệ thống này là phần mở rộng nâng cao tiếp theo của bài tập lớn, tập trung vào việc hiểu ngữ nghĩa sâu sắc của câu lệnh tiếng Việt và thực thi các hành động tương ứng trên cơ sở dữ liệu giả lập. Không chỉ dừng lại ở việc nhận diện từ khóa, hệ thống hướng tới việc mô phỏng khả năng hiểu ngôn ngữ của con người trong miền ứng dụng cụ thể là đặt món ăn nhà hàng.

Mục tiêu cốt lõi của hệ thống không chỉ dừng lại ở việc phân tích cú pháp để xác định cấu trúc ngữ pháp của câu, mà còn chuyển đổi cây cú pháp đó thành các biểu diễn ngữ nghĩa trừu tượng. Nhờ đó, máy tính có thể thực sự hiểu ý định và các thông tin chi tiết trong câu hỏi hoặc yêu cầu của người dùng, từ đó đưa ra phản hồi chính xác và thực hiện các tác vụ nghiệp vụ như tra cứu giá, kiểm tra món, hay cập nhật giỏ hàng.

### 2.2. Mục tiêu kỹ thuật

Hệ thống tập trung vào việc chuyển đổi ngôn ngữ tự nhiên (Natural Language) sang ngôn ngữ máy có thể thực thi (Machine Executable Procedures) thông qua các bước:

1.  **Phân tích hình thái**: Tách từ và gán nhãn từ loại.
    
2.  **Phân tích cú pháp**: Xây dựng cây phụ thuộc (Dependency Tree).
    
3.  **Phân tích ngữ nghĩa**: Trích xuất quan hệ ngữ nghĩa (Semantic Relations) và dạng logic (Logical Form).
    
4.  **Thực thi**: Ánh xạ sang thủ tục nghiệp vụ (Database Transaction).


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
│   ├── grammar.txt             # Luật ngữ pháp phụ thuộc (dùng để backup)
│   ├── menu.json               # Dữ liệu Menu & Lịch sử đặt hàng (dùng để backup)
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

### 4.1. Quy trình xử lý

Hệ thống hoạt động theo mô hình đường ống (Pipeline) tuần tự, dữ liệu đầu ra của bước trước là đầu vào của bước sau. Quy trình bao gồm các bước chính sau:

1.  **Tokenization & POS Tagging (`data.py`):**

    *   Chuẩn hóa chuỗi đầu vào (lowercase, chuẩn hóa Unicode).
    
    *   Tách câu thành các tokens.
        
    *   Gán nhãn từ loại (POS Tagging): `N` (Danh từ), `V` (Động từ), `NAME` (Tên món), `ADJ` (Tính từ).
        
2.  **Phân tích cú pháp (`maltparser.py`):**
    
    *   Sử dụng thuật toán **MaltParser** và sử dụng cấu trúc Stack và Buffer.
        
    *   Đọc tập luật từ `data/grammar.txt` để định nghĩa các quan hệ như `root`, `nmod`, `dobj`, `attr`.
        
    *   **Output:** Cây cú pháp phụ thuộc mô tả mối quan hệ giữa các từ trong câu (ghi vào `qhvp.txt`).
        
3.  **Phân tích ngữ nghĩa (`grammar_relation.py`, `logical_form.py`):**
    
    *   **Relationalize:** Chuyển đổi cây cú pháp thành danh sách các quan hệ ngữ nghĩa (AGENT, THEME, LOCATION, QUANTITY). **Output:** `qhnn.txt`.
        
    *   **Logicalize:** Tổng hợp các quan hệ thành biểu diễn Logic (Logical Form) có cấu trúc (ví dụ: `(PRICE-QUERY 's1' ...)`).

    *   **Xử lý Options**: Hỗ trợ đệ quy để bắt chuỗi các tùy chọn món ăn (ví dụ: "ít đường" + "ít đá").
        
4.  **Thủ tục ngữ nghĩa (`semantic_procedure.py`):**
    
    *   Ánh xạ từ Logical Form sang thủ tục thực thi cụ thể.

    *   Các thủ tục bao gồm: `ADD_TO_CART(item, quantity, options)`, `GET_PRICE(item)`, `CHECK_AVAILABILITY(item_name)`, `GET_ORDER_HISTORY()`, `LIST_ALL_ITEMS()`, `RESET_CART()`, `RESET_CART()`
        
    *   Ví dụ:
```
(STATEMENT, PRED:thêm, THEME:phở_bò) -> ADD_TO_CART(phở_bò, 1, [])

(PRICE-QUERY, THEME:cơm_tấm) -> GET_PRICE(cơm_tấm)
```

        
5.  **Thực thi và phản hồi (`answer_generator.p`y`):**
    
    * Gọi xuống Database (`models/database.py`) để lấy dữ liệu hoặc cập nhật giỏ hàng, sau đó sinh câu trả lời tiếng Việt tự nhiên trả về cho người dùng.
        
    *   **Output:** answer.txt.
    

## 5. Hướng dẫn sử dụng

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
    

### C. Nén thành file  `.zip` để nộp bài

Lệnh này sẽ tự động chạy Batch Mode một lần để sinh kết quả mới nhất, sau đó nén toàn bộ source code và output vào file .zip.

```bash
 ./util.sh submit
 ```

*   **Kết quả:** File 2311402.zip sẽ được tạo tại thư mục gốc.
    

## 5. Các truy vấn hỗ trợ

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
        
5.  **Đặt món:**
    
    *   "Thêm 1 ly trà sữa vào đơn."
        
    *   "Cho 2 phần phở bò."
        

6. **Reset giỏ hàng:**

    *   "Reset"
        
    *   "Xóa giỏ hàng"

7. **Thoát chương trình:**

    *   "Quit"
        
    *   "Exit"

## 6. Tổng kết & Đánh giá hệ thống

### 6.1. Ưu điểm

1.  **Kiến trúc rõ ràng:** Hệ thống được chia tách thành các module độc lập tương ứng với từng tầng xử lý ngôn ngữ (Lexical -> Syntactic -> Semantic -> Pragmatic). Điều này giúp dễ dàng debug và bảo trì.
    
2.  **Xử lý ngữ nghĩa sâu:** Không chỉ bắt từ khóa, hệ thống hiểu được cấu trúc câu. Ví dụ: phân biệt được câu hỏi *Yes/No* ("Có bán phở không?") và câu hỏi Wh- ("Bán món gì?").
    
3.  **Hỗ trợ tùy chọn phức tạp:** Hệ thống có khả năng xử lý các món ăn đi kèm nhiều tùy chọn nối tiếp nhau (Chain options) như "Trà sữa _trân châu đen_ _ít đường_ _ít đá_".
    
4.  **Dữ liệu tách biệt logic:** Menu và Luật ngữ pháp được lưu trong file cấu hình (json, txt), giúp dễ dàng cập nhật thực đơn hoặc mở rộng ngữ pháp mà không cần sửa code (Hard-coding).
    
5.  **Triển khai dễ dàng:** Sử dụng Docker đảm bảo môi trường thực thi đồng nhất, tránh lỗi phụ thuộc thư viện.
    
### 6.2. Nhược điểm và Hạn chế

1.  **Phụ thuộc từ điển cứng nhắc:** Hệ thống chỉ hiểu các từ đã được khai báo trong data.py. Nếu gặp từ lạ (OOV - Out of Vocabulary) chưa được định nghĩa, Tokenizer có thể xử lý không chính xác.
    
2.  **Văn phạm thủ công (Rule-based Grammar):** Các luật ngữ pháp trong grammar.txt được viết tay. Điều này gây khó khăn khi mở rộng sang các mẫu câu phức tạp hơn hoặc các cách diễn đạt quá tự do của ngôn ngữ tự nhiên.
    
3.  **Chưa xử lý lỗi chính tả (No Spell Checking):** Hệ thống chưa tích hợp module sửa lỗi chính tả, do đó người dùng cần nhập đúng từ vựng đã định nghĩa.
    
4.  **Khả năng mở rộng:** Do sử dụng phương pháp dựa trên luật, việc mở rộng hệ thống để hiểu mọi câu nói tiếng Việt là rất tốn kém công sức so với các phương pháp Học máy hiện đại.
    

### 6.3. Hướng phát triển

*   Tích hợp thuật toán đối sánh mờ (Fuzzy Matching) để xử lý lỗi chính tả nhẹ.
    
*   Mở rộng bộ luật ngữ pháp để bao phủ nhiều biến thể câu lệnh hơn.
    
*   Kết hợp mô hình thống kê hoặc Deep Learning đơn giản để gán nhãn POS Tagging tự động thay vì dùng từ điển cứng.

## 7. Thông tin liên hệ
Mọi thắc mắc về source code hoặc báo cáo, vui lòng liên hệ:

*   **Sinh viên:** Bùi Trần Duy Khang
    
*   **MSSV:** 2311402
    
*   **Email:** khang.buitranduycse@hcmut.edu.vn
*   **Github repository:** [https://github.com/khangbkk23/NaturalLanguageProcessing_RAGsystem/tree/BTL-II]