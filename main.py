import math

from integral_solver import (
    rect_method,
    simpson_method,
    runge_err,
    normalized_rect_method,
    normalized_simpson_method
)

k = 2


def ask(functions):
    print('Выберите функцию для интегрирования:')
    for i, fun in enumerate(functions, 1):
        print(f"{i}. {fun['s']}")

    fun_i = int(input())
    if not 1 <= fun_i <= len(functions):
        print('Неверное значение')
        dop()

    fun = functions[fun_i - 1]
    f, F, s = fun['f'], fun['F'], fun['s']

    print(f'''Выберите метод для вычисления интеграла функции: {fun["s"]}
            1. Метод левых прямоугольников
            2. Метод средних прямоугольников
            3. Метод правых прямоугольников
            4. Метод Симпсона'''
          )

    method = int(input())
    a, b = map(float, input('Введите границы интегрирования через пробел: ').split())
    n = int(input('Введите число разбиений: '))

    return f, F, s, method, a, b, n


def main():
    functions = [
        {
            'f': lambda x: -x ** 3 - x ** 2 - 2 * x + 1,
            'F': lambda x: -x ** 4 / 4 - x ** 3 / 3 - x ** 2 + x,
            's': '-x^3 - x^2 - 2x + 1'
        },
        {
            'f': lambda x: -4 * x ** 3 - 3 * x ** 2 - 2 * x + 10,
            'F': lambda x: -x ** 4 - x ** 3 - x ** 2 + 10 * x,
            's': '-4x^3 - 3x^2 - 2x + 10'
        },
        {
            'f': lambda x: -8 * x ** 3 - 6 * x ** 2 - 4 * x - 8,
            'F': lambda x: -2 * x ** 4 - 2 * x ** 3 - 2 * x ** 2 - 8 * x,
            's': '-8x^3 - 6x^2 - 4x - 8'
        }
    ]

    f, F, s, method, a, b, n = ask(functions)
    fun = None
    err_f = 0

    match method:
        case 1 | 2 | 3:
            fun = lambda: rect_method(f, a, b, method - 2, n)
            err_f = lambda: rect_method(f, a, b, method - 2, n // 2)
        case 4:
            fun= lambda: simpson_method(f, a, b, n)
            err_f = lambda: simpson_method(f, a, b, n // 2)

    res = fun()
    print('Результат вычисления:', res)
    print('Число разбиений:', n)

    err_abs = abs(F(b) - F(a) - res)
    print(f'Погрешность: {err_abs:.4f} ({abs(err_abs / (F(b) - F(a))):.2f}%)')

    res2 = err_f()
    err = runge_err(res, res2, k)
    print(f'Погрешность по правилу Рунге: {err:.4f}')
    print('По методу Ньютона-Лейбница:', F(b) - F(a))


def get_end_result(result):
    if not isinstance(result, tuple):
        return result

    status, res = result
    if status:
        return res

    return get_end_result(res)


def dop():
    functions = [
        {
            'f': lambda x: 1 / x,
            'F': lambda x: math.log(x),
            's': '1 / x'
        },
        {
            'f': lambda x: 1 / (3 - x) ** 0.5,
            'F': lambda x: -2 * (3 - x) ** 0.5,
            's': '1 / sqrt(3 - x)'
        },
    ]

    f, F, s, method, a, b, n = ask(functions)
    fun = None

    match method:
        case 1 | 2 | 3:
            fun = lambda: normalized_rect_method(f, F, a, b, method - 2, n)
        case 4:
            fun = lambda: normalized_simpson_method(f, F, a, b, n)

    res = fun()
    if res is None:
        print('Интеграл расходится')
    else:
        print('Результат вычисления:', res)


if __name__ == '__main__':
    main()
    dop()
