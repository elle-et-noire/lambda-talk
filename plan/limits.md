# 実行上限と講義で使う値

測定日: 2026-10-15。指定された `.venv/bin/python` を使用した。
この venv の実体は **CPython 3.14.7** であり、依頼に記載された
Python 3.12 とは異なる。以下はこの環境での結果である。
再帰上限はデフォルトの **1000** のまま測定した。

## 測定条件

- 入力の自然数は `ZERO` から `SUCC` を n 回適用して構築した。
- 通常実行は新しい Python プロセスのトップレベルで実行した。
- doctest は実際の `tools/check_slides.py --preload-core` を通した。
  数を構築する窓 `to_n` は観測開始前に戻るため、そのフレームは
  演算中に残らない。doctest の実行用フレームは残る。
- 返り値は通常の Python の参照実装と比較した。各候補は新しい
  プロセスで実行し、成功値と次の失敗値を再確認した。
- 探索は倍増と二分探索。1 プロセスの時間予算は 15 秒。
  時間切れは `RecursionError` と区別した。時間による境界は
  マシンの負荷で動くため、「今回完了を確認できた値」として読む。
- 安全値は通常実行と doctest の小さい方の 80% 以下を基本とする。
  階乗・累乗は、計算時間にも余裕がある講義用の値を選ぶ。

## 結果を最後まで観測した上限

表の n は Church 数で渡す入力を表す。`POW` は下の表記ごとに
指数または底を変化させた。各欄の「次の値」は最大値 + 1。

| 観測 | 通常実行 | doctest | 小さい方 | 次の値の結果 | 安全な n |
|---|---:|---:|---:|---|---:|
| FACT の整数化 | 11 | 11 | 11 | 15 秒で時間切れ | 8 |
| SUM_TO_N の整数化 | 44 | 44 | 44 | RecursionError | 35 |
| FIB の整数化 | 16 | 16 | 16 | RecursionError | 12 |
| SUCC で作った数の整数化 | 997 | 992 | 992 | RecursionError | 793 |
| RANGE + to_list（各要素も整数化） | 247 | 246 | 246 | RecursionError | 196 |
| SUM(RANGE) の整数化 | 44 | 44 | 44 | RecursionError | 35 |
| FIZZBUZZ + to_list/to_str | 247 | 246 | 246 | RecursionError | 196 |
| MOD の整数化、除数 1〜7 をすべて確認 | 495 | 493 | 493 | RecursionError | 394 |
| DIV の整数化、除数 1〜7 をすべて確認 | 495 | 493 | 493 | RecursionError | 394 |
| TO_DIGITS + to_str | 979 | 974 | 974 | RecursionError | 779 |
| POW、底 TWO・指数 n | 27 | 26 | 26 | 15 秒で時間切れ | 20 |
| POW、底 n・指数 FOUR | 110 | 108 | 108 | 15 秒で時間切れ | 86 |

呼び出しはそれぞれ次の形である。`N` は上記の SUCC 鎖で構築した数。
MOD/DIV は正の除数だけを対象とし、上限の支配要因は除数 1 だった。
doctest の n=494 では、除数 1 が失敗し、2〜7 は成功することも確認した。

```python
to_int(FACT(N))
to_int(SUM_TO_N(N))
to_int(FIB(N))
to_int(N)
to_list(RANGE(ONE)(N), to_int)
to_int(SUM(RANGE(ONE)(N)))
to_list(FIZZBUZZ(N), to_str)
to_int(MOD(N)(D))
to_int(DIV(N)(D))
to_str(TO_DIGITS(N))
to_int(POW(TWO)(N))
```

指数 FOUR の測定は `to_int(POW(N)(FOUR))` を使用した。
講義では底 0〜5・指数 0〜4 程度で十分であり、0 の 0 乗は 1 となる。

## 大きな階乗・累乗のスタック上限

