def merge_sort(array):
    number_of_inversions = 0
    if len(array) <= 1:
        return 0

    middle_point = len(array) // 2
    left_part = array[:middle_point]
    right_part = array[middle_point:]

    number_of_inversions += merge_sort(left_part)
    number_of_inversions += merge_sort(right_part)

    left_array_index = 0
    right_array_index = 0
    sorted_index = 0

    while left_array_index < len(left_part) and right_array_index < len(right_part):

        if left_part[left_array_index] <= right_part[right_array_index]:
            array[sorted_index] = left_part[left_array_index]
            left_array_index += 1
        else:
            array[sorted_index] = right_part[right_array_index]
            right_array_index += 1
            number_of_inversions += (len(left_part) - left_array_index)

        sorted_index += 1

    while left_array_index < len(left_part):
        array[sorted_index] = left_part[left_array_index]
        left_array_index += 1
        sorted_index += 1

    while right_array_index < len(right_part):
        array[sorted_index] = right_part[right_array_index]
        right_array_index += 1
        sorted_index += 1

    return number_of_inversions

numbers = [8, 4, 2, 1]
print('Unsorted array: ', numbers)
inversions = merge_sort(numbers)
print('Sorted array: ', numbers)
print('Number of inversions: ', inversions)