# This is a sample Python script.
import inline as inline
import matplotlib as matplotlib

# step #1 the required libraries

import math
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Step#2 create the variables
windows = [30, 60, 90, 120]  # number of days I want to compute volatility
quantiles = [0.25, 0.75]  # defines the % of top 25% of values

min_ = []
max_ = []
median = []
top_q = []
bottom_q = []
realized = []

data = yf.download("SPY", start="2020-08-01", end="2022-08-25")


# Step #3 realized the volatility

# the following is a func to compute the volatility of SPY
def realized_vol(price_data, window=30):
    log_return = (price_data["Close"] / price_data["Close"].shift(1).apply(np.log))
    return log_return.rolling(window=window, center=False).std() * math.sqrt(252)


# now we loop through each of the windows, and we compute the realized

for window in windows:
    # get a dataframe with realized volatility
    # estimator is pandas DataFrame
    estimator = realized_vol(window=window, price_data=data)
    min_.append(estimator.min())
    max_.append(estimator.max())
    median.append(estimator.median())
    top_q.append(estimator.quantile(quantiles[1]))
    bottom_q.append(estimator.quantile(quantiles[0]))
    realized.append(estimator[-1])

# Step 4: plot the results

# create the plots on the chart
plt.plot(windows, min_, "-o", linewidth=1, label="Min")
plt.plot(windows, max_, "-o", linewidth=1, label="Max")
plt.plot(windows, median, "-o", linewidth=1, label="Median")
plt.plot(windows, top_q, "-o", linewidth=1, label=f"{quantiles[1] * 100:.0f} Prctl")
plt.plot(windows, bottom_q, "-o", linewidth=1, label=f"{quantiles[0] * 100:.0f} Prctl")
plt.plot(windows, realized, "ro-.", linewidth=1, label="Realized")

# set the x-axis labels
plt.xticks(windows)

# format the legend
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
