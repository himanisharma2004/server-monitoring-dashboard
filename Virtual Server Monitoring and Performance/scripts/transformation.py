import pandas as pd
import numpy as np

# Load cleaned dataset
file_path = "data/processed/clean_server_data.csv"
df = pd.read_csv(file_path)

# Convert timestamp column to datetime
df["Log_Timestamp"] = pd.to_datetime(df["Log_Timestamp"], format="%d-%m-%Y %H:%M")

# Create alert flags
df["High_CPU_Flag"] = df["CPU_Utilization (%)"].apply(lambda x: 1 if x > 85 else 0)
df["High_Memory_Flag"] = df["Memory_Usage (%)"].apply(lambda x: 1 if x > 90 else 0)
df["High_Disk_IO_Flag"] = df["Disk_IO (%)"].apply(lambda x: 1 if x > 85 else 0)
df["Downtime_Flag"] = df["Downtime (Hours)"].apply(lambda x: 1 if x > 0 else 0)

# Create server health status
def get_server_status(row):
    if row["CPU_Utilization (%)"] > 85 or row["Memory_Usage (%)"] > 90 or row["Disk_IO (%)"] > 85:
        return "Critical"
    elif row["CPU_Utilization (%)"] > 70 or row["Memory_Usage (%)"] > 75 or row["Disk_IO (%)"] > 70:
        return "Warning"
    else:
        return "Healthy"

df["Server_Status"] = df.apply(get_server_status, axis=1)

# Create total network traffic column
df["Total_Network_Traffic (MB/s)"] = df["Network_Traffic_In (MB/s)"] + df["Network_Traffic_Out (MB/s)"]

# Save transformed detailed dataset
df.to_csv("data/processed/server_metrics_detailed.csv", index=False)

# Create aggregated server-level summary
server_summary = df.groupby(
    ["Server_ID", "Hostname", "OS_Type", "Server_Location", "Server_Status"],
    as_index=False
).agg({
    "CPU_Utilization (%)": "mean",
    "Memory_Usage (%)": "mean",
    "Disk_IO (%)": "mean",
    "Network_Traffic_In (MB/s)": "mean",
    "Network_Traffic_Out (MB/s)": "mean",
    "Total_Network_Traffic (MB/s)": "mean",
    "Uptime (Hours)": "mean",
    "Downtime (Hours)": "mean",
    "High_CPU_Flag": "sum",
    "High_Memory_Flag": "sum",
    "High_Disk_IO_Flag": "sum",
    "Downtime_Flag": "sum"
})

# Rename columns for better readability
server_summary = server_summary.rename(columns={
    "CPU_Utilization (%)": "Avg_CPU_Utilization",
    "Memory_Usage (%)": "Avg_Memory_Usage",
    "Disk_IO (%)": "Avg_Disk_IO",
    "Network_Traffic_In (MB/s)": "Avg_Network_In",
    "Network_Traffic_Out (MB/s)": "Avg_Network_Out",
    "Total_Network_Traffic (MB/s)": "Avg_Total_Network_Traffic",
    "Uptime (Hours)": "Avg_Uptime_Hours",
    "Downtime (Hours)": "Avg_Downtime_Hours",
    "High_CPU_Flag": "CPU_Alert_Count",
    "High_Memory_Flag": "Memory_Alert_Count",
    "High_Disk_IO_Flag": "Disk_Alert_Count",
    "Downtime_Flag": "Downtime_Event_Count"
})

# Save aggregated summary
server_summary.to_csv("data/processed/server_summary.csv", index=False)

print("Transformation completed successfully.")
print("Files created:")
print("1. data/processed/server_metrics_detailed.csv")
print("2. data/processed/server_summary.csv")