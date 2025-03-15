# Bài tập lớn Kho dữ Liệu và Hệ hỗ trợ Quyết định (CO4031)

## 1. Yêu cầu:
- Chủ đề: tự chọn.
- Input: tập dữ liệu từ nhiều nguồn.
- Trả lời câu hỏi: Tại sao? Giải quyết vấn đề gì?
- Yêu cầu: hệ thống chạy bằng các công cụ Data Warehouse.
- Output: Kết quả + Visualization (BI).
- Tuần báo cáo: 4 hoặc 5 tuần cuối (mỗi buổi 2-3 nhóm).
- Tuần submit: tất cả các nhóm, tuần học thứ 10 (trước tuần báo cáo 1 tuần, deadline: 06/04/2025).

## 2. Nội dung Bài Tập Lớn:
- **Chủ đề**: ***Phân tích dữ liệu tai nạn giao thông***
  - Hệ thống Data Warehouse này sẽ lưu trữ, tổng hợp và phân tích dữ liệu về tai nạn giao thông, từ đó giúp xác định các yếu tố nguy cơ gây ra tai nạn, hỗ trợ đưa ra các giải pháp cải thiện tình trạng tai nạn giao thông.
- **Dữ liệu đầu vào**: 
  - Nguồn dữ liệu: [Traffic Accidents Dataset](https://www.kaggle.com/datasets/oktayrdeki/traffic-accidents)
  - Mô tả dữ liệu: Bộ dữ liệu này chứa thông tin chi tiết về các vụ tai nạn giao thông ở nhiều khu vực và thời gian khác nhau; bao gồm các số liệu về thời gian, điều kiện thời tiết, điều kiện ánh sáng, loại va chạm, hậu quả,... của vụ tai nạn.
- **Tại sao lại cần Hệ thống Data Warehouse này?**
  - Hiện nay, tai nạn giao thông là một vấn đề nghiêm trọng, gây thiệt hại nghiêm trọng về người và tài sản *(1,3 triệu người chết, 50 triệu người bị thương mỗi năm - Số liệu năm 2024)*. Việc phân tích dữ liệu có được từ hệ thống này giúp phát hiện nguyên nhân, dự báo nguy cơ và tối ưu hóa công tác phòng tránh tai nạn dựa trên các yếu tố được xem xét có thể gây ra tai nạn.
- **Dữ liệu từ Hệ thống Data Warehouse này giải quyết vấn đề gì?** <br>
  - Điều chỉnh thời gian tuần tra giao thông, lắp đặt đèn tín hiệu phù hợp, cảnh báo theo thời tiết và theo mùa dựa trên việc phân tích dữ liệu về thời gian xảy ra tai nạn.
  - Xác định các điểm đen giao thông để cải thiện cơ sở hạ tầng, xây dựng kế hoạch quy hoạch phù hợp, bổ sung các biển báo phù hợp dựa trên việc phân tích dữ liệu về vị trí xảy ra tai nạn.
  - Xây dựng các điều luật khi tham gia giao thông phù hợp với tình hình thực tế dựa trên việc phân tích dữ liệu về các nguyên nhân chủ quan (Tốc độ, Vi phạm,...) gây ra tai nạn.