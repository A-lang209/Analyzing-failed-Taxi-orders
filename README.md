# Gett: Diagnosing Marketplace Ride Failures & Supply Bottlenecks

An end-to-end data analytics project investigating order matching metrics, cancellation patterns, and supply-demand imbalances for failed taxi requests.

## 📌 Executive Summary
In ride-hailing networks, uncompleted orders represent lost revenue, frustrated passengers, and disengaged drivers. This project explores real-world order logs from **Gett** to determine why trips fail. By breaking down cancellations (before vs. after driver assignment) and evaluating system rejections, the analysis identifies exactly when and why marketplace liquidity breaks down.

## 🛠️ Tech Stack & Tools
- **Language:** Python 3.x
- **Data Manipulation:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Environment:** Google Colab / Jupyter Notebooks

## 📊 Core Analytical Insights

### 1. The Failure Funnel (Task 1)
- **Insight:** The vast majority of failed orders are categorized as **Client Cancelled (Before Assignment)**.
- **Business Impact:** Users are abandoning the booking funnel early on, signaling either immediate frustration or poor upfront expectations (e.g., long wait times).

### 2. The Rush Hour Capacity Crunch (Task 2)
- **Insight:** Failed orders heavily peak during morning commute windows (**07:00 – 09:00**) and late-evening social hours (**21:00 – 23:00**). Notably, automatic **System Rejections (No Driver Found)** scale dramatically during the morning rush.
- **Business Impact:** This indicates a structural supply shortage. There are simply not enough active drivers to meet commuting demand, causing the matching algorithm to repeatedly time out.

### 3. User Patience vs. Congestion (Task 3)
- **Insight:** After removing statistical outliers (99th percentile), the data reveals that the average Time to Cancellation (TTC) for matched drivers jumps significantly during heavy traffic hours.
- **Business Impact:** When a driver accepts a trip but gets stuck or moves in the opposite direction, the user tracks this delay visually and cancels. Conversely, during peak shortages without a driver assigned, users wait significantly longer before giving up.

### 4. ETA as a Failure Trigger (Task 4)
- **Insight:** The average Estimated Time of Arrival (ETA) directly mirrors the overall failure distribution curve, spiking sharply during high-demand windows.
- **Business Impact:** As local supply dries up, the engine must source drivers from further away. This lengthens the initial ETA presented to the user, acting as the primary catalyst for the surge in early client cancellations.

## 💡 Operational Recommendations
1. **Dynamic Supply Incentives:** Implement targeted driver bonuses or launch localized surge pricing during the 7 AM–9 AM window to draw more supply onto the road.
2. **Expectation Management:** Optimize upfront ETA calculations to remain accurate and transparent, minimizing the friction that leads to post-assignment cancellations.

## 📂 Repository Structure
- `data_orders.csv` & `data_offers.csv`: Raw marketplace datasets.
- `Ride_Failures_Analysis.ipynb`: Fully documented Google Colab notebook containing code and visualizations.
- `README.md`: Project summary and business conclusions.
