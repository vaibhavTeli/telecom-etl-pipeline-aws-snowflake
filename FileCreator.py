import pandas as pd
import numpy as np

# The Target: 1 Million records
n_records = 1_000_000

print("Generating 1 million telecom records. Standby...")

# Vectorized generation is lightning fast
df = pd.DataFrame({
    # Simulating your 10k unique accounts
    'account_id': np.random.randint(1000, 11000, n_records),

    # 50% data, 40% voice, 10% sms
    'service_type': np.random.choice(['voice', 'data', 'sms'], n_records, p=[0.4, 0.5, 0.1]),

    # Random timestamps over the last 30 days
    'timestamp': pd.Timestamp.now() - pd.to_timedelta(np.random.randint(0, 30 * 24 * 60 * 60, n_records), unit='s'),
    # Random sms (up to 1 hour)
    'messages_sent': np.random.randint(0,2500, n_records),
    # Random durations (up to 1 hour)
    'duration_seconds': np.random.randint(0, 3600, n_records),

    # Random data usage (up to 500MB per session)
    'data_mb_used': np.round(np.random.uniform(0, 500, n_records), 2),

    # Real-world payment failure rates
    'payment_status': np.random.choice(['Success', 'Failed', 'Pending'], n_records, p=[0.85, 0.10, 0.05])
})

# Logic correction: Voice/SMS shouldn't have data usage, Data shouldn't have duration
df.loc[df['service_type'] != 'data', 'data_mb_used'] = 0.0
df.loc[df['service_type'] != 'sms', 'messages_sent'] = 0
df.loc[df['service_type'] != 'voice', 'duration_seconds'] = 0

print("Processing complete. Saving to CSV...")

# Dump to CSV
file_name = "telecom_billing_raw.csv"
df.to_csv(file_name, index=False)

print(f"Success. File '{file_name}' created.")