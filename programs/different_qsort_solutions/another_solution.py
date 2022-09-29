import random

def partition(array, start, end):
    pivot = array[start]
    left = start + 1
    right = end

    while True:
        while left <= right and array[right] >= pivot:
            right -= 1

        while left <= right and array[left] <= pivot:
            left += 1

        if left > right:
            break
        else:
            array[left], array[right] = array[right], array[left]

    array[start], array[right] = array[right], array[start]

    return right
    

def quicksort(array, start, end):
    if start < end:
        separator = partition(array, start, end)
        quicksort(array, start, separator - 1)
        quicksort(array, separator + 1, end)


arr = list(map(int, input().split()))
quicksort(arr, 0, len(arr) - 1)
print(*arr)