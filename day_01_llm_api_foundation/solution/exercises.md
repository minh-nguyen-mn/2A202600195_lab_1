# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature = 0, phản hồi rất ổn định và mang tính xác định cao, gần như không thay đổi giữa các lần chạy. Khi tăng lên 0.5 và 1.0, câu trả lời trở nên đa dạng, chi tiết và tự nhiên hơn. Ở mức 1.5, chất lượng bắt đầu giảm, có thể xuất hiện nội dung nhiễu hoặc kém chính xác, đặc biệt với model nhỏ.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Khoảng 0.2-0.4, vì cần đảm bảo câu trả lời nhất quán, chính xác và tránh việc model tạo ra thông tin sai lệch hoặc không ổn định.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Với giá ~0.010 vs ~0.0006 mỗi 1K tokens, GPT-4o đắt hơn khoảng 16-17 lần so với GPT-4o-mini cho cùng workload.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o phù hợp cho các tác vụ cần reasoning phức tạp như phân tích tài chính, lập trình hoặc ra quyết định quan trọng. GPT-4o-mini phù hợp cho các tác vụ đơn giản, quy mô lớn như chatbot FAQ, xử lý văn bản cơ bản hoặc autocomplete, nơi chi phí và tốc độ quan trọng hơn độ chính xác tuyệt đối.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng trong các ứng dụng tương tác thời gian thực như chatbot hoặc coding assistant, vì nó giúp giảm cảm giác chờ đợi bằng cách hiển thị kết quả từng phần ngay khi được tạo ra. Điều này cải thiện trải nghiệm người dùng, đặc biệt với các phản hồi dài. Ngược lại, non-streaming phù hợp với các tác vụ backend hoặc batch processing, nơi cần toàn bộ kết quả trước khi xử lý tiếp và không yêu cầu hiển thị từng phần.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
