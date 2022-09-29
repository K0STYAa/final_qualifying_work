# Quick sort solution by K.Shalavin.

import random

# quicksort returns nothing
# nums - input array
# fst - first element index to sort
# lst -  last element index to sort 


def quicksort(nums, fst, lst):
   if fst >= lst:
       return
 
   i, j = fst, lst
   pivot = nums[random.randint(fst, lst)]
 
   while i <= j:
       while nums[i] < pivot: i += 1
       while nums[j] > pivot: j -= 1
       if i <= j:
           nums[i], nums[j] = nums[j], nums[i]
           i, j = i + 1, j - 1
   quicksort(nums, fst, j)
   quicksort(nums, i, lst)

# main returns nothing
# no arguments
# input from stdin array of integers variables
# print to stdout sorted array

def main():
    input_list = list(map(int, input().split()))

    size = len(input_list)
    quicksort(input_list, 0, size - 1)

    print(*input_list)

# entrance to main
if __name__ == "__main__":
    main()