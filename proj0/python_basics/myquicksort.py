def quicksort(list):
    list1 = filter(lambda x: x < list[0], list)
    if len(list1) != 0 and len(list1) != 1:
        list1 = quicksort(list1)
    list2 = filter(lambda x: x > list[0], list)
    if len(list2) != 0 and len(list2) != 1:
        list2 = quicksort(list2)
    list3 = filter(lambda x: x == list[0], list)
    return list1 + list3 + list2

k = [3, 4, 2, 6, 10, 33, 22, 3]
if __name__ == '__main__':
    print quicksort(k)
