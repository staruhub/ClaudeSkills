# 量化因子库

## 价值因子

### EP (收益价格比)
```python
def factor_ep(net_profit, market_cap):
    """EP = 净利润 / 市值，越高越便宜"""
    return net_profit / market_cap
```

### BP (账面市值比)
```python
def factor_bp(book_value, market_cap):
    """BP = 净资产 / 市值，越高越便宜"""
    return book_value / market_cap
```

### SP (销售价格比)
```python
def factor_sp(revenue, market_cap):
    """SP = 营收 / 市值"""
    return revenue / market_cap
```

### CFP (现金流价格比)
```python
def factor_cfp(operating_cf, market_cap):
    """CFP = 经营现金流 / 市值"""
    return operating_cf / market_cap
```

### DP (股息率)
```python
def factor_dp(dividend, price):
    """DP = 每股分红 / 股价"""
    return dividend / price
```

## 动量因子

### MOM (价格动量)
```python
def factor_momentum(close, period=20):
    """过去N日收益率"""
    return close.pct_change(period)
```

### REV (反转因子)
```python
def factor_reversal(close, period=5):
    """短期反转：过去N日收益率取负"""
    return -close.pct_change(period)
```

### VOL_MOM (成交量动量)
```python
def factor_vol_momentum(volume, period=20):
    """成交量动量"""
    return volume.rolling(5).mean() / volume.rolling(period).mean()
```

### RSRS (阻力支撑相对强度)
```python
def factor_rsrs(high, low, period=18):
    """回归斜率作为趋势强度"""
    from sklearn.linear_model import LinearRegression
    rsrs = []
    for i in range(period, len(high)):
        X = low[i-period:i].values.reshape(-1, 1)
        y = high[i-period:i].values
        reg = LinearRegression().fit(X, y)
        rsrs.append(reg.coef_[0])
    return pd.Series(rsrs, index=high.index[period:])
```

## 质量因子

### ROE (净资产收益率)
```python
def factor_roe(net_profit, equity):
    return net_profit / equity
```

### ROIC (投入资本回报率)
```python
def factor_roic(nopat, invested_capital):
    """ROIC = 税后经营利润 / 投入资本"""
    return nopat / invested_capital
```

### GP (毛利率)
```python
def factor_gross_profit(revenue, cogs):
    return (revenue - cogs) / revenue
```

### ACCRUAL (应计盈余)
```python
def factor_accrual(net_profit, operating_cf, total_assets):
    """应计盈余 = (净利润 - 经营现金流) / 总资产"""
    return (net_profit - operating_cf) / total_assets
```

## 规模因子

### SIZE (市值因子)
```python
def factor_size(market_cap):
    """对数市值，通常取负表示小盘股溢价"""
    return -np.log(market_cap)
```

### NLSIZE (非线性市值)
```python
def factor_nlsize(market_cap):
    """市值三次方根"""
    return np.cbrt(market_cap)
```

## 波动率因子

### VOL (波动率)
```python
def factor_volatility(returns, period=20):
    """收益率标准差"""
    return returns.rolling(period).std()
```

### IVOL (特质波动率)
```python
def factor_idio_vol(returns, market_returns, period=60):
    """剔除市场因素后的特质波动率"""
    from sklearn.linear_model import LinearRegression
    resid = []
    for i in range(period, len(returns)):
        X = market_returns[i-period:i].values.reshape(-1, 1)
        y = returns[i-period:i].values
        reg = LinearRegression().fit(X, y)
        pred = reg.predict(X)
        resid.append(np.std(y - pred))
    return pd.Series(resid, index=returns.index[period:])
```

### SKEW (偏度)
```python
def factor_skewness(returns, period=20):
    return returns.rolling(period).skew()
```

## 技术因子

### TURN (换手率)
```python
def factor_turnover(volume, float_shares, period=20):
    """平均换手率"""
    return (volume / float_shares).rolling(period).mean()
```

### ILLIQ (非流动性)
```python
def factor_illiquidity(returns, volume, period=20):
    """Amihud非流动性指标"""
    return (returns.abs() / volume).rolling(period).mean()
```

### CORR (相关性)
```python
def factor_correlation(returns, market_returns, period=60):
    """与市场的相关性"""
    return returns.rolling(period).corr(market_returns)
```

## 成长因子

### SUE (标准化盈余惊喜)
```python
def factor_sue(actual_eps, expected_eps, std_eps):
    """SUE = (实际EPS - 预期EPS) / 标准差"""
    return (actual_eps - expected_eps) / std_eps
```

### REVG (营收增长率)
```python
def factor_revenue_growth(revenue):
    return revenue.pct_change(4)  # 同比增长
```

### EPG (盈利增长率)
```python
def factor_earnings_growth(net_profit):
    return net_profit.pct_change(4)  # 同比增长
```

## 因子合成与选股

### 多因子评分模型
```python
def multi_factor_score(df, factors_config):
    """
    factors_config = {
        'EP': {'weight': 0.2, 'ascending': False},
        'MOM_20': {'weight': 0.15, 'ascending': False},
        'ROE': {'weight': 0.2, 'ascending': False},
        'REV_5': {'weight': 0.15, 'ascending': True},
        'VOL': {'weight': 0.1, 'ascending': True},
        'SIZE': {'weight': 0.2, 'ascending': True},
    }
    """
    scores = pd.DataFrame(index=df.index)
    for factor, config in factors_config.items():
        # 标准化因子值
        factor_values = df[factor]
        factor_rank = factor_values.rank(pct=True, ascending=config['ascending'])
        scores[factor] = factor_rank * config['weight']
    
    scores['total'] = scores.sum(axis=1)
    return scores.sort_values('total', ascending=False)
```

### 选股示例
```python
def select_stocks(df, top_n=30):
    """
    选股流程：
    1. 剔除ST股票
    2. 剔除上市不满60天的新股
    3. 剔除涨停/跌停股票
    4. 计算多因子评分
    5. 选取评分前N名
    """
    # 基础筛选
    df = df[~df['name'].str.contains('ST')]
    df = df[df['list_days'] > 60]
    df = df[df['pct_change'].abs() < 9.9]
    
    # 计算因子评分
    scores = multi_factor_score(df, factors_config)
    
    return scores.head(top_n)
```

## 回测框架

```python
def backtest_strategy(df, signal_col, hold_days=5):
    """
    简单回测框架
    df: 包含日期、收盘价、信号的DataFrame
    signal_col: 信号列名 (1=买入, 0=持有, -1=卖出)
    hold_days: 持仓天数
    """
    df['future_return'] = df['close'].shift(-hold_days) / df['close'] - 1
    df['strategy_return'] = df[signal_col].shift(1) * df['future_return']
    
    total_return = (1 + df['strategy_return']).cumprod().iloc[-1] - 1
    sharpe = df['strategy_return'].mean() / df['strategy_return'].std() * np.sqrt(252/hold_days)
    max_drawdown = (df['strategy_return'].cumsum() - df['strategy_return'].cumsum().cummax()).min()
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_drawdown,
        'win_rate': (df['strategy_return'] > 0).mean()
    }
```
