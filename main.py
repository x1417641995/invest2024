import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

'''
if download fail, update yfinance
pip install yfinance --upgrade
'''

# 獲取 TQQQ 的數據
start_date = "2024-01-01"
tqqq_data = yf.download("TQQQ", start=start_date)

# 確認數據是否成功下載
if tqqq_data.empty:
    print("無法獲取數據，請檢查網絡連接或股票代碼是否正確。")
else:
    # 計算 20 天 EMA
    tqqq_data["20EMA"] = tqqq_data["Close"].ewm(span=20, adjust=False).mean()

    # 畫圖
    fig, ax = plt.subplots(figsize=(12, 6))
    line1, = ax.plot(tqqq_data.index, tqqq_data["Close"], label="TQQQ Close Price", linewidth=1.5)
    line2, = ax.plot(tqqq_data.index, tqqq_data["20EMA"], label="20-Day EMA", linewidth=2, linestyle="--", color="orange")
    plt.title(f"TQQQ Close Price and 20-Day EMA (from {start_date})", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Price", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(alpha=0.3)

    # 添加動態文字
    annotation = ax.annotate(
        "",
        xy=(0, 0),
        xytext=(-50, 50),
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
        arrowprops=dict(arrowstyle="->"),
    )
    annotation.set_visible(False)

    def on_hover(event):
        if event.inaxes == ax:  # 確保在圖表範圍內
            print(event.inaxes, "inaxes")
            print(event)
            print(event.xdata, "xdat")
            # 找到滑鼠最近的日期索引
            closest_idx = min(
                range(len(tqqq_data.index)),
                key=lambda i: abs((tqqq_data.index[i] - pd.Timestamp(event.xdata)).total_seconds())
            )
            print(closest_idx, "closest_idx1")

            mouse_date = pd.to_datetime(event.xdata, unit='D', origin='1970-01-01')
            # 計算滑鼠日期與資料日期的時間差（以秒為單位）
            time_differences = (tqqq_data.index - mouse_date).total_seconds()
            closest_idx = np.argmin(np.abs(time_differences))
            
            print(closest_idx, "closest_idx2")
            closest_date = tqqq_data.index[closest_idx]
            close_price = tqqq_data["Close"].iloc[closest_idx]
            ema_value = tqqq_data["20EMA"].iloc[closest_idx]
            
            # 明確使用 iloc[0] 提取值
            close_price = float(close_price) if isinstance(close_price, pd.Series) else close_price
            ema_value = float(ema_value) if isinstance(ema_value, pd.Series) else ema_value

            # 更新 annotation
            annotation.set_visible(True)
            annotation.xy = (closest_date, close_price)
            annotation.set_text(f"Date: {closest_date.strftime('%Y-%m-%d')}\nPrice: {close_price:.2f}\n20EMA: {ema_value:.2f}")
            fig.canvas.draw_idle()
        else:
            annotation.set_visible(False)
            fig.canvas.draw_idle()


    # 連接事件處理程序
    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    plt.show()
 