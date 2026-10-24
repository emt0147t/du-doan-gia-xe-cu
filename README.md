# Used Car Price Prediction in Vietnam
## Xây Dựng Hệ Thống Machine Learning Định Giá Ô Tô Đã Qua Sử Dụng Toàn Diện & Đánh Giá Độ Bền Khoa Học


---

1. Tổng Quan Bài Toán 

Used Car Price Prediction in Vietnam giải quyết bài toán định lượng hóa và dự báo giá chào bán ô tô đã qua sử dụng trên thị trường thứ cấp tại Việt Nam từ 15 đặc trưng kỹ thuật, vận hành và phân khúc thị trường.

2. Cấu Trúc Repository 

Repository được tinh gọn tối đa để người chấm dễ dàng theo dõi toàn bộ logic trong một notebook duy nhất và đối chiếu số liệu kiểm toán:

```text
├── README.md                                
├── requirements.txt                        
├── notebooks/
│   └── used_car_price_prediction.ipynb     
├── data/
│   ├── DATA_README.md                       
│   └── dataset_manifest.json              
├── reports/
│   └── model_comparison.csv                
└── .gitignore                              
```



3. Kết Quả Thực Nghiệm & So Sánh Mô Hình (Model Comparison)

Tất cả kết quả thực nghiệm được tổng hợp chuẩn xác tại [`reports/model_comparison.csv`](reports/model_comparison.csv):

3.1. Bảng xếp hạng Validation (Phase 6 — Random Split, 2,351 dòng Val)

| Hạng | Tên cấu hình mô hình | Không gian Target | Val MAE (VND) | Val RMSE (VND) | Val $R^2$ | Val MdAPE (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `Tree_RandomForest_Tuned_LogTarget` (CHAMPION) | log | 142,934,537 | 950,065,306 | 0.8694 | 4.25% |
| 2 | `Tree_RandomForest_LogTarget` (Default) | log | 159,102,971 | 1,043,403,506 | 0.8425 | 4.94% |
| 3 | `Tree_RandomForest_RawTarget` | raw | 168,751,598 | 852,439,763 | 0.8949 | 6.61% |
| 4 | `Tree_HistGBM_LogTarget` | log | 180,831,847 | 1,208,263,095 | 0.7888 | 5.37% |
| 5 | `Tree_HistGBM_RawTarget` | raw | 201,925,471 | 1,051,262,546 | 0.8401 | 7.84% |
| 6 | `Linear_Ridge_LogTarget` | log | 255,658,033 | 1,441,060,500 | 0.6996 | 7.72% |
| 7 | `Linear_Lasso_LogTarget` | log | 370,691,840 | 1,772,436,353 | 0.5455 | 12.22% |
| 8 | `Linear_Ridge_RawTarget` | raw | 379,429,332 | 1,153,551,727 | 0.8075 | 23.72% |
| 9 | `Baseline_Dummy_Median` | raw | 914,616,759 | 2,721,373,088 | -0.0714 | 39.83% |
| 10 | `Baseline_Dummy_Mean` | raw | 1,164,209,470 | 2,629,312,836 | -0.0001 | 94.34% |

3.2. Đánh giá một lần trên tập Test (Phase 6 Random Test vs Phase 6.2 Group-Aware Test)

| Tập kiểm thử | Tên mô hình | Rò rỉ tin trùng | Test MAE (VND) | Test RMSE (VND) | Test $R^2$ | Test MdAPE (%) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Phase 6 Random Test (2,351 xe) | `Tree_RandomForest_Tuned_LogTarget` | $9.15\%$ | 111,793,581 | 482,625,123 | 0.9448 | 4.29% |
| Phase 6.2 Group-Aware Test (2,350 xe) | `Tree_RandomForest_Tuned_LogTarget` | 0.00% | 130,761,443 | 821,395,226 | 0.8638 | 4.29% |


