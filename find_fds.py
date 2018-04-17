
# -*- coding: utf-8 -*-
"""
Data Mining Programming Assignment

This script aims to discover approximate functional dependencies in a given 
data set.
"""
import sys
import time

def pprint(list_keys_fds):
    """
    Pretty print of discovered list_keys_fds
    """
    print('\nDiscovered list_keys_fds:')
    for fd in list_keys_fds:
        print(', '.join(fd[0]), " -> ", fd[1], ' with support ', fd[2])

def load_data(data_file_name):
    """
    Read data from data_file_name and return a list of lists, 
    where the first list (in the larger list) is the list of attribute names, 
    and the remaining lists correspond to the tuples (rows) in the file.
    """
    with open(data_file_name, 'r') as f:
        results = []
        for line in f:
                words = line.split(',')
                results.append(words[:])
    return results

def find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support):
    """
    Main function which you need to implement!
    
    The function discovers approximate functional dependencies in a given data
    
    Input:
        data_file_name  - name of a CSV file with data 
        depth_limit     - integer that limits the depth of search through the space of 
            domains of functional dependencies
        minimum_support - threshold for identifying adequately approximate list_keys_fds
        
    Output:
        list_keys_fds - a list of tuples. Each tuple represents a discovered FD.
        The first element of each tuple is a list containing LHS of discovered FD
        The second element of the tuple is a single attribute name, which is RHS of that FD
        The third element of the tuple is support for that FD
    
    Output example:
        [([A],C, 0.91), ([C, F],E, 0.97), ([A,B,C],D, 0.98), ([A, G, H],F, 0.92)]
        The above list represent the following list_keys_fds:
            A -> C, with support 0.91
            C, F -> E, with support 0.97 
            A, B, C -> D, with support 0.98
            A, G, H -> F, with support 0.92                   
    """
    # Read input data:
    input_data = load_data(data_file_name)
    
    # Transform input_data (list of lists) into some better representation.
    # You need to decide what that representation should be.
    # Data transformation is optional!
    
    # Get first row (headers)
    first_row = input_data[0]

    # Find total rows
    total_rows = len(input_data) - 1
    
    # Remove \n on the last column header
    first_row[-1] = first_row[-1].strip()

    # Create a dictionary of 
    # key = header column and 
    # value = index of column
    dic_header_to_index = {k: v for v, k in enumerate(first_row)}

    # Create a set that contains the header elements
    first_row_set = set(first_row)

    # Get a list of all possible keys of FDs
    list_keys_fds = find_all_keys(first_row, depth_limit)

    # Create a dictionary of FDs
    dic_fds = {}

    # Loop through the list of FD keys
    for i in range(len(list_keys_fds)):
        # Find remaining attributes that are not a part of the FD
        remaining = list(first_row_set - set(list_keys_fds[i]))

        # Loop through the remaining attributes
        for x in range(len(remaining)):
            # Register the key into the dictionary
            dic_fds[(tuple(list_keys_fds[i]), remaining[x])] = {}

    # A list container to store all the FDs up to depth_limit and satisfy minimum_support
    FDs = []

    # Loop through the keys in the dictionary
    for i in dic_fds:
        attr = list(i[0])

        # Go through each column in spreadsheet except the first row
        for x in input_data[1:]:
            tmp = []
            for z in attr: # Find keys
                tmp.append(x[dic_header_to_index[z]].strip())

            val = x[dic_header_to_index[i[1]]].strip()

            tmp_tuple = tuple(tmp)

            if tmp_tuple in dic_fds[i]:
                if val in dic_fds[i][tmp_tuple]:
                    dic_fds[i][tmp_tuple][val] = dic_fds[i][tmp_tuple][val] + 1
                else:
                    dic_fds[i][tmp_tuple][val] = 1
            else:
                dic_fds[i][tmp_tuple] = {}
                dic_fds[i][tmp_tuple][val] = 1
        
        # Calculate the sum
        sum = 0
        for x in dic_fds[i]:
            # Find the maximum key
            maxi = max(dic_fds[i][x], key=dic_fds[i][x].get)
            sum = sum + dic_fds[i][x][maxi]
        
        # Calculate the probability
        prob = sum / total_rows

        # Add probability to corresponding key if greater or equal to minimum support
        if prob >= minimum_support:
            FDs.append((list(i[0]), i[1], prob))
    
    return FDs

def find_all_keys(data, depth, target=[], output=[]):
    """
    Finding all possible keys of list_keys_fds via recursion
    (Combination problem)

    Input:
        data    - a list containing the first row elements
        depth   - integer that limits the depth of search through the space of 
                  domains of functional dependencies
        target  - threshold for identifying adequately approximate list_keys_fds
        output  - a list container that holds all the possible FD keys

    Output:
        output/list_keys_fds - a list of all FD keys.
    """
    for i in range(len(data)):
        new_target = target[:]
        new_data = data[:]
        new_target.append(data[i])
        new_data = data[i+1:]
        
        # Only consider keys up to length of depth
        if len(new_target) <= depth:
            output.append(new_target)
            find_all_keys(new_data, depth, new_target, output)
    return output

def avg_runtime(data_file_name, depth_limit, minimum_support, trial=1):
    """
    Calculates the average runtime of calculating the FDs

    Input:
        data_file_name  - name of a CSV file with data 
        depth_limit     - integer that limits the depth of search through the space of 
            domains of functional dependencies
        minimum_support - threshold for identifying adequately approximate list_keys_fds
        trial - an integer representing the number of runs to calculate FDs

    Output:
        runtime - a float that represents the average runtime
    """
    sum = 0
    for i in range(trial):
        # Start timer
        start_time = time.time()

        # Find FDs
        FDs = find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support)

        # Only print the first trial (i = 0)
        if i == 0:
            pprint(FDs)
            print()

        # Stop timer
        stop_time = time.time()

        # Calculate runtime
        runtime = stop_time - start_time

        # Print runtime result
        print('Runtime (%s): %s seconds' % (str(i + 1), str(runtime)))

        # Calculate runtime and sum them
        sum = sum + runtime

    # Return average
    return sum / trial

if __name__ == '__main__':
    # Parse command line arguments:
    if (len(sys.argv) < 3):
        print('Wrong number of arguments. Correct example:')
        print('python find_fds.py rssi.csv 3 0.91')
    else:
        data_file_name = str(sys.argv[1])
        depth_limit = int(sys.argv[2])
        minimum_support = float(sys.argv[3])

        # Accepts an optional 4th argument which is the number of trials to calculate FDs
        trial = int(sys.argv[4]) if 4 < len(sys.argv) else 1

        # Main function which you need to implement. 
        # It discover list_keys_fds in the input data with given minimum support and depth limit

        # Calculate average runtime and print FDs
        runtime = avg_runtime(data_file_name, depth_limit, minimum_support, trial)
        print('\nAverage Runtime: %s seconds (Average of %s trials)' % (str(runtime), str(trial)))