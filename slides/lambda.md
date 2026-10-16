---
marp: true
theme: quiet
paginate: true
math: katex
size: 16:9
title: ラムダ計算を Python で動かす
author: elle-et-noire
description: Python の 1 引数 lambda で真偽値・自然数・足し算・再帰を作り、ラムダ計算を動かして学ぶ入門講義
lang: ja
---

<!-- _class: title -->
<!-- _paginate: false -->

# ラムダ計算を Python で動かす

## 1 引数の lambda で真偽値・数・再帰を作る

Python の lambda で真偽値・自然数・足し算を作り、最後に Y コンビネータで再帰を書きます。

<div class="small">

elle-et-noire ・ [github.com/elle-et-noire/lambda-talk](https://github.com/elle-et-noire/lambda-talk)

</div>

<!--
目安 0.5 分。こんにちは。今日はラムダ計算 (lambda calculus) を Python で動かしてみます。ふだん言語に用意されている真偽値や数、足し算を、引数が 1 つの lambda を組み合わせて自分で作ります。最後は Y コンビネータを使って再帰も書きます。
-->

---

## 今日作るもの

- **真偽値**：`TRUE`、`FALSE`、`IF`
- **自然数**：チャーチ数 (Church numerals) `ZERO`、`SUCC`
- **足し算**：`ADD`（掛け算・累乗も）
- **再帰**：Y コンビネータ (Y combinator) と、その仲間 Z

最後には、lambda だけで作った階乗が動く。

```text
to_int(FACT(FIVE))   →   120
```

<div class="note">

コード：[Colab ノートブック（lambda.ipynb）](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb)。§番号は章番号に対応

</div>

<!--
目安 0.5 分。今日作るものはこの 4 つです。真偽値、自然数、足し算、そして再帰です。最後には、lambda だけで作った階乗 FACT に、lambda だけで作った 5 を渡して、120 が出てくるところまで行きます。to_int は結果を Python の整数に変換して見るための関数で、すぐ後で説明します。今日のコードは Colab のノートブックにまとめてあり、章と同じ番号の節で手元でも試せます。
-->

---

## lambda と関数呼び出しだけで書く

ラムダ計算の項は、変数・関数を作る式・関数呼び出しの 3 種類だけ。そこで Python でも次のものだけで書く。

- 1 引数の `lambda` と関数呼び出し `f(x)`
- 式に付ける名前（`ADD = ...`）。名前は定義の右辺に置き換えられる

数値リテラル、`True`・`False`、`if`、`class`、`+` や `==` などの演算子は使わず、真偽値・数・分岐・再帰を関数で作る。

例外：`to_bool`、`to_int`、`to_list`、`to_str` は、結果を Python の値に変換して表示するための関数。数値リテラルや `+` も使う普通の Python で書き、計算の途中では使わない。

<!--
目安 1 分。ラムダ計算の項は、変数と、関数を作る式と、関数呼び出しの 3 種類だけです。そこで Python でも、引数が 1 つの lambda と関数呼び出しだけで書きます。式には ADD = … のように名前を付けます。名前が出てくるところは、定義の右辺に置き換えられます。数値リテラル、True と False、if、class、足し算や比較の演算子は使わず、真偽値や数、分岐、再帰を関数で作ります。例外は to_ で始まる変換関数です。lambda で作った TRUE や 3 は、print しても function としか表示されないので、Python の True や 3 に変換して表示します。変換関数は普通の Python で書き、計算の途中には入れません。
-->

---

## 時間割

<div class="small">

| 章 | 内容 | 必須 | 発展 |
|---|---|---:|---:|
| [1](#ch1) | 導入：Church と Turing | 2.5 分 | |
| [2](#ch2) | 文法と評価：Python との対応 | 4.75 分 | 1.75 分 |
| [3](#ch3) | チャーチ真偽値 | 6.25 分 | 2 分 |
| [4](#ch4) | チャーチ数：足し算・掛け算 | 8.25 分 | 3 分 |
| [5](#ch5) | ペアと引き算 | 4 分 | 6 分 |
| [6](#ch6) | 再帰と Y コンビネータ | 15.5 分 | 2 分 |
| [7](#ch7) | リストと FizzBuzz | | 15.25 分 |
| [8](#ch8) | SKI コンビネータ | | 6.5 分 |
| [9](#ch9) | まとめと先へ | 3 分 | 1 分 |

</div>

必須のみ約 46.5 分（冒頭 2.25 分込み）。「発展」は時間次第で飛ばす。

<!--
目安 0.25 分。見せるだけにします。必須だけで約 45 分、右上に「発展」とあるスライドは時間を見て飛ばします。いちばん時間を使うのは 6 章です。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch1">1</span>導入

目安 2.5 分

<!--
目安 0.25 分。まず、なぜこんなことをするのか、背景の話を少しします。
-->

---

## Python の道具を減らしていく

Python にはたくさんの道具がある。

- 数と演算子、`if` と `while`、`class`、`def`……

これらの道具を減らしていくと、どこで「計算」できなくなるか。

答え：関数を作ることと関数を呼ぶことがあれば足りる。

<!--
目安 0.75 分。Python には、数や演算子、if、while、class、def と、たくさんの道具があります。これを 1 つずつ取り上げていくと、どこで計算できなくなるかを考えます。答えを先に言うと、関数を作ることと関数を呼ぶことが残っていれば、数や分岐や再帰は作り直せます。今日はそれを実際にコードを書いて確かめます。
-->

---

## 1930 年代：二つの「計算」の定義

| | Church（1936） | Turing（1936–37） |
|---|---|---|
| モデル | ラムダ計算 | チューリング機械 (Turing machine) |
| 中身 | 関数を作る・呼ぶ | テープを読み書きする |

- **定理**（Turing 1937）：ラムダ計算で定義できる関数と、チューリング機械で計算できる関数は一致する
- **Church–Turing thesis**：人が機械的な手順（アルゴリズム）で計算できる関数は、ちょうどこの定理の関数である、という主張
- 「機械的な手順」は数学的に定義された概念ではないので、thesis は証明できる定理ではない。計算可能性の定義として受け入れられている

<!--
目安 1.5 分。1930 年代に、「計算できる」とはどういうことかを数学的に定義しようとした人が二人います。アロンゾ・チャーチはラムダ計算、つまり関数を作って呼ぶだけの体系を考えました。アラン・チューリングは、テープに記号を読み書きする機械を考えました。どちらも 1936 年ごろに論文を出し、「機械的に解けない問題がある」ことを示しました（λ記法自体は 1932 年の論文で導入）。Church はその論文で、実効的に計算できる関数を、ラムダ計算で定義できる関数と同一視することを提案しました。Turing も独立に、機械的に計算できる関数はチューリング機械で計算できる関数だ、と主張しました。1937 年に Turing は、ラムダ計算で定義できる関数とチューリング機械で計算できる関数が一致することを証明しました。ここまでは証明された事実です。そのうえで、人が機械的な手順で計算できる関数は、ちょうどこれらの関数である、という主張を Church–Turing thesis と呼びます。「機械的な手順」は数学的に定義された概念ではないので、これは証明できる定理ではなく、計算可能性の定義として受け入れられている主張です。受け入れられている理由は、λ計算、チューリング機械、一般再帰関数という、独立に提案されたモデルがどれも同じ関数の範囲を与えたことです。今日は、そのうちラムダ計算を Python で動かします。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch2">2</span>文法と評価

目安 4.75 分（発展 +1.75 分）

コード：[Colab §2](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec2)

<!--
目安 0.25 分。この章では、ラムダ計算の基本の用語を、Python のコードで何に当たるかと対応させて確認します。取り上げるのは、この後の章で使う用語だけです。
-->

---

## λ記法と Python の lambda：項は 3 種類

| 項 (term) | λ記法 | Python |
|---|---|---|
| 変数 (variable) | $x$ | `x` |
| 抽象 (abstraction) | $\lambda x.\,M$ | `lambda x: M` |
| 適用 (application) | $M\,N$ | `M(N)` |

$\lambda$ → `lambda`、ドット → コロン、$M\,N$ → `M(N)`。数や `if` に当たる項はない。

```python
>>> ID = lambda x: x
>>> ID("a"), ID(ID)("b")
('a', 'b')
```

<!--
目安 1 分。ラムダ計算の式を項と呼び、項は 3 種類だけです。変数は Python の名前、抽象は lambda 式、適用は関数呼び出しに当たります。ギリシャ文字のラムダが Python のキーワード lambda、ドットがコロンに対応し、λ記法では関数の呼び出しを f x のように並べて書きます。Python の lambda という名前も、このラムダ計算から来ています。数や if に当たる項はありません。最初の定義として、受け取った値をそのまま返す恒等関数 ID を作ります。3 章以降で何度も使います。文字列 "a" は結果を見るためだけに渡し、定義の中には使いません。
-->

---

## カリー化：2 引数の関数を `f(a)(b)` で呼ぶ

```python
>>> (lambda x: lambda y: x)("a")
<function <lambda>.<locals>.<lambda> at 0x...>
>>> (lambda x: lambda y: x)("a")("b")
'a'
```

- `lambda x, y: x` の代わりに `lambda x: lambda y: x` と書く：カリー化 (currying)
- `f(a)` は、残りの引数 `y` を受け取る関数を返す
- λ記法の $f\,a\,b$ は $(f\,a)\,b$（適用は左結合）。Python の `f(a)(b)`
- $\lambda x.\,M\,N$ の本体は $M\,N$ 全体。Python の `lambda x: M(N)`

<!--
目安 0.75 分。この講義では lambda の引数を 1 つだけにしています。Python なら lambda x, y: x と書く 2 引数の関数は、x を受け取って「y を受け取る関数」を返す形で、lambda x: lambda y: x と書きます。これをカリー化と呼びます。f(a) だけを評価すると、y を待つ関数が返ってきます。それに b を渡すと答えが出ます。λ記法では f a b と並べて書き、左から (f a) b と読みます。Python の f(a)(b) と同じです。また、λx. M N は M N 全体が本体です。
-->

---

## 束縛変数と自由変数：引数と外側の名前

```python
>>> (lambda y: lambda x: (x, y))("外")("引数")
('引数', '外')
```

内側の `lambda x: (x, y)` だけを見ると

- `x`：この lambda の引数。束縛変数 (bound variable)
- `y`：この lambda の外で決まる名前。自由変数 (free variable)

Python の引数・ローカル変数が束縛変数、外側の関数やグローバルの名前の参照が自由変数に当たる。

<!--
目安 0.5 分。lambda の引数として受け取る名前を束縛変数、その lambda の外で決まる名前を自由変数と呼びます。内側の lambda x: (x, y) では、x が束縛変数、y が自由変数です。Python では、引数やローカル変数が束縛変数、外側の関数やグローバルの名前を参照するのが自由変数です。
-->

---

## β簡約：関数を呼ぶと引数が本体に代入される

$$(\lambda x.\,M)\;N \;\to_\beta\; M[x := N]$$

```python
>>> (lambda x: x(x))(ID)("a")          # ID(ID)("a") と同じ
'a'
>>> (lambda x: lambda x: x)("a")("b")  # 内側の x は "b"
'b'
```

- 本体 M の x を引数 N で置き換える：β簡約 (beta reduction)。置き換えを代入 (substitution) と呼ぶ。Python の関数呼び出しに当たる
- 置き換えるのは自由な x だけ。内側の `lambda x:` の x は内側の引数を指す
- $(\lambda x.\,M)\;N$ の形を簡約基 (redex) と呼ぶ

<!--
目安 0.75 分。ラムダ計算の計算規則は β簡約です。λx.M に N を渡すと、本体 M の x を N で置き換えた式になります。この置き換えを代入と呼び、M[x := N] と書きます。Python の関数呼び出しと同じです。1 つ目の例では、本体 x(x) の x に ID が入って ID(ID) になります。置き換えるのは自由な x だけです。2 つ目の例では、内側の lambda x の x は内側の引数を指すので、"b" が返ります。(λx.M) N の形を簡約基と呼びます。
-->

---

## α変換：代入の前に引数名を付け替える

- 引数名を付け替えても同じ関数：α変換 (alpha conversion)
- 引数の自由変数と内側の引数が同名だと、文字どおりの代入で取り違えが起きる

$$(\lambda x.\,\lambda y.\,x)\;y \;\to_\beta\; \lambda w.\,y \qquad (\lambda y.\,y \text{ は誤り})$$

```python
>>> (lambda y: (lambda x: lambda y: x)(y))("外")("内")
'外'
>>> (lambda y: lambda y: y)("外")("内")   # 文字どおり代入
'内'
>>> (lambda y: lambda w: y)("外")("内")   # y を w に付け替え
'外'
```

<!--
目安 0.75 分。引数名は付け替えても関数は変わりません。これを α変換と呼びます。α変換が必要になるのは代入のときです。λx.λy.x に外側の変数 y を渡すとします。本体の x を文字どおり y に置き換えると λy.y になり、外側の y が内側の引数 y と取り違えられます。Python で確かめます。1 行目は Python が実際に呼び出した結果で、"外" が返ります。2 行目は文字どおり代入した式で、"内" が返ります。3 行目のように、先に内側の y を w に付け替えてから代入すれば、正しい結果になります。
-->

---

## Python は引数を先に計算する：正格評価

```python
>>> (lambda x: "a")(print("引数を計算"))
引数を計算
'a'
>>> (lambda x: "a")(lambda _: print("引数を計算"))
'a'
```

- 関数を呼ぶ前に引数を値まで計算する：正格評価 (strict evaluation)、値呼び (call by value)。使わない引数も計算する
- lambda の本体は、呼ばれるまで計算しない。式を `lambda _:` で包むと計算を遅らせられる
- この 2 点を [3 章](#ch3)の `IF` と [6 章](#ch6)の Y・Z で使う

<!--
目安 0.75 分。Python は、関数を呼ぶ前に引数を値まで計算します。これを正格評価、または値呼びと呼びます。1 つ目の例では、関数は x を使いませんが、引数の print が先に実行されます。一方、lambda の本体は呼ばれるまで計算されません。2 つ目の例では print を lambda _: で包んだので、引数は関数として作られるだけで、print は実行されません。3 章では正格評価のために IF が両方の枝を計算する問題が起き、lambda で包んで解決します。6 章の Y と Z でも同じ問題と解決方法が出てきます。
-->

---

<!-- _class: optional -->

## η変換：`lambda v: f(v)` と `f` は同じ関数

$$\lambda v.\,M\,v \;\to_\eta\; M \qquad (v \text{ は } M \text{ に自由に出てこない})$$

```python
>>> (lambda v: len(v))("abc"), len("abc")
(3, 3)
```

- 引数をそのまま M に渡す関数は M と同じ：η変換 (eta conversion)。逆向きは η展開 (eta expansion)
- Python では計算のタイミングが違う：`lambda v: M(v)` は、呼ばれるまで M を計算しない
- [6 章](#ch6)の Z コンビネータで、この違いを使う

<!--
目安 0.75 分。発展です。受け取った v をそのまま M に渡すだけの関数 λv. M v は、M と同じふるまいをします。これを η変換と呼びます。Python でも lambda v: len(v) と len は同じ結果を返します。逆向きに M を λv. M v に書き換えることを η展開と呼びます。ただし Python では違いが 1 つあります。lambda v: M(v) は、呼ばれるまで M を計算しません。前のスライドで見た lambda の性質です。6 章の Z コンビネータは、この違いを使って Y が止まらない問題を解決します。
-->

---

<!-- _class: optional -->

## 評価順序：正規順序と適用順序

$\Omega = (\lambda x.\,x\;x)\,(\lambda x.\,x\;x)$ は簡約しても自分に戻る。$(\lambda x.\,a)\;\Omega$ の結果は評価順序で変わり、Python は適用順序に近い

| 評価順序 | 先に簡約する簡約基 | 結果 |
|---|---|---|
| 正規順序 (normal order) | 外側・左（関数を先に呼ぶ） | $a$ |
| 適用順序 (applicative order) | 内側・左（引数を先に計算） | 止まらない |

```python
>>> (lambda x: "a")((lambda x: x(x))(lambda x: x(x)))
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

<!--
目安 1 分。発展です。項の中に簡約基が複数あるとき、どれから簡約するかを評価順序と呼びます。Ω は 6 章で出てくる、簡約しても自分自身に戻る項です。λx.a に Ω を渡すとき、外側の簡約基から、つまり関数を先に呼べば、x は使われないので a で終わります。これが正規順序です。内側、つまり引数から先に簡約する適用順序では、Ω の計算が終わりません。Python は引数を先に計算するので適用順序に近く、この例は RecursionError になります。ただし lambda の本体は呼ばれるまで計算しない点が違います。正規順序は、これ以上簡約できない形（正規形）があれば必ずそこへたどり着くことが知られています。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch3">3</span>チャーチ真偽値

目安 6.25 分（発展 +2 分）

コード：[Colab §3](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec3)

<!--
目安 0.25 分。この章では True も False も if も使わずに、真偽値と分岐を関数だけで作ります。手がかりは「if は 2 つのうちどちらかを選ぶもの」という見方です。
-->

---

## `TRUE` と `FALSE`：2 つの値から 1 つを選ぶ関数

```python
TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
to_bool = lambda b: b(True)(False)
```

```python
>>> to_bool(TRUE), to_bool(FALSE)
(True, False)
```

- `TRUE` は 2 つ受け取って 1 つ目を、`FALSE` は 2 つ目を返す：チャーチ真偽値 (Church booleans)。`TRUE(a)(b)` は `a if True else b` に当たる
- `to_bool` は変換関数。候補に Python の `True`、`False` を渡し、どちらが返るかを見る

<!--
目安 1 分。if の仕事は、2 つの候補から 1 つを選ぶことです。そこで真偽値そのものを、選ぶ関数として表します。TRUE は 2 つ受け取って 1 つ目を返し、FALSE は 2 つ目を返します。Church の名前を取ってチャーチ真偽値と呼びます。TRUE(a)(b) は Python の a if True else b と同じ値になります。引数名の t と f は then と else のつもりです。to_bool は結果を見るための変換関数で、候補として Python の True と False を渡し、どちらが返るかを見ます。数・ペア・リストも、この後同じように関数で表します。
-->

---

## `IF`：`IF(b)(x)(y)` は `x if b else y` に当たる

```python
IF = lambda b: lambda t: lambda f: b(t)(f)
```

```python
>>> IF(TRUE)("then")("else"), IF(FALSE)("then")("else")
('then', 'else')
```

$$\mathrm{IF}\;\mathrm{TRUE}\;a\;b \;\twoheadrightarrow_\beta\; \mathrm{TRUE}\;a\;b \;\twoheadrightarrow_\beta\; a$$

- 選ぶのは真偽値 `b` 自身。`IF` は `b(t)(f)` を if らしく読むための名前
- $\twoheadrightarrow_\beta$ は β簡約を何回か続けること

<!--
目安 0.75 分。IF は条件 b と 2 つの枝 t、f を受け取って、b に t と f を渡すだけです。IF(b)(x)(y) は Python の x if b else y に当たります。β簡約すると IF TRUE a b は TRUE a b になり、さらに a になります。矢印の先を 2 つにした記号は、β簡約を何回か続けることを表します。選んでいるのは TRUE 自身で、IF は if らしく読めるように付けた名前です。IF はこの後の正格評価の話と、6 章の再帰でも使います。
-->

---

## `NOT` と `AND`：真偽値に渡す候補を工夫する

```python
NOT = lambda b: b(FALSE)(TRUE)
AND = lambda a: lambda b: a(b)(FALSE)
```

```python
>>> to_bool(NOT(TRUE))
False
>>> to_bool(AND(TRUE)(TRUE)), to_bool(AND(TRUE)(FALSE))
(True, False)
```

- `NOT`：`b` が真なら `FALSE`、偽なら `TRUE` を選ぶ
- `AND`：`a` が真なら答えは `b` 次第。偽なら即 `FALSE`

<!--
目安 1 分。NOT は候補を逆順に渡すだけです。b が TRUE なら 1 つ目の FALSE が選ばれます。AND は「a が真なら、答えは b そのもの」「a が偽なら、b に関係なく FALSE」と言い換えると、a に b と FALSE の 2 択を選ばせればよいとわかります。下の実行例の 2 行目は、2 つの結果をカンマで並べて、タプルでまとめて表示しています。
-->

---

<!-- _class: exercise -->

## `OR` を書く

`OR = lambda a: lambda b: ＿＿＿` を完成させよ。

| `a` | `b` | `OR(a)(b)` |
|---|---|---|
| `TRUE` | 何でも | `TRUE` |
| `FALSE` | `b` | `b` |

<p class="note">ヒント：AND と同じく「a に 2 択を選ばせる」。2 つの候補は何か。</p>

<!--
目安 1.5 分。演習です。1 分ほど手を動かしてもらいます。残りの 30 秒は、手が止まっている人向けにヒントを読み上げる時間です。表のように場合分けすると、a が真なら TRUE、偽なら b です。AND の形をまねてください。
-->

---

<!-- _class: answer -->

## `OR` の解答

```python
OR = lambda a: lambda b: a(TRUE)(b)
```

```python
>>> to_bool(OR(FALSE)(TRUE)), to_bool(OR(FALSE)(FALSE))
(True, False)
```

- `a` が真なら `TRUE`、偽なら `b` を選ぶ

<!--
目安 0.5 分。a に TRUE と b の 2 択を選ばせます。AND と比べると、FALSE の代わりに TRUE を、1 つ目の候補として渡しています。
-->

---

## 正格評価のため `IF` の枝をサンクで包む

```python
>>> IF(TRUE)(TRUE)((lambda x: x(x))(lambda x: x(x)))
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
>>> to_bool(IF(TRUE)(lambda _: TRUE)(
...     lambda _: (lambda x: x(x))(lambda x: x(x)))(ID))
True
```

- 正格評価（[2 章](#ch2)）のため、`IF` が選ぶ前に else 側の止まらない式を計算する
- 対策：枝を `lambda _:` で包み、選んだ枝に `(ID)` を渡して呼ぶ。包んだ式をサンク (thunk) と呼ぶ（[6 章](#ch6)でも使う）

<!--
目安 1.25 分。1 つ目の例では、else 側に、自分自身を呼び続けて終わらない式を置いています。TRUE を選ぶので else 側は使われないはずですが、RecursionError になります。2 章で見たとおり、Python は関数を呼ぶ前に引数を全部計算するので、IF に渡す前に else 側の計算が始まって終わらないからです。この式は 6 章で Ω として扱います。対策は、両方の枝を lambda _: で包むことです。lambda の本体は呼ばれるまで計算されないので、IF は包んだ枝の一方を選ぶだけです。選んだ枝に ID を渡したときに初めて中身が計算されます。渡す値は何でもよいのですが、ID を使うと決めておきます。包んだ式をサンクと呼びます。この書き方は 6 章で再帰を書くときにもそのまま使います。
-->

---

<!-- _class: exercise optional -->

## `XOR` を書く

`XOR = lambda a: lambda b: ＿＿＿` を完成させよ（排他的論理和）。

| `a` | `b` | `XOR(a)(b)` |
|---|---|---|
| `TRUE` | `b` | `NOT(b)` |
| `FALSE` | `b` | `b` |

<p class="note">ヒント：これまでと同じく a に 2 択を選ばせる。NOT を使う。</p>

<!--
目安 1.5 分。発展の演習です。XOR は「ちょうど一方だけ真」のときに真です。表のように a で場合分けすると、a が真なら NOT b、偽なら b そのものです。
-->

---

<!-- _class: answer optional -->

## `XOR` の解答

```python
XOR = lambda a: lambda b: a(NOT(b))(b)
```

```python
>>> to_bool(XOR(TRUE)(FALSE)), to_bool(XOR(TRUE)(TRUE))
(True, False)
>>> to_bool(XOR(FALSE)(TRUE)), to_bool(XOR(FALSE)(FALSE))
(True, False)
```

- `NOT`・`AND`・`OR`・`XOR` は、どれも最初の引数（真偽値）に 2 つの候補を渡す形

<!--
目安 0.5 分。a に NOT(b) と b の 2 択を選ばせます。この章の論理演算は、どれも最初の引数に渡す 2 つの候補を決めれば書けました。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch4">4</span>チャーチ数

目安 8.25 分（発展 +3 分）

コード：[Colab §4](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec4)

<!--
目安 0.25 分。次は数値リテラルなしで自然数を作ります。真偽値を「選ぶ」というふるまいで表したのと同じく、数を「繰り返す回数」というふるまいで表します。
-->

---

## チャーチ数：数 n を「f を n 回適用する関数」で表す

```python
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
to_int = lambda n: n(lambda x: x + 1)(0)
```

```python
>>> to_int(ZERO), to_int(ONE)
(0, 1)
```

- チャーチ数 (Church numerals)：$\overline{n} = \lambda f.\,\lambda x.\,f^n\,x$。`ZERO` は `FALSE` と同じ形
- `n(f)(x)` は、`x` に `for _ in range(n): x = f(x)` を行った結果
- `to_int`：f に「1 足す」、x に `0` を渡して適用の回数を数える変換関数

<!--
目安 1 分。チャーチ数では、数 n を「関数 f と初期値 x を受け取って、f を n 回適用する関数」として表します。上線付きの n はチャーチ数としての n という意味です。Python で言えば、x に f を n 回適用する for ループです。ZERO は 1 回も適用しないので x をそのまま返し、ONE は 1 回適用します。to_int は 2 つ目の変換関数で、f に Python の「1 を足す関数」、x に 0 を渡せば、結果がちょうど n になります。ZERO は 2 つ受け取って 2 つ目を返すので、3 章の FALSE とα変換で同じ項です。
-->

---

## `SUCC`：f を適用する回数を 1 回増やす

<div class="cols">
<div>

$$\mathrm{SUCC} = \lambda n.\,\lambda f.\,\lambda x.\,f\,(n\,f\,x)$$

```python
SUCC = (lambda n: lambda f:
        lambda x: f(n(f)(x)))
```

```python
>>> to_int(SUCC(ONE))
2
```

</div>
<div>

```python
TWO = SUCC(ONE)
THREE = SUCC(TWO)
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
SIX = SUCC(FIVE)
SEVEN = SUCC(SIX)
EIGHT = SUCC(SEVEN)
NINE = SUCC(EIGHT)
TEN = SUCC(NINE)
```

</div>
</div>

- 後者関数 (successor)：`n(f)(x)` で f を n 回適用し、その外側でもう 1 回 `f(...)`。以降の例のために `TEN` まで名前を付ける

<!--
目安 0.75 分。後者関数 SUCC は、n を受け取って n+1 を返します。n(f)(x) で f を n 回適用し、その結果にさらに f を 1 回適用するので、合計 n+1 回です。これで ONE から TWO、THREE と作れます。以降の例のために、右のように TEN まで名前を付けておきます。どれも直前の数の SUCC です。
-->

---

## `ADD`：n に `SUCC` を m 回適用する

$$\mathrm{ADD}\;m\;n = m\;\mathrm{SUCC}\;n = \mathrm{SUCC}^m\,n$$

```python
ADD = lambda m: lambda n: m(SUCC)(n)
```

```python
>>> to_int(ADD(TWO)(THREE))
5
```

- 数 m は「渡された関数を m 回適用する」関数。その関数として `SUCC` を渡す

<!--
目安 0.75 分。足し算 m+n は「n に 1 を足すことを m 回繰り返す」ことです。チャーチ数 m は「m 回繰り返す」関数なので、f として SUCC、x として n を渡せば足し算になります。繰り返しを別に書かなくても、数そのものが繰り返しの役をします。
-->

---

## `MUL`：関数合成 (composition) で書く

$$\mathrm{MUL}\;m\;n\;f = m\,(n\,f) = (f^n)^m = f^{m n}$$

```python
MUL = lambda m: lambda n: lambda f: m(n(f))
```

```python
>>> to_int(MUL(THREE)(FOUR))
12
```

- `n(f)` は「f を n 回適用する」1 つの関数。`m` がそれを m 回適用するので、f は全部で m × n 回
- 足し算の繰り返し `m(ADD(n))(ZERO)` でも書けるが、関数合成なら `ADD` も `SUCC` も使わない

<!--
目安 1 分。掛け算は、0 に n を足すことを m 回繰り返す m(ADD(n))(ZERO) でも書けますが、もっと短く書けます。n(f) は「f を n 回適用する関数」で、これを 1 まとまりの関数とみなして m に渡すと、そのまとまりを m 回繰り返します。合計で f が m×n 回適用されます。ADD も SUCC も使わず、関数の合成で掛け算が書けました。
-->

---

<!-- _class: exercise -->

## `POW` を書く（`EXP` とも）

`POW = lambda m: lambda n: ＿＿＿` を完成させよ（$m^n$）。

- 目標：`to_int(POW(TWO)(THREE))` が `8`
- `MUL` より短く書ける

<p class="note">ヒント：数 m 自身も「関数 f を受け取り、f の m 回合成を返す関数」。それを n 回繰り返すと？</p>

<p class="note">2 択のヒント：答えは <code>n(m)</code> か <code>m(n)</code> のどちらか。</p>

<!--
目安 2.5 分。演習です。累乗は EXP と呼ぶこともあります。MUL では f を n 回合成したものを m 回繰り返しました。今度は「m 回合成する」という操作そのものを n 回繰り返します。2 分取ります。最初の 1 分はヒントなしで考えてもらい、手が止まっている人が多ければ、下の小さい 2 択のヒントを読み上げて「n(m) と m(n)、TWO と THREE で 8 になるのはどちら？」と問いかけます。
-->

---

<!-- _class: answer -->

## `POW` の解答

```python
POW = lambda m: lambda n: n(m)
```

<div class="steps">

| | |
|---|---|
| | $\mathrm{POW}\;\overline{2}\;\overline{3}\;f$ |
| $\twoheadrightarrow_\beta$ | $\overline{3}\;\overline{2}\;f \;\twoheadrightarrow_\beta\; \overline{2}\,(\overline{2}\,(\overline{2}\,f))$ |
| $=$ | $\overline{2}\,(\overline{2}\,(f^2)) = \overline{2}\,(f^4) = f^8$ |

</div>

```python
>>> to_int(POW(TWO)(THREE)), to_int(POW(TWO)(TEN))
(8, 1024)
```

- 数 m は「f を m 回合成する」関数。`n(m)` でそれを n 段重ねる

<!--
目安 1.25 分。答えは n(m) です。数 m は「f を受け取って f の m 乗、つまり m 回合成を返す関数」です。n(m) はこれを n 回繰り返すので、f は m 回合成をさらに m 回……と n 段重ねられ、m の n 乗回になります。表は 2 の 3 乗の例で、↠β は β簡約を何回か、最後の行のイコールは「f を何回合成したか」の書き換えです。内側から f が 2 回、4 回、8 回と倍々になります。引数の順番が m と n で逆になるのに注意してください。2 の 10 乗の 1024 もすぐ計算できます。ただし数は一進法なので、大きな数はすぐ遅くなります。
-->

---

## `IS_ZERO`：n が f を 1 回でも適用すれば `FALSE`

```python
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
```

```python
>>> to_bool(IS_ZERO(ZERO)), to_bool(IS_ZERO(THREE))
(True, False)
```

- n の x に `TRUE`、f に「何を受け取っても `FALSE` を返す関数」を渡す
- n が 0 なら f は 1 回も適用されず `TRUE` のまま。1 以上なら `FALSE`

<!--
目安 0.75 分。数を真偽値に変える最初の関数です。初期値を TRUE にして、f には何を受け取っても FALSE を返す定数関数を渡します。ZERO は f を 1 回も使わないので TRUE のまま、1 以上なら必ず FALSE になります。ここの lambda _ はサンクではなく、引数を無視する定数関数です。IS_ZERO は 6 章の再帰で終了条件として使います。
-->

---

<!-- _class: exercise optional -->

## `IS_EVEN` を書く

`IS_EVEN = lambda n: ＿＿＿` を完成させよ（偶数なら `TRUE`）。

- 目標：`IS_EVEN(FOUR)` は真、`IS_EVEN(SEVEN)` は偽
- `IS_ZERO` と同じく、n に f と x を渡す

<p class="note">ヒント：0 は偶数。1 増えるたびに偶奇は反転する。真偽値を反転する関数は <a href="#ch3">3 章</a>で作った。</p>

<!--
目安 2 分。発展の演習です。IS_ZERO の形を思い出しながら、f と x に何を渡せばよいか考えてもらいます。1 分半ほど待ちます。
-->

---

<!-- _class: answer optional -->

## `IS_EVEN` の解答

```python
IS_EVEN = lambda n: n(NOT)(TRUE)
```

```python
>>> to_bool(IS_EVEN(FOUR)), to_bool(IS_EVEN(SEVEN))
(True, False)
```

- `TRUE`（0 は偶数）から始めて、`NOT` を n 回適用する
- [4 章](#ch4)の数 n に、[3 章](#ch3)の `NOT` をそのまま渡せる

<!--
目安 1 分。x に TRUE、f に NOT を渡します。NOT を偶数回かければ TRUE のまま、奇数回なら FALSE です。真偽値も数も関数なので、数に真偽値の関数をそのまま渡せます。
-->


---

<!-- _class: chapter -->

# <span class="num" id="ch5">5</span>ペアと引き算

目安 4 分（発展 +6 分）

コード：[Colab §5](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec5)

<!-- 目安 0.25 分。足し算・掛け算・累乗はできました。次は引き算です。引き算を書くのにペアを使うので、まずペアを作ります。後半の発展は引き算と大小比較で、7 章のリストを扱うならここも必要です。 -->

---

<!-- _class: twocol -->

## ペア：2 つの値を 1 つの関数にまとめる

<div class="cols">
<div>

$$\mathrm{PAIR} = \lambda a.\,\lambda b.\,\lambda s.\,s\,a\,b$$

$$\mathrm{FIRST} = \lambda p.\,p\;\mathrm{TRUE}$$

$$\mathrm{SECOND} = \lambda p.\,p\;\mathrm{FALSE}$$

</div>
<div>

```python
PAIR = lambda a: lambda b: (
    lambda s: s(a)(b))
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
```

```python
>>> to_int(FIRST(PAIR(ONE)(TWO)))
1
>>> to_int(SECOND(PAIR(ONE)(TWO)))
2
```

</div>
</div>

<!-- 目安 1 分。PAIR は a と b を覚えておいて、関数 s を待つ関数です。s に a と b を両方渡すので、どちらを使うかは s が決めます。ここで 3 章の TRUE と FALSE を思い出してください。TRUE は 2 つのうち前を、FALSE は後ろを選ぶ関数でした。なので FIRST はペアに TRUE を、SECOND は FALSE を渡せば書けます。このように、データ構造も関数で作れます。 -->

---

## 前者関数 `PRED`：1 つ前の値もペアで持ち歩く

- 数 n でできるのは「f を n 回適用する」ことだけで、適用を 1 回取り消す方法はない
- そこで、n 回適用した結果が n − 1 になる f と x を用意する（Kleene の方法）
  - ペア（前, 今）を (0, 0) から始め、1 回ごとに (a, b) ↦ (b, b + 1) とずらす
  - n 回後のペアは (n − 1, n)。前の値を取り出せば n − 1。n = 0 なら 0

```text
# 同じ計算を普通の Python で書くと
prev, cur = 0, 0
for _ in range(n):
    prev, cur = cur, cur + 1
# prev が n - 1（n = 0 なら 0）
```

<!--
目安 1.25 分。前者関数 PRED は n を受け取って n−1 を返す関数です。チャーチ数 n でできるのは「f を n 回適用する」ことだけで、適用を 1 回分取り消す方法はありません。そこで、n 回適用した結果がちょうど n−1 になる f と x を用意します。Kleene の方法では、「1 つ前の値」と「今の値」のペアを持ち歩きます。(0, 0) から始めて、1 回ごとに今の値を前へずらし、今の値に 1 を足します。n 回後には (n−1, n) なので、前の値を取り出せば n−1 です。0 回なら (0, 0) のままなので、0 の前は 0 とします。下は同じ計算を普通の Python のループで書いたものです。
-->

---

## `SHIFT` と `PRED`

```python
SHIFT = lambda p: PAIR(SECOND(p))(SUCC(SECOND(p)))
PRED = lambda n: FIRST(n(SHIFT)(PAIR(ZERO)(ZERO)))
```

- `SHIFT`：ペア (a, b) から (b, b+1) を作る。ループの 1 回分
- `PRED`：(0, 0) に `SHIFT` を n 回適用し、`FIRST` で前の値を取り出す

```python
>>> to_int(PRED(FIVE)), to_int(PRED(ZERO))
(4, 0)
```

<p class="note">Kleene は親知らずの治療の麻酔中に思いついた、と伝わっている（Barendregt 1997 による紹介）。</p>

<!-- 目安 1.5 分。ループの 1 回分をそのまま書いたのが SHIFT です。前のペアの SECOND を新しい左側に、それに SUCC したものを新しい右側にします。PRED は (0, 0) に SHIFT を n 回適用して FIRST を取るだけ。n 回適用するのはチャーチ数 n そのものの仕事なので、n(SHIFT) と書けます。小ネタとして、この方法を思いついたのは Church の弟子の Kleene で、親知らずを抜くときの麻酔の最中にひらめいた、という話が伝わっています。Barendregt の 1997 年の論文が、Crossley が編んだ論理学者の回想録の Kleene の話として紹介しています。Kleene 本人の 1981 年の回想では、歯医者の話は出てきますが、笑気ガスには触れていない、という指摘もあるので、あくまで「そう伝わっている話」として聞いてください。 -->

---

<!-- _class: exercise optional -->

## `SUB` を書く

`SUB(m)(n)` が m − n（m < n なら 0）になるように定義せよ。

```text
# 穴埋め（このままでは動かない）
SUB = lambda m: lambda n: ...
# to_int(SUB(SEVEN)(THREE)) が 4 になれば正解
```

<p class="note">ヒント：数 n は「何かを n 回適用する」関数。m に何を n 回適用すればよい？ <a href="#ch4">4 章</a>の ADD も思い出す。</p>

<!-- 目安 2 分。発展の演習です。1 分半ほど考えてもらいます。ヒントは 4 章の ADD です。ADD は「n に SUCC を m 回」でした。SUB は「m に PRED を n 回」なので、関数を替えるだけでなく、m と n の役割も入れ替えます。そこに気づけば一行です。 -->

---

<!-- _class: answer optional -->

## `SUB` の解答

```python
SUB = lambda m: lambda n: n(PRED)(m)
```

```python
>>> to_int(SUB(SEVEN)(THREE)), to_int(SUB(TWO)(FIVE))
(4, 0)
```

- m に `PRED` を n 回適用する。`ADD` と比べて `SUCC` を `PRED` に替え、m と n の役割を逆にした形
- m < n で引きすぎても、結果は 0 で止まる（PRED 0 = 0 のため）

<!-- 目安 2 分。答えは n(PRED)(m)、つまり m から n 回 PRED するだけです。4 章の ADD = m(SUCC)(n) は「n に SUCC を m 回」でした。向きと関数が変わっただけの同じ形です。2 から 5 を引くと 0 になります。マイナスの数はないので、PRED 0 = 0 で止まります。この「引きすぎたら 0」という性質が次のスライドの比較で役に立ちます。 -->

---

<!-- _class: optional -->

## 大小比較：`LEQ` と `EQ`

```python
LEQ = lambda m: lambda n: IS_ZERO(SUB(m)(n))
EQ = lambda m: lambda n: AND(LEQ(m)(n))(LEQ(n)(m))
```

- m ≤ n ⇔ m − n が 0（引きすぎは 0 で止まるから）
- m = n ⇔ m ≤ n かつ n ≤ m

```python
>>> to_bool(LEQ(THREE)(FIVE)), to_bool(EQ(FOUR)(FIVE))
(True, False)
```

<p class="note">この比較は遅い：PRED は 1 回呼ぶごとに SHIFT を n 回適用し、SUB はその PRED を n 回呼ぶ。</p>

<!-- 目安 2 分。引き算ができると比較ができます。m が n 以下なら m − n は引きすぎて 0 になるので、IS_ZERO で調べれば LEQ です。等しいかどうかは、両方向の LEQ が真かどうか、つまり AND で書けます。ただし遅いです。PRED は 1 回呼ぶだけで中で SHIFT を n 回、SUB はその PRED を n 回呼ぶので、数が大きくなると目に見えて遅くなります。7 章の RANGE や MOD はこの LEQ と SUB を使います。 -->

---

<!-- _class: chapter -->

# <span class="num" id="ch6">6</span>再帰と Y コンビネータ

目安 15.5 分（発展 +2 分）

コード：[Colab §6](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec6)

<!-- 目安 0.25 分。ここまでで真偽値、数、引き算まで作りましたが、まだ繰り返しがありません。この章では、名前を定義の右辺に置き換えるだけで再帰を書く方法を考えます。Y コンビネータの式は、一歩ずつ組み立てて導きます。 -->

---

## 再帰定義は置き換えが終わらない

```text
FACT = lambda n: IF(IS_ZERO(n))(lambda _: ONE)(
    lambda _: MUL(n)(FACT(PRED(n))))(ID)    # 右辺に FACT
```

FACT を右辺に置き換えると、その中にまた FACT が現れる（… は変わらない部分）

<div class="steps">

| | |
|---|---|
| | $\mathrm{FACT} = \lambda n.\,\cdots\,\mathrm{FACT}\,(\mathrm{PRED}\,n)\,\cdots$ |
| $=$ | $\lambda n.\,\cdots\,\bigl(\lambda n.\,\cdots\,\mathrm{FACT}\,(\mathrm{PRED}\,n)\,\cdots\bigr)\,(\mathrm{PRED}\,n)\,\cdots$ |
| $=$ | $\lambda n.\,\cdots\,\bigl(\lambda n.\,\cdots\,\bigl(\lambda n.\,\cdots\,\mathrm{FACT}\,\cdots\bigr)\,\cdots\bigr)\,\cdots$ |

</div>

<p class="note">Python で動くのは、呼び出した時点でグローバル名 FACT を探すから。ラムダ計算に名前の表はない。</p>

<!-- 目安 1.25 分。n の階乗は、n が 0 なら 1、そうでなければ n かける (n−1) の階乗です。ここまでの関数で素直に書くとこうなり、右辺に FACT 自身が出てきます。ラムダ計算では、名前が出てくるところは定義の右辺に置き換えられるだけです。FACT を右辺に置き換えると、その中にまた FACT が現れます。もう 1 段置き換えても FACT が残り、置き換えはいつまでも終わりません。Python でこの定義が動くのは、FACT を呼んだ時点でグローバル変数 FACT を探しに行く仕組みがあるからです。ラムダ計算には名前の表がないので、この仕組みは使えません。そこで、自分の名前を使わずに再帰する方法を考えます。手がかりは自己適用です。 -->

---

<!-- _class: twocol -->

## 自己適用：関数を自分自身に渡す

<div class="cols">
<div>

<div class="steps">

| | |
|---|---|
| | $\omega = \lambda x.\,x\,x$ |
| | $\Omega = \omega\;\omega$ |
| $=$ | $(\lambda x.\,x\,x)\;\omega$ |
| $\twoheadrightarrow_\beta$ | $\omega\;\omega$ |
| $\twoheadrightarrow_\beta$ | $\cdots$ |

</div>

</div>
<div>

```python
omega = lambda x: x(x)
```

```python
>>> omega(omega)
Traceback (most recent call last):
  ...
RecursionError: ...
```

</div>
</div>

Ω は簡約しても元に戻るので終わらない。ただ、関数が自分自身を受け取れることはわかる

<!-- 目安 0.75 分。手がかりは自己適用です。ω は「受け取った x を x 自身に適用する」関数です。ω を ω に渡すと、β簡約の結果がまた ω ω に戻ってしまい、永遠に終わりません。これを Ω と呼びます。Python でも omega(omega) は RecursionError になります。これだけでは止まりませんが、関数が自分自身を引数として受け取って呼び出せることはわかります。終わらない繰り返しが作れたので、止め方を工夫すれば再帰になりそうです。 -->

---

## `FACT_GEN`：再帰の相手を引数 `self` で受け取る

```python
FACT_GEN = lambda self: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(self(self)(PRED(n))))
      (ID)
)
```

- 再帰の相手を引数 `self` で受け取り、使う側が `FACT_GEN(FACT_GEN)` と自分自身を渡す（ω と同じ自己適用）
- `self` はまだ self を待つ FACT_GEN なので、再帰でも `self(self)` と渡し直す。右辺に FACT_GEN 自身は出てこない

<!-- 目安 1.25 分。名前で自分を呼べないなら、引数でもらえばよい、という考え方です。関数の外側に引数 self を 1 つ足して、使う人に自分自身を渡してもらいます。FACT_GEN(FACT_GEN) と書くので、ω の自己適用と同じ形です。注意が 1 つあります。self が受け取るのは FACT_GEN、つまり「self を待っている関数」です。なので再帰呼び出しするときも、まず self に self を渡し直してから n−1 を渡します。それが self(self) です。最初の FACT と比べると、違いは先頭の lambda self と self(self) の 2 か所だけで、右辺に FACT_GEN という名前は出てきません。なお、この self はクラスの self とは関係のない、ただの引数名です。 -->

---

## `FACT_GEN(FACT_GEN)` で階乗を計算する

```python
>>> to_int(FACT_GEN(FACT_GEN)(THREE))
6
>>> to_int(FACT_GEN(FACT_GEN)(FIVE))
120
```

```text
G = FACT_GEN(FACT_GEN) とおく（中では self = FACT_GEN）
G(THREE) = MUL(THREE)( self(self)(TWO) )
         = MUL(THREE)( FACT_GEN(FACT_GEN)(TWO) )
         = MUL(THREE)( G(TWO) )      self(self) は G 自身
```

<!-- 目安 1 分。実際に動きます。3 の階乗が 6、5 の階乗が 120 です。なぜ動くのかを追ってみます。FACT_GEN(FACT_GEN) を G と呼ぶことにします。G の中では self が FACT_GEN です。すると再帰呼び出しの self(self) は FACT_GEN(FACT_GEN)、つまり G 自身です。図では PRED(THREE) を TWO と書いています。名前を使わずに自分自身を呼べています。もう 1 つ見ておいてほしいのは、self(self) が else 側のサンク lambda _: の中にあることです。だから n が 0 のときは呼ばれず、そこで止まります。 -->

---

## `self(self)` を本体の外へ出す

FACT_GEN の本体には `self(self)` という特殊な呼び方が混ざっている。本体はふつうの `fact(n−1)` の形で書きたい（self を s と書く）

<div class="steps">

| | |
|---|---|
| | $\mathrm{FACT\_GEN} = \lambda s.\,\lambda n.\,\cdots\,(s\,s)\,(\mathrm{PRED}\,n)\,\cdots$ |
| $=_\beta$ | $\lambda s.\,\bigl(\lambda f.\,\lambda n.\,\cdots\,f\,(\mathrm{PRED}\,n)\,\cdots\bigr)\,(s\,s)$ |
| $=$ | $\lambda s.\,F\,(s\,s)$ |

</div>

<div class="steps">

| | |
|---|---|
| | $F = \lambda f.\,\lambda n.\,\cdots\,f\,(\mathrm{PRED}\,n)\,\cdots$　（ふつうの再帰の形） |

</div>

$=_\beta$（β同値）は、β簡約を逆向きも含めて何回か使うと移り合えること。2 行目を β簡約すると 1 行目に戻る

<!-- 目安 2 分。FACT_GEN は動きますが、本体を書く人が self(self) という書き方を知っていなければなりません。そこで self(self) を本体の外へ出します。…の部分は IF や MUL など、変わらない部分です。1 行目の (s s) を、外から引数 f として渡してもらう形に書き換えたのが 2 行目です。2 行目を β簡約すると f に (s s) が入って 1 行目に戻るので、同じものです。β簡約を逆向きに使ったわけです。このように、β簡約を前向きにも逆向きにも使って移り合えることを β同値と呼び、イコールに β を添えて書きます。こうして括弧の中に、self(self) を含まない、ふつうの再帰の形 F が取り出せました。FACT_GEN は「F に s s を渡すもの」になりました。ただし、ラムダ計算としては同じですが、Python では計算のタイミングが変わります。元の FACT_GEN では self(self) が lambda _: のサンクの中にありましたが、2 行目では s s が F の引数として外に出ています。この違いが、後で Python の Y が止まらない原因になります。 -->

---

## `FACT_BODY`：再帰の相手を引数 `fact` で受け取る

F を Python で書く。再帰呼び出しの相手は引数 `fact` で受け取る

```python
FACT_BODY = lambda fact: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(fact(PRED(n))))
      (ID)
)
```

```python
>>> to_int(FACT_BODY(FACT_GEN(FACT_GEN))(FIVE))
120
```

本物の階乗を fact に渡せば階乗になる。残る問題は、その fact をどう作るか

<!-- 目安 0.5 分。F を Python で書いたのが FACT_BODY です。最初の FACT とほぼ同じで、FACT と書いていたところが引数 fact になっただけです。試しに、さっき動いた FACT_GEN(FACT_GEN) を fact として渡すと、ちゃんと 120 になります。つまり、本物の階乗さえもらえれば FACT_BODY は階乗になります。残る問題は、その本物をどう作るかです。 -->

---

## FACT_GEN を組み立て直すと Y コンビネータになる

<div class="steps">

| | |
|---|---|
| | $\mathrm{FACT} = \mathrm{FACT\_GEN}\;\mathrm{FACT\_GEN}$ |
| $=_\beta$ | $(\lambda s.\,F\,(s\,s))\;(\lambda s.\,F\,(s\,s))$ |

</div>

F を引数 f にくくり出すと（s は x に α変換）

$$Y = \lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x)) \qquad \mathrm{FACT} = Y\,F$$

Y にふつうの再帰の形 F を渡すと、再帰する関数が返ってくる

<p class="note">コンビネータ (combinator)：自由変数のない λ 項。Y も、この後の Z も、<a href="#ch8">8 章</a>の S・K・I もこれ。</p>

<!-- 目安 1 分。さっきの結果を使って組み立て直します。FACT は FACT_GEN を FACT_GEN に渡したもので、FACT_GEN は λs. F (s s) と β同値でした。これを 2 つ並べるだけです。ここで F は階乗に限らず何でもよいので、F を引数 f にくくり出します。変数名 s は x に付け替えました。これが Y コンビネータです。コンビネータとは、2 章の自由変数を 1 つも含まない λ 項のことです。ふつうの再帰の形をした関数を渡すと、再帰する関数を作ってくれます。Y の式は、自分を引数でもらう工夫を整理すると、このように出てきます。 -->

---

## Y F は F の不動点

<div class="steps">

| | |
|---|---|
| | $Y\,F$ |
| $\twoheadrightarrow_\beta$ | $(\lambda x.\,F\,(x\,x))\;(\lambda x.\,F\,(x\,x))$ |
| $\twoheadrightarrow_\beta$ | $F\;\bigl((\lambda x.\,F\,(x\,x))\;(\lambda x.\,F\,(x\,x))\bigr)$ |
| $=_\beta$ | $F\;(Y\,F)$ |

</div>

- 不動点 (fixed point)：F p = p となる p。**Y F は F の不動点**
- FACT = Y F なら FACT = F FACT。最初に書きたかった `FACT = … FACT …` が、名前なしで成り立つ

<!-- 目安 1 分。Y F を簡約して確かめます。3 行目の F の引数全体は、Y F を 1 歩 β簡約した項、つまり 2 行目と同じです。そこを逆向きに β展開すると Y F に戻るので、最後の行は F (Y F) です。したがって Y F =β F (Y F)、β同値の意味で Y F は F の不動点です。関数 F に渡しても変わらない値を不動点と呼ぶので、Y は不動点を作るコンビネータ、不動点コンビネータ (fixed-point combinator) と呼ばれます。意味を読むと、FACT = Y F は「fact として FACT 自身を渡された FACT_BODY」です。最初のスライドで書きたかった、自分の名前を使う式が、名前を使わずに成り立ちました。 -->

---

## Python の Y は引数を先に計算して止まらない

<div class="cols">
<div>

```python
Y = lambda f: (
    (lambda x: f(x(x)))
    (lambda x: f(x(x))))
```

</div>
<div>

```python
>>> Y(FACT_BODY)
Traceback (most recent call last):
  ...
RecursionError: ...
```

</div>
</div>

```text
W = lambda x: F(x(x))  Y(F) = W(W) -> F(W(W)) -> F(F(W(W))) ...
F を呼ぶ前に引数 W(W) を計算するので、F は一度も呼ばれない
```

- 正格評価（[2 章](#ch2)）のため、`Y(FACT_BODY)` を作った時点で止まらない。FACT_GEN の `self(self)` と違い、Y の `x x` はサンクの中にない

<!-- 目安 1.75 分。理屈は完成したので Python で書きます。Y の定義はそのまま写せますが、Y(FACT_BODY) は RecursionError になります。数を渡して計算させる前、関数を作る段階で落ちています。原因は 3 章の IF と同じ正格評価です。Y(F) は W を W に渡したものです。W(W) を計算すると F(W(W)) になりますが、Python は F を呼ぶ前に引数の W(W) を計算しようとします。それがまた F(W(W)) になり、F が一度も呼ばれないまま展開が続きます。正規順序なら、Y F に ZERO を渡した項は外側の F、つまり FACT_BODY から簡約されるので、fact を使わずに ONE まで行けます。FACT_GEN が動いたのは、self(self) が lambda _: のサンクの中にあり、呼ばれるまで計算されなかったからです。外へ出したことで、x x は F の引数になり、F を呼ぶ前に計算されるようになりました。 -->

---

<!-- _class: twocol -->

## Z コンビネータ：Y の x x を η展開で包む

<div class="cols">
<div>

$$
\begin{aligned}
Z = \lambda f.\,&(\lambda x.\,f\,(\lambda v.\,x\,x\,v))\\
&(\lambda x.\,f\,(\lambda v.\,x\,x\,v))
\end{aligned}
$$

</div>
<div>

```python
Z = lambda f: (
  (lambda x:
     f(lambda v: x(x)(v)))
  (lambda x:
     f(lambda v: x(x)(v))))
```

</div>
</div>

```python
>>> lambda v: omega(omega)(v)    # 包むだけなら落ちない
<function <lambda> at ...>
```

- `x x` を `λv. x x v` に書き換える η展開 (eta expansion)：呼べば同じ結果だが、Python は呼ばれるまで `x(x)` を計算しない（FACT_GEN のサンクと同じ）

<!-- 目安 1.25 分。Y の中で問題だった x(x) を、lambda v: x(x)(v) で包んだものが Z コンビネータです。Y との違いはこの 2 か所だけです。M を λv. M v に書き換えても、v を渡して呼べば結果は同じです。これを η展開と呼びます。2 章の発展で η変換を見た人は、その逆向きです。ただし Python では lambda の本体は呼ばれるまで計算されません。実際 omega(omega) は落ちましたが、それを lambda で包んだだけなら落ちません。f に渡るのは計算済みの値ではなく「呼ばれたら x(x) を計算する関数」なので、f を呼ぶ前に無限に展開することはありません。ラムダ計算の中では、Z F も η変換を許せば F の不動点です。Z は、Python のような正格評価の言語でも使える不動点コンビネータです。 -->

---

## `FACT = Z(FACT_BODY)`

```python
FACT = Z(FACT_BODY)
```

```python
>>> to_int(FACT(ZERO)), to_int(FACT(THREE))
(1, 6)
>>> to_int(FACT(FIVE))
120
```

- FACT_BODY が fact を呼ぶのは n ≠ 0 のときだけ。そのとき初めて x(x) が 1 段展開される
- IF の枝がサンクなので n = 0 で止まる。包まないと n = 0 でも else 側を計算する
- 自分の名前を使わずに再帰が書けた

<!-- 目安 0.5 分。Z に FACT_BODY を渡すと、今度は落ちずに 1、6、120 と階乗が返ってきます。lambda で包まれた自分自身が fact として渡され、n が 0 でないときに初めて 1 段だけ展開されます。IF の枝もサンクで包んであるので、n が 0 なら else 側は計算されません。包まないと 3 章の落とし穴に戻ります。自分の名前を使わずに再帰できました。 -->

---

<!-- _class: exercise -->

## Z で `SUM_TO_N` を書く

0 + 1 + … + n を計算する `SUM_TO_N` を定義せよ。

```text
# 穴埋め（このままでは動かない）
SUM_TO_N = Z(lambda sum_to_n: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ...)
      (lambda _: ...)
      (ID)
))
# to_int(SUM_TO_N(FOUR)) が 10 になれば正解
```

<p class="note">ヒント：FACT_BODY をまねる。n = 0 なら ZERO、そうでなければ n + sum_to_n(n − 1)。</p>

<!-- 目安 2.5 分。演習です。2 分ほど時間を取ります。FACT_BODY を Z に渡したのと同じように、ふつうの再帰の形を Z に直接渡します。中身は階乗とほとんど同じで、どこを変えればよいかを考えてください。 -->

---

<!-- _class: answer -->

## `SUM_TO_N` の解答

```python
SUM_TO_N = Z(lambda sum_to_n: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ZERO)
      (lambda _: ADD(n)(sum_to_n(PRED(n))))
      (ID)
))
```

```python
>>> to_int(SUM_TO_N(FOUR)), to_int(SUM_TO_N(TEN))
(10, 55)
```

- FACT_BODY の `ONE` を `ZERO` に、`MUL` を `ADD` に変えた形

<!-- 目安 0.5 分。解答です。FACT_BODY の ONE を ZERO に、MUL を ADD に変えるだけでした。Z に渡すのは、ふつうの再帰の形そのものです。一度 Z を作ってしまえば、再帰はいくらでも書けます。 -->

---

<!-- _class: optional -->

## `FIB`：本体で自分を 2 回呼ぶ再帰

```python
FIB = Z(lambda fib: lambda n: (
    IF(IS_ZERO(PRED(n)))
      (lambda _: n)
      (lambda _: ADD(fib(PRED(n)))
                       (fib(PRED(PRED(n)))))
      (ID)
))
```

```python
>>> to_int(FIB(TEN))
55
```

- n ≤ 1（PRED n が 0）なら n を返す。それ以外は FIB(n−1) と FIB(n−2) の和

<!-- 目安 2 分。発展です。フィボナッチ数も同じ形で書けます。PRED(n) が 0、つまり n が 0 か 1 なら n そのものを返し、それ以外は fib(n−1) と fib(n−2) を足します。再帰呼び出しが 2 つあっても、Z に渡す形は変わりません。10 番目のフィボナッチ数は 55 です。FIB は 16 まで動き、17 で RecursionError になります（9 章の表）。講習中にその場で試すなら、FACT は 5、FIB は 10 程度が安心です。 -->


---

<!-- _class: chapter optional -->

# <span class="num" id="ch7">7</span>リスト

発展 10 分（FizzBuzz +5.25 分）

コード：[Colab §7](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec7)

<!--
目安 0.25 分。ここから発展の章です。5 章のペアを入れ子にしてリストを作り、最後は数値リテラルや文字列を使わずに FizzBuzz を書きます。5 章発展の LEQ と SUB を使うので、5 章発展を飛ばした場合はこの章も飛ばします。
-->

---

<!-- _class: optional -->

## リストをペアの入れ子で表す：`NIL`、`CONS`、`HEAD`、`TAIL`

```python
NIL = PAIR(TRUE)(TRUE)
CONS = lambda h: lambda t: PAIR(FALSE)(PAIR(h)(t))
IS_NIL = FIRST
HEAD = lambda l: FIRST(SECOND(l))
TAIL = lambda l: SECOND(SECOND(l))
```

```python
>>> to_int(HEAD(CONS(ONE)(NIL)))
1
>>> to_bool(IS_NIL(NIL)), to_bool(IS_NIL(CONS(ONE)(NIL)))
(True, False)
```

- 外側のペアは（空か, （先頭, 残り））
- `[a, b]` ＝ `(FALSE, (a, (FALSE, (b, NIL))))`

<!--
目安 1.5 分。リストは「先頭」と「残り」のペアとして作るのが定番で、Lisp の cons セルと同じ連結リストです。空のリストと空でないリストを見分けるため、外側にもう 1 段ペアをかぶせて、1 つ目に「空かどうか」を表す真偽値を入れます。空でないリストは 1 つ目が FALSE で、2 つ目に先頭と残りのペアが入ります。空のリスト NIL は 1 つ目が TRUE で、2 つ目は使わないので TRUE を詰めておきます。IS_NIL は 1 つ目の真偽値を取り出すので FIRST そのものです。HEAD と TAIL は、まず SECOND で中身のペアを取り出し、そこから FIRST か SECOND を取ります。
-->

---

<!-- _class: optional -->

## `to_list`：Python のリストに変換する

```python
def to_list(l, conv=lambda x: x):
    result = []
    while not to_bool(IS_NIL(l)):
        result.append(conv(HEAD(l)))
        l = TAIL(l)
    return result
```

```python
>>> to_list(CONS(ONE)(CONS(TWO)(NIL)), to_int)
[1, 2]
```

- 結果の確認だけに使う変換関数なので、`def` と `while` で書く
- 各要素は `conv` に渡した関数で変換する（`to_int` など）

<!--
目安 1.25 分。3 つ目の変換関数です。IS_NIL が真になるまで先頭を取り出しては残りに進み、Python のリストに詰めます。結果の確認だけに使う変換関数なので、def と while を使って普通の Python で書きます。要素はチャーチ数などのままなので、2 つ目の引数 conv で要素ごとの変換関数を指定します。
-->

---

<!-- _class: optional -->

## `RANGE`：m から n までの数のリストを作る

```python
RANGE = Z(lambda range_: lambda m: lambda n: (
    IF(LEQ(m)(n))
      (lambda _: CONS(m)(range_(SUCC(m))(n)))
      (lambda _: NIL)
      (ID)
))
```

```python
>>> to_list(RANGE(ONE)(FIVE), to_int)
[1, 2, 3, 4, 5]
```

- [6 章](#ch6)の Z と、`IF(c)(lambda _: A)(lambda _: B)(ID)` の形で書く
- m ≤ n なら m を先頭に置き、残りは m+1 から n まで。それ以外は `NIL`

<!--
目安 1.5 分。最初の再帰的なリスト関数です。形は 6 章の FACT や SUM_TO_N と同じで、Z に「自分自身」を引数として渡してもらいます。range_ の下線は Python 組み込みの range と名前がぶつからないようにするためだけのものです。5 章発展の LEQ を使って、m が n 以下なら m を先頭にして残りを m+1 から作り、そうでなければ NIL を返します。
-->

---

<!-- _class: optional -->

## 右畳み込み `FOLD`：`CONS` を `f` に、`NIL` を `z` に置き換える

```text
CONS(a)(CONS(b)(CONS(c)(NIL)))   →   f(a)(f(b)(f(c)(z)))
```

```python
FOLD = Z(lambda fold: lambda f: lambda z: lambda l: (
    IF(IS_NIL(l))
      (lambda _: z)
      (lambda _: f(HEAD(l))(fold(f)(z)(TAIL(l))))
      (ID)
))
```

```python
>>> to_list(FOLD(CONS)(NIL)(RANGE(ONE)(THREE)), to_int)
[1, 2, 3]
>>> to_int(FOLD(lambda _: SUCC)(ZERO)(RANGE(ONE)(FIVE)))
5
```

<!--
目安 1.5 分。リストを 1 つの値にまとめる基本の道具が畳み込みです。リストは CONS と NIL でできているので、CONS を 2 引数関数 f に、NIL を初期値 z にそっくり置き換えます。FOLD は、空なら z、そうでなければ先頭と「残りを畳み込んだ結果」に f を適用します。リストの右端から計算が進むので右畳み込み (right fold) と呼びます。Python の functools.reduce を右から行う形です。例の 1 つ目は CONS を CONS に、NIL を NIL に置き換えるので、元と同じリストが返ります。これは後で FizzBuzz の文字列連結に使います。2 つ目は要素を無視して 1 ずつ足すので、長さを数えています。
-->

---

<!-- _class: optional -->

## `MAP`：`FOLD` で書く

```python
MAP = lambda f: lambda l: (
    FOLD(lambda x: lambda acc: CONS(f(x))(acc))(NIL)(l)
)
```

```python
>>> to_list(MAP(SUCC)(RANGE(ONE)(THREE)), to_int)
[2, 3, 4]
```

- `FOLD` で、`CONS` を「要素に `f` を適用してから `CONS`」に置き換える
- `MAP` 自身は Z を使わない。再帰は `FOLD` の中で済んでいる

<!--
目安 1 分。各要素に f を適用したリストを作る MAP です。先ほどの FOLD(CONS)(NIL) はリストを写すだけでしたが、CONS の前に f を挟めば MAP になります。acc は「残りを処理し終えたリスト」です。MAP 自身は Z を使っていません。再帰は FOLD の中で済んでいるので、以降は FOLD を使って他の関数を定義できます。
-->

---

<!-- _class: exercise optional -->

## `SUM` を `FOLD` で書く

リストの要素をすべて足す `SUM` を定義せよ

```text
# 穴埋め（このままでは動かない）
SUM = ...
to_int(SUM(RANGE(ONE)(FOUR)))   # 10 になってほしい
```

- 使うもの：`FOLD`、`ADD`、`ZERO`
- 余裕があれば：何行で書ける？

<p class="note">ヒント：CONS を何に、NIL を何に置き換える？</p>

<!--
目安 2 分。演習です。FOLD の図を思い出して、CONS と NIL をそれぞれ何に置き換えればよいか考えてもらいます。6 章の SUM_TO_N では Z を使って数行書きましたが、今回はもっと短くなります。2 分ほど待ちます。
-->

---

<!-- _class: answer optional -->

## `SUM` の解答：`FOLD` を使えば 1 行

```python
SUM = FOLD(ADD)(ZERO)
```

```python
>>> to_int(SUM(RANGE(ONE)(FOUR)))
10
```

- `CONS` → `ADD`、`NIL` → `ZERO` に置き換えると
  `ADD(ONE)(ADD(TWO)(ADD(THREE)(ADD(FOUR)(ZERO))))`
- 引数 `l` は書かなくてよい。`FOLD(ADD)(ZERO)` が「リストを待つ関数」になる

<!--
目安 1 分。答えは 1 行です。CONS を ADD に、NIL を ZERO に置き換えれば足し算になります。引数の l も書かなくて済みます。カリー化のおかげで、FOLD に f と z だけ渡したものが、すでに「リストを受け取って合計を返す関数」になっています。6 章で Z と IF を手で組んだ SUM_TO_N が、RANGE と組み合わせて SUM(RANGE(ONE)(n)) と書けるわけです。FOLD や RANGE のような関数がそろうと、普通のプログラムに近い書き方ができます。
-->

---

<!-- _class: optional -->

## FizzBuzz を関数だけで書く

```text
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz,
11, Fizz, 13, 14, FizzBuzz
```

- 新しく必要なもの：割り算の余り、数を各桁のリストにする関数、文字の表現、リストの連結
- 数値リテラル・文字列・`if` を使わず、ここまでに定義した関数と組み合わせて書く
- 定義が多いので、細部は追わずに形を見ていく

<p class="note">Tom Stuart「Programming with Nothing」（Ruby の lambda（proc）だけで FizzBuzz）へのオマージュ</p>

<!--
目安 0.75 分。ここから FizzBuzz です。3 の倍数で Fizz、5 の倍数で Buzz、両方なら FizzBuzz、それ以外は数を出す、という定番の課題です。Tom Stuart さんが Ruby の lambda（proc）だけで同じことをした「Programming with Nothing」という有名な記事と講演があり、今回はその Python 版のオマージュです。定義の数が多いので、1 行ずつ読むより「どこかで見た形だな」と眺めていきます。
-->

---

<!-- _class: optional -->

## `MOD`：m から n を引けるだけ引く

```python
MOD = Z(lambda mod: lambda m: lambda n: (
    IF(LEQ(n)(m))
      (lambda _: mod(SUB(m)(n))(n))
      (lambda _: m)
      (ID)
))
```

```python
>>> to_int(MOD(TEN)(THREE))
1
```

- `MOD(TEN)(THREE)`：10 → 7 → 4 → 1。3 を引けなくなったときの 1 が余り

<p class="note">前提：除数 n は 1 以上。n = ZERO は未定義で、この実装では止まらない。</p>

<!--
目安 0.5 分。割り算の余りです。n が m 以下である限り、m から n を引いて繰り返します。引けなくなったときの m が余りです。形はもう見慣れた Z と IF の組み合わせです。除数が 0 だと、いくら引いても減らないので止まりません。除数は 1 以上が前提です。
-->

---

<!-- _class: optional -->

## `DIV`：m から n を引けた回数を数える

```python
DIV = Z(lambda div: lambda m: lambda n: (
    IF(LEQ(n)(m))
      (lambda _: SUCC(div(SUB(m)(n))(n)))
      (lambda _: ZERO)
      (ID)
))
```

```python
>>> to_int(DIV(TEN)(THREE))
3
```

- 10 → 7 → 4 → 1 と 3 を引けた回数 3 が商。`MOD` との違いは `IF` の 2 つの枝

<p class="note">前提：除数 n は 1 以上。n = ZERO は未定義で、この実装では止まらない。</p>

<!--
目安 0.5 分。割り算の商は、MOD とほぼ同じ形で、引けるたびに SUCC で 1 を数えます。違いは 2 つの枝の中身だけです。前提も MOD と同じで、除数は 1 以上です。
-->

---

<!-- _class: optional -->

## `PUSH` と `TO_DIGITS`：数を各桁のリストにする

```python
PUSH = lambda l: lambda x: FOLD(CONS)(CONS(x)(NIL))(l)
TO_DIGITS = Z(lambda digits: lambda n: (
    IF(LEQ(n)(NINE))
      (lambda _: CONS(n)(NIL))
      (lambda _: PUSH(digits(DIV(n)(TEN)))(MOD(n)(TEN)))
      (ID)
))
```

```python
>>> to_list(TO_DIGITS(POW(TEN)(TWO)), to_int)
[1, 0, 0]
```

- `PUSH(l)(x)`：`FOLD(CONS)` で `l` を写し、末尾の `NIL` を `[x]` に替える

<!--
目安 0.75 分。PUSH はリストの末尾に 1 つ足します。FOLD(CONS) で写しながら、NIL を「x だけのリスト」に置き換えるだけです。TO_DIGITS は 10 進の各桁のリストを作ります。9 以下なら 1 桁、そうでなければ 10 で割った商の桁を作ってから、末尾に余りを足します。100 は POW(TEN)(TWO) で作っています。
-->

---

<!-- _class: optional -->

## 文字を 0〜14 の数で表す：`to_str`

| 数 | 0〜9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|
| 文字 | 0〜9 | B | F | i | u | z |

<div class="cols">
<div>

```python
ELEVEN = SUCC(TEN)
TWELVE = SUCC(ELEVEN)
THIRTEEN = SUCC(TWELVE)
FOURTEEN = SUCC(THIRTEEN)
```

</div>
<div>

```python
to_str = lambda l: "".join(
  to_list(l, lambda c:
    "0123456789BFiuz"[to_int(c)]))
```

```python
>>> to_str(TO_DIGITS(FOURTEEN))
'14'
```

</div>
</div>

- 文字列は、文字を表す数のリスト。Fizz と Buzz に要る文字は B、F、i、u、z の 5 つ

<!--
目安 0.75 分。文字列は文字のリストにします。数字の 0 から 9 はそのまま数で、Fizz と Buzz に必要な文字は B、F、i、u、z の 5 つしかないので、10 から 14 を割り当てます。この割り当ても Tom Stuart さんの記事と同じです。そのために TEN の続きを 14 まで作っておきます。最後の変換関数 to_str は、各要素を to_int で数にして、"0123456789BFiuz" の何文字目かを引きます。文字列リテラルを使うのはこの変換関数の中だけです。
-->

---

<!-- _class: optional -->

## `FIZZ`、`BUZZ`、`FIZZBUZZ_WORD`

```python
FIZZ = CONS(ELEVEN)(
    CONS(TWELVE)(CONS(FOURTEEN)(CONS(FOURTEEN)(NIL)))
)
BUZZ = CONS(TEN)(
    CONS(THIRTEEN)(CONS(FOURTEEN)(CONS(FOURTEEN)(NIL)))
)
FIZZBUZZ_WORD = FOLD(CONS)(BUZZ)(FIZZ)
```

```python
>>> to_str(FIZZ), to_str(BUZZ), to_str(FIZZBUZZ_WORD)
('Fizz', 'Buzz', 'FizzBuzz')
```

- `FIZZBUZZ_WORD` は連結：`FIZZ` の末尾の `NIL` を `BUZZ` に置き換える（`PUSH` と同じ方法）

<!--
目安 0.5 分。Fizz は F、i、z、z なので 11、12、14、14 のリストです。Buzz も同様です。FizzBuzz はこの 2 つの連結で、FOLD(CONS) で FIZZ を写しながら、末尾の NIL を BUZZ に置き換えると連結になります。PUSH と同じ発想です。
-->

---

<!-- _class: optional -->

## `FIZZBUZZ_ITEM`：数 n を FizzBuzz の 1 項目に変える

```python
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
      (ID))
```

<!--
目安 0.5 分。1 つの数 n を、FizzBuzz の 1 項目の文字列に変換します。3 で割り切れるか、5 で割り切れるかで 4 通りに分けているだけで、普通の FizzBuzz と同じ構造です。if の代わりに IF とサンク、という書き方もここまでと同じです。
-->

---

<!-- _class: optional -->

## `FIZZBUZZ`：1 から n までを変換して並べる

```python
FIZZBUZZ = lambda n: MAP(FIZZBUZZ_ITEM)(RANGE(ONE)(n))
FIFTEEN = MUL(THREE)(FIVE)
```

```python
>>> to_list(FIZZBUZZ(FIFTEEN), to_str)
['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8',
 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']
```

- 1〜15 の計算は約 3 ms。再帰上限 1000 のままで n は **240 程度まで** 動く

<p class="note">実測（入力は SUCC の鎖）：通常実行で 247、検証スクリプト経由で 246 まで完走。</p>

<!--
目安 1 分。1 から n までの RANGE に FIZZBUZZ_ITEM を MAP するだけです。15 は MUL(THREE)(FIVE) で作りました。to_str で変換すると、FizzBuzz の列が出てきます。数値リテラルも文字列も if も使わずに書けています。手元の計測では 1 から 15 で約 3 ミリ秒、Python の再帰上限を変えずに 240 程度まで動きます。入力を SUCC の鎖で作った実測では、ふつうに実行して 247、検証用のスクリプト経由では 246 まで完走し、その次で RecursionError でした。実行のしかたや数の作り方で、境界は少し変わります。
-->

---

<!-- _class: chapter optional -->

# <span class="num" id="ch8">8</span>SKI コンビネータ

発展 6.5 分

コード：[Colab §8](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec8)

<!--
目安 0.25 分。最後の発展章です。ここまでは 1 引数の lambda と適用だけで計算してきましたが、この章では lambda も使わずに計算します。
-->

---

<!-- _class: twocol optional -->

## コンビネータ `S`、`K`、`I`：`I` は `S K K`

<div class="cols">
<div>

$$S = \lambda x.\,\lambda y.\,\lambda z.\,x\,z\,(y\,z)$$

$$K = \lambda x.\,\lambda y.\,x$$

$$I = \lambda x.\,x$$

</div>
<div>

```python
S = (lambda x: lambda y:
     lambda z: x(z)(y(z)))
K = lambda x: lambda y: x
I = S(K)(K)
```

```python
>>> to_int(I(THREE))
3
```

</div>
</div>

- $S$：$z$ を $x$ と $y$ の両方に配る　$K$：2 つ目の引数を捨てる　$I$：引数を返す
- $S\,K\,K\,x \twoheadrightarrow_\beta K\,x\,(K\,x) \twoheadrightarrow_\beta x$ なので $I = S\,K\,K$。この章では S と K の適用だけで計算する

<!--
目安 1.5 分。コンビネータ論理 (combinatory logic) の 3 つの基本コンビネータです。K は 2 引数のうち 1 つ目を返し、2 つ目を捨てます。I は恒等関数です。S は 3 つ目の引数 z を x と y の両方に配って、x(z) に y(z) を適用します。Schönfinkel が 1924 年に導入し、Curry が発展させました。カリー化の名前の由来の Curry です。I は S と K から作れます。S K K を x に適用すると、S が x を 2 つの K に配って K x (K x) になり、外側の K x が 2 つ目の引数を捨てて x が残ります。だから I を別に用意しなくても、S と K の 2 つで足ります。
-->

---

<!-- _class: optional -->

## `K` は `TRUE`、`K I` は `FALSE`

<div class="cols">
<div>
<div class="steps">

| | |
|---|---|
| | $K\,a\,b$ |
| $\twoheadrightarrow_\beta$ | $a$ |

</div>
</div>
<div>
<div class="steps">

| | |
|---|---|
| | $K\,I\,a\,b$ |
| $\twoheadrightarrow_\beta$ | $I\,b$ |
| $\twoheadrightarrow_\beta$ | $b$ |

</div>
</div>
</div>

```python
>>> to_bool(K), to_bool(K(I))
(True, False)
```

- `K` は 1 つ目の引数を選ぶので **TRUE** と同じ。式も同じ形
- `K I` は 2 つ目の引数を選ぶので **FALSE** と同じ

<!--
目安 0.75 分。K a b は a なので、2 つから 1 つ目を選ぶ TRUE です。定義 λx.λy.x は TRUE の λt.λf.t と変数名が違うだけです。K I a b は、まず K が a を捨てて I が残り、I b で b になります。2 つ目を選ぶので FALSE と同じです。to_bool で変換しても、True と False が返ります。
-->

---

<!-- _class: optional -->

## ブラケット抽象 (bracket abstraction)

λ を外す変換 $\mathcal{T}$：3 つの規則

$$
\begin{aligned}
\mathcal{T}[\lambda x.\,x] &= I \\
\mathcal{T}[\lambda x.\,E] &= K\,\mathcal{T}[E] \\
\mathcal{T}[\lambda x.\,E_1\,E_2] &= S\,\mathcal{T}[\lambda x.\,E_1]\,\mathcal{T}[\lambda x.\,E_2]
\end{aligned}
$$

- 2 行目は $x$ が $E$ に **自由に出ない** とき：引数を捨てる
- 3 行目は引数 $x$ を $E_1$ と $E_2$ の両方に **配る**
- λ が入れ子なら内側の λ から変換する。λ のない部分はそのまま残す

<!--
目安 1.5 分。λ項から λ を消して、S、K、I の式に書き換える変換がブラケット抽象です。自由変数はそのまま残るので、S、K、I だけになるのは自由変数のない閉じた項です。ここでは雰囲気だけ紹介します。λx の本体が x そのものなら I。本体に x が自由に出てこなければ、引数は捨ててよいので K。本体が適用 E1 E2 なら、引数 x を両側に配る S を使い、それぞれの側で同じ変換を続けます。規則は、引数をそのまま返す、捨てる、両側に配る、の 3 つだけです。λ が入れ子のときは内側の λ から順に消していきます。
-->

---

<!-- _class: optional -->

## ブラケット抽象の例：ω と λx. SUCC x

<div class="cols">
<div>
<div class="steps">

| | |
|---|---|
| | $\mathcal{T}[\lambda x.\,x\,x]$ |
| $=$ | $S\,\mathcal{T}[\lambda x.\,x]\,\mathcal{T}[\lambda x.\,x]$ |
| $=$ | $S\,I\,I$ |

</div>
</div>
<div>
<div class="steps">

| | |
|---|---|
| | $\mathcal{T}[\lambda x.\,\mathrm{SUCC}\,x]$ |
| $=$ | $S\,\mathcal{T}[\lambda x.\,\mathrm{SUCC}]\,\mathcal{T}[\lambda x.\,x]$ |
| $=$ | $S\,(K\,\mathrm{SUCC})\,I$ |

</div>
</div>
</div>

```python
>>> to_int(S(I)(I)(ID)(THREE)), to_int(S(K(SUCC))(I)(TWO))
(3, 3)
```

- $S\,I\,I\,a \twoheadrightarrow_\beta a\,a$ なので $S\,I\,I$ は ω と同じふるまい。右の例は η変換を使えばただの $\mathrm{SUCC}$

<!--
目安 1.5 分。2 つの例です。左は 6 章の ω、つまり λx.x x です。本体は x と x の適用なので S で配り、両側は λx.x なので I、結果は S I I です。S I I a は I a (I a)、つまり a a になるので ω と同じふるまいです。自分自身に適用すると omega(omega) と同じく止まりません（ノートブックで試せます）。右は 3 つの規則がすべて出てくる例です。本体は SUCC と x の適用なので S で配り、左の SUCC には x が出てこないので K、右は x そのものなので I です。S (K SUCC) I に 2 を渡すと 3 になります。η変換を使えばただの SUCC ですが、規則どおり機械的に変換するとこうなります。
-->

---

<!-- _class: optional -->

## S・K・I の適用だけでチューリング完全

- どんな λ 項も、ブラケット抽象で $S$・$K$・$I$ と元の自由変数からなる式になる
- 閉じた項（自由変数のない項）なら、残るのは $S$・$K$・$I$ の適用だけ。変数も λ もいらない
- $I = S\,K\,K$ なので、$S$ と $K$ の 2 つで足りる
- この体系はラムダ計算と同じ計算能力を持つ：**チューリング完全** (Turing complete)

<p class="note"><a href="#ch6">6 章</a>の Z も、FizzBuzz も、原理的には S と K の適用だけで書ける（とても長くなる）。</p>

<!--
目安 1 分。まとめです。ブラケット抽象を使えば、どんな λ 項からも λ を消せます。自由変数はそのまま残りますが、自由変数のない閉じた項なら、S、K、I の適用だけの式になります。しかも I は S K K なので、S と K の 2 つだけで足ります。ラムダ計算と同じ計算能力を持つので、チューリング機械とも同じ、つまりチューリング完全です。この章で見た Z や FizzBuzz も、原理的には S と K を並べた式で書けます。1 章で見た「Python の道具を減らしていく」話は、S と K の 2 つと適用まで減らせることになります。
-->


---

<!-- _class: chapter -->

# <span class="num" id="ch9">9</span>まとめと先へ

目安 3 分（発展 +1 分）

コード：[Colab §9](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec9)（性能の計測を含む）

<!--
目安 0.25 分。最後に、今日作ったものを振り返って、この先につながる話をいくつかします。
-->

---

## 今日作ったもの

| 種類 | 定義 |
|---|---|
| 真偽値 | `TRUE` `FALSE` `IF` `NOT` `AND` `OR` |
| 自然数 | `ZERO` `SUCC` `ADD` `MUL` `POW` `IS_ZERO` |
| ペアと引き算 | `PAIR` `FIRST` `SECOND` `PRED` |
| 再帰 | `Y` `Z` `FACT` `SUM_TO_N` |

```python
>>> to_int(FACT(FIVE))
120
```

<!--
目安 0.5 分。今日は lambda だけで、真偽値、自然数と四則の一部、ペアと引き算、そして再帰を作りました。冒頭で見せたとおり、FACT に FIVE を渡すと 120 になります。数値リテラルも if も def も使っていません。発展まで進んだ場合は、リストや FizzBuzz、SKI コンビネータも作りました。
-->

---

<!-- _class: optional -->

## 型を付けると Y は書けない

単純型付きラムダ計算 (simply typed lambda calculus)：どの項にも型 $A \to B$ などが付く。

自己適用 $x\;x$ に型を付けようとすると

$$x : A \to B \quad\text{かつ}\quad x : A \qquad\Rightarrow\qquad A = A \to B$$

- これを満たす型 $A$ はない → $\omega$、$Y$、$Z$ は型が付かない
- **強正規化** (strong normalization)：型の付く項はすべて停止する
- そのため一般の再帰は書けない。型のある実用言語は再帰を別に用意する

<!--
目安 1 分。発展です。今日のラムダ計算には型がありませんでした。項に型を付ける単純型付きラムダ計算では、x x のような自己適用に型が付きません。x が関数としての型 A→B と、その引数としての型 A を同時に持つ必要があり、A と A→B が等しい型は作れないからです。そのため ω も Y も Z も書けません。実際、単純型付きラムダ計算では型の付く項はすべて停止することが知られていて、これを強正規化と呼びます。止まることが保証される代わりに、一般の再帰は書けません。型のある実用言語は、再帰を言語の機能として別に用意しています。
-->

---

## 実用言語とのつながり

- **クロージャ** (closure)：自由変数を捕まえた lambda。今日のコードはクロージャの塊
- **Lisp**：`lambda` という名前はラムダ計算から。Python の `lambda` もその流れ
- **Haskell**：遅延評価 (lazy evaluation)。引数を必要になるまで計算しない
  - 不動点を `fix f = f (fix f)` とそのまま書ける（Z の工夫が要らない）
- 型付きラムダ計算は、ML や Haskell の型システムの土台

<!--
目安 0.75 分。今日の話は実用言語とつながっています。lambda が外側の変数を覚えている仕組みはクロージャそのもので、今日のコードは全部クロージャでできています。Lisp は lambda という名前をラムダ計算から借りていて、Python の lambda もその流れです。Haskell は遅延評価の言語で、引数を必要になるまで計算しないので、Python で苦労した Y の問題が起きず、不動点を素直に定義できます。型付きラムダ計算は ML や Haskell の型システムの土台になっています。なお、型を付けると Y は書けなくなります（詳しくは発展スライドを参照）。
-->

---

## 性能：チャーチ数の計算は遅く、スタックもすぐ溢れる

- チャーチ数は**一進法** (unary)：$n$ は「$f$ を $n$ 回」
- `SUCC`・`ADD` を重ねて作った数は、`to_int` で変換するときスタックを深く使う
- `MUL`・`POW` で作った数は、値が大きくてもスタックの深さは値に比例しない
- 実測（CPython 3.14、再帰上限 1000 の既定値）：

| 計算 | 最後まで動いた最大の $n$ | 次の値 |
|---|---:|---|
| `FIB`（[6 章](#ch6)発展） | 16 | RecursionError |
| `SUM_TO_N` | 44 | RecursionError |
| `FACT` | 11（約 10 秒） | 15 秒で打ち切り（時間切れ） |

<!--
目安 1 分。この方法はとても遅く、スタックもすぐに溢れます。チャーチ数は一進法で、n を表すのに f を n 回使うので、整数に直す仕事は数に比例して大きくなります。SUCC や ADD でつないだ数は、見るときにスタックも深く使います。ただし MUL や POW で作った数は関数の合成なので、値が大きくても深さはそれほどではありません。実測では、FIB（6 章の発展）は 16、SUM_TO_N は 44 まで動き、その次で RecursionError でした。FACT は 11 で約 10 秒かかり、12 は 15 秒で打ち切りました。FACT の境界はスタックではなく時間です。実用には向かず、計算の仕組みを確かめるためのものです。
-->

---

## 参考文献（1/2）原論文と歴史

<div class="small">

- A. Church. [An Unsolvable Problem of Elementary Number Theory](https://doi.org/10.2307/2371045). American Journal of Mathematics 58(2), 345–363, 1936.
- A. M. Turing. [On Computable Numbers, with an Application to the Entscheidungsproblem](https://doi.org/10.1112/plms/s2-42.1.230). Proc. London Math. Soc. s2-42(1), 230–265, 1936–37.
- A. M. Turing. [Computability and λ-Definability](https://doi.org/10.2307/2268280). Journal of Symbolic Logic 2(4), 153–163, 1937.
- S. C. Kleene. [Origins of Recursive Function Theory](https://doi.org/10.1109/MAHC.1981.10004). Annals of the History of Computing 3(1), 52–67, 1981.
- J. N. Crossley (ed.). [Reminiscences of Logicians](https://doi.org/10.1007/BFb0062850). In: Algebra and Logic, Lecture Notes in Mathematics 450, 1–62, Springer, 1975.
- H. P. Barendregt. [The Impact of the Lambda Calculus in Logic and Computer Science](https://doi.org/10.2307/421013). Bulletin of Symbolic Logic 3(2), 181–215, 1997.

</div>

<!--
目安 0.1 分。映すだけにします。前半は原論文と、5 章で紹介した Kleene の前者関数の逸話の出典（Barendregt 1997、Crossley 編の回想録、Kleene 1981）です。
-->

---

## 参考文献（2/2）教科書と読み物

<div class="small">

- H. P. Barendregt. [The Lambda Calculus: Its Syntax and Semantics](https://shop.elsevier.com/books/the-lambda-calculus/barendregt/978-0-444-87508-2). North-Holland, 1981; revised ed. 1984.
- B. C. Pierce. [Types and Programming Languages](https://mitpress.mit.edu/9780262162098/types-and-programming-languages/). MIT Press, 2002.
- 高橋正子『[計算論 計算可能性とラムダ計算](https://www.kindaikagaku.co.jp/book_list/detail/9784764901841/)』近代科学社, 1991.
- T. Stuart. [Programming with Nothing](https://tomstu.art/programming-with-nothing). Ruby Manor 3 での講演と同名の記事, 2011.
- T. Stuart. [Understanding Computation](https://www.oreilly.com/library/view/understanding-computation/9781449330071/). O'Reilly, 2013.

</div>

<!--
目安 0.15 分。映すだけにします。日本語なら高橋正子さんの『計算論』、手を動かすなら Tom Stuart さんの Programming with Nothing（Ruby の lambda（proc）だけで FizzBuzz まで書く講演と記事）がおすすめです。
-->

---

<!-- _class: title -->
<!-- _paginate: false -->

# おわり

## ラムダ計算を Python で動かす

質疑応答

<div class="small">

スライドとコード：[github.com/elle-et-noire/lambda-talk](https://github.com/elle-et-noire/lambda-talk)

参照実装：[code/lambda_core.py](https://github.com/elle-et-noire/lambda-talk/blob/main/code/lambda_core.py) ・ ノートブック：[Colab](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb)

</div>

<!--
目安 0.25 分。今日は、関数を作って呼ぶことだけで、真偽値や数、再帰まで作りました。スライドと今日のコードは GitHub の elle-et-noire/lambda-talk に置いてあります。同じコードは Colab のノートブックでも動かせます。ありがとうございました。質問があればどうぞ。
-->