`MUL` と `POW` は関数の合成で数を表す。一方、`ADD` は SUCC の鎖を
作る。この違いにより、階乗や累乗の値そのものが 1000 を超えても
直ちに再帰上限に達するとは限らない。例えば `POW(TWO)(TEN)` は
**1024** を返し、通常実行・doctest の両方で成功した（約 0.2 ms）。

巨大な値については、観測の先頭経路を実行して深さを測定した。
窓の増分関数を同じ 1 フレームの `to_tick` に置き換え、最初の増分で
あらかじめ作った `StopIteration` を投げる。数を作る純粋な定義と
`to_int` 自体のフレーム数は同じに保つ。

SUCC の本体 `f(n(f)(x))` は内側の x を先に評価するため、最初の
増分に向かう経路に最も多くの呼び出しが積み重なる。MUL による
この反復の合成でも、後続の増分は同じ深さ以下を通る。
数の構築部分も、先頭の増分までに実行済みとなる。
したがって、先頭経路から観測全体のスタック上限を推定できる。

この性質を `sys.setprofile` による全観測の最大深さと照合した。
FACT 0〜8、底 TWO の POW の指数 0〜10、指数 FOUR の POW の底 1〜8 の
**28 ケースすべて**で、
先頭増分の深さと全観測の最大深さが一致した。
通常実行の観測部分の Python フレーム数は、FACT で
`n(n+1)/2 + 4`、底 TWO の POW で `2n + 3` となった。

| 先頭経路から推定したスタック上限 | 通常実行 | doctest | 小さい方 |
|---|---:|---:|---:|
| FACT の n | 44 | 44 | 44 |
| POW、底 TWO の指数 n | 498 | 496 | 496 |
| POW、指数 FOUR の底 n | 249 | 248 | 248 |

先頭経路の次の値では、どちらも `RecursionError` を確認した。
これらは先頭経路から推定した上限であり、巨大な整数への全変換を
完走した範囲は前の表に記載した。FACT 11 は約 10 秒かかり、
FACT 12 は 15 秒で時間切れになった。講義では FACT 8 以下、
底 TWO の POW は指数 10（1024）を推奨する。

## FIB の時間

数の構築と整数への観測を含む。doctest 欄には例の実行間の小さな
管理コストも含む。起動・コアの読み込み時間は含まない。

| n | FIB の値 | 通常実行 (ms) | doctest (ms) |
|---:|---:|---:|---:|
| 13 | 233 | 4.73 | 4.70 |
| 14 | 377 | 7.49 | 9.38 |
| 15 | 610 | 12.32 | 10.97 |
| 16 | 987 | 18.76 | 20.96 |

FIB 17 は両方の実行方法で `RecursionError`。
講義の推奨は FIB 12（144）以下である。

## FizzBuzz の講義例

**FizzBuzz 1〜15 はデフォルトの再帰上限 1000 で成功した。**
通常実行で約 3.05 ms、doctest で約 3.05 ms。
再帰上限の引き上げは不要である。

```text
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz,
11, Fizz, 13, 14, FizzBuzz
```

## 再現方法と生データ

```sh
.venv/bin/python tools/measure_limits.py
.venv/bin/python tools/measure_limits.py \
  --kinds FACT POW_TWO POW_BASE --stack-prefix \
  --output plan/limits-prefix.json
.venv/bin/python tools/measure_limits.py \
  --verify-prefix-profile --output plan/limits-profile.json
.venv/bin/python -m pytest code/tests -q
.venv/bin/python tools/check_slides.py \
  code/tests/fixtures/sample.md
```

- [limits.json](limits.json): 全結果の観測、候補ごとの成否、時間。
- [limits-prefix.json](limits-prefix.json): 先頭経路の深さの境界。
- [limits-profile.json](limits-profile.json): 全観測と先頭経路の深さの照合。

pytest 内や REPL のラッパー内では、さらにフレームが増える。
境界値の再現には上記の通常実行・検証ツールの経路を使用する。
