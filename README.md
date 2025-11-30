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

Trong phần này, hệ thống tập trung vào **Xử lý ngôn ngữ tự nhiên dựa trên văn phạm phi ngữ cảnh (CFG)** và **thuật toán phân tích cú pháp Earley**. Bao gồm ba nhiệm vụ chính:

### 2.1. Xây dựng tập luật và văn phạm cho miền đặt món ăn online

- Thiết kế và hiện thực một **Context-Free Grammar (CFG)** mô tả được các kiểu câu phổ biến trong ngữ cảnh khách hàng đặt món ăn, đồ uống tại nhà hàng (tiếng Việt).
- Văn phạm phải:
  - Biểu diễn được các thành phần cơ bản như: **món ăn, đồ uống, số lượng, đơn vị, tùy chọn (ít đá, nhiều đường, size lớn/nhỏ), thời gian giao, tên quán,…**
  - Hỗ trợ nhiều kiểu cấu trúc câu: **yêu cầu, đặt món, hỏi thông tin, hủy/đổi đơn, ...**
- **Input:** dữ liệu grammar nội bộ (ví dụ: file `data/grammar.txt` trong thư mục dự án).
- **Output chuẩn:**  
  File văn phạm sau khi hoàn thiện và sử dụng trong hệ thống được lưu tại:

  ```text
  output/grammar.txt
  ```
### 2.2. Viết giải thuật sinh câu từ CFG (Sentence Generator)

*   Xây dựng **bộ sinh câu** dựa trên văn phạm đã thiết kế ở mục 2.1.
    
*   Mục tiêu:
    
    *   **Tự động sinh ra các câu tiếng Việt hợp lệ theo CFG**.
        
    *   Dùng các câu này để:
        
        *   Mô phỏng các câu mà khách hàng có thể nhập khi đặt món online.
            
        *   Kiểm tra độ bao phủ và tính hợp lý của văn phạm.
            
*   Bộ sinh câu cần có cơ chế giới hạn số lượng câu sinh ra **(tối đa 10.000 câu)**.
    
*   **Input:** văn phạm CFG đã xây dựng.
    
*   **Output**: ghi vào trong: 
`output/samples.txt` (Giới hạn tối đa: **10.000 câu**)

### 2.3. Xây dựng bộ phân tích cú pháp (Parser)

*   Ở đây, em sử dụng thuật toán **Earley Parser** để phân tích cú pháp các câu đầu vào trong miền đặt món ăn online mà tránh phụ thuộc vào thư viện có sẵn.
    
*   Nhiệm vụ:
    
    *   Nhận các câu tiếng Việt trong `input/sentences.txt`
        
    *   Kiểm tra câu đó có phù hợp với CFG hay không.
        
    *   Nếu phù hợp, dựng lại **cây phân tích cú pháp (parse tree)** dựa trên các bước của thuật toán Earley. Với mỗi câu đầu vào, hệ thống ghi ra một dòng kết quả tương ứng trong: `output/parse-results.txt`
    
    *   Nếu câu **hợp lệ theo văn phạm** → ghi cấu trúc **cây cú pháp** (parse tree), thường ở dạng s-expression.
        
    *   Nếu câu không hợp lệ / không phân tích được → ghi:`()`

## 3. Cấu trúc thư mục & Môi trường thực thi

### 3.1. Yêu cầu môi trường

- **Python**: phiên bản >= 3.8  
- Thư viện chuẩn Python:
  - `os`, `re`, `random`, `collections`, `itertools`, `sys`
- **Không sử dụng** các thư viện nặng như `numpy`, `pandas` cho phần lõi của BTL Phần I.

### 3.2. Cấu trúc thư mục

```text
python/
└── hcmut/
    └── iaslab/
        └── nlp/
            ├── app/
            │   ├── earley_parser.py   # Cài đặt thuật toán Earley
            │   ├── generator.py       # Logic sinh câu từ CFG
            │   ├── grammar.py         # Định nghĩa lớp CFG & quản lý Rule
            │   ├── parser.py          # Xử lý tác vụ parse câu
            │   ├── utils.py           # Hàm tiện ích, load lexicon, config
            │   └── main.py            # Điểm vào chính (entry point)
            └── data/
                ├── grammar.txt        # File grammar chính (CFG)
                ├── food_names.txt     # Từ vựng: món ăn
                ├── drink_names.txt    # Từ vựng: đồ uống
                ├── common_opts.txt    # Từ vựng: tùy chọn chung (đường, đá,...)
                └── ...                # Các file từ vựng khác (đơn vị, quán,...)

input/
└── sentences.txt                      # Danh sách câu đầu vào cần parse

2311402/
└── output/
    ├── samples.txt                    # Các câu sinh ra từ CFG
    └── parse-results.txt              # Kết quả cây phân tích cú pháp

```

## 4. Chức năng chính của hệ thống
#### 4.1. Nạp văn phạm & quản lý từ vựng

**File chính**: `grammar.py`, `utils.py`

Hệ thống hỗ trợ:

- Nạp **grammar cơ bản** từ `data/grammar.txt`.
- Mở rộng grammar bằng **lexicon động** (món ăn, đồ uống, đơn vị, tên quán...).

**Hàm trọng tâm** (trong `utils.py`):

```python
load_grammar_with_lexicons(grammar_file, lexicon_config)
```

**Chức năng chính:**

*   Đọc các luật cấu trúc từ `grammar.txt`.
    
*   Thay thế các non-terminal đặc biệt (vd: `\_DO\_AN\_`, `\_DO\_UONG\_`, `\_TEN\_QUAN\_`, `\_DON\_VI\_`,…) bằng danh sách từ vựng từ những file tương ứng trong thư mục `data/`.
    
*   Sử dụng `simple\_tokenizer` tự xây dựng để tách từ thống nhất với quá trình parse.
    

**Ý nghĩa:**

*   Cho phép **thay đổi domain từ vựng** (món mới, đồ uống mới…) chỉ bằng cách chỉnh file `.txt` mà **không cần sửa code** hay grammar.
    
*   Grammar vừa mang tính **cấu trúc**, vừa linh hoạt theo dữ liệu thực tế.
    

### 4.2. Bộ sinh câu từ CFG (`generator.py`)

**Mục tiêu**: Tự động sinh các câu tiếng Việt đúng theo CFG, mô phỏng lời nói/nhắn tin của khách đặt món.

*   Hàm chính:
    

```python
run_generation_task(limit=10000)
```

**Chức năng:**

* Nạp đầy đủ grammar (bao gồm rule + lexicon).
        
**Ghi kết quả:** 
Toàn bộ câu sinh ra sẽ được ghi vào:
```
2311402/output/samples.txt
``` 

**Kết quả thực tế:**

*   Hệ thống sinh được nhiều mẫu câu đa dạng.
        
*   Các mẫu câu được dùng để:
    
    *   Kiểm tra **độ bao phủ** của grammar.
        
    *   Test nhanh **Earley Parser** với lượng dữ liệu lớn.
        

### 4.3. Bộ phân tích cú pháp Earley (`earley\_parser.py`)

**Mục tiêu**: Cài đặt **thuật toán Earley** cho phép phân tích cú pháp với:

*   Văn phạm phi ngữ cảnh **có thể mơ hồ** (*ambiguous CFG*).
    
*   Hỗ trợ cả:
    
    *   **Predictor**: dự đoán những rule tiếp theo có thể xuất hiện.
        
    *   **Scanner**: kiểm tra token hiện tại có khớp terminal không.
        
    *   **Completer**: hoàn thiện một constituent và đẩy tiến dấu chấm `·` trong các state khác.
        

**Lớp chính**: `EarleyParser`

**Một số phương thức quan trọng:**

*   `parse(tokens)`:
    
    *   Khởi tạo *bảng Earley (chart)*.
        
    *   Chạy vòng lặp qua từng vị trí token.
        
    *   Gọi lần lượt **`\_predictor**, **\_scanner**, **\_completer`**.
        
*   `\_predictor(step)`: mở rộng các rule có non-terminal ngay sau dấu chấm.
    
*   `\_scanner(step)`: nếu ký hiệu sau dấu chấm là terminal, kiểm tra có khớp token hiện tại không.
    
*  ` \_completer(step)`: khi một rule hoàn tất, cập nhật các state đã chờ non-terminal đó.
    
*   `build\_parse\_tree()`:
    
    *   Từ các **back-pointer**, dựng lại cây phân tích cú pháp cho câu đã parse thành công.
        

