import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SIM_TIME = 180
LAMBDA_NORMAL = 1
PEAK = 1.5   

def simulate(num_cashiers=2):
    time = 0
    arrivals = []

    while time < SIM_TIME:
        if time < 120:
            interarrival = np.random.exponential(1 / LAMBDA_NORMAL)
        else:
            interarrival = np.random.exponential(1 / PEAK)

        time += interarrival
        if time > SIM_TIME:
            break
        arrivals.append(time)

    cashier_available = [0] * num_cashiers
    cashier_busy_time = [0] * num_cashiers

    data = []

    for arrival in arrivals:
        service_time = random.uniform(2, 6)

        idx = np.argmin(cashier_available)

        start_time = max(arrival, cashier_available[idx])
        departure_time = start_time + service_time
        waiting_time = start_time - arrival

        
        if start_time < SIM_TIME:
            busy_end = min(departure_time, SIM_TIME)
            cashier_busy_time[idx] += max(0, busy_end - start_time)

        cashier_available[idx] = departure_time

        data.append([arrival, start_time, waiting_time, departure_time])

    df = pd.DataFrame(data, columns=[
        "Arrival", "Start", "Waiting", "Departure"
    ])

    return df, cashier_busy_time

df, cashier_busy_time = simulate()

before_peak = df[df["Arrival"] < 120]
during_peak = df[df["Arrival"] >= 120]

avg_before = before_peak["Waiting"].mean()
avg_peak = during_peak["Waiting"].mean()

print("Average waiting BEFORE peak:", round(avg_before, 2))
print("Average waiting DURING peak:", round(avg_peak, 2))
