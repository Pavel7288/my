def sum_all_numbers(*, item):
    return sum(int(i) ** 2 for i in str(item))


def doing(numb: int, counter: int = 8) -> bool:
    for _ in range(counter):
        print(sum_all_numbers(item=numb))
        numb = sum_all_numbers(item=numb)
        if numb == 1:
            return True
    return False


try:
    number = int(input('введите число: '))

    if doing(sum_all_numbers(item=number)):
        print('счастливое')
    else:
        print('неа')
except ValueError:
    print('что-то не так')