# 第2章: 文法と評価
ID = lambda x: x

# 第3章: チャーチ真偽値
TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
to_bool = lambda b: b(True)(False)
IF = lambda b: lambda t: lambda f: b(t)(f)
NOT = lambda b: b(FALSE)(TRUE)
AND = lambda a: lambda b: a(b)(FALSE)
OR = lambda a: lambda b: a(TRUE)(b)
XOR = lambda a: lambda b: a(NOT(b))(b)

# 第4章: チャーチ数
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
to_int = lambda n: n(lambda x: x + 1)(0)
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
TWO = SUCC(ONE)
THREE = SUCC(TWO)
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
SIX = SUCC(FIVE)
SEVEN = SUCC(SIX)
EIGHT = SUCC(SEVEN)
NINE = SUCC(EIGHT)
TEN = SUCC(NINE)
ADD = lambda m: lambda n: m(SUCC)(n)
MUL = lambda m: lambda n: lambda f: m(n(f))
POW = lambda m: lambda n: n(m)
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
IS_EVEN = lambda n: n(NOT)(TRUE)

# 第5章: ペアと引き算
PAIR = lambda a: lambda b: lambda s: s(a)(b)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
SHIFT = lambda p: PAIR(SECOND(p))(SUCC(SECOND(p)))
PRED = lambda n: FIRST(n(SHIFT)(PAIR(ZERO)(ZERO)))
SUB = lambda m: lambda n: n(PRED)(m)
LEQ = lambda m: lambda n: IS_ZERO(SUB(m)(n))
EQ = lambda m: lambda n: AND(LEQ(m)(n))(LEQ(n)(m))

# 第6章: 再帰と不動点コンビネータ
omega = lambda x: x(x)
FACT_GEN = lambda self: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(self(self)(PRED(n))))
      (ID)
)
FACT_BODY = lambda fact: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(fact(PRED(n))))
      (ID)
)
Y = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))
Z = lambda f: (
    (lambda x: f(lambda v: x(x)(v)))
    (lambda x: f(lambda v: x(x)(v)))
)
FACT = Z(FACT_BODY)
SUM_TO_N = Z(lambda sum_to_n: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ZERO)
      (lambda _: ADD(n)(sum_to_n(PRED(n))))
      (ID)
))
FIB = Z(lambda fib: lambda n: (
    IF(IS_ZERO(PRED(n)))
      (lambda _: n)
      (lambda _: ADD(fib(PRED(n)))
                       (fib(PRED(PRED(n)))))
      (ID)
))

# 第7章: リストと FizzBuzz
NIL = PAIR(TRUE)(TRUE)
CONS = lambda h: lambda t: PAIR(FALSE)(PAIR(h)(t))
IS_NIL = FIRST
HEAD = lambda l: FIRST(SECOND(l))
TAIL = lambda l: SECOND(SECOND(l))


def to_list(l, conv=lambda x: x):
    result = []
    while not to_bool(IS_NIL(l)):
        result.append(conv(HEAD(l)))
        l = TAIL(l)
    return result


RANGE = Z(lambda range_: lambda m: lambda n: (
    IF(LEQ(m)(n))
      (lambda _: CONS(m)(range_(SUCC(m))(n)))
      (lambda _: NIL)
      (ID)
))
FOLD = Z(lambda fold: lambda f: lambda z: lambda l: (
    IF(IS_NIL(l))
      (lambda _: z)
      (lambda _: f(HEAD(l))(fold(f)(z)(TAIL(l))))
      (ID)
))
MAP = lambda f: lambda l: (
    FOLD(lambda x: lambda acc: CONS(f(x))(acc))(NIL)(l)
)
SUM = FOLD(ADD)(ZERO)
# 前提：除数 n は 1 以上。n = ZERO は未定義で停止しない。
MOD = Z(lambda mod: lambda m: lambda n: (
    IF(LEQ(n)(m))
      (lambda _: mod(SUB(m)(n))(n))
      (lambda _: m)
      (ID)
))
# 前提：除数 n は 1 以上。n = ZERO は未定義で停止しない。
DIV = Z(lambda div: lambda m: lambda n: (
    IF(LEQ(n)(m))
      (lambda _: SUCC(div(SUB(m)(n))(n)))
      (lambda _: ZERO)
      (ID)
))
PUSH = lambda l: lambda x: FOLD(CONS)(CONS(x)(NIL))(l)
TO_DIGITS = Z(lambda digits: lambda n: (
    IF(LEQ(n)(NINE))
      (lambda _: CONS(n)(NIL))
      (lambda _: PUSH(digits(DIV(n)(TEN)))
                       (MOD(n)(TEN)))
      (ID)
))
ELEVEN = SUCC(TEN)
TWELVE = SUCC(ELEVEN)
THIRTEEN = SUCC(TWELVE)
FOURTEEN = SUCC(THIRTEEN)
to_str = lambda l: "".join(
    to_list(l, lambda c: "0123456789BFiuz"[to_int(c)])
)
FIZZ = CONS(ELEVEN)(
    CONS(TWELVE)(CONS(FOURTEEN)(CONS(FOURTEEN)(NIL)))
)
BUZZ = CONS(TEN)(
    CONS(THIRTEEN)(CONS(FOURTEEN)(CONS(FOURTEEN)(NIL)))
)
FIZZBUZZ_WORD = FOLD(CONS)(BUZZ)(FIZZ)
FIZZBUZZ_ITEM = lambda n: (
    IF(IS_ZERO(MOD(n)(THREE)))
      (lambda _: IF(IS_ZERO(MOD(n)(FIVE)))
          (lambda _: FIZZBUZZ_WORD)
          (lambda _: FIZZ)
          (ID))
      (lambda _: IF(IS_ZERO(MOD(n)(FIVE)))
          (lambda _: BUZZ)
          (lambda _: TO_DIGITS(n))
          (ID))
      (ID)
)
FIZZBUZZ = lambda n: MAP(FIZZBUZZ_ITEM)(RANGE(ONE)(n))

# 第8章: SKI コンビネータ
S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
I = S(K)(K)
