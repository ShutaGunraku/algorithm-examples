"""dynamic_programming.py: This module demonstrates an exemplative code of the dynamic programming paradigm.
    Neither python dictionaries or sets are used in this module.
    Complexities mentioned in this file is of Worst Time unless otherwise specified."""

__author__ = "Shuta Gunraku"

def best_schedule(weekly_income, competitions):
    """
    This function returns the maximum amount of money that can be earned by combining the personal training and
    the competitions.

    :param weekly_income: (list)
        a list of non-negative integers, where weekly_income[i] is the amount of money
        that will be earned as a personal trainer in week i.
    :param competitions: (list)
        a list of tuples, each representing a sporting competition. Each tuple contains 3 non-negative integers,
        (start_time, end_time, winnings).
        :var start_time: is the week that you will need to begin preparing for the competition.
        :var end_time:   is the last week that you will need to spend recovering from the competition.
        :var winning:    is the amount of money you will win if you compete in this competition.
    :return (int)
        the maximum amount of money that can be earned.
    :Complexity
        Let N be the total number of elements in weekly_income and competitions put together.
        Auxiliary Space Complexity: O(N)
            1d memo array which takes O(N)
        Space Complexity: O(N)
            2 inputs (weekly_income and competitions) == O(N), and with the auxiliary space complexity,
            O(2*N) == O(N)
        Time Complexity: O(NlogN)
            It takes O(N) to create memo array and iterate through all_income[] to save optimums into memo[],
            and it takes O(NlogN) time to sort all_income[]
    """

    # Initialise memo array with additional column to store income before week 0
    # base case: memo[i] == 0 if i == 0
    memo = [0] * (1 + len(weekly_income))
    all_income = competitions[:]

    # Convert weekly_income[] and formalise in the same style as competitions, then append to all_income[]
    for i in range(len(weekly_income)):
        tuple = (i,i,weekly_income[i])
        all_income.append(tuple)

    # sort() uses Timsort thus O(n log n) where n is len(competitions)
    all_income.sort(key=lambda x: x[1])

    # for each week, if the end_time of a tuple ends at that week,
    # check if the money optimal or not.
    # Time Complexity: The for loop itself costs O(weekly_income),
    # and while loop is executed twice every for loop iteration at worst case,
    # the complexity of which is O(1).
    # Thus the entire cost is O(weekly_income)*O(1) == O(weekly_income) < O(N) where N is len(all_income).
    j = 0
    for i in range(len(weekly_income)):
        while j < len(all_income) and all_income[j][1] == i:
            opt_income = memo[all_income[j][0]] + all_income[j][2]
            if opt_income > memo[all_income[j][1]+1]:
                memo[all_income[j][1]+1] = opt_income
            j += 1

    return memo[-1]

def best_itinerary(profit, quarantine_time, home):
    """
    This function returns the maximum amount of money that can be earned by a salesperson who lives on the coast
    and who can decide which cities to travel to and to work in.
    This function uses a 3d memo array (or three 2d arrays per se), dividing situations into 3 patterns
    and make recurrence relations and solve the problem.

    :param profit: (list)
        A list of lists. All interior lists are length n. Each interior list represents a different day.
        profit[d][c] is the profit that the salesperson will make by working in city c on day d.
    :param quarantine_time: (list)
        List of non-negative integers. quarantine_time[i] is the number of days city i requires visitors to
        quarantine before they can work there.
    :param home: (int)
        An integer between 0 and n-1 inclusive, which represents the city that the salesperson starts in.
    :return (int)
        The maximum amount of money that can be earned by the salesperson.
    :Complexity
        Let n be the number of cities, and d be the number of days.
        Auxiliary Space Complexity: O(n*d)
            3 memo arrays which takes O(3*n*d) == O(n*d)
        Space Complexity: O(n*d)
            3 inputs takes O(n*d + n + 1) == O(n*d) + (auxiliary space complexity) == O(n*d)
        Time Complexity: O(n*d)
            It takes O(3 * (n*d)) == O(n*d) time to create 3 memo arrays,
            and takes O(n*d) time to iterate through the 2d input array.
    """

    # profit is empty
    if len(profit) == 0:
        return 0

    # profit is only for 1 week
    if len(profit) == 1:
        return profit[0][home]

    # There's only one city
    if len(quarantine_time) == 1:
        sum = 0
        for day_salary in profit:
            sum += day_salary[0]
        return sum

    # Initialise 3d memo array, where each item of the most interior arrays
    # shows the maximum profit earned at city n from day d til the end,
    # in 3 cases: stay in the same city on the next day without quarantine on day d,
    #             move to an adjacent city on the next day without quarantine on day d,
    #             stay in the same city on the next day starting quarantine.
    memo = [[[0,0,0] for item in quarantine_time] for row in profit]

    for d in range(len(profit) - 1, -1, -1):
        for n in range(len(profit[d])):
            # base case: memo[d][n][0] is profit[d][n] if d is at end
            if d == len(profit) - 1:
                memo[d][n][0] = profit[d][n]
                if quarantine_time[n] == 0:
                    memo[d][n][2] = profit[d][n]
            else:
            # No quarantine on city n at day d, and stay in the same city til day d+1.
                memo[d][n][0] = profit[d][n] + max(memo[d + 1][n])

            # No quarantine on city n at day d, and move to an adjacent city on day d+1.
                # base case for memo[d][n][1]
                # If moved to an adjacent city on the last day, can only get profit from the second last day.
                if d == len(profit) - 2:
                    memo[d][n][1] = profit[d][n]

                # n at left most column
                elif n == 0:
                    memo[d][n][1] = max(profit[d][n] + memo[d+1][n+1][1] - profit[d+1][n+1], profit[d][n] + memo[d+2][n+1][2])
                # n at right most column
                elif n == len(profit[d]) - 1:
                    memo[d][n][1] = max(profit[d][n] + memo[d+1][n-1][1] - profit[d+1][n-1], profit[d][n] + memo[d+2][n-1][2])
                # n not in the left most nor the right most
                else:
                    profit_city_left = max(profit[d][n] + memo[d+1][n-1][1] - profit[d+1][n-1], profit[d][n] + memo[d+2][n-1][2])
                    profit_city_right = max(profit[d][n] + memo[d+1][n+1][1] - profit[d+1][n+1], profit[d][n] + memo[d+2][n+1][2])

                    memo[d][n][1] = max(profit_city_left, profit_city_right)

            # Start quarantine on city n at day d
                # check if index inside the range or not
                if d + (quarantine_time[n]) < len(profit):
                    quarantine_end = d + (quarantine_time[n])
                    memo[d][n][2] = max(memo[quarantine_end][n])
                # base case for memo[d][n][2]
                # if index out of range
                else:
                    memo[d][n][2] = 0

    # Deal with the cases where the salesman moves cities in the first day
    if home == 0:
        # if in city 0, it can move to city 1 in day 0
        opt_money = max(max(memo[0][home]), max(memo[0][home+1][1] - profit[0][home+1], memo[1][home+1][2]))
    elif home == len(quarantine_time) - 1:
        # if in last city, it can move to its left adjacent city in day 0
        opt_money = max(max(memo[0][home]), max(memo[0][home-1][1] - profit[0][home-1], memo[1][home-1][2]))
    else:
        # it can move to left or right city on day 0
        opt_money_right = max(max(memo[0][home]), max(memo[0][home+1][1] - profit[0][home+1], memo[1][home+1][2]))
        opt_money_left = max(max(memo[0][home]), max(memo[0][home-1][1] - profit[0][home-1], memo[1][home-1][2]))
        opt_money = max(opt_money_right, opt_money_left)

    return opt_money