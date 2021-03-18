import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def start_simulation():
    delta_time = 0.0
    #time = {
    #    "delta": 0.0,
    #    "arrivalEvent2": np.random.gamma(shape=3, scale=0.5),
    #    "arrivalEvent1": np.random.poisson(lam=0.2),
    #    "departure": 501
    #}
    time = [np.random.gamma(shape=3, scale=0.5),
            np.random.poisson(lam=0.2)]
            #501]
    departure_time = 501
    #arrivalTimeEventType1 = np.random.gamma(shape=3, scale=0.5)
    #arrivalTimeEventType2 = np.random.poisson(lam=0.2)
    arrival = [
        lambda: np.random.gamma(shape=3, scale=0.5),
        lambda: np.random.poisson(lam=0.2)
    ]
    departure = [
        lambda: np.random.normal(15, 2),
        lambda: np.random.exponential(1/3)
    ]

    ### erlang
    import matplotlib.pyplot as plt

    def erlang(lam, s):
        return np.random.exponential(1./lam, size=s) \
               + np.random.exponential(1./lam, size=s) \
               + np.random.exponential(1./lam, size=s)

    sample = erlang(3.0, 1000)
    plt.hist(sample)
    plt.show()

    overall_simulation_time = 500
    #departureTime = 501
    #serverStatus = 0
    #queueType = 1
    #currentQueueLength = 0

    #def get_current_min_time():
    #    currentMin = min(time[1:].values())
    #    currentMinIndex = list(time[1:].values())[currentMin]
    #    return currentMin, currentMinIndex

    idle_start = 0.0
    idle_finish = 0.0
    total_idle = 0.0

    # 0 - server
    # 1..n - queue
    #model = [0]

    status = 0
    queue = []

    while delta_time < overall_simulation_time:

        # Check if idle
        if len(queue) == 0 and idle_start != 0:
            idle_finish = delta_time
            total_idle += idle_finish - idle_start
            continue

        # Updating the total (delta) time
        delta_time = current_min_time = min(time)

        # If departure time is the nearest time - freeing the server and removing current active event from the queue
        if departure_time < current_min_time:
            # Free the server
            status = 0

            # Remove the current active event from the queue
            #model = model[0::len(model) - 1]
            queue = queue[1:]

        # Get index of a nearest event time (type 1 or type 2)
        current_min_index = time.index(current_min_time)

        # Updating nearest event's time
        time[current_min_index] += current_min_time

        # Updating departure time to the time of a currently nearest event
        departure_time = time[current_min_index] + departure[current_min_index]

        queue.append(current_min_index + 1)
        status = 1

    # Calculate idle coefficient
    idle_coefficient = total_idle / overall_simulation_time
    print(f'Idle coefficient: {idle_coefficient}\n')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_simulation()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
