# Experiment Record

## Goal

补齐传统机器学习中的第二类核心任务：回归预测。

Complete the second core task in classical machine learning: regression prediction.

This experiment focuses on turning a housing-price regression problem into a reproducible project, including dataset preparation, model training, metric comparison, prediction export, and a local web interface.

本实验重点不是只训练一个模型，而是把房价回归任务整理成可复现的工程项目，包括数据准备、模型训练、指标对比、预测导出和本地网页演示。

## Dataset

当前使用 California Housing 数据集。目标列为：

The current dataset is California Housing. Target column:

```text
median_house_value
```

It represents median house value in a California block group. The dataset is suitable for learning feature engineering, regression errors, model comparison, and the difference between model units and user-facing business units.

它表示加州街区组层面的房价中位数。该数据集适合用于学习特征工程、回归误差、模型对比，以及“模型内部单位”和“用户展示单位”之间的区别。

## First Version

当前版本完成：

- 自动准备房价数据 CSV
- 自动生成预测样本 CSV
- 数值特征缺失值填充与标准化
- 训练 `random_forest` 回归模型
- 保存模型
- 生成预测结果
- 生成 MAE、RMSE、R2 指标
- 生成预测值对真实值图
- 生成特征重要性图
- 生成 HTML 报告

Current version includes:

- automatic housing CSV preparation
- automatic sample prediction CSV generation
- median imputation and scaling for numeric features
- `random_forest` regression training
- model persistence
- prediction result export
- MAE, RMSE, and R2 metrics
- predicted-versus-actual visualization
- feature importance visualization
- HTML report generation

## Metrics

MAE 表示平均绝对误差，适合直观理解“平均差多少”。RMSE 会更重视大误差，适合检查模型是否存在严重偏差。R2 表示解释能力，越接近 1 越好。

MAE measures average absolute error and is easy to interpret. RMSE penalizes large errors more strongly, making it useful for spotting serious mistakes. R2 measures explanatory power; closer to 1 is better.

## Price Unit

California Housing 的目标值原始单位是 `100k USD`。为了让中文读者更直观，本项目额外输出 `10k RMB` 展示值。

The original target unit in California Housing is `100k USD`. For Chinese readers, the project also exports values in `10k RMB`.

Fixed showcase assumption:

```text
1 USD = 6.6 RMB
```

这个汇率是作品展示用的固定假设，不是实时汇率，也不构成任何金融建议。

This exchange rate is a fixed showcase assumption. It is not a real-time exchange rate and should not be treated as financial advice.

## Model Comparison

Random Forest performs best in the current comparison. It reaches a much higher R2 than Linear Regression and Ridge Regression while keeping the optimized model file small enough for local deployment.

当前对比中 Random Forest 表现最好。它的 R2 明显高于 Linear Regression 和 Ridge Regression，同时优化后的模型文件仍然足够小，适合本地部署。

## Next Steps

- Add richer sample records for more realistic demos.
- Add optional cross-validation for more stable evaluation.
- Add screenshots or GIFs for GitHub presentation.
- Replace fixed exchange-rate display with configurable presentation settings if the project becomes production-oriented.

后续可继续改进：

- 增加更贴近真实演示场景的样本记录
- 增加可选交叉验证，让评估更稳定
- 为 GitHub 展示补充截图或 GIF
- 如果项目转向生产用途，将固定汇率改为可配置展示项
