number = str(input('введите число: '))


def lkl(ho):
    ho = [int(i) for i in number]
    for x in ho:
        if len(ho) == 1:
            q = x
            return q ** 2
        elif len(ho) == 2:
            q, w = ho
            return q ** 2 + w ** 2
        elif len(ho) == 3:
            q, w, e = ho
            return q ** 2 + w ** 2 + e ** 2


print(lkl(number))
counter = 0
while counter != 8:
    counter += 1
    if lkl(number) == 1:
        print('число счастливое')
        break
    else:
        result = lkl(number)
        print(result)
        number = str(result)
        if counter == 8:
            print('число несчастливое')

