
import random

N = ["Вы", "Компьютер"]
K = 5
A = ["ставите", "ставит"]
B = ["говорите", "говорит"]
C = ["теряете", "теряет"]


def roll(n):

    r = []
    for i in range(n):
        r.append(random.randint(1, 6))
    return r


def count_value(h, v):

    t = 0
    for a in h:
        for d in a:
            if d == v or (d == 1 and v != 1):
                t = t + 1
    return t


def is_valid(c, v, p, q):
    if v < 1 or v > 6 or c < 1:
        return False
    if p == 0:
        return True
    if q != 1 and v != 1:
        return c > p or (c == p and v > q)
    if q != 1 and v == 1:
        return c >= (p + 1) // 2
    if q == 1 and v != 1:
        return c >= p * 2 + 1
    return c > p


def expected(a, v, t):
    m = 0
    for d in a:
        if d == v or (d == 1 and v != 1):
            m = m + 1
    o = t - len(a)
    if v == 1:
        s = 1 / 6
    else:
        s = 1 / 3
    return m + o * s


def bot_move(a, t, p, q):

    o = []
    for c in range(1, t + 1):
        for v in range(1, 7):
            if is_valid(c, v, p, q) and expected(a, v, t) >= c - 0.5:
                o.append((c, v))
    if p > 0:
        if expected(a, q, t) < p - 1.5 or len(o) == 0:
            return ("doubt",)
        if random.random() < 0.1:
            return ("doubt",)
    if len(o) == 0:
        return ("bid", 1, random.randint(2, 6))
    b = random.choice(o[:4])
    return ("bid", b[0], b[1])


def human_move(a, t, p, q):
    # ход человека
    print("Ваши кости:", a)
    while True:
        if p == 0:
            s = input("Ваша ставка (например '3 5' = три пятёрки): ")
        else:
            s = input("Ваша ставка ('3 5') или 'н' = не верю: ")
        s = s.strip().lower()
        if s == "н" and p > 0:
            return ("doubt",)
        x = s.split()
        if len(x) == 2 and x[0].isdigit() and x[1].isdigit():
            c = int(x[0])
            v = int(x[1])
            if c <= t and is_valid(c, v, p, q):
                return ("bid", c, v)
        print("Так нельзя. Ставка должна быть выше предыдущей.")
        print("Подсказка: единицы - джокеры; на единицы можно ставить вдвое меньше")


def play():
    L = [K, K]
    u = 0
    n = 0

    while L[0] > 0 and L[1] > 0:
        n = n + 1
        print("\n" + "=" * 40)
        print("Раунд", n)
        print("Костей:  Вы -", L[0], "| Компьютер -", L[1])

        H = [roll(L[0]), roll(L[1])]
        T = L[0] + L[1]

        p = 0
        q = 0
        w = -1

        while True:
            if u == 0:
                m = human_move(H[0], T, p, q)
            else:
                m = bot_move(H[1], T, p, q)

            if m[0] == "doubt":
                print(N[u], B[u], ": НЕ ВЕРЮ!")
                break

            p = m[1]
            q = m[2]
            w = u
            print(N[u], A[u], ":", p, "x", q)
            u = 1 - u

        print("\nВсе открывают кости:")
        print("  Вы:", H[0])
        print("  Компьютер:", H[1])
        r = count_value(H, q)
        print("Ставка была:", p, "x", q, "| на самом деле:", r)

        if r >= p:
            z = u
        else:
            z = w
        print(N[z], C[z], "одну кость.")
        L[z] = L[z] - 1
        u = z

    print("\n" + "=" * 40)
    if L[0] > 0:
        print("Вы победили!")
    else:
        print("Компьютер победил. Попробуйте ещё раз!")


play()