import random

def quicksort(nums, fst, lst):
   if lst <= fst:
       return
 
   i = fst
   j = lst
   rand_num = random.randint(fst, lst)
   pivot = nums[rand_num]
 
   while j >= i:
       while nums[i] < pivot: i = i + 1
       while nums[j] > pivot: j = j - 1
       if j >= i:
           tmp = nums[i]
           nums[i] = nums[j]
           nums[j] = tmp
           i += 1
           j -= 1
   quicksort(nums, i, lst)
   quicksort(nums, fst, j)

def main():
    input_list = list(map(int, input().split()))

    size = len(input_list)
    quicksort(input_list, 0, size - 1)

    for element in input_list:
        print(element, end=" ")
    print()

if __name__ == "__main__":
    main()