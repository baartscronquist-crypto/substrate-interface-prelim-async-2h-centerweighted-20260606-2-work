# Coupled Interface Response Model

请实现当前目录中的 `desensitized_interface_response.py`。这是一个空试卷骨架；你需要根据下面的题目原文建立可运行的无量纲耦合界面响应模拟，并保持公开接口兼容。

## 题目原文

考虑一个由两个连续介质子域 Ω1 与 Ω2 构成的耦合界面系统。Ω1 具有广义位移/场-形变交叉耦合响应；Ω2 中存在一种可迁移标量组分 c(x,t) 以及广义势 ψ(x,t)，并含有预置的静态背景源项 ρ0(x)。组分 c 的跨界面输运不采用线性扩散近似，而由依赖界面两侧标量水平、势差和温度尺度的非线性交换通量 F(c1,c2,Δψ;θ) 描述。系统受到小幅时间周期调制，该调制通过边界条件或耦合系数进入模型。

请在无量纲化后：

1. 给出最小连续介质控制方程和弱形式；
2. 在线性频率响应近似下，分析二阶响应观测量 Q(α)=<R^2> 与控制参数 α、调制频率 ω、背景源项幅度 β 之间的关系；
3. 给出稳态或周期稳态下标量场 c(x,t) 的空间分布诊断，包括均值场、一阶谐波幅值和相位，并讨论在哪些参数区间会出现边界层、相位滞后或响应峰值。

## 编程目标

你需要把上述建模问题落成一个 Python 模拟模块。评测不会要求你输出论文式报告，但代码中的变量和数值结构应能对应题目中的核心对象：

- 控制参数 `alpha`
- 二阶响应观测量 `Q(alpha)=<R^2>`，其中 `R(t)` 可由返回的 `rate` 表示
- 非线性界面交换/通量响应
- 带背景源项的二维标量场 `c(x,t)`
- 小幅周期调制和频率参数 `omega`
- 可用于诊断均值场、一阶谐波幅值和相位的时空采样

## 必须保持的接口

模块必须提供：

```python
Config
make_grid(cfg)
run_trial(alpha, cfg, grid, rng, record_fields=False)
```

`Config` 必须是 `dataclasses.dataclass` 或兼容 `dataclasses.replace()` 的对象。评测可能覆盖这些字段：

```python
num_trials
t_total
nx
nz
history_window
seed
```

`make_grid(cfg)` 应返回带有 `X`、`Z` 网格数组的对象，使评测脚本可以在相同网格上计算空间诊断。

`run_trial(...)` 必须返回一个字典，至少包含：

```python
{
    "time": ...,
    "rate": ...,
    "feedback_scalar": ...,
    "scalar_surface_mean": ...,
    "scalar_samples": ...,
}
```

要求：

- `time`、`rate`、`feedback_scalar`、`scalar_surface_mean` 是长度一致的一维数值序列。
- `rate` 表示二阶响应观测量中的响应信号 `R(t)`。
- `feedback_scalar` 表示模型中进入响应耦合支路的局部标量诊断量，不应简单等同于二维标量场的全局均值。
- `scalar_surface_mean` 表示靠近界面或表面的标量场平均诊断。
- 当 `record_fields=True` 时，`scalar_samples` 必须是形状 `(nz, nx, nt)` 的三维数值数组，其中 `nt == len(time)`。
- 所有返回数值应为有限值。

## 本地公开检查

可以先运行：

```bash
python3 test_dev.py
```

公开测试只检查接口、形状和有限性，不代表模型的物理诊断已经完整。

## 限制

- 不要硬编码评测输出、随机查表或按输入参数直接返回固定答案。
- 不要修改 `test_dev.py`。
- 可以创建辅助函数和内部类，但最终提交必须包含 `desensitized_interface_response.py`。
