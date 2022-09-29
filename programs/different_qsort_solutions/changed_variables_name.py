import random

def quicksort(array, x, y):
   if x >= y:
       return
 
   a, b = x, y
   tmp = array[random.randint(x, y)]
 
   while a <= b:
       while array[a] < tmp: a += 1
       while array[b] > tmp: b -= 1
       if a <= b:
           array[a], array[b] = array[b], array[a]
           a, b = a + 1, b - 1
   quicksort(array, x, b)
   quicksort(array, a, y)

def main():
    arr = list(map(int, input().split()))

    arr_size = len(arr)
    quicksort(arr, 0, arr_size - 1)

    print(*arr)

if __name__ == "__main__":
    main()