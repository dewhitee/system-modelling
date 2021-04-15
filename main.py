import numpy as np
import matplotlib.pyplot as plt


def erlang(lam, s):
    return np.random.exponential(1. / lam, size=s) \
           + np.random.exponential(1. / lam, size=s) \
           + np.random.exponential(1. / lam, size=s)


def start_simulation(overall_simulation_time=500):
    delta_time = 0.0

    arrival = [
        lambda: np.random.gamma(shape=3, scale=0.5),
        lambda: np.random.poisson(lam=1./0.2)
        #lambda: np.random.exponential(1 / 0.2)
        # lambda: erlang(0.5, 3)[0]
    ]
    departure = [
        lambda: np.random.normal(15, 2),
        lambda: np.random.exponential(1 / 3)
    ]

    arrival_time = [arrival[0](),
                    arrival[1]()]
    # 501]
    departure_time = 501

    # sample = erlang(3.0, 1000)
    # plt.hist(sample)
    # plt.show()

    idle_start = 0.0
    idle_finish = 0.0
    idle_total = 0.0

    total_event_count = 0

    # 0 - server
    # 1..n - queue
    # status = 0
    queue = []
    times = []
    events = []
    firstclass_indices = []
    secondclass_indices = []


    def print_delta_time():
        nonlocal delta_time
        return f'{round(delta_time, 2):<10}'

    def print_departure_time():
        nonlocal departure_time
        return f'{round(departure_time, 2):<12}'

    def arrive():
        nonlocal delta_time, queue, departure_time, arrival_time

        # Updating the total (delta) time
        delta_time = current_min_time = min(arrival_time)

        # Get index of a nearest event time (type 1 or type 2)
        current_min_index = arrival_time.index(current_min_time)

        # Updating nearest event's time
        arrival_time[current_min_index] += current_min_time
        if len(queue) == 0:
            departure_time = delta_time + departure[current_min_index]()

        queue.append(current_min_index)
        print(f'{"(ARRIVAL)":<12} ', f'{("(" + str(current_min_index) + ")"):<6}', print_delta_time(),
              f'| {len(queue):<15} | {print_departure_time()} | q = {queue}')

        return current_min_index

    def depart():
        nonlocal delta_time, queue, departure_time

        delta_time = departure_time
        current_class = queue.pop(0)
        if len(queue) == 0:
            departure_time = float('inf')
        else:
            departure_time = delta_time + departure[current_class]()
        print(f'{"(DEPARTURE)":<12} ', f'{("(" + str(current_class) + ")"):<6}', print_delta_time(),
              f'| {len(queue):<15} | {print_departure_time()} | q = {queue}')

        return current_class

    def advance_in_time():
        nonlocal delta_time, queue, times, events, idle_start, idle_total, idle_finish, total_event_count

        current_class = 0

        if min(arrival_time) <= departure_time:
            current_class = arrive()
        else:
            current_class = depart()

        times.append(delta_time)
        events.append(len(queue))

        # Check if idle
        if len(queue) == 0 and idle_start != 0:
            idle_finish = delta_time
            idle_total += idle_finish - idle_start
            print(f'{"(IDLE)":<18} ', print_delta_time(), f': {0:<12}')

        total_event_count += 1

    print('Initial state:\n'
          f'queue: {queue}, status: {"empty" if len(queue) == 0 else "busy"}, '
          f'overall_simulation_time: {overall_simulation_time}, time: {arrival_time}'
          f'\n-------------------------------------------------------------\n'
          f'{"Event":<10} | {"Class"} | {"Delta time"} | {"Items in system"} | {"Departure at"} | q')

    while delta_time < overall_simulation_time:
        advance_in_time()

        # Updating the total (delta) time
        # delta_time = current_min_time = min(arrival_time)

        # If departure time is the nearest time - freeing the server and removing current active event from the queue
        # Event 3
        # if departure_time < current_min_time:
        # Remove the current active event from the queue
        # queue = queue[1:]
        # queue.pop(0)

        # Free the server
        # status = 0

        # Check if idle
        # if len(queue) == 0 and idle_start != 0:
        #    idle_finish = delta_time
        #    idle_total += idle_finish - idle_start
        #     continue

        # Get index of a nearest event time (type 1 or type 2)
        # current_min_index = arrival_time.index(current_min_time)

        # Updating nearest event's time
        # arrival_time[current_min_index] += current_min_time

        # If server is Free - calculate and update the departure time
        # if status == 0:
        # if len(queue) == 0:
        # Updating departure time to the time of a currently nearest event
        #    departure_time = arrival_time[current_min_index] + departure[current_min_index]()

        # Set server status to busy
        # status = 1

        # Add current event to the queue (type 1 or type 2)
        # queue.append(current_min_index + 1)

        # Update total count of events
        # total_event_count += 1

        # print(f'delta_time: {delta_time}, '
        #      f'total_event_count: {total_event_count}, '
        #      f'current_min_index: {current_min_index}, current_min_time: {current_min_time}\n'
        #      f'time: {arrival_time}\n'
        #      f'departure_time: {departure_time}\n'
        #      f'queue: {queue}\n'
        #      f'idle_total: {idle_total}, idle_finish: {idle_finish}, idle_start: {idle_start}\n')

    # Calculate idle coefficient
    idle_coefficient = idle_total / overall_simulation_time
    average_event_time = delta_time / total_event_count
    print(f'Idle coefficient: {idle_coefficient}\n'
          f'Average event time: {average_event_time}\n'
          f'Total event count: {total_event_count}\n')

    #firstclass_indices = events[events == 0]
    #secondsclass_indices = events[events == 1]

    plt.plot(times, events, '--g')
             #v for v in times.values() if v == 0], events, '--r',
             #[v for v in times.values() if v == 1], events, '--y')
    plt.xlabel("time")
    plt.ylabel("queue length")
    plt.grid()
    plt.show()


if __name__ == '__main__':
    start_simulation(overall_simulation_time=500)
