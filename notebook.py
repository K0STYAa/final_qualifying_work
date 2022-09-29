# 0-100%
import matplotlib.pylab as plt
import collections

my_dict = {}
od = collections.OrderedDict(sorted(my_dict.items()))
print(od)
sum = 0
for _, value in od.items():
  sum += value
print(sum)
od.pop(0.0)

myList = od.items()
myList = sorted(myList)
sum2 = 0
for key, value in od.items():
  sum2 += value
  if sum2 > sum * 0.99 - 7411:
    print(key)
    break
x, y = zip(*myList) 

plt.plot(x, y)
plt.show()


# 0-20%
import matplotlib.pylab as plt

my_dict = {}
sum = 0
for _, value in my_dict.items():
  sum += value
print(sum)
print(100*my_dict[0.0]/sum, "%", sep="")
my_dict.pop(0.0)
list_to_pop = []
for key in my_dict.keys():
  if key > 20:
    list_to_pop.append(key)
for key in list_to_pop:
  my_dict.pop(key)

myList = my_dict.items()
myList = sorted(myList) 
x, y = zip(*myList) 

plt.plot(x, y)
plt.show()