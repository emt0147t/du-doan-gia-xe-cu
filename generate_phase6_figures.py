"""Tạo các biểu đồ phân tích sai số và tầm quan trọng đặc trưng (Error Analysis & Interpretability Plots).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer
"""

from __future__ import annotations

import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

FIGURES_DIR = Path("reports/figures/phase6")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Cấu hình phong cách đồ thị học thuật
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.unicode_minus"] = False


def main():
    print("Bắt đầu tạo các biểu đồ phân tích sai số Phase 6...")

    val_df = pd.read_csv("data/processed/splits/val.csv")
    preds_df = pd.read_csv("reports/model_experiments/validation_predictions.csv")

    champion_col = "Tree_RandomForest_Tuned_LogTarget"
    if champion_col not in preds_df.columns:
        print(f"Lỗi: Không tìm thấy cột {champion_col} trong validation_predictions.csv")
        sys.exit(1)

    y_true = preds_df["actual_price_vnd"].values
    y_pred = preds_df[champion_col].values
    residual = y_true - y_pred

    # Đơn vị tỷ VND để trực quan hóa đẹp và dễ đọc
    y_true_b = y_true / 1e9
    y_pred_b = y_pred / 1e9
    residual_b = residual / 1e9

    # 1. Actual vs Predicted Plot
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.scatter(y_true_b, y_pred_b, alpha=0.3, color="#1f77b4", edgecolor="none", s=25)
    max_val = max(y_true_b.max(), y_pred_b.max()) * 1.05
    ax.plot([0, max_val], [0, max_val], "r--", linewidth=1.5, label="Đường dự đoán hoàn hảo (y = x)")
    ax.set_title("Thực tế vs Dự đoán — Random Forest Tuned (Tập Validation)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Giá thực tế (Tỷ VND)", fontsize=11)
    ax.set_ylabel("Giá dự đoán (Tỷ VND)", fontsize=11)
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.legend(frameon=True)
    plt.tight_layout()
    fig_path1 = FIGURES_DIR / "actual_vs_predicted.png"
    plt.savefig(fig_path1, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path1}")

    # 2. Residual Distribution Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    # Cắt lọc các ngoại lai quá xa để hiển thị phân phối trung tâm
    res_bounded = residual_b[(residual_b >= -1.0) & (residual_b <= 1.0)]
    sns.histplot(res_bounded, kde=True, bins=50, color="#2ca02c", ax=ax)
    ax.axvline(0, color="red", linestyle="--", linewidth=1.2, label="Phần dư = 0")
    ax.set_title("Phân phối phần dư (Residual Distribution: [-1 Tỷ, +1 Tỷ])", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Phần dư (Thực tế - Dự đoán, Tỷ VND)", fontsize=11)
    ax.set_ylabel("Số lượng mẫu (Mật độ)", fontsize=11)
    ax.legend(frameon=True)
    plt.tight_layout()
    fig_path2 = FIGURES_DIR / "residual_distribution.png"
    plt.savefig(fig_path2, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path2}")

    # 3. Residual vs Predicted Plot (Heteroscedasticity Analysis)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_pred_b, residual_b, alpha=0.35, color="#ff7f0e", edgecolor="none", s=25)
    ax.axhline(0, color="red", linestyle="--", linewidth=1.2)
    ax.set_title("Phần dư vs Giá dự đoán (Heteroscedasticity Check)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Giá dự đoán (Tỷ VND)", fontsize=11)
    ax.set_ylabel("Phần dư (Thực tế - Dự đoán, Tỷ VND)", fontsize=11)
    plt.tight_layout()
    fig_path3 = FIGURES_DIR / "residual_vs_predicted.png"
    plt.savefig(fig_path3, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path3}")

    # 4. Error by Manufacturing Year
    eval_df = val_df.copy()
    eval_df["y_true"] = y_true
    eval_df["y_pred"] = y_pred
    eval_df["abs_error_m"] = np.abs(y_true - y_pred) / 1e6
    eval_df["pct_error"] = np.abs(y_true - y_pred) / y_true * 100.0

    year_stats = eval_df.groupby("year")["abs_error_m"].agg(["mean", "median", "count"]).reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    bar_width = 0.35
    x = np.arange(len(year_stats))
    ax.bar(x - bar_width/2, year_stats["mean"], bar_width, label="MAE Trung bình (Triệu VND)", color="#4c72b0")
    ax.bar(x + bar_width/2, year_stats["median"], bar_width, label="MAE Trung vị (Triệu VND)", color="#55a868")
    ax.set_xticks(x)
    ax.set_xticklabels(year_stats["year"].astype(int))
    ax.set_title("Sai số dự đoán theo Năm sản xuất (2015 - 2023)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Năm sản xuất", fontsize=11)
    ax.set_ylabel("Sai số tuyệt đối (Triệu VND)", fontsize=11)
    ax.legend(frameon=True)
    plt.tight_layout()
    fig_path4 = FIGURES_DIR / "error_by_year.png"
    plt.savefig(fig_path4, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path4}")

    # 5. Error by Price Segment
    bins = [0, 500e6, 1e9, 2e9, 50e9]
    labels = ["Dưới 500M", "500M - 1 Tỷ", "1 Tỷ - 2 Tỷ", "Trên 2 Tỷ"]
    eval_df["price_segment"] = pd.cut(eval_df["y_true"], bins=bins, labels=labels)

    seg_stats = eval_df.groupby("price_segment")["pct_error"].agg(["mean", "median", "count"]).reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=seg_stats, x="price_segment", y="median", palette="Blues_d", ax=ax)
    ax.set_title("Sai số tỷ đối trung vị (MdAPE %) theo Phân khúc giá", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Phân khúc giá thực tế", fontsize=11)
    ax.set_ylabel("MdAPE (%)", fontsize=11)
    for i, row in seg_stats.iterrows():
        ax.text(i, row["median"] + 0.15, f"{row['median']:.1f}% (n={row['count']})", ha="center", fontsize=10, fontweight="bold")
    plt.tight_layout()
    fig_path5 = FIGURES_DIR / "error_by_price_segment.png"
    plt.savefig(fig_path5, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path5}")

    # 6. Error by Top 6 Brands
    top_brands = eval_df["brand"].value_counts().head(6).index.tolist()
    brand_df = eval_df[eval_df["brand"].isin(top_brands)]
    brand_stats = brand_df.groupby("brand")["abs_error_m"].agg(["mean", "median", "count"]).reindex(top_brands).reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(brand_stats))
    ax.bar(x - bar_width/2, brand_stats["mean"], bar_width, label="MAE Trung bình (Triệu VND)", color="#c44e52")
    ax.bar(x + bar_width/2, brand_stats["median"], bar_width, label="MAE Trung vị (Triệu VND)", color="#8172b3")
    ax.set_xticks(x)
    ax.set_xticklabels(brand_stats["brand"], rotation=15)
    ax.set_title("Sai số dự đoán theo Top 6 Thương hiệu xe phổ biến nhất", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Hãng xe", fontsize=11)
    ax.set_ylabel("Sai số tuyệt đối (Triệu VND)", fontsize=11)
    ax.legend(frameon=True)
    plt.tight_layout()
    fig_path6 = FIGURES_DIR / "error_by_brand.png"
    plt.savefig(fig_path6, dpi=300)
    plt.close()
    print(f"  Đã lưu: {fig_path6}")

    print("Hoàn tất tạo toàn bộ biểu đồ phân tích sai số Phase 6!")


if __name__ == "__main__":
    main()
