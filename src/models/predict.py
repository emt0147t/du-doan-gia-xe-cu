"""Module suy luận và dự đoán giá xe thực tế (Model Inference & Prediction).

Dự án: Used Car Price Prediction in Vietnam
Tác giả: Senior Data Scientist & ML Engineer

Cung cấp interface nạp artifact mô hình vô địch (Champion Pipeline) để dự đoán
giá rao bán ô tô đã qua sử dụng từ thông số đầu vào của người dùng.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

# Ensure project root is in sys.path for direct execution
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.data.cleaning import LUXURY_BRANDS
from src.data.preprocessing import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from src.models.evaluate import inverse_log_transform

DEFAULT_MODEL_PATH = Path("models/champion_random_forest.joblib")


def load_champion_model(model_path: Union[str, Path, None] = None) -> Pipeline:
    """Nạp artifact mô hình vô địch đã được huấn luyện và tuần tự hóa."""
    path = Path(model_path) if model_path is not None else DEFAULT_MODEL_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy artifact mô hình tại '{path}'. "
            f"Vui lòng chạy 'python save_champion_model.py' trước khi thực hiện suy luận."
        )
    model = joblib.load(path)
    if not isinstance(model, Pipeline):
        raise TypeError(f"Artifact nạp được không phải là scikit-learn Pipeline: {type(model)}")
    return model


def format_vnd_price(price_vnd: float) -> str:
    """Định dạng số tiền VND thành chuỗi đọc tiếng Việt trực quan (Ví dụ: 1 Tỷ 250 Triệu VNĐ)."""
    if np.isnan(price_vnd) or price_vnd <= 0:
        return "N/A"

    ty = int(price_vnd // 1_000_000_000)
    trieu = int(round((price_vnd % 1_000_000_000) / 1_000_000))

    if ty > 0 and trieu > 0:
        return f"{ty} Tỷ {trieu} Triệu VNĐ ({price_vnd:,.0f} đ)"
    elif ty > 0 and trieu == 0:
        return f"{ty} Tỷ VNĐ ({price_vnd:,.0f} đ)"
    else:
        return f"{trieu} Triệu VNĐ ({price_vnd:,.0f} đ)"


def prepare_car_features(data: Union[Dict[str, Any], pd.DataFrame]) -> pd.DataFrame:
    """Chuẩn hóa dữ liệu đầu vào và tự động tạo các đặc trưng dẫn xuất nếu người dùng chưa cung cấp.

    Đặc trưng dẫn xuất tự động:
    - car_age = 2024 - year
    - is_zero_mileage = 1 nếu mileage_km == 0 ngược lại 0
    - is_luxury_brand = 1 nếu brand thuộc LUXURY_BRANDS ngược lại 0
    """
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        raise TypeError(f"Dữ liệu đầu vào phải là dict hoặc DataFrame, nhận được: {type(data)}")

    # 1. Tự động tính car_age nếu thiếu
    if "car_age" not in df.columns:
        if "year" in df.columns and not df["year"].isna().all():
            df["car_age"] = 2024.0 - df["year"].astype("float64")
        else:
            df["car_age"] = np.nan

    # 2. Tự động tính is_zero_mileage nếu thiếu
    if "is_zero_mileage" not in df.columns:
        if "mileage_km" in df.columns:
            df["is_zero_mileage"] = (df["mileage_km"] == 0).astype("float64")
        else:
            df["is_zero_mileage"] = 0.0

    # 3. Tự động tính is_luxury_brand nếu thiếu
    if "is_luxury_brand" not in df.columns:
        if "brand" in df.columns:
            luxury_lower = {b.lower() for b in LUXURY_BRANDS}
            df["is_luxury_brand"] = df["brand"].astype(str).str.lower().isin(luxury_lower).astype("float64")
        else:
            df["is_luxury_brand"] = 0.0

    # 4. Đảm bảo đầy đủ các cột numeric theo chuẩn schema
    for col in NUMERIC_FEATURES:
        if col not in df.columns:
            df[col] = np.nan
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Đảm bảo đầy đủ các cột categorical theo chuẩn schema
    for col in CATEGORICAL_FEATURES:
        if col not in df.columns:
            df[col] = np.nan
        else:
            df[col] = df[col].astype(str).replace({"nan": np.nan, "None": np.nan, "<NA>": np.nan})

    required_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    return df[required_cols]


def predict_car_price(
    data: Union[Dict[str, Any], pd.DataFrame],
    model: Union[Pipeline, None] = None,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Dự đoán giá rao bán ô tô đã qua sử dụng từ thông số đầu vào.

    Args:
        data: Dict chứa thông số của 1 xe hoặc DataFrame chứa nhiều xe.
        model: Pipeline đã huấn luyện (nếu None sẽ tự nạp Champion Model).

    Returns:
        Dict hoặc List các Dict chứa:
        - 'predicted_price_vnd': float (giá dự đoán theo đồng)
        - 'formatted_price': str (giá đọc tiếng Việt)
        - 'features_used': dict (thông số trích xuất đã đưa vào pipeline)
    """
    if model is None:
        model = load_champion_model()

    is_single_dict = isinstance(data, dict)
    X = prepare_car_features(data)

    # Dự đoán trên không gian Log
    pred_log = model.predict(X)

    # Nghịch đảo logarit về thang đo thực tế VND
    pred_vnd = inverse_log_transform(pred_log)

    results = []
    for i in range(len(pred_vnd)):
        price_val = float(pred_vnd[i])
        res = {
            "predicted_price_vnd": price_val,
            "formatted_price": format_vnd_price(price_val),
            "features_used": X.iloc[i].to_dict(),
        }
        results.append(res)

    return results[0] if is_single_dict else results