**Ý nghĩa:**

*   Earley Parser linh hoạt, phù hợp với:
    
    *   Câu không cố định độ dài.
        
    *   Văn phạm phức tạp, nhiều dạng câu (câu hỏi, câu nhờ vả, câu mệnh lệnh, có thời gian, có tùy chọn món…).
        

### 4.4. Tác vụ phân tích câu (`parser.py`)

**Hàm chính**: `run\_parser\_task()`

**Chức năng:**

1.  Đọc danh sách câu từ: 
```
input/sentences.txt
```
    
4.  Tiền xử lý & tokenization.
    
5.  Với mỗi câu:
    
    *   Gọi `EarleyParser.parse(tokens)`.
        
    *   Nếu parse thành công thì dựng cây cú pháp.
        
    *   Nếu thất bại thì ghi `()` để biểu diễn “không phân tích được” theo yêu cầu đề bài.
        
6.  Ghi kết quả vào:
```
2311402/output/parse-results.txt
```

**Dạng kết quả:**

*   Mỗi dòng tương ứng với một câu trong `sentences.txt`.
    
```
(Sentences (Sentence (BasicSentence (Subject (Pronoun 'tôi')) (Predicate (VerbPhrase (VerbStructure (ModalVerb 'muốn') (VerbCore (Verb (OrderVerb 'đặt'))) (NounPhrase (FoodPhrase (FoodCore (Quantifier (_NUMBER_ '2')) (Unit (_DON_VI_ 'phần')) (FoodName (_MON_AN_MAN_ 'phở' 'bò'))))))))) (DeliveryTimePhrase 'giao' 'lúc' (TimeExpression (_NUMBER_ '12') 'giờ'))))
```

Hoặc nếu không parse được:
`   ()   `

## 5. Quy trình chạy chương trình (sử dụng `util.sh`)

Hệ thống có **2 task hoàn toàn độc lập** trong Phần I:

1. **Task 1 – Sinh câu từ CFG**: tạo ra các câu ví dụ đúng grammar, lưu vào `samples.txt`.
2. **Task 2 – Phân tích cú pháp câu đầu vào**: đọc các câu sẵn có trong `input/sentences.txt`, phân tích bằng Earley Parser và lưu parse tree vào `parse-results.txt`.

Cả hai task đều được điều khiển bằng script **`util.sh`** ở thư mục gốc.

**Lưu ý:** Tất cả lệnh dưới đây đều chạy ở **thư mục gốc của project**, nơi chứa:

> - `python/`
> - `input/`
> - `2311402/`
> - `util.sh`
> - `README.md`

**Yêu cầu**:

* Hệ điều hành: `Linux/Ubuntu` hoặc `MacOS`.

* Đã cài đặt `Python 3.8+`.

* Đứng tại thư mục gốc (ngang hàng với python/, input/, util.sh).

**Cấp quyền thực thi (chạy 1 lần đầu):**
```bash
chmod +x util.sh
```
**Cách chạy**
```bash
./util.sh generate
```

**Tóm tắt quy trình:**

1.  Tạo thư mục output: `2311402/output/` (nếu chưa tồn tại).
    
2.  `cd` vào thư mục `python/`.

3. Build Docker image:
```bash
docker build -t nlp\_assignment .
```
4. Chạy container để gọi các lệnh đi thực thi yêu cầu đề bài:
```bash
python3 -m hcmut.iaslab.nlp.app.main generate
```
```bash
python3 -m hcmut.iaslab.nlp.app.main parse
```
với:
* `2311402/output` được mount vào **/src/output**.
        
* **input** được mount vào `/src/input`.
        
### 5.1. Task 2.2 – Sinh câu từ CFG (Generator)

**Mục tiêu:**  
Sinh tự động các câu tiếng Việt **đúng theo CFG** để mô phỏng câu của khách đặt món, và ghi vào:

```text
2311402/output/samples.txt
```
**Cách chạy:**

```bash
./util.sh generate
```

**Tóm tắt quy trình bên trong `run_generate`:**

1.  Tạo thư mục output: `2311402/output/` (nếu chưa tồn tại).
    
2.  `cd` vào thư mục `python/`.
    
