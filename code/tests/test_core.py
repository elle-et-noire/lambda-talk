import itertools
import math

import pytest

import lambda_core as c


def church(n):
    value = c.ZERO
    for _ in range(n):
        value = c.SUCC(value)
    return value


NUMERALS = [church(n) for n in range(36)]
BOOLS = [(False, c.FALSE), (True, c.TRUE)]


@pytest.mark.parametrize("value,b", BOOLS)
def test_not(value, b):
    assert c.to_bool(c.NOT(b)) is (not value)


@pytest.mark.parametrize("av,a", BOOLS)
@pytest.mark.parametrize("bv,b", BOOLS)
def test_binary_booleans(av, a, bv, b):
    assert c.to_bool(c.AND(a)(b)) is (av and bv)
    assert c.to_bool(c.OR(a)(b)) is (av or bv)
    assert c.to_bool(c.XOR(a)(b)) is (av != bv)


@pytest.mark.parametrize("bv,b", BOOLS)
@pytest.mark.parametrize("tv,t", BOOLS)
@pytest.mark.parametrize("fv,f", BOOLS)
def test_if(bv, b, tv, t, fv, f):
    assert c.to_bool(c.IF(b)(t)(f)) is (tv if bv else fv)


@pytest.mark.parametrize("n", range(11))
def test_unary_numerals(n):
    value = NUMERALS[n]
    assert c.to_int(value) == n
    assert c.to_int(c.SUCC(value)) == n + 1
    assert c.to_bool(c.IS_ZERO(value)) is (n == 0)
    assert c.to_bool(c.IS_EVEN(value)) is (n % 2 == 0)
    assert c.to_int(c.PRED(value)) == max(n - 1, 0)


@pytest.mark.parametrize("m,n", list(itertools.product(range(11), repeat=2)))
def test_binary_numerals(m, n):
    a, b = NUMERALS[m], NUMERALS[n]
    assert c.to_int(c.ADD(a)(b)) == m + n
    assert c.to_int(c.MUL(a)(b)) == m * n
    assert c.to_int(c.SUB(a)(b)) == max(m - n, 0)
    assert c.to_bool(c.LEQ(a)(b)) is (m <= n)
    assert c.to_bool(c.EQ(a)(b)) is (m == n)


@pytest.mark.parametrize("m,n", list(itertools.product(range(6), range(5))))
def test_pow(m, n):
    assert c.to_int(c.POW(NUMERALS[m])(NUMERALS[n])) == m ** n


def test_named_numerals():
    names = "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN"
    for n, name in enumerate(names.split()):
        assert c.to_int(getattr(c, name)) == n


def test_pairs_and_shift():
    first, second = object(), object()
    pair = c.PAIR(first)(second)
    assert c.FIRST(pair) is first
    assert c.SECOND(pair) is second
    for m, n in itertools.product(range(11), repeat=2):
        shifted = c.SHIFT(c.PAIR(NUMERALS[m])(NUMERALS[n]))
        assert c.to_int(c.FIRST(shifted)) == n
        assert c.to_int(c.SECOND(shifted)) == n + 1


@pytest.mark.parametrize("n", range(9))
def test_factorial(n):
    assert c.to_int(c.FACT(NUMERALS[n])) == math.factorial(n)
    assert c.to_int(c.FACT_GEN(c.FACT_GEN)(NUMERALS[n])) == math.factorial(n)


@pytest.mark.parametrize("n", range(36))
def test_sum_to_n(n):
    assert c.to_int(c.SUM_TO_N(NUMERALS[n])) == n * (n + 1) // 2


@pytest.mark.parametrize("n", range(16))
def test_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    assert c.to_int(c.FIB(NUMERALS[n])) == a


def test_strict_evaluation_diverges():
    with pytest.raises(RecursionError):
        c.Y(c.FACT_BODY)
    with pytest.raises(RecursionError):
        c.omega(c.omega)


def test_lazy_if():
    explode = lambda _: c.omega(c.omega)
    assert c.IF(c.TRUE)(lambda _: c.ONE)(explode)(c.ID) is c.ONE
    assert c.IF(c.FALSE)(explode)(lambda _: c.ZERO)(c.ID) is c.ZERO


def test_list_primitives_and_windows():
    assert c.to_bool(c.IS_NIL(c.NIL)) is True
    assert c.to_list(c.NIL) == []
    head = object()
    value = c.CONS(head)(c.NIL)
    assert c.to_bool(c.IS_NIL(value)) is False
    assert c.HEAD(value) is head
    assert c.TAIL(value) is c.NIL
    assert c.to_list(value) == [head]
    assert c.to_list(value, lambda x: x is head) == [True]


@pytest.mark.parametrize("m,n", list(itertools.product(range(11), repeat=2)))
def test_range_fold_map_sum(m, n):
    value = c.RANGE(NUMERALS[m])(NUMERALS[n])
    reference = list(range(m, n + 1))
    assert c.to_list(value, c.to_int) == reference
    assert c.to_int(c.SUM(value)) == sum(reference)
    mapped = c.MAP(c.SUCC)(value)
    assert c.to_list(mapped, c.to_int) == [x + 1 for x in reference]
    # A noncommutative combiner verifies right-fold order and f(x)(acc).
    fold = c.FOLD(lambda x: lambda acc: [c.to_int(x), acc])("end")(value)
    expected = "end"
    for x in reversed(reference):
        expected = [x, expected]
    assert fold == expected
    if reference:
        assert c.to_int(c.HEAD(value)) == m
        assert c.to_list(c.TAIL(value), c.to_int) == reference[1:]
    else:
        assert c.to_bool(c.IS_NIL(value)) is True


@pytest.mark.parametrize("m,n", list(itertools.product(range(21), range(1, 8))))
def test_mod_div(m, n):
    assert c.to_int(c.MOD(NUMERALS[m])(NUMERALS[n])) == m % n
    assert c.to_int(c.DIV(NUMERALS[m])(NUMERALS[n])) == m // n


@pytest.mark.parametrize("n", [*range(21), 42, 99, 100, 123, 200])
def test_digits(n):
    value = c.TO_DIGITS(church(n))
    assert c.to_list(value, c.to_int) == [int(x) for x in str(n)]
    assert c.to_str(value) == str(n)


def fizzbuzz_reference(n):
    return [("Fizz" if x % 3 == 0 else "")
            + ("Buzz" if x % 5 == 0 else "") or str(x)
            for x in range(1, n + 1)]


@pytest.mark.parametrize("n", [0, 1, 2, 3, 5, 10, 15, 20, 30])
def test_fizzbuzz(n):
    assert c.to_list(c.FIZZBUZZ(church(n)), c.to_str) == fizzbuzz_reference(n)


def test_char_encoding_and_words():
    chars = c.RANGE(c.ZERO)(c.FOURTEEN)
    assert c.to_str(chars) == "0123456789BFiuz"
    assert c.to_str(c.FIZZ) == "Fizz"
    assert c.to_str(c.BUZZ) == "Buzz"
    assert c.to_str(c.FIZZBUZZ_WORD) == "FizzBuzz"


def test_ski():
    value = object()
    assert c.I(value) is value
    assert c.S(c.K)(c.K)(value) is value
    t, f = object(), object()
    assert c.K(t)(f) is c.TRUE(t)(f) is t
    assert c.K(c.I)(t)(f) is c.FALSE(t)(f) is f
