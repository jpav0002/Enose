#!/usr/bin/env python3

arr = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
mean = len(arr)
new_arr = [0]*len(arr[0])
for array in arr:
    it = 0
    for val in array:
        new_arr[it] += val
        it += 1

average = [x / mean for x in new_arr]
print(average)
