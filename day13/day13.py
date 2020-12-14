"""

--- Day 13: Shuttle Search ---
Your ferry can make it safely to a nearby port, but it won't get much further. When you call to book another ship, you discover that no ships embark from that port to your vacation island. You'll need to get from the port to the nearest airport.

Fortunately, a shuttle bus service is available to bring you from the sea port to the airport! Each bus has an ID number that also indicates how often the bus leaves for the airport.

Bus schedules are defined based on a timestamp that measures the number of minutes since some fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea port. After that, each bus travels to the airport, then various other locations, and finally returns to the sea port to repeat its journey forever.

The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!

Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)

For example, suppose you have the following notes:

939
7,13,x,x,59,x,31,19
Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:

time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .
The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.

What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?

-- Part Two ---
The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute. (The first line in your input is no longer relevant.)

For example, suppose you have the same list of bus IDs as above:

7,13,x,x,59,x,31,19
An x in the schedule means there are no constraints on what bus IDs must depart at that time.

This means you are looking for the earliest timestamp (called t) such that:

Bus ID 7 departs at timestamp t.
Bus ID 13 departs one minute after timestamp t.
There are no requirements or restrictions on departures at two or three minutes after timestamp t.
Bus ID 59 departs four minutes after timestamp t.
There are no requirements or restrictions on departures at five minutes after timestamp t.
Bus ID 31 departs six minutes after timestamp t.
Bus ID 19 departs seven minutes after timestamp t.
The only bus departures that matter are the listed bus IDs at their specific offsets from t. Those bus IDs can depart at other times, and other bus IDs can depart at those times. For example, in the list above, because bus ID 19 must depart seven minutes after the timestamp at which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes after timestamp t.

In this example, the earliest timestamp at which this occurs is 1068781:

time     bus 7   bus 13  bus 59  bus 31  bus 19
1068773    .       .       .       .       .
1068774    D       .       .       .       .
1068775    .       .       .       .       .
1068776    .       .       .       .       .
1068777    .       .       .       .       .
1068778    .       .       .       .       .
1068779    .       .       .       .       .
1068780    .       .       .       .       .
1068781    D       .       .       .       .
1068782    .       D       .       .       .
1068783    .       .       .       .       .
1068784    .       .       .       .       .
1068785    .       .       D       .       .
1068786    .       .       .       .       .
1068787    .       .       .       D       .
1068788    D       .       .       .       D
1068789    .       .       .       .       .
1068790    .       .       .       .       .
1068791    .       .       .       .       .
1068792    .       .       .       .       .
1068793    .       .       .       .       .
1068794    .       .       .       .       .
1068795    D       D       .       .       .
1068796    .       .       .       .       .
1068797    .       .       .       .       .
In the above example, bus ID 7 departs at timestamp 1068788 (seven minutes after t). This is fine; the only requirement on that minute is that bus ID 19 departs then, and it does.

Here are some other examples:

The earliest timestamp that matches the list 17,x,13,19 is 3417.
67,7,59,61 first occurs at timestamp 754018.
67,x,7,59,61 first occurs at timestamp 779210.
67,7,x,59,61 first occurs at timestamp 1261476.
1789,37,47,1889 first occurs at timestamp 1202161486.
However, with so many bus IDs in your list, surely the actual earliest timestamp will be larger than 100000000000000!

What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?



"""
from datetime import datetime
from math import prod

def check_buses(t, bus_list):
    for i, bus in bus_list:
        if (t + i) % bus != 0:
            return False
    return True

if __name__ == "__main__":
    with open("input.txt") as input:
        lines = input.readlines()
        lines = [line.strip() for line in lines]
    depart_time = int(lines[0])
    bus_list = [int(bus) for bus in lines[1].split(",") if bus != "x"]

    print(depart_time, bus_list)
    min_wait_time = depart_time
    min_bus = None
    for bus in bus_list:
        wait_time = bus - depart_time % bus
        if wait_time < min_wait_time:
            min_wait_time = wait_time
            min_bus = bus
    print(min_bus, min_wait_time, min_bus*min_wait_time)

    # part 2
    # bus_list = [7, 13, "x", "x", 59, "x", 31, 19]
    # line = "7,13,x,x,59,x,31,19"
    line = "19,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,859,x,x,x,x,x,x,x,23,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,373,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,37"
    bus_list = [(i, int(bus)) for i, bus in enumerate(line.split(",")) if bus != "x"]
    # (i, n) in bus_list if x + i == 0 mod n
    # if x + i == 0 mod n then x == -i mod n
    # Since all of the bus times are prime then we can apply CRT and we look for a solution x = -i mod prod(n) for all n
    bus_mod_list = [n for (i, n) in bus_list]
    bus_prod = prod(bus_mod_list)
    print("bus_prod", bus_prod)
    start = datetime.now()
    # part 2
    # bus_list = [(50, 13014343)]
    t = 104601289 - 19
    i = 0
    while True:
        if check_buses(t, bus_list):
            break
        # t += bus0[1]
        # t += (7*19)
        # t += (19*859)
        t += 104601289  # (373*41*23)
        i += 1
        if i % 1000000 == 0:
            print(t)
    print("time =", t)
    end = datetime.now()
    print(end - start)

    """
    x = 0 mod 19 --
    x = 32 mod 41 --
    x = 840 mod 859 --
    x = 19 mod 23 =>  x + 27 = 0 mod 23
    x = 7 mod 13 --
    x = 15 mod 17
    x = 10 mod 29 --
    x = 323 mod 373
    x = 24 mod 37
    
    x + 19 = 0 mod 19
    x + 19 = 0 mod 41
    x + 19 = 0 mod 859
    x + 19 = 0 mod 29    
    x + 19 = 0 mod 13
    
    
    s = t + 19 == 0 mod 19
    s = t + 19 == 0 mod 859
    
    [(0, 19), (9, 41), (19, 859), (27, 23), (32, 13), (36, 17), (48, 29), (50, 373), (87, 37)]
    [(9, 41), (19, 859*19), (27, 23), (32, 13), (36, 17), (48, 29), (50, 373), (87, 37)]
    [(9, 41), (19, 859*19*13), (27, 23), (36, 17), (48, 29), (50, 373), (87, 37)]
    [(9, 41), (19, 859*19*13*17), (27, 23), (48, 29), (50, 373), (87, 37)]
    [(9, 41), (19, 859*19*13*17*29), (27, 23), (50, 373), (87, 37)]
    [(9, 41), (19, 859*19*13*17*29), (50, 373*23), (87, 37)]
    [(19, 859*19*13*17*29), (50, 373*23*37*41)]
        
    """