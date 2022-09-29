import random



def quicksort(nums, fst, lst):
   if    fst >= lst:
         return



   i ,  j =  fst,   lst
   pivot   =   nums[ random.randint(  fst ,  lst ) ]


   while  i  <=   j:
       while  nums[i ] < pivot: i +=   1
       while   nums[  j] > pivot: j -=  1
       if i <=   j:
           nums[i ], nums[j ] = nums[  j], nums[  i]
           i  ,   j =   i   + 1   , j  -   1
   quicksort(nums,   fst, j)
   quicksort(nums, i,    lst)


def main():
    input_list   =   list(   map(   int , input().split(  )))



    size   = len  (input_list)

    quicksort(input_list  ,   0, size - 1)
    print(*input_list  )



if __name__ == "__main__":

    main()