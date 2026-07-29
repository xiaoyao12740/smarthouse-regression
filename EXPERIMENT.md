# Experiment Record / 实验记录

## Goal / 目标

补齐传统机器学习中的第二类核心任务：回归预测。

Complete the second core task in classical machine learning: regression prediction.

## Dataset / 数据集

当前使用 California Housing 数据集。目标列为：

The current dataset is California Housing. Target column:

```text
median_house_value
```

它表示区域房价中位数。这个数据集适合学习特征工程、回归误差和模型对比。

It represents median house value. The dataset is suitable for learning feature engineering, regression errors, and model comparison.

## First Version / 第一版

当前版本完成：

Current version includes:

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

## Metrics / 指标理解

- MAE：平均差多少，适合直观理解误差。
- RMSE：更重视大错误，适合检查严重偏差。
- R2：解释能力，越接近 1 越好。

- MAE: average absolute error.
- RMSE: stronger penalty for large errors.
- R2: explanatory power; closer to 1 is better.

## Price Unit / 价格单位

California Housing 的目标值原始单位是 `十万美元 / 100k USD`。为了让中文读者更直观，本项目额外输出 `万元人民币 / 10k RMB`。

换算假设：

```text
1 USD = 6.6 RMB
```

这个汇率是作品展示用的固定假设，不是实时汇率。

The original target unit is `100,000 USD`. For Chinese readers, the project also exports `10,000 RMB` values using a fixed showcase assumption:

```text
1 USD = 6.6 RMB
```

## Next Steps / 下一步

- 增加 Streamlit 交互页面
- 增加模型版本记录
- 增加自动模型比较
- 增加更贴近业务的中文字段解释