3. Build Docker image:
```bash
docker build -t nlp\_assignment .
````
    
4.  Chạy container để gọi tác vụ sinh câu:
``` bash
docker run --rm \
	-v "$S\_OUT":/src/output \
	-v "$S\_IN":/src/input \
	nlp\_assignment python3 -m hcmut.iaslab.nlp.app.main generate
```
với:
    
    *   2311402/output được mount vào /src/output.
        
    *   input được mount vào /src/input.
        

**Kết quả:**
* File sinh câu nằm tại:
```text
2311402/output/samples.txt
```

### 5.2. Task 2.3 – Phân tích cú pháp các câu đầu vào (Parser)

**Mục tiêu:**
Đọc **các câu đã chuẩn bị sẵn** trong: `input/sentences.txt   `

Sau đó phân tích cú pháp từng câu bằng **Earley Parser**, rồi ghi kết quả parse tree vào:`   2311402/output/parse-results.txt   `

**Cách chạy:**
```bash
./util.sh parse
```

**Tóm tắt quy trình:**

1.  Tạo thư mục output: `2311402/output/`.
    
2.  cd vào python/.
    
3.  docker build -t nlp\_assignment .
    
4.  Chạy container:
```bash
docker run --rm \
    -v "$S_OUT":/src/output \
    -v "$S_IN":/src/input \
    nlp_assignment
```
            
5.  Bên trong container:
    
    *   Chương trình đọc `input/sentences.txt`.
        
    *   Parse từng câu bằng **EarleyParser**.
        
    *   Ghi kết quả vào:
```text
2311402/output/parse-results.txt
```
        

### 5.3. Tạo file .zip nộp hoàn chỉnh – submit

**Dùng lệnh**
```   bash 
./util.sh submit   
```

để:

1.  Gọi **Task 2.2**: `run\_generate`.
    
2.  Gọi **Task 2.3**: `run\_test`.
    
3.  Copy `python/hcmut/iaslab/nlp/data/grammar.txt` vào `2311402/output/`.
    
4.  Đóng gói toàn bộ thành:
    
`   2311402.zip   `

bao gồm:

> - `python/`
> - `input/`
> - `2311402/output/`
> - `util.sh`
> - `README.md`
    

Đây là **file nộp chính thức** cho bài tập lớn.

## 6. Đánh giá, Hạn chế & Hướng phát triển
### 6.1. Ưu điểm

*   Xây dựng được **một grammar rõ ràng**, tách bạch:
    
    *   Cấu trúc câu (Subject, Predicate, VerbPhrase, NounPhrase…).
        
    *   Từ vựng linh hoạt (`Food`, `Drink`, `FoodOption`, `DrinkOption`, `Unit`, `Restaurant`,…).
        
*   Cài đặt thành công:
    
    *   **CFG Generator** với hai chiến lược sinh câu.
        
    *   **Earley Parser** tự viết, có khả năng xử lý grammar mơ hồ.
        
*   Tổ chức mã nguồn:
    
    *   Tách thành nhiều module: `grammar.py`, `earley\_parser.py`, `generator.py`, `parser.py`, `utils.py`.
        
    *   Dễ bảo trì, dễ mở rộng.
        

### 6.2. Hạn chế

*   Grammar vẫn còn mang tính **mô phỏng**, chưa bao phủ hết:
    
    *   Cách nói “chat” rất tự nhiên của người dùng.
        
    *   Các câu rút gọn, câu sai chính tả, viết tắt…
        
*   Earley Parser xử lý được nhưng:
    
    *   **Thời gian chạy** có thể tăng nếu grammar mở rộng quá nhiều và câu quá dài.
        
*   Chưa tích hợp:
    
    *   Bước **ngữ nghĩa (semantic)** để trích xuất trực tiếp intent, slot (món, số lượng, thời gian…) từ cây cú pháp.
        
## 7. Kết luận
Trong phạm vi BTL Phần I, hệ thống đã:

1.  Xây dựng được **văn phạm phi ngữ cảnh** mô tả bài toán đặt món ăn/đồ uống trực tuyến.
    
2.  Cài đặt **Sentence Generator** sinh được số lượng lớn câu đúng grammar.
    
3.  Cài đặt thành công **Earley Parser**, phân tích cú pháp các câu đầu vào từ file `input/sentences.txt` và ghi kết quả ra `parse-results.txt`.