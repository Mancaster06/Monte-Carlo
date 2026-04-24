import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SIM_TIME = 180
LAMBDA = 1

def simulate(num_cashiers=2):

    time = 0
    arrivals = []

    while time < SIM_TIME:
        interarrival = np.random.exponential(1 / LAMBDA)
        time += interarrival
        if time > SIM_TIME:
            break
        arrivals.append(time)

    # Cashier next free time
    cashier_available = [0] * num_cashiers

    # REAL busy tracking (correct method)
    cashier_busy_time = [0] * num_cashiers

    data = []

    for arrival in arrivals:

        service_time = random.uniform(2, 6)

        # choose earliest available cashier
        idx = np.argmin(cashier_available)

        start_time = max(arrival, cashier_available[idx])
        departure_time = start_time + service_time
        waiting_time = start_time - arrival

        # If cashier becomes free before SIM_TIME boundary
        actual_start = start_time
        actual_end = departure_time

        if actual_start < SIM_TIME:
            busy_start = actual_start
            busy_end = min(actual_end, SIM_TIME)

            cashier_busy_time[idx] += max(0, busy_end - busy_start)

        cashier_available[idx] = departure_time

        data.append([arrival, start_time, waiting_time, departure_time, service_time])

    df = pd.DataFrame(data, columns=[
        "Arrival", "Start", "Waiting", "Departure", "Service"
    ])

    return df, cashier_busy_time

df, cashier_busy_time = simulate()

avg_wait = df["Waiting"].mean()
max_wait = df["Waiting"].max()
prob_wait_5 = (df["Waiting"] > 5).mean()

total_capacity = 2 * SIM_TIME
total_busy = sum(cashier_busy_time)

utilisation = (total_busy / total_capacity) * 100

print("Average Waiting Time:", round(avg_wait, 2))
print("Max Waiting Time:", round(max_wait, 2))
print("P(Wait > 5):", round(prob_wait_5, 3))

print("\nCashier Busy Times:", cashier_busy_time)
print("Total Busy Time:", round(total_busy, 2))
print("Total Capacity:", total_capacity)
print("Utilisation (%):", round(utilisation, 2))

print("\nSample Table (First 20 Customers):")
print(df.head(20))
results = []

# Repeat simulation 50 times
for i in range(50):
    df, cashier_busy_time = simulate()
    
    avg_wait = df["Waiting"].mean()
    results.append(avg_wait)

results = np.array(results)

mean_wait = results.mean()
std_wait = results.std()

print("Average waiting time across simulations:", round(mean_wait, 2))
print("Standard deviation:", round(std_wait, 2))


plt.hist(df["Waiting"], bins=15)
plt.title("Distribution of Customer Waiting Times")
plt.xlabel("Waiting Time (minutes)")
plt.ylabel("Number of Customers")

plt.show()


