"""Kết xuất biểu đồ đối chiếu và phân tích sai số Phase 6.2 (Task F).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & Independent ML Evaluation Reviewer
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

FIGURES_DIR = Path("reports/figures/phase6_2")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("Bắt đầu kết xuất biểu đồ và phân tích đối chiếu Phase 6 vs Phase 6.2...")
    
    # Đọc kết quả test Phase 6 cũ và Phase 6.2 mới
    p6_preds = pd.read_csv("reports/model_experiments/final_test_predictions.csv")
    p6_test = pd.read_csv("data/processed/splits/test.csv")
    
    p62_preds = pd.read_csv("reports/model_experiments/phase6_2_grouped/test_predictions.csv")
    p62_test = pd.read_csv("data/processed/splits_grouped_v1/test.csv")
    
    # 1. Tính sai số cho cả hai
    p6_err = np.abs(p6_preds["actual_price_vnd"] - p6_preds["Tree_RandomForest_Tuned_LogTarget (CHAMPION)"])
    p6_ape = p6_err / p6_preds["actual_price_vnd"] * 100
    p6_preds["abs_error"] = p6_err
    p6_preds["ape"] = p6_ape
    p6_preds["brand"] = p6_test["brand"]
    p6_preds["year"] = p6_test["year"]
    
    p62_err = np.abs(p62_preds["actual_price_vnd"] - p62_preds["Tree_RandomForest_Tuned_LogTarget"])
    p62_ape = p62_err / p62_preds["actual_price_vnd"] * 100
    p62_preds["abs_error"] = p62_err
    p62_preds["ape"] = p62_ape
    p62_preds["brand"] = p62_test["brand"]
    p62_preds["year"] = p62_test["year"]
    
    # Phân khúc giá
    bins = [0, 500_000_000, 1_000_000_000, 2_000_000_000, 5_000_000_000, float("inf")]
    labels = ["<500M", "500M-1B", "1B-2B", "2B-5B", ">5B"]
    p6_preds["price_bin"] = pd.cut(p6_preds["actual_price_vnd"], bins=bins, labels=labels)
    p62_preds["price_bin"] = pd.cut(p62_preds["actual_price_vnd"], bins=bins, labels=labels)
    
    p6_seg = p6_preds.groupby("price_bin", observed=True).agg(
        count=("abs_error", "count"),
        mae=("abs_error", "mean"),
        mdape=("ape", "median")
    )
    p62_seg = p62_preds.groupby("price_bin", observed=True).agg(
        count=("abs_error", "count"),
        mae=("abs_error", "mean"),
        mdape=("ape", "median")
    )
    
    print("\n--- ĐỐI CHIẾU SAI SỐ THEO PHÂN KHÚC GIÁ ---")
    seg_cmp = pd.DataFrame({
        "P6_Count": p6_seg["count"],
        "P6_MAE_M": p6_seg["mae"] / 1e6,
        "P6_MdAPE": p6_seg["mdape"],
        "P62_Count": p62_seg["count"],
        "P62_MAE_M": p62_seg["mae"] / 1e6,
        "P62_MdAPE": p62_seg["mdape"],
    })
    print(seg_cmp.to_string())
    
    # 2. Vẽ biểu đồ 1: So sánh Actual vs Predicted trên Group-Aware Test
    fig, ax = plt.subplots(figsize=(8, 7))
    act = p62_preds["actual_price_vnd"] / 1e9
    pred = p62_preds["Tree_RandomForest_Tuned_LogTarget"] / 1e9
    ax.scatter(act, pred, alpha=0.35, edgecolors="none", color="#1f77b4", s=25)
    max_val = max(act.max(), pred.max())
    ax.plot([0, max_val], [0, max_val], "r--", linewidth=1.5, label="Đường chuẩn lý tưởng (y = x)")
    ax.set_title("Group-Aware Test Set: Giá Thực Tế vs Giá Dự Đoán (Phase 6.2)", fontsize=12, fontweight="bold")
    ax.set_xlabel("Giá rao bán thực tế (Tỷ VNĐ)", fontsize=10)
    ax.set_ylabel("Giá dự đoán mô hình (Tỷ VNĐ)", fontsize=10)
    ax.legend()
    plt.tight_layout()
    fig1_path = FIGURES_DIR / "group_aware_actual_vs_predicted.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"Đã lưu: {fig1_path}")
    
    # 3. Vẽ biểu đồ 2: So sánh MAE và MdAPE giữa Phase 6 (Random) và Phase 6.2 (Group-Aware)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Barplot MAE by segment
    seg_df_mae = pd.DataFrame({
        "Phân khúc": list(seg_cmp.index) * 2,
        "MAE (Triệu VNĐ)": list(seg_cmp["P6_MAE_M"]) + list(seg_cmp["P62_MAE_M"]),
        "Quy trình": ["Phase 6 (Random Split)"] * len(seg_cmp) + ["Phase 6.2 (Group-Aware Split)"] * len(seg_cmp)
    })
    sns.barplot(data=seg_df_mae, x="Phân khúc", y="MAE (Triệu VNĐ)", hue="Quy trình", ax=axes[0], palette="Set2")
    axes[0].set_title("So sánh MAE theo phân khúc giá (Phase 6 vs Phase 6.2)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("MAE (Triệu VNĐ)")
    
    # Barplot MdAPE by segment
    seg_df_mdape = pd.DataFrame({
        "Phân khúc": list(seg_cmp.index) * 2,
        "MdAPE (%)": list(seg_cmp["P6_MdAPE"]) + list(seg_cmp["P62_MdAPE"]),
        "Quy trình": ["Phase 6 (Random Split)"] * len(seg_cmp) + ["Phase 6.2 (Group-Aware Split)"] * len(seg_cmp)
    })
    sns.barplot(data=seg_df_mdape, x="Phân khúc", y="MdAPE (%)", hue="Quy trình", ax=axes[1], palette="Set1")
    axes[1].set_title("So sánh MdAPE theo phân khúc giá (Phase 6 vs Phase 6.2)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("MdAPE (%)")
    
    plt.tight_layout()
    fig2_path = FIGURES_DIR / "phase6_vs_phase6_2_comparison.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"Đã lưu: {fig2_path}")


if __name__ == "__main__":
    main()
