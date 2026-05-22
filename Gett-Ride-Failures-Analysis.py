import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ==========================================
# STEP 1: DATA LOADING & PREPARATION
# ==========================================
print("Loading dataset...")
try:
    df_orders = pd.read_csv('/content/data_orders.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure '/content/data_orders.csv' is uploaded to your Colab workspace.\n")

# Extract hour from the timestamp string (format is 'HH:MM:SS')
df_orders['order_hour'] = pd.to_datetime(df_orders['order_datetime'], format='%H:%M:%S').dt.hour


# ==========================================
# TASK 1: DISTRIBUTION OF FAILURES
# ==========================================
print("\n--- Processing Task 1: Distribution of Failure Reasons ---")

def categorize_failure(row):
    if row['order_status_key'] == 4 and row['is_driver_assigned_key'] == 1:
        return 'Client Cancelled (After Assignment)'
    elif row['order_status_key'] == 4 and row['is_driver_assigned_key'] == 0:
        return 'Client Cancelled (Before Assignment)'
    elif row['order_status_key'] == 9:
        return 'System Rejected (No Driver Found)'
    else:
        return 'Unknown'

df_orders['failure_reason'] = df_orders.apply(categorize_failure, axis=1)

# Calculate distribution
failure_counts = df_orders['failure_reason'].value_counts()
print("Order Count by Failure Reason:")
print(failure_counts)

# Plot Task 1
plt.figure(figsize=(10, 5))
sns.barplot(x=failure_counts.values, y=failure_counts.index, palette='viridis', hue=failure_counts.index, legend=False)
plt.title('Distribution of Orders According to Reasons for Failure', fontsize=14, pad=15)
plt.xlabel('Number of Orders', fontsize=12)
plt.ylabel('Failure Category', fontsize=12)
plt.tight_layout()
plt.show()

# ==========================================
# TASK 2: HOURLY DISTRIBUTION OF FAILED ORDERS
# ==========================================
print("\n--- Processing Task 2: Hourly Distribution of Failed Orders ---")

# Pivot data to get counts of each failure reason per hour
hourly_failures = df_orders.groupby(['order_hour', 'failure_reason']).size().unstack(fill_value=0)

# Plot Task 2 (Stacked Bar Chart)
hourly_failures.plot(kind='bar', stacked=True, colormap='viridis', edgecolor='none', figsize=(13, 6))
plt.title('Distribution of Failed Orders by Hour of Day', fontsize=14, pad=15)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Number of Failed Orders', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Failure Category', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


# ==========================================
# TASK 3: AVERAGE TIME TO CANCELLATION
# ==========================================
print("\n--- Processing Task 3: Average Time to Cancellation with and without Driver ---")

# Filter rows where cancellation time is documented
df_cancels = df_orders[df_orders['cancellations_time_in_seconds'].notna()].copy()

# Identify and filter out extreme outliers using the 99th percentile threshold
ttc_upper_limit = df_cancels['cancellations_time_in_seconds'].quantile(0.99)
print(f"Removing cancellation time outliers above the 99th percentile: {ttc_upper_limit:.1f} seconds")

df_cancels_clean = df_cancels[df_cancels['cancellations_time_in_seconds'] <= ttc_upper_limit]

# Group by hour and driver assignment status
hourly_ttc = df_cancels_clean.groupby(['order_hour', 'is_driver_assigned_key'])['cancellations_time_in_seconds'].mean().unstack()
hourly_ttc.columns = ['Without Driver Assigned', 'With Driver Assigned']

# Plot Task 3
plt.figure(figsize=(12, 6))
plt.plot(hourly_ttc.index, hourly_ttc['With Driver Assigned'], marker='o', color='teal', linewidth=2.5, label='With Driver Assigned')
plt.plot(hourly_ttc.index, hourly_ttc['Without Driver Assigned'], marker='s', color='coral', linewidth=2.5, label='Without Driver Assigned')
plt.title('Average Time to Cancellation by Hour (Outliers Removed)', fontsize=14, pad=15)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Average Cancellation Time (Seconds)', fontsize=12)
plt.xticks(range(0, 24))
plt.legend(loc='best')
plt.tight_layout()
plt.show()


# ==========================================
# TASK 4: DISTRIBUTION OF AVERAGE ETA BY HOURS
# ==========================================
print("\n--- Processing Task 4: Average ETA by Hours ---")

# Group data by hour and calculate average ETA (filtering out null values)
hourly_eta = df_orders[df_orders['m_order_eta'].notna()].groupby('order_hour')['m_order_eta'].mean()

# Plot Task 4
plt.figure(figsize=(12, 6))
sns.lineplot(x=hourly_eta.index, y=hourly_eta.values, marker='D', color='crimson', linewidth=2.5)
plt.title('Distribution of Average Estimated Time of Arrival (ETA) by Hour', fontsize=14, pad=15)
plt.xlabel('Hour of the Day', fontsize=12)
plt.ylabel('Average ETA (Seconds)', fontsize=12)
plt.xticks(range(0, 24))
plt.tight_layout()
plt.show()
