import numpy as np
import matplotlib.pyplot as plt

def start_simulation():
    delta_time = 0.0

    arrival = [
        lambda: np.random.gamma(shape=3, scale=0.5),
        #lambda: np.random.poisson(lam=0.2)
        lambda: np.random.exponential(1/0.2)
    ]
    departure = [
        lambda: np.random.normal(15, 2),
        lambda: np.random.exponential(1/3)
    ]

    time = [arrival[0](),
            arrival[1]()]
            #501]
    departure_time = 501

    def erlang(lam, s):
        return np.random.exponential(1./lam, size=s) \
               + np.random.exponential(1./lam, size=s) \
               + np.random.exponential(1./lam, size=s)

    #sample = erlang(3.0, 1000)
    #plt.hist(sample)
    #plt.show()

    overall_simulation_time = 500
    idle_start = 0.0
    idle_finish = 0.0
    idle_total = 0.0

    total_event_count = 0

    # 0 - server
    # 1..n - queue
    status = 0
    queue = []

    print('Initial state:\n'
          f'queue: {queue}, status: {status}, overall_simulation_time: {overall_simulation_time}, time: {time}'
          f'\n-------------------------------------------------------------\n')

    while delta_time < overall_simulation_time:

        # Updating the total (delta) time
        delta_time = current_min_time = min(time)

        # If departure time is the nearest time - freeing the server and removing current active event from the queue
        # Event 3
        if departure_time < current_min_time:
            # Remove the current active event from the queue
            queue = queue[1:]

            # Free the server
            status = 0

            # Check if idle
            if len(queue) == 0 and idle_start != 0:
                idle_finish = delta_time
                idle_total += idle_finish - idle_start
                continue

        # Get index of a nearest event time (type 1 or type 2)
        current_min_index = time.index(current_min_time)

        # Updating nearest event's time
        time[current_min_index] += current_min_time

        # If server is Free - calculate and update the departure time
        if status == 0:
            # Updating departure time to the time of a currently nearest event
            departure_time = time[current_min_index] + departure[current_min_index]()

            # Set server status to busy
            status = 1

        # Add current event to the queue (type 1 or type 2)
        queue.append(current_min_index + 1)

        # Update total count of events
        total_event_count += 1

        print(f'delta_time: {delta_time}, '
              f'total_event_count: {total_event_count}, '
              f'current_min_index: {current_min_index}, current_min_time: {current_min_time}\n'
              f'time: {time}\n'
              f'departure_time: {departure_time}\n'
              f'queue: {queue}\n'
              f'idle_total: {idle_total}, idle_finish: {idle_finish}, idle_start: {idle_start}\n')

    # Calculate idle coefficient
    idle_coefficient = idle_total / overall_simulation_time
    average_event_time = delta_time / total_event_count
    print(f'Idle coefficient: {idle_coefficient}\n'
          f'Average event time: {average_event_time}\n')


if __name__ == '__main__':
    start_simulation()