def build_arg_parser() -> argparse.ArgumentParser:
    """Tạo bộ parser tham số dòng lệnh CLI."""
    parser = argparse.ArgumentParser(
        description="Dự đoán giá ô tô đã qua sử dụng tại Việt Nam bằng Champion Model (Random Forest)."
    )
    parser.add_argument("--brand", type=str, default="Toyota", help="Hãng xe (VD: Toyota, Mazda, Mercedes-Benz)")
    parser.add_argument("--model", type=str, default="Vios", help="Dòng xe (VD: Vios, CX-5, C200)")
    parser.add_argument("--year", type=int, default=2020, help="Năm sản xuất (VD: 2020)")
    parser.add_argument("--mileage", type=float, default=45000.0, help="Số km đã đi (VD: 45000)")
    parser.add_argument("--transmission", type=str, default="Tự động", choices=["Tự động", "Số tay"], help="Hộp số")
    parser.add_argument("--engine", type=float, default=1.5, help="Dung tích động cơ lít (VD: 1.5, 2.0)")
    parser.add_argument("--fuel", type=str, default="Xăng", choices=["Xăng", "Dầu", "Hybrid", "Điện"], help="Nhiên liệu")
    parser.add_argument("--origin", type=str, default="Trong nước", choices=["Trong nước", "Nhập khẩu"], help="Xuất xứ")
    parser.add_argument("--body", type=str, default="Sedan", help="Kiểu dáng (VD: Sedan, SUV, Crossover, Bán tải / Pickup)")
    parser.add_argument("--condition", type=str, default="Xe đã dùng", choices=["Xe đã dùng", "Xe mới"], help="Tình trạng")
    parser.add_argument("--seats", type=float, default=5.0, help="Số chỗ ngồi (VD: 5, 7)")
    parser.add_argument("--doors", type=float, default=4.0, help="Số cửa (VD: 4, 5)")
    parser.add_argument("--demo", action="store_true", help="Chạy kịch bản minh họa dự đoán mẫu")
    return parser


def run_demo():
    """Chạy kịch bản minh họa dự đoán trên 3 mẫu xe phổ biến tại thị trường Việt Nam."""
    print("=" * 70)
    print("CHẠY DEMO DỰ ĐOÁN GIÁ XE VỚI CHAMPION RANDOM FOREST PIPELINE")
    print("=" * 70)

    model = load_champion_model()

    sample_cars = [
        {
            "brand": "Toyota",
            "model": "Vios",
            "year": 2020,
            "mileage_km": 45000,
            "transmission": "Tự động",
            "engine_displacement_l": 1.5,
            "fuel_type": "Xăng",
            "origin": "Trong nước",
            "body_type": "Sedan",
            "condition": "Xe đã dùng",
            "seats": 5.0,
            "doors": 4.0,
            "description": "Xe sedan phân khúc B phổ thông 4 năm tuổi"
        },
        {
            "brand": "Mazda",
            "model": "CX-5",
            "year": 2022,
            "mileage_km": 20000,
            "transmission": "Tự động",
            "engine_displacement_l": 2.0,
            "fuel_type": "Xăng",
            "origin": "Trong nước",
            "body_type": "SUV",
            "condition": "Xe đã dùng",
            "seats": 5.0,
            "doors": 5.0,
            "description": "Xe Crossover đô thị tầm trung lướt 2 năm tuổi"
        },
        {
            "brand": "Mercedes-Benz",
            "model": "C200",
            "year": 2021,
            "mileage_km": 35000,
            "transmission": "Tự động",
            "engine_displacement_l": 1.5,
            "fuel_type": "Xăng",
            "origin": "Trong nước",
            "body_type": "Sedan",
            "condition": "Xe đã dùng",
            "seats": 5.0,
            "doors": 4.0,
            "description": "Xe hạng sang Đức lướt 3 năm tuổi"
        },
    ]

    for car in sample_cars:
        desc = car.pop("description")
        result = predict_car_price(car, model=model)
        print(f"\n[Xe]: {car['brand']} {car['model']} ({car['year']}) - ODO: {car['mileage_km']:,} km")
        print(f"  Mô tả tình huống: {desc}")
        print(f"  Hộp số: {car['transmission']} | Động cơ: {car['engine_displacement_l']}L | Xuất xứ: {car['origin']}")
        print(f"  ==> GIÁ RAO BÁN DỰ ĐOÁN: {result['formatted_price']}")
    print("\n" + "=" * 70)


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    parser = build_arg_parser()
    args = parser.parse_args()

    if args.demo or len(sys.argv) == 1:
        run_demo()
        return

    car_input = {
        "brand": args.brand,
        "model": args.model,
        "year": args.year,
        "mileage_km": args.mileage,
        "transmission": args.transmission,
        "engine_displacement_l": args.engine,
        "fuel_type": args.fuel,
        "origin": args.origin,
        "body_type": args.body,
        "condition": args.condition,
        "seats": args.seats,
        "doors": args.doors,
    }

    result = predict_car_price(car_input)
    print("\n" + "=" * 60)
    print("KẾT QUẢ DỰ ĐOÁN GIÁ Ô TÔ ĐÃ QUA SỬ DỤNG")
    print("=" * 60)
    print(f"Hãng & Dòng xe: {args.brand} {args.model} ({args.year})")
    print(f"Số km đã đi:   {args.mileage:,.0f} km")
    print(f"Động cơ:        {args.engine} L ({args.fuel})")
    print(f"Hộp số:         {args.transmission} | Xuất xứ: {args.origin}")
    print(f"Kiểu dáng:      {args.body} ({int(args.seats)} chỗ)")
    print("-" * 60)
    print(f"DỰ BÁO GIÁ RAO BÁN: {result['formatted_price']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
