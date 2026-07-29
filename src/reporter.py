from __future__ import annotations

from pathlib import Path

from field_metadata import display_name
from price_units import display_unit_label, source_unit_label


def build_report(
    dataset_name: str,
    model_type: str,
    row_count: int,
    feature_count: int,
    target_column: str,
    feature_columns: list[str],
    field_descriptions: dict,
    metrics: dict,
    unit_config: dict,
    model_size_mb: float,
    best_model: str | None,
    report_path: Path,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    target_label = display_name(target_column, field_descriptions)
    source_unit = source_unit_label(unit_config)
    display_unit = display_unit_label(unit_config)
    exchange_rate = unit_config.get("usd_to_rmb", 6.6)
    best_model_line = best_model or model_type

    feature_rows = "\n".join(
        (
            "<tr>"
            f"<td>{display_name(column, field_descriptions)}</td>"
            f"<td>{field_descriptions.get(column, {}).get('description_zh', '')}</td>"
            f"<td>{field_descriptions.get(column, {}).get('description_en', '')}</td>"
            "</tr>"
        )
        for column in feature_columns
    )

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>SmartHouse Regression Report</title>
  <style>
    body {{ font-family: Arial, "Microsoft YaHei", sans-serif; margin: 40px; line-height: 1.6; color: #1f2933; }}
    h1, h2 {{ color: #17324d; }}
    .metric {{ display: inline-block; min-width: 170px; margin: 8px 12px 8px 0; padding: 12px; border: 1px solid #d9e2ec; border-radius: 6px; }}
    .value {{ font-size: 24px; font-weight: 700; color: #2f6f73; }}
    code {{ background: #f3f4f6; padding: 2px 4px; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 12px; }}
    th, td {{ border: 1px solid #d9e2ec; padding: 8px 10px; text-align: left; vertical-align: top; }}
    th {{ background: #f3f7f7; }}
  </style>
</head>
<body>
  <h1>SmartHouse Regression Report / 智能房价回归报告</h1>
  <p>Dataset / 数据集：<strong>{dataset_name}</strong></p>
  <p>Model / 当前模型：<strong>{model_type}</strong></p>
  <p>Best Model / 比较后推荐模型：<strong>{best_model_line}</strong></p>
  <p>Target / 预测目标：<code>{target_label}</code></p>
  <p>Rows / 样本数：{row_count}，Features / 特征数：{feature_count}</p>
  <p>Source Unit / 原始单位：<strong>{source_unit}</strong></p>
  <p>Display Unit / 展示单位：<strong>{display_unit}</strong></p>
  <p>Exchange Rate Statement / 汇率声明：展示换算按固定假设 <strong>1 USD = {exchange_rate} RMB</strong>，仅用于作品展示，不代表实时汇率。</p>
  <p>Model File Size / 模型文件大小：<strong>{model_size_mb:.2f} MB</strong></p>

  <h2>Metrics / 评价指标</h2>
  <div class="metric"><div>平均绝对误差 / MAE</div><div class="value">{metrics["mae"]:.4f}</div></div>
  <div class="metric"><div>均方根误差 / RMSE</div><div class="value">{metrics["rmse"]:.4f}</div></div>
  <div class="metric"><div>解释能力 / R2</div><div class="value">{metrics["r2"]:.4f}</div></div>

  <h2>How To Read / 怎么看</h2>
  <p>MAE 表示平均预测误差；RMSE 会更重地惩罚大误差；R2 越接近 1，表示模型解释房价变化的能力越强。</p>
  <p>MAE is average prediction error. RMSE penalizes large errors more strongly. R2 closer to 1 means the model explains more price variation.</p>
  <p>California Housing 的原始目标单位是十万美元。为了让中文读者更直观，本项目同时按固定汇率换算为万元人民币展示。</p>
  <p>The original California Housing target unit is 100,000 USD. For Chinese readers, this project also displays converted values in 10,000 RMB using a fixed exchange rate.</p>

  <h2>Field Dictionary / 字段说明</h2>
  <table>
    <tr><th>字段 / Field</th><th>中文说明</th><th>English Description</th></tr>
    {feature_rows}
  </table>
</body>
</html>
"""
    report_path.write_text(html, encoding="utf-8")
