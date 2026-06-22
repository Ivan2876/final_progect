
import random

choice = random.choice([1, 0])

number = 10
# result = 0
# if choice != 0:
#     result = number / choice

#
# try:
#     print(choice)
#     result = number / choice
#     print(333333)
# except (ZeroDivisionError, MemoryError):
#     result = 855555676
#     print('111111')
# else:
#     print(9999999)
# finally:
#     print(999996688686868686886)
#     result = 99999
#
# print(result)

def foo():
    choice = random.choice([1, 0])

    number = 10
    try:
        print(choice)
        result = number / choice
        return result
    except (ZeroDivisionError, MemoryError):
        result = 855555676
        print('111111')
    else:
        print(9999999)
    finally:
        print(999996688686868686886)
        # result = 99999

    return result

resulttt = foo()
print(resulttt, 8888888)
