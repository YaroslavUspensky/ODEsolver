# ODESolver
В данном файле содержатся инструкции по использованию **ODESolver**

---

## Запуск приложения
Для начала работы запустите файл _main.py_.


___
## Работа с приложением

### First order solver
Решает уравнения первого порядка, заданные в нормальной форме:\
**_dy/dx = f(x, y)_**

Пользователь вводит правую часть такого уравнения, а также интервал поиска решения, и начальное условие для выделения частного решения.

В случае необходимости есть возможность указать **_n_** -- количество точек разбиения интервала **_(x0, x1)_**.

Расширенные настройки позволяют выбрать метод решения уравнения. В программе реализованы явные методы Рунге-Кутты
до 4 стадии _(erk1, erk2, erk3, erk4)_, а также схема Розенброка первой стадии _(ros1)_. 
Точность методов Рунге-Кутты возрастает с возрастанием стадии. 
Если решение ведет себя "неустойчиво" стоит использовать схему Розенброка _ros1_.
Параметр _alpha_ влияет на решение следующим образом:\
alpha = 0.5 -- устойчивые схемы со вторым порядком точности\
alpha = 1 -- схемы поустойчивее с первым порядком точности\
alpha = (1+i)/2 -- самые устойчивые схемы ваще жесть со вторым порядком точности

___
### High order solver
Решает уравнения высшый порядков (в тч неразрешенные относительно высшей производной), заданные в форме:\
**_F(x, y, y', y'', ...) = 0_**

Пользователь вводит функцию **_F_** (а предварительно порядок высшей производной). 
Производные вводятся в формате _"y_i"_ (без кавычек), где _i_ - порядок производной.
Сама функция **_y_** вводится как просто _"y"_ (без кавычек).

Интервал вводится аналогично **_First order solver_**.\
Начальные условия вводятся как tuple в следующем порядке:\
"(y(x0), y_1(x0), y_2(x0) ....)" (без кавычек)\
Число начальных условий должно равнятся порядку высшей производной + 1\
Подстановка всех начальных условий (x0, y(x0), y_1(x0), ...) в _**F**_ должна обнулять ее.

Под капотом уравнение сводится к дифференциально-алгебраической системе, 
которая решается неявной схемой Розенброка. Параметр _alpha_ отвечает за то же самое (см. First order solver)

---
### Slope field
Строит поле направлений уравнения первого порядка, заданного в нормальной форме (см. First order input)\
Интервалы задаются аналогично. 
_nx_ и _ny_ отвечают за число стрелочек по x и по y соответственно.

---
### Примеры ввода:
(Кавычки вводить не надо, знаки умножения надо)\
Уравнение первого порядка:
* "cos(x) + sin(y)", 
* "exp(cos(x**y))", 
* "12\*pi + exp(1)\*1E19 + x"

Уравнения высших порядков:
* "y_2 + 4 * y" (гармонический осцилятор)
* "y_2 - 9\*y + sin(3\*x) + exp(3*x)"

Интервал: 
* "(-10, 10)", 
* "(-2\*pi, 2\*pi)"

Начальное условие:
* "4" (для уравнения 1 порядка в нормальной форме)
* "(0, 1, 0)" (для уравнения 2 порядка)
* "(1E-3, 12, exp(1), pi, 2*pi)" (для уравнения 4 порядка)