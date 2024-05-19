def set_nested_value(nested_list, indexes, value):
    current = nested_list
    for index in indexes[:-1]:
        current = current[index]
    current[indexes[-1]] = value


a = [[1, 2, 3], [4, 5, 6]]
b = [1,2]
c = [1, 0]

set_nested_value(a, c, b)
print(a)  # Output: [[1, 2, 3], [10, 5, 6]]