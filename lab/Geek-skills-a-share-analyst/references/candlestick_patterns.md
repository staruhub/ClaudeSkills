# K线形态识别

## 反转形态

### 底部反转

**锤子线 (Hammer)**
- 条件：下影线 >= 实体×2，上影线极小，出现在下跌末端
```python
def is_hammer(open, high, low, close):
    body = abs(close - open)
    lower_shadow = min(open, close) - low
    upper_shadow = high - max(open, close)
    return lower_shadow >= body * 2 and upper_shadow <= body * 0.3
```

**早晨之星 (Morning Star)**
- 三根K线组合：大阴线 + 小实体(十字星) + 大阳线
```python
def is_morning_star(df, idx):
    d1 = df.iloc[idx-2]  # 大阴线
    d2 = df.iloc[idx-1]  # 小实体
    d3 = df.iloc[idx]    # 大阳线
    return (d1['close'] < d1['open'] and 
            abs(d2['close'] - d2['open']) < (d1['high']-d1['low'])*0.3 and
            d3['close'] > d3['open'] and 
            d3['close'] > (d1['open'] + d1['close'])/2)
```

**双底 (Double Bottom)**
- W形态，两个低点接近，颈线突破确认

### 顶部反转

**流星线 (Shooting Star)**
- 条件：上影线 >= 实体×2，下影线极小，出现在上涨末端
```python
def is_shooting_star(open, high, low, close):
    body = abs(close - open)
    upper_shadow = high - max(open, close)
    lower_shadow = min(open, close) - low
    return upper_shadow >= body * 2 and lower_shadow <= body * 0.3
```

**黄昏之星 (Evening Star)**
- 三根K线组合：大阳线 + 小实体(十字星) + 大阴线

**双顶 (Double Top)**
- M形态，两个高点接近，颈线跌破确认

## 持续形态

### 上升趋势中

**红三兵 (Three White Soldiers)**
- 三根连续阳线，每根开盘价在前一根实体内，收盘创新高
```python
def is_three_white_soldiers(df, idx):
    for i in range(3):
        if df.iloc[idx-i]['close'] <= df.iloc[idx-i]['open']:
            return False
    return (df.iloc[idx]['close'] > df.iloc[idx-1]['close'] > df.iloc[idx-2]['close'])
```

**上升三法 (Rising Three Methods)**
- 大阳线 + 3根小阴线(不破大阳线低点) + 大阳线

### 下降趋势中

**三只乌鸦 (Three Black Crows)**
- 三根连续阴线，每根开盘价在前一根实体内，收盘创新低

**下降三法 (Falling Three Methods)**
- 大阴线 + 3根小阳线(不破大阴线高点) + 大阴线

## 整理形态

### 三角形整理

**上升三角形**
- 高点水平，低点上移，向上突破概率大
```python
def is_ascending_triangle(highs, lows, period=20):
    high_max = highs[-period:].max()
    high_range = highs[-period:].max() - highs[-period:].min()
    low_slope = (lows.iloc[-1] - lows.iloc[-period]) / period
    return high_range / high_max < 0.02 and low_slope > 0
```

**下降三角形**
- 低点水平，高点下移，向下突破概率大

**对称三角形**
- 高点下移，低点上移，方向不确定

### 旗形整理

**上升旗形**
- 急涨后小幅回调整理，形成向下倾斜通道

**下降旗形**
- 急跌后小幅反弹整理，形成向上倾斜通道

## 缺口分析

### 缺口类型

| 类型 | 特征 | 意义 |
|------|------|------|
| 普通缺口 | 整理区间内 | 通常会回补 |
| 突破缺口 | 突破重要位置 | 趋势开始信号 |
| 持续缺口 | 趋势中间 | 趋势加速信号 |
| 衰竭缺口 | 趋势末端 | 趋势结束信号 |

```python
def find_gaps(df):
    gaps = []
    for i in range(1, len(df)):
        if df.iloc[i]['low'] > df.iloc[i-1]['high']:  # 向上缺口
            gaps.append(('up', i, df.iloc[i-1]['high'], df.iloc[i]['low']))
        elif df.iloc[i]['high'] < df.iloc[i-1]['low']:  # 向下缺口
            gaps.append(('down', i, df.iloc[i]['high'], df.iloc[i-1]['low']))
    return gaps
```

## 实战信号组合

### 强买入信号
1. 早晨之星 + MACD金叉 + 成交量放大
2. 突破缺口 + 站上MA20 + KDJ金叉
3. 锤子线 + RSI超卖反弹 + 布林下轨支撑

### 强卖出信号
1. 黄昏之星 + MACD死叉 + 成交量放大
2. 跌破颈线 + MA20死叉MA60 + KDJ死叉
3. 流星线 + RSI超买回落 + 布林上轨压力
