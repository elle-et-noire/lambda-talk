---
marp: true
theme: quiet
paginate: true
math: katex
size: 16:9
title: Python からクラスも数も消す（ラムダ計算）
author: elle-et-noire
description: Python の lambda だけで真偽値・自然数・足し算・再帰を作るラムダ計算入門
lang: ja
---

<!-- _class: title -->
<!-- _paginate: false -->

# Python からクラスも数も消す

## ラムダ計算 (lambda calculus) 入門

lambda だけで真偽値・自然数・足し算を作り、最後は Y コンビネータで再帰を書きます。計算の最小単位を体験できます。

<div class="small">

elle-et-noire ・ [github.com/elle-et-noire/lambda-talk](https://github.com/elle-et-noire/lambda-talk)

</div>

<!--
目安 0.5 分。こんにちは。今日は Python の lambda だけを使って、ふだん当たり前に使っている真偽値や数、足し算を自分で作ってみます。最後は Y コンビネータという仕掛けで再帰まで書きます。数もクラスも if もない世界で、計算の最小単位は何かを体験してもらうのが今日のゴールです。
-->

---

## 今日作るもの

- **真偽値**：`TRUE`、`FALSE`、`IF`
- **自然数**：チャーチ数 (Church numerals) `ZERO`、`SUCC`
- **足し算**：`ADD`（掛け算・累乗も）
- **再帰**：Y コンビネータ (Y combinator) と、その仲間 Z

最後にはこれが動く。

```text
to_int(FACT(FIVE))   →   120
```

<div class="note">

手を動かす用：[Colab ノートブック（lambda.ipynb）](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb)。§番号＝章番号

</div>

<!--
目安 0.5 分。今日作るものはこの 4 つです。真偽値、自然数、足し算、そして再帰です。最後には、lambda だけで作った階乗 FACT に、lambda だけで作った 5 を渡して、120 が出てくるところまで行きます。to_int は結果を見るための窓で、すぐ後で説明します。今日のコードは Colab のノートブックにまとめてあり、章と同じ番号の節で手元でも試せます。
-->

---

## ルール

<div class="cols">
<div>

**使ってよい**

- 1 引数の `lambda`
- 関数適用 `f(x)`
- 名前付け（長い式の略記）

</div>
<div>

**使わない**

- 数値リテラル `0`、`1`、……
- `True`、`False`、`if`
- `class`、組み込み演算子 `+` `==` など
- `def` による再帰

</div>
</div>

名前付けは**略記だけ**。自分自身を参照する名前付け（再帰定義）は禁止。

<p class="note">「自分の名前を呼ばずに再帰できるか」が <a href="#ch6">6 章</a>（Y コンビネータ）の動機になる。</p>

<!--
目安 0.75 分。ルールです。使ってよいのは、引数が 1 つの lambda と、関数を呼ぶことと、名前を付けることだけです。名前はあくまで長い式の略記で、名前を中身の式に置き換えても意味が変わらない、という約束です。だから、定義の中で自分自身の名前を使う、つまり再帰定義は禁止です。これが 6 章の Y コンビネータの動機になります。数値リテラル、True と False、if、class、足し算や比較の演算子、def による再帰は使いません。
-->

---

## 例外：観測用関数＝窓

純粋な世界の値は lambda なので、そのままでは中身が見えない。

| 純粋な世界 | 窓 | Python の値 |
|---|---|---|
| `TRUE`、`FALSE` | `to_bool` | `True`、`False` |
| `ZERO`、`SUCC(...)` | `to_int` | `0`、`1`、`2`、…… |
| リスト（[7 章](#ch7)） | `to_list` | `[...]` |
| 文字列（[7 章](#ch7)） | `to_str` | `'FizzBuzz'` |

窓は**純粋な世界の外側**にある。結果を見るだけで、計算には使わない。

<!--
目安 0.5 分。唯一の例外が観測用の関数で、今日は「窓」と呼びます。lambda で作った TRUE や 3 は、print しても function としか表示されません。そこで、外側から覗いて Python の True や 3 に直して見せる関数を用意します。窓の中身は普通の Python で、数値リテラルも + も使いますが、それは純粋な世界の外側だからです。窓は見るためだけに使い、計算の途中には入れません。to_bool は 3 章、to_int は 4 章で作ります。
-->

---

## 時間割

<div class="small">

| 章 | 内容 | 必須 | 発展 |
|---|---|---:|---:|
| [1](#ch1) | 導入：Church と Turing | 3.5 分 | |
| [2](#ch2) | 文法と評価：β簡約 | 9.5 分 | 5 分 |
| [3](#ch3) | チャーチ真偽値 | 8 分 | 2 分 |
| [4](#ch4) | チャーチ数：足し算・掛け算 | 9.5 分 | 4 分 |
| [5](#ch5) | ペアと引き算 | 5 分 | 6 分 |
| [6](#ch6) | 再帰と Y コンビネータ（山場） | 16.5 分 | 2 分 |
| [7](#ch7) | リストと FizzBuzz | | 17.5 分 |
| [8](#ch8) | SKI コンビネータ | | 10 分 |
| [9](#ch9) | まとめと先へ | 3 分 | 1 分 |

</div>

必須のみ約 57.5 分（冒頭 2.5 分込み）。「発展」は時間次第で飛ばす。

<!--
目安 0.25 分。見せるだけにします。必須だけで約 1 時間、右上に「発展」とあるスライドは時間を見て飛ばします。山場は 6 章です。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch1">1</span>導入

目安 3.5 分

<!--
目安 0.25 分。まず、なぜこんなことをするのか、背景の話を少しします。
-->

---

## 計算に本当に必要なものは？

Python にはたくさんの道具がある。

- 数と演算子、`if` と `while`、`class`、`def`……

どこまで削っても、まだ「計算」できるか？

**答え：関数を作ることと、関数を呼ぶことだけで足りる。**

<!--
目安 0.75 分。Python には、数や演算子、if、while、class、def と、たくさんの道具があります。これを 1 つずつ取り上げていったら、どこで計算できなくなるでしょうか。今日の答えを先に言ってしまうと、関数を作ることと関数を呼ぶこと、この 2 つだけ残せば、数も分岐も再帰も全部作り直せます。それを実際に手を動かして確かめるのが今日の講習です。
-->

---

## 1930 年代：二つの「計算」の定義

| | Church | Turing |
|---|---|---|
| モデル | ラムダ計算 | チューリング機械 (Turing machine) |
| 中身 | 関数を作る・呼ぶ | テープを読み書きする |
| 論文 | 1936 年 | 1936 年 |

- 1937 年、Turing が**両者は同じ計算能力**を持つことを示す
- チャーチ＝チューリングのテーゼ (Church–Turing thesis)：機械的な手順で計算できる関数は、ちょうどこれ。**定理ではなく提唱**
- 根拠：独立に提案された主要なモデル（λ計算、チューリング機械、一般再帰関数）が同じ範囲を与えた

<!--
目安 1.5 分。1930 年代に、「計算できる」とはどういうことかを数学的に定義しようとした人が二人います。アロンゾ・チャーチはラムダ計算、つまり関数を作って呼ぶだけの体系を考えました。アラン・チューリングは、テープに記号を読み書きする機械を考えました。どちらも 1936 年に論文を出し、「機械的に解けない問題がある」ことを示しました（λ記法自体は 1932 年の論文で導入）。見た目はまったく違いますが、1937 年にチューリングが、この二つで計算できる関数の範囲が一致することを示しました。これを背景に、「有限の規則に従って機械的に計算できる関数は、まさにこれだ」と主張するのがチャーチ＝チューリングのテーゼです。「機械的に計算できる」は直観的な概念で数学的な定義がないので、定理ではなく提唱です。根拠は、λ計算、チューリング機械、一般再帰関数という、独立に提案された主要なモデルが同じ範囲を与えたことです。今日は、そのうち一番小さいラムダ計算を Python で動かします。
-->

---

<!-- _class: twocol -->

## λ記法と Python の lambda

<div class="cols">
<div>

$$\lambda x.\,x$$

$$\lambda x.\,\lambda y.\,x$$

$$\lambda f.\,\lambda x.\,f\,x$$

$$(\lambda x.\,x)\;(\lambda y.\,y)$$

</div>
<div>

```python
lambda x: x

lambda x: lambda y: x

lambda f: lambda x: f(x)

(lambda x: x)(lambda y: y)
```

</div>
</div>

$\lambda$ → `lambda`、ドット → コロン、並べて書く → 括弧で呼ぶ。

<!--
目安 1 分。λ記法と Python の対応です。ギリシャ文字のラムダが Python のキーワード lambda、ドットがコロンに対応します。違うのは関数の呼び出しで、λ記法では f x のように並べて書くだけ、Python では f(x) と括弧を付けます。2 段目のように、引数を 2 つ取る関数は lambda を 2 つ重ねて書きます。これは次の章で詳しく見ます。Python の lambda という名前自体、このラムダ計算から来ています。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch2">2</span>文法と評価

目安 9.5 分（発展 +5 分）

[Colab §2 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec2)

<!--
目安 0.25 分。ラムダ計算の文法と、式がどう計算されるかを見ます。ここが今日の全部の土台です。
-->

---

## 項は 3 種類だけ

ラムダ計算の式＝項 (term)。BNF で書くと：

$$
M,\,N \;::=\; x \;\mid\; \lambda x.\,M \;\mid\; M\,N
$$

| 形 | 名前 | 意味 |
|---|---|---|
| $x$ | 変数 (variable) | 名前 |
| $\lambda x.\,M$ | 抽象 (abstraction) | 関数を作る |
| $M\,N$ | 適用 (application) | 関数を呼ぶ |

<p class="note">読み方：「::=」は「次のどれか」、「|」は「または」。M, N は任意の項を表す記号（メタ変数）。</p>

<!--
目安 0.75 分。ラムダ計算の式、項は、この 3 種類しかありません。上の式は BNF という文法の書き方で、「項 M は、変数 x か、λx.M か、M N のどれか」と読みます。M や N は任意の項を表す記号です。抽象は「x を受け取って M を返す関数を作る」、適用は「M という関数に N を渡して呼ぶ」です。数も if もありません。これで全部です。
-->

---

<!-- _class: twocol -->

## Python に写すと

<div class="cols">
<div>

$$\lambda x.\,x$$

$$(\lambda x.\,x)\;a$$

$$(\lambda x.\,x)\,(\lambda x.\,x)\;b$$

</div>
<div>

```python
>>> ID = lambda x: x
>>> ID("a")
'a'
>>> ID(ID)("b")
'b'
```

</div>
</div>

変数＝名前、抽象＝`lambda`、適用＝呼び出し `f(x)`。

<p class="note">自由な名前 a, b の代わりに文字列 "a", "b" を渡して観察する（窓と同じく、外側の値）。</p>

<!--
目安 1 分。Python では、変数は名前、抽象は lambda、適用は関数呼び出しです。ここで最初の定義、恒等関数 ID を作ります。受け取ったものをそのまま返すだけの関数です。地味ですが、3 章以降で何度も使うので覚えておいてください。動作を見るときは、外側の値として文字列 "a" を渡します。文字列は観察のための外側の値で、定義の中には使いません。ID に ID を渡すと ID が返るので、さらに "b" を渡すと "b" が出ます。関数に関数を渡せる、というのがラムダ計算の基本です。
-->

---

## 表記の約束

| 約束 | 書き方 | 意味 |
|---|---|---|
| 適用は左結合 | $f\,a\,b$ | $(f\,a)\,b$ |
| 抽象は右へ伸びる | $\lambda x.\,M\,N$ | $\lambda x.\,(M\,N)$ |
| 抽象の入れ子 | $\lambda x.\,\lambda y.\,M$ | $\lambda x.\,(\lambda y.\,M)$ |

Python では括弧が明示される：`f(a)(b)`、`lambda x: M(N)`。

<!--
目安 0.75 分。括弧を減らすための約束が 2 つあります。適用は左から順にまとめます。f a b は、f に a を渡して、その結果に b を渡す、です。抽象の本体は、できるだけ右へ伸ばして読みます。λx. M N は M N 全体が本体です。Python では括弧で書くので迷いませんが、λ記法を読むときはこの約束を思い出してください。
-->

---

## 自由変数と束縛変数

$$\lambda x.\,x\;y$$

- $x$：$\lambda x$ に**束縛**されている → 束縛変数 (bound variable)
- $y$：どの $\lambda$ にも捕まっていない → 自由変数 (free variable)

Python で言えば、自由変数＝外側から借りてくる名前。

```python
>>> (lambda y: lambda x: y)("外")("a")
'外'
```

<p class="note">内側の <code>lambda x: y</code> だけを見ると、y は自由変数。</p>

<!--
目安 0.75 分。項の中の変数には 2 種類あります。λx の x のように、引数として受け取った変数を束縛変数と呼びます。y のように、どの λ にも捕まっていない変数を自由変数と呼びます。Python で言うと、自由変数は lambda の外側から借りてくる名前です。下の例の内側の lambda x: y だけを見ると、y は自由変数で、外側の lambda y が渡した値を借りています。クロージャを書いたことがあれば、閉じ込められた外側の変数が自由変数です。
-->

---

## α変換：束縛変数の名前は自由

$$\lambda x.\,x \;\equiv_\alpha\; \lambda y.\,y$$

- 束縛変数の名前を付け替えても同じ関数：α変換 (alpha conversion)
- Python でも `lambda x: x` と `lambda y: y` は同じふるまい
- ただし**自由変数と同じ名前**には付け替えない

$$\lambda x.\,x\;y \;\not\equiv_\alpha\; \lambda y.\,y\;y$$

<!--
目安 0.75 分。束縛変数の名前は、関数の引数名と同じで、何と付けても意味は変わりません。この付け替えを α変換と呼びます。ただし 1 つ注意があります。下の例のように x を y に付け替えると、もともと外側の y を指していたものと区別がつかなくなり、別の関数になってしまいます。付け替える先は、まだ使われていない名前にします。
-->

---

## β簡約：関数を呼ぶ規則

$$(\lambda x.\,M)\;N \;\to_\beta\; M[x := N]$$

- 本体 $M$ における $x$ の**自由な出現だけ**を、引数 $N$ で置き換える：β簡約 (beta reduction)
- $M[x := N]$ は代入 (substitution)。内側の $\lambda x$ に束縛された $x$ は置き換えない
- 左辺の形を簡約基 (redex) と呼ぶ
- 名前がぶつかりそうなら、先に α変換してから代入する
- Python の関数呼び出しが、まさにこれ

<!--
目安 1 分。ラムダ計算の計算規則は、実質これ 1 つです。λx.M に N を適用したら、本体 M の中の x を N に置き換える。これを β簡約と呼びます。ただし置き換えるのは、M の中で自由に出てくる x だけです。たとえば (λx.λx.x) a は λx.x で、λx.a ではありません。内側の x は内側の λx に捕まっているからです。左辺のように、λ の関数に引数が渡されていて、すぐ簡約できる形を簡約基と呼びます。置き換えるときに名前がぶつかりそうなら、さっきの α変換で先に名前を変えておきます。Python で関数を呼ぶと、引数が引数名に結び付いて本体が実行されますが、やっていることは同じです。
-->

---

## β簡約を 1 ステップずつ

<div class="steps">

| | |
|---|---|
| | $(\lambda x.\,\lambda y.\,x)\;a\;b$ |
| $\to_\beta$ | $(\lambda y.\,a)\;b$ |
| $\to_\beta$ | $a$ |

</div>

1 回目：$x$ に $a$ を代入。2 回目：$y$ に $b$ を代入（本体に $y$ はない）。

```python
>>> (lambda x: lambda y: x)("a")("b")
'a'
```

<!--
目安 0.75 分。具体例です。左結合なので、まず λx.λy.x に a を渡します。本体 λy.x の x を a に置き換えて λy.a になります。次にそれに b を渡します。本体は a で、y はどこにも出てこないので、b は捨てられて a が残ります。2 つ受け取って最初の方を返す関数です。Python でも同じく "a" が返ります。この形は 3 章で TRUE として再登場します。
-->

---

## カリー化：`f(a)(b)` の読み方

引数は 1 つだけ。2 引数は「関数を返す関数」で表す：カリー化 (currying)

```python
>>> (lambda x: lambda y: x)("a")
<function <lambda>.<locals>.<lambda> at 0x...>
>>> (lambda x: lambda y: x)("a")("b")
'a'
```

- `f(a)` は「残りの引数 `y` を待つ関数」を返す
- `f(a)(b)` は、それにもう 1 回 `b` を渡す
- λ記法の $f\,a\,b$ ＝ Python の `f(a)(b)`

<!--
目安 0.75 分。今日のルールでは lambda の引数は 1 つだけです。2 つ必要なときは、1 つ受け取って「残りを待つ関数」を返します。これをカリー化と呼びます。f(a) だけを評価すると、関数がそのまま返ってきます。まだ y を待っている状態です。それに b を渡すと答えが出ます。今日のコードには f(a)(b)(c) のように括弧がずらっと並びますが、左から 1 つずつ渡している、と読んでください。
-->

---

<!-- _class: exercise -->

## 手で β簡約する

1 ステップずつ簡約して、これ以上進めない形にする。

1. $(\lambda x.\,x\;x)\;(\lambda y.\,y)$
2. $(\lambda x.\,\lambda y.\,y\;x)\;a\;(\lambda z.\,z)$

<p class="note">ヒント：適用は左結合。いちばん外側の λ から引数を受け取る。</p>

<!--
目安 2 分。演習です。紙の上で、1 ステップずつ β簡約してみてください。1 問目は自分自身を 2 回使う関数に恒等関数を渡します。2 問目は左結合に注意して、まず a を渡し、その結果に λz.z を渡します。2 分取ります。
-->

---

<!-- _class: answer -->

## 手で β簡約する：解答

<div class="cols">
<div>
<div class="steps">

| | |
|---|---|
| | $(\lambda x.\,x\;x)\;(\lambda y.\,y)$ |
| $\to_\beta$ | $(\lambda y.\,y)\;(\lambda y.\,y)$ |
| $\to_\beta$ | $\lambda y.\,y$ |

</div>
</div>
<div>
<div class="steps">

| | |
|---|---|
| | $(\lambda x.\,\lambda y.\,y\;x)\;a\;(\lambda z.\,z)$ |
| $\to_\beta$ | $(\lambda y.\,y\;a)\;(\lambda z.\,z)$ |
| $\to_\beta$ | $(\lambda z.\,z)\;a$ |
| $\to_\beta$ | $a$ |

</div>
</div>
</div>

```python
>>> (lambda x: lambda y: y(x))("a")(ID)
'a'
```

<!--
目安 0.75 分。1 問目は、x に λy.y を入れると、λy.y を λy.y に適用する形になり、もう 1 回簡約して λy.y が残ります。2 問目は、まず x に a を入れて λy.y a、次に y に λz.z を入れて (λz.z) a、最後に a です。Python でも、λz.z の代わりに ID を渡すと "a" が返ります。
-->

---

<!-- _class: optional -->

## η変換 (eta conversion)

$x$ が $M$ の自由変数でないとき

$$\lambda x.\,M\,x \;\to_\eta\; M$$

- 「受け取って、そのまま M に渡す」関数は M と同じふるまい
- Python では `lambda v: f(v)` と `f` は同じ結果
- ただし **`f` を評価するタイミング**が変わる（[6 章](#ch6)の Z の伏線）

<!--
目安 1.5 分。発展です。λx. M x は、受け取った x をそのまま M に渡すだけなので、M と同じふるまいをします。これを η変換と呼びます。Python でも lambda v: f(v) と f は、呼べば同じ結果になります。ただし大事な違いがあって、lambda v: f(v) と書くと、f の部分は呼ばれるまで評価されません。この「包むと評価が遅れる」性質が、6 章の Z コンビネータの鍵になります。
-->

---

<!-- _class: optional -->

## 評価戦略：どの簡約基から簡約するか

$\Omega = (\lambda x.\,x\;x)\,(\lambda x.\,x\;x)$ は簡約しても自分に戻る（[6 章](#ch6)）。

$$(\lambda x.\,a)\;\Omega$$

| 戦略 | 順番 | 結果 |
|---|---|---|
| 正規順序 (normal order) | いちばん外側・左の簡約基から | $a$ |
| 適用順序 (applicative order) | いちばん内側・左（引数）から | 止まらない |

正規順序は、正規形 (normal form) があれば必ずたどり着く。

<!--
目安 2 分。発展です。項の中に簡約できる場所が複数あるとき、どこから簡約するかを評価戦略と呼びます。Ω は 6 章で出てくる、簡約しても自分自身に戻ってしまう項です。λx.a に Ω を渡すとき、いちばん外側・左の簡約基から簡約すれば x は使われないので a で終わります。これが正規順序です。一方、いちばん内側、つまり引数の中から先に簡約する適用順序だと、Ω の計算が終わらず止まりません。これ以上簡約できない形を正規形と呼びますが、正規順序は、正規形があれば必ずそこへたどり着くことが知られています。
-->

---

<!-- _class: optional -->

## Python は正格評価（値呼び）

関数を呼ぶ前に、**引数を値まで計算**する：値呼び (call by value)

```python
>>> (lambda x: "a")(print("引数を先に評価"))
引数を先に評価
'a'
```

- 使わない引数でも計算される：正格評価 (strict evaluation)
- ただし **lambda の中身は呼ばれるまで計算しない**
- [3 章](#ch3)：`IF` が両方の枝を計算／[6 章](#ch6)：Y コンビネータが止まらない

対策はどちらも「`lambda _: ...` で包んで、後で開ける」。

<!--
目安 1.5 分。発展です。では Python はどうでしょうか。引数を先に計算するので、適用順序に近い動きをします。関数を呼ぶ前に、引数を必ず値まで計算する。これを値呼び、または正格評価と呼びます。この例では x を使わないのに、print が先に実行されています。ただし適用順序と違って、lambda の中身は呼ばれるまで計算しません。この性質が、後で出てくる対策の鍵です。これが後で 2 回効いてきます。3 章では IF が両方の枝を計算してしまう問題、6 章では Y コンビネータが止まらない問題です。対策はどちらも、式を lambda で包んで評価を遅らせ、必要なときに開ける、という方法です。開けるのに、さっき作った ID を使います。
-->


---

<!-- _class: chapter -->

# <span class="num" id="ch3">3</span>チャーチ真偽値

目安 8 分（発展 +2 分）

[Colab §3 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec3)

<!--
目安 0.25 分。この章では True も False も if も使わずに、真偽値と分岐を関数だけで作ります。手がかりは「if は 2 つのうちどちらかを選ぶもの」という見方です。
-->

---

## 真偽値は「2 択から選ぶ関数」

- `if` の仕事：2 つの候補から **どちらか 1 つを選ぶ**
- それなら真偽値そのものに選ばせればよい
  - 真：2 つ受け取り、**1 つ目** を返す
  - 偽：2 つ受け取り、**2 つ目** を返す
- チャーチ真偽値 (Church booleans) と呼ぶ

<p class="note">データではなく「ふるまい」で真偽を表す。この見方が数・ペア・リストまで続く。</p>

<!--
目安 0.75 分。Python の True と False は「値」ですが、使い道はほぼ if で分岐することだけです。分岐とは 2 つから 1 つ選ぶことなので、真偽値自体を「選ぶ関数」にしてしまいます。真なら 1 つ目、偽なら 2 つ目。これを Church の名前を取ってチャーチ真偽値と呼びます。
-->

---

<!-- _class: twocol -->

## `TRUE` と `FALSE`

<div class="cols">
<div>

$$\mathrm{TRUE} = \lambda t.\,\lambda f.\,t$$

$$\mathrm{FALSE} = \lambda t.\,\lambda f.\,f$$

</div>
<div>

```python
TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
```

</div>
</div>

- カリー化で 2 引数：`TRUE(a)(b)` は `a`、`FALSE(a)(b)` は `b`
- 引数名 `t`、`f` は then／else のつもり

<!--
目安 0.75 分。2 章でやったカリー化のおかげで、2 引数関数は lambda を 2 段重ねるだけです。TRUE は 1 つ目の t を、FALSE は 2 つ目の f を返します。f は false ではなく「else 側」の意味で付けた名前です。中身はたったこれだけです。
-->

---

## 窓その1：`to_bool`

```python
to_bool = lambda b: b(True)(False)
```

```python
>>> to_bool(TRUE)
True
>>> to_bool(FALSE)
False
```

- 純粋な世界の **外側にある窓**：ここだけ Python の `True`/`False` を使う
- やっていることは「選ばせる」だけ。2 択に `True`、`False` を渡す

<!--
目安 0.75 分。今日最初の窓です。最初に約束したとおり、窓は純粋な世界の外側にあって、結果を人間が読める形にするためだけに使います。TRUE と FALSE はただの関数なので、表示しても何もわかりません。そこで 2 択の候補として Python の True と False を渡し、どちらを選ぶかを見ます。窓の定義の中では普通の Python を使ってよいことにします。
-->

---

## `IF`：実は何もしない

```python
IF = lambda b: lambda t: lambda f: b(t)(f)
```

<div class="steps">

| | |
|---|---|
| | $\mathrm{IF}\;\mathrm{TRUE}\;a\;b$ |
| $\twoheadrightarrow_\beta$ | $\mathrm{TRUE}\;a\;b$ |
| $\twoheadrightarrow_\beta$ | $a$ |

</div>

- 選ぶのは真偽値 `b` 自身。`IF` は読みやすさのための名前
- $\twoheadrightarrow_\beta$：β簡約を何回か（最初の矢印は 3 回、次は 2 回）

<!--
目安 0.75 分。IF は条件 b と 2 つの枝 t、f を受け取って、b に t と f を渡すだけです。β簡約すると IF TRUE a b は TRUE a b になり、さらに a になります。ここから矢印の先を 2 つにした記号を使います。β簡約を何回かまとめて行う、という意味です。選んでいるのは TRUE 自身で、IF は if らしく読めるように付けた包装紙にすぎません。この IF は後の落とし穴と再帰の章でまた出てきます。
-->

---

## `NOT` と `AND`：選ばせ方を工夫する

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
目安 0.5 分。a に TRUE と b の 2 択を選ばせます。AND と見比べると、候補の位置が鏡写しになっています。
-->

---

## 落とし穴：`IF` が両方の枝を計算してしまう

else 側に **止まらない式** を置くと、then が選ばれるはずでも失敗する。

```python
>>> to_bool(IF(TRUE)(TRUE)(
...     (lambda x: x(x))(lambda x: x(x))))
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

- Python は関数を呼ぶ **前に** 引数をすべて計算する：正格評価 (strict evaluation)
- `IF` が選ぶより先に、else 側の計算が始まって止まらない

<!--
目安 1 分。ここが Python でラムダ計算をやるときの最大の落とし穴です。Python は関数を呼ぶ前に、引数を全部計算します。これを正格評価と呼びます（2 章の発展で評価戦略を見た人には復習です）。だから IF に渡す前に、else 側の (lambda x: x(x))(lambda x: x(x)) まで計算してしまいます。これは自分自身を呼び続ける式で、計算が終わりません。だから TRUE を選ぶはずなのに RecursionError になります。この式は 6 章で Ω（大文字のオメガ）として詳しく扱います。ここでは「Python は引数を先に全部計算する」とだけ押さえれば十分です。
-->

---

## 対策：サンク `lambda _: ...` で包む

```python
>>> to_bool(IF(TRUE)(lambda _: TRUE)(
...     lambda _: (lambda x: x(x))(lambda x: x(x)))(ID))
True
```

1. 両方の枝を `lambda _:` で包む：作るだけで、中身は **まだ計算しない**
2. `IF` で包みを 1 つ選ぶ
3. 選んだ包みに `(ID)` を渡して、はじめて中身を計算する

包んだ式をサンク (thunk) と呼ぶ。[6 章](#ch6)の **Z コンビネータ** で再帰を書くときの鍵

<!--
目安 0.75 分。lambda で包むと、包み自体は関数という値なのですぐ作れますが、中身は呼ばれるまで計算されません。IF は包みを選ぶだけで、選ばれた包みに ID を渡したときに初めて中身が動きます。渡す値は何でもよいのですが、2 章の ID を使うと決めておきます。この「サンクで包んで選んでから実行する」形は、6 章で再帰を書くときにそのまま使います。ここが伏線です。
-->

---

<!-- _class: exercise optional -->

## `XOR` を書く

`XOR = lambda a: lambda b: ＿＿＿` を完成させよ（排他的論理和）。

| `a` | `b` | `XOR(a)(b)` |
|---|---|---|
| `TRUE` | `b` | `NOT(b)` |
| `FALSE` | `b` | `b` |

<p class="note">ヒント：これまでと同じく a に 2 択を選ばせる。使ってよいのは NOT。</p>

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

- `NOT`・`AND`・`OR`・`XOR`、どれも「最初の引数に 2 択を選ばせる」形

<!--
目安 0.5 分。a に NOT(b) と b の 2 択を選ばせます。この章の論理演算は、全部「最初の引数に何と何を選ばせるか」を決めるだけで書けました。
-->

---

<!-- _class: chapter -->

# <span class="num" id="ch4">4</span>チャーチ数

目安 9.5 分（発展 +4 分）

[Colab §4 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec4)

<!--
目安 0.25 分。次は数値リテラルなしで自然数を作ります。真偽値を「選ぶ」というふるまいで表したのと同じく、数を「繰り返す回数」というふるまいで表します。
-->

---

## 数 n ＝「f を n 回適用する関数」

$$\overline{n} = \lambda f.\,\lambda x.\,f^n\,x \qquad\text{（}f^n\,x = \underbrace{f\,(f\,(\cdots(f}_{n\text{ 回}}\,x)\cdots))\text{）}$$

| 数 | λ記法 | 意味 |
|---|---|---|
| $\overline{0}$ | $\lambda f.\,\lambda x.\,x$ | 1 回も適用しない |
| $\overline{1}$ | $\lambda f.\,\lambda x.\,f\,x$ | 1 回 |
| $\overline{2}$ | $\lambda f.\,\lambda x.\,f\,(f\,x)$ | 2 回 |

- チャーチ数 (Church numerals)：数を「繰り返しの回数」で表す

<!--
目安 0.75 分。チャーチ数では、数 n を「関数 f と初期値 x を受け取って、f を n 回適用する関数」として表します。上線付きの n はチャーチ数としての n という意味です。0 は 1 回も適用しないので x をそのまま返します。指の本数で数えるのと同じ、一進法の表現です。
-->

---

<!-- _class: twocol -->

## `ZERO` と `ONE`

<div class="cols">
<div>

$$\overline{0} = \lambda f.\,\lambda x.\,x$$

$$\overline{1} = \lambda f.\,\lambda x.\,f\,x$$

</div>
<div>

```python
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
```

</div>
</div>

- `ZERO` は `FALSE` と同じ形（引数名が違うだけ）

<!--
目安 0.75 分。ZERO と ONE をそのまま Python に写します。ZERO を見ると、2 つ受け取って 2 つ目を返す関数なので、3 章の FALSE とα変換で同じ項です。C 言語で 0 が偽になるのと少し似ています。
-->

---

## 窓その2：`to_int`

```python
to_int = lambda n: n(lambda x: x + 1)(0)
```

```python
>>> to_int(ZERO), to_int(ONE)
(0, 1)
```

- f に「1 足す」、x に `0` を渡して、何回適用されたかを数える
- `+` と `0` を使うのは窓の中だけ

<!--
目安 0.5 分。2 つ目の窓です。チャーチ数は f を n 回適用する関数なので、f に Python の「1 を足す関数」、x に 0 を渡せば、結果がちょうど n になります。to_bool と同じく、純粋な世界の外側で Python の数に変換しているだけです。
-->

---

## `SUCC`：もう 1 回 f を適用する

$$\mathrm{SUCC} = \lambda n.\,\lambda f.\,\lambda x.\,f\,(n\,f\,x)$$

```python
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
TWO = SUCC(ONE)
THREE = SUCC(TWO)
```

```python
>>> to_int(THREE)
3
```

- 後者関数 (successor)：n を受け取って n + 1 を返す
- `n(f)(x)` で f を n 回、その外側にもう 1 回 `f(...)`

<!--
目安 0.75 分。後者関数 SUCC は、n を受け取って n+1 を返します。中身を読むと、n(f)(x) で f を n 回適用し、その結果にさらに f を 1 回かぶせています。合計 n+1 回です。これで ONE から TWO、THREE と作れます。
-->

---

## `TEN` まで名前を付けておく

```python
FOUR = SUCC(THREE)
FIVE = SUCC(FOUR)
SIX = SUCC(FIVE)
SEVEN = SUCC(SIX)
EIGHT = SUCC(SEVEN)
NINE = SUCC(EIGHT)
TEN = SUCC(NINE)
```

```python
>>> to_int(TEN)
10
```

<!--
目安 0.25 分。以降の例のために、TEN まで略記用の名前を付けておきます。どれも直前の数の SUCC です。名前は長い式の略記で、自分自身は参照していないのでルールの範囲内です。
-->

---

## `ADD`：`SUCC` を m 回

$$\mathrm{ADD}\;m\;n = m\;\mathrm{SUCC}\;n = \mathrm{SUCC}^m\,n$$

```python
ADD = lambda m: lambda n: m(SUCC)(n)
```

```python
>>> to_int(ADD(TWO)(THREE))
5
```

- 数 m は「何かを m 回適用する」関数。その何かに `SUCC` を渡す

<!--
目安 0.75 分。足し算 m+n は「n に 1 を足すことを m 回繰り返す」ことです。チャーチ数 m はまさに「m 回繰り返す」装置なので、f として SUCC、x として n を渡せば終わりです。数が「ループそのもの」になっているのがチャーチ数の面白いところです。
-->

---

<!-- _class: optional -->

## 掛け算：まずは足し算の繰り返しで

$m \times n$ ＝ 0 に「n を足す」を m 回

```python
MUL_BY_ADD = lambda m: lambda n: m(ADD(n))(ZERO)
```

```python
>>> to_int(MUL_BY_ADD(TWO)(THREE))
6
```

- `ADD(n)` は「n を足す」関数。それを m 回、`ZERO` から
- 小学校の定義どおり。ただし後でもっと短く書ける

<!--
目安 1 分。発展です。説明用の名前 MUL_BY_ADD です。ADD はカリー化されているので、ADD(n) だけで「n を足す関数」になります。これを ZERO から m 回適用すれば m×n です。ADD と同じパターンで、素直な定義です。次のスライドで、もっと短い本物の MUL を見ます。
-->

---

## `MUL`：関数合成 (composition) だけ

$$\mathrm{MUL}\;m\;n\;f = m\,(n\,f) = (f^n)^m = f^{m n}$$

```python
MUL = lambda m: lambda n: lambda f: m(n(f))
```

```python
>>> to_int(MUL(THREE)(FOUR))
12
```

- `n(f)` は「f を n 回」という 1 つの関数
- それを `m` 回繰り返す → f を m × n 回。足し算すら使わない

<!--
目安 1 分。掛け算は足し算の繰り返しでも書けますが（前の発展スライド）、実は驚くほど短く書けます。n(f) は「f を n 回適用する関数」で、これを 1 まとまりの関数とみなして m に渡すと、そのまとまりを m 回繰り返します。合計で f が m×n 回適用されます。ADD も SUCC も出てきません。関数を合成するだけで掛け算になりました。
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

## `POW` の解答：`n` に `m` を渡すだけ

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
目安 1.25 分。答えは n(m) だけです。数 m は「f を受け取って f の m 乗、つまり m 回合成を返す関数」です。n(m) はこれを n 回繰り返すので、f は m 回合成をさらに m 回……と n 段重ねられ、m の n 乗回になります。表は 2 の 3 乗の例で、↠β は β簡約を何回か、最後の行のイコールは「f を何回合成したか」の書き換えです。内側から f が 2 回、4 回、8 回と倍々になります。引数の順番が m と n で逆になるのに注意してください。2 の 10 乗の 1024 もすぐ計算できます。ただし数は一進法なので、大きな数はすぐ遅くなります。
-->

---

## `IS_ZERO`：1 回でも適用されたら偽

```python
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
```

```python
>>> to_bool(IS_ZERO(ZERO)), to_bool(IS_ZERO(THREE))
(True, False)
```

- x に `TRUE`、f に「何が来ても `FALSE`」を渡す
- 0 回なら `TRUE` のまま。1 回でも適用されれば `FALSE`

<!--
目安 0.75 分。数を真偽値に変える最初の関数です。初期値を TRUE にして、f には何を受け取っても FALSE を返す定数関数を渡します。ZERO は f を 1 回も使わないので TRUE のまま、1 以上なら必ず FALSE になります。ここの lambda _ はサンクではなく、引数を無視する定数関数です。IS_ZERO は 6 章の再帰で終了条件として使います。
-->

---

<!-- _class: exercise optional -->

## `IS_EVEN` を書く

`IS_EVEN = lambda n: ＿＿＿` を完成させよ（偶数なら `TRUE`）。

- 目標：`IS_EVEN(FOUR)` は真、`IS_EVEN(SEVEN)` は偽
- `IS_ZERO` と同じく、n に f と x を渡す

<p class="note">ヒント：0 は偶数。1 増えるたびに偶奇は反転する。反転する関数は <a href="#ch3">3 章</a>にあった。</p>

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

- `TRUE`（0 は偶数）から始めて、`NOT` を n 回
- [3 章](#ch3)の真偽値と [4 章](#ch4)の数が、そのまま組み合わさる

<!--
目安 1 分。x に TRUE、f に NOT を渡します。NOT を偶数回かければ TRUE のまま、奇数回なら FALSE です。真偽値も数も関数なので、数に真偽値の関数をそのまま渡せます。
-->


---

<!-- _class: chapter -->

# <span class="num" id="ch5">5</span>ペアと引き算

目安 5 分（発展 +6 分）

[Colab §5 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec5)

<!-- 目安 0.25 分。足し算・掛け算・累乗はできました。次は引き算です。実は引き算はずっと難しく、そのための道具として、まず「ペア」を作ります。後半の発展は引き算と大小比較で、7 章のリストを扱うならここも必要です。 -->

---

<!-- _class: twocol -->

## ペア：2 つを覚えて、選び手に渡す

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

<!-- 目安 1 分。PAIR は a と b を覚えておいて、「選び手」s を待つ関数です。s に a と b を両方渡すので、どちらを使うかは s が決めます。ここで 3 章の TRUE と FALSE を思い出してください。TRUE は 2 つのうち前を、FALSE は後ろを選ぶ関数でした。なので FIRST はペアに TRUE を渡すだけ、SECOND は FALSE を渡すだけです。データ構造も関数だけで作れる、というのがこの章の最初のポイントです。 -->

---

## 引き算はなぜ難しいか

$$n\;f\;x \;=\; \underbrace{f\,(f\,(\cdots\,(f}_{n\ \text{回}}\;x)))$$

- 数 n にできることは 1 つだけ：**f と x を渡して、f を n 回適用させる**
- `SUCC`：外側に f をもう 1 回かぶせる。簡単
- `PRED`（前者関数 (predecessor)：n − 1 を返したい）：f を 1 回分「取り消す」？ 中身を覗く手段も、f の逆関数もない
- 発想を変える：取り消すのではなく、**うまい f と x を選び、n 回適用した結果が n−1 になるようにする**

<!-- 目安 1 分。チャーチ数 n は「f を n 回適用する」という働きそのものでした。足すのは簡単で、f をもう 1 回かぶせればよい。ところが 1 回分を取り消そうとすると困ります。n はブラックボックスで、中を覗いて f を 1 枚はがすことはできません。f に逆関数があるとも限りません。そこで発想を変えます。n にできるのは「何かを n 回やる」ことだけなので、n 回やった結果がちょうど n−1 になるような f と x を自分で用意しよう、という方針です。 -->

---

## Kleene のトリック：1 つ遅れて追いかける

ペア（前, 今）を持ち歩き、1 回ごとに **今を前へずらし、今は +1**

$$(a,\;b) \;\longmapsto\; (b,\;b+1)$$

| f の適用回数 | 0 | 1 | 2 | 3 | … | n |
|---|---|---|---|---|---|---|
| ペア | (0, 0) | (0, 1) | (1, 2) | (2, 3) | … | (n−1, n) |

- n 回適用してから **前**（FIRST）を取れば n−1
- 0 回なら (0, 0) のまま。PRED 0 = 0（自然数なので 0 で止まる）

<!-- 目安 1.25 分。Kleene のアイデアです。ペアの右側は「今いくつか」を数え、左側は「1 つ前の値」を覚えておきます。1 回ごとに、右の値を左へずらし、右は 1 増やす。(0, 0) から始めると、1 回で (0, 1)、2 回で (1, 2)、3 回で (2, 3) となり、n 回後には (n−1, n) です。右側はずっと 1 つ遅れて追いかけてくる左側を連れているので、最後に左側を取り出せば n−1 が手に入ります。何かを取り消したのではなく、最初から 1 つ遅れの値も一緒に作っておいた、というのがポイントです。0 のときは何もしないので (0, 0) のまま、つまり 0 の前は 0 とします。 -->

---

## `SHIFT` と `PRED`

```python
SHIFT = lambda p: PAIR(SECOND(p))(SUCC(SECOND(p)))
PRED = lambda n: FIRST(n(SHIFT)(PAIR(ZERO)(ZERO)))
```

- `SHIFT`：(a, b) から (b, b+1) を作る。表の 1 歩
- `PRED`：(0, 0) に `SHIFT` を n 回、最後に `FIRST`

```python
>>> to_int(PRED(FIVE)), to_int(PRED(ZERO))
(4, 0)
```

<p class="note">Kleene は親知らずの治療の麻酔中に思いついた、と伝わっている（Barendregt 1997 による紹介）。</p>

<!-- 目安 1.5 分。表の 1 歩をそのまま書いたのが SHIFT です。前のペアの SECOND を新しい左側に、それに SUCC したものを新しい右側にします。PRED は (0, 0) に SHIFT を n 回適用して FIRST を取るだけ。n 回適用するのはチャーチ数 n そのものの仕事なので、n(SHIFT) と書けます。小ネタとして、この方法を思いついたのは Church の弟子の Kleene で、親知らずを抜くときの麻酔の最中にひらめいた、という話が伝わっています。Barendregt の 1997 年の論文が、Crossley が編んだ論理学者の回想録の Kleene の話として紹介しています。Kleene 本人の 1981 年の回想では、歯医者の話は出てきますが、笑気ガスには触れていない、という指摘もあるので、あくまで「そう伝わっている話」として聞いてください。 -->

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
- 引きすぎても 0 で止まる（PRED 0 = 0 のおかげ）

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

<p class="note">遅い：PRED は 1 回ごとに SHIFT を n 回。SUB はその PRED を n 回繰り返す。</p>

<!-- 目安 2 分。引き算ができると比較ができます。m が n 以下なら m − n は引きすぎて 0 になるので、IS_ZERO で調べれば LEQ です。等しいかどうかは、両方向の LEQ が真かどうか、つまり AND で書けます。ただし遅いです。PRED は 1 回呼ぶだけで中で SHIFT を n 回、SUB はその PRED を n 回呼ぶので、数が大きくなると目に見えて遅くなります。7 章の RANGE や MOD はこの LEQ と SUB を使います。 -->

---

<!-- _class: chapter -->

# <span class="num" id="ch6">6</span>再帰と Y コンビネータ

目安 16.5 分（発展 +2 分）

[Colab §6 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec6)

<!-- 目安 0.25 分。今日の山場です。ここまでで真偽値、数、引き算まで作りましたが、まだ「繰り返し」がありません。この章では、自分の名前を使えないというルールのまま、再帰を手作りします。いきなり答えを見せるのではなく、一歩ずつ組み立てていきます。 -->

---

## 階乗を書きたい。でも自分の名前は呼べない

```text
# ルール違反の例
FACT = lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(FACT(PRED(n))))  # 自分の名前
      (ID)
)
```

- ふつうの `fact` を、[3 章](#ch3)のサンクの形でそのまま写した
- でも右辺に **FACT 自身** がいる。ルール違反
- 名前は長い式の略記。展開すると FACT の中に FACT の中に……で終わらない

<!-- 目安 1 分。n の階乗は、n が 0 なら 1、そうでなければ n かける (n−1) の階乗。これを今日の部品で素直に書くとこうなります。IF の枝は 3 章で導入したサンクで包んであります。ところが右辺に FACT 自身が出てきます。今日のルールでは、名前は長い式の略記にすぎません。FACT を中身で置き換えると、その中にまた FACT が出てきて、いつまでも置き換えが終わりません。なお Python でこれを実行すると実は動いてしまいますが、それは呼び出した時点でグローバル変数 FACT を探しに行く Python の名前の仕組みに頼っているからです。ラムダ計算にはその仕組みがありません。 -->

---

<!-- _class: twocol -->

## 手がかり：自分を自分に渡す

<div class="cols">
<div>

$$\omega = \lambda x.\,x\,x$$

<div class="steps">

| | |
|---|---|
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

簡約しても元に戻る＝終わらない。でも **関数は自分自身を受け取れる**

<!-- 目安 0.75 分。手がかりは自己適用です。ω は「受け取った x を x 自身に適用する」関数です。ω を ω に渡すと、β簡約の結果がまた ω ω に戻ってしまい、永遠に終わりません。これを Ω と呼びます。Python でも omega(omega) は RecursionError になります。失敗に見えますが、大事なのは「関数は自分自身を引数として受け取り、呼び出せる」ということです。終わらない繰り返しが作れたなら、あとは止め方を工夫すれば再帰になるはずです。 -->

---

## アイデア：自分を引数でもらう

| | 名前で呼ぶ（禁止） | 引数でもらう |
|---|---|---|
| 定義 | `FACT = lambda n: …` | `FACT_GEN = lambda self: lambda n: …` |
| 再帰呼び出し | `FACT(PRED(n))` | `self(self)(PRED(n))` |
| 使うとき | `FACT(FIVE)` | `FACT_GEN(FACT_GEN)(FIVE)` |

- 呼びたい相手（自分）を **引数 self** で受け取る
- 使う側が自分自身を渡す。ω と同じ「自分を自分に渡す」
- 中で再帰するときも `self(self)`：self は FACT_GEN（まだ self を待っている関数）なので、まず自分を渡し直す

<p class="note">クラスを消したのに self が再登場。中身はただの引数名。</p>

<!-- 目安 1 分。名前で自分を呼べないなら、引数でもらえばいい、という発想です。関数の外側に引数 self を 1 つ足して、使う人に自分自身を渡してもらいます。これは ω の自己適用と同じです。ここで注意が 1 つ。self が受け取るのは FACT_GEN、つまり「self を待っている関数」です。なので再帰呼び出しするときも、まず self に self を渡し直してから n−1 を渡します。それが self(self) です。クラスを消したはずの講習に self が戻ってきましたが、これはただの引数名です。 -->

---

## `FACT_GEN`：`self(self)` で再帰する

```python
FACT_GEN = lambda self: lambda n: (
    IF(IS_ZERO(n))
      (lambda _: ONE)
      (lambda _: MUL(n)(self(self)(PRED(n))))
      (ID)
)
```

- さっきの FACT との違いは 2 か所：先頭の `lambda self:` と `self(self)`
- 右辺に FACT_GEN 自身は出てこない。ルールどおり

<!-- 目安 0.5 分。表のとおりに書いたものです。違反版の FACT と見比べてください。先頭に lambda self が増え、FACT(PRED(n)) が self(self)(PRED(n)) に変わっただけです。右辺に FACT_GEN という名前は出てこないので、ルールを守っています。 -->

---

## 動いた：`FACT_GEN(FACT_GEN)`

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

<!-- 目安 1 分。実際に動きます。3 の階乗が 6、5 の階乗が 120 です。なぜ動くのかを追ってみます。FACT_GEN(FACT_GEN) を G と呼ぶことにします。G の中では self が FACT_GEN です。すると再帰呼び出しの self(self) は FACT_GEN(FACT_GEN)、つまり G 自身です。図では PRED(THREE) を TWO と書いています。名前を使わずに「自分自身」を手に入れられました。自分の名前の代わりに、自分のコピーを持ち歩いているイメージです。もう 1 つ見ておいてほしいのは、self(self) が else 側のサンク lambda _: の中にあることです。だから n が 0 のときは呼ばれず、そこで止まります。 -->

---

## `self(self)` を外へ追い出す

本体に `self(self)` という仕掛けが混ざっている。ふつうの形 `fact(n−1)` で書きたい（self を s と略記）

<div class="steps">

| | |
|---|---|
| | $\mathrm{FACT\_GEN} = \lambda s.\,\lambda n.\,\cdots\,(s\,s)\,(\mathrm{PRED}\,n)\,\cdots$ |
| $=_\beta$ | $\lambda s.\,\bigl(\lambda f.\,\lambda n.\,\cdots\,f\,(\mathrm{PRED}\,n)\,\cdots\bigr)\,(s\,s)$ |
| $=$ | $\lambda s.\,F\,(s\,s)$ |

</div>

$$F = \lambda f.\,\lambda n.\,\cdots\,f\,(\mathrm{PRED}\,n)\,\cdots \qquad \text{ふつうの再帰の形}$$

$=_\beta$（β同値）：β簡約を逆向きも含めて何回か使うと移り合える。2 行目を β簡約すると 1 行目

<!-- 目安 2 分。FACT_GEN は動きますが、本体を書く人が self(self) という仕掛けを知っていなければなりません。そこで仕掛けを本体の外へ追い出します。…の部分は IF や MUL など、変わらない部分です。1 行目の (s s) を、外から引数 f として渡してもらう形に書き換えたのが 2 行目です。2 行目を β簡約すると f に (s s) が入って 1 行目に戻るので、同じものです。β簡約を逆向きに使ったわけです。このように、β簡約を前向きにも逆向きにも使って移り合えることを β同値と呼び、イコールに β を添えて書きます。こうして括弧の中に、self(self) を含まない、ふつうの再帰の形 F が取り出せました。FACT_GEN は「F に s s を渡すもの」になりました。ただし 1 つ覚えておいてください。ラムダ計算としては同じですが、Python では計算のタイミングが変わります。元の FACT_GEN では self(self) が lambda _: のサンクの中にありましたが、2 行目では s s が F の引数として外に出ています。これが後で効いてきます。 -->

---

## `FACT_BODY`：ふつうの再帰の形

F を Python に。再帰呼び出しの相手 `fact` を引数でもらう

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

本物の階乗を fact に渡せば階乗になる。**その fact をどこから持ってくるか？**

<!-- 目安 0.5 分。F を Python で書いたのが FACT_BODY です。最初の違反版 FACT とほぼ同じで、FACT と書いていたところが引数 fact になっただけです。試しに、さっき動いた FACT_GEN(FACT_GEN) を fact として渡すと、ちゃんと 120 になります。つまり、本物の階乗さえもらえれば FACT_BODY は階乗になります。残る問題は、その本物をどう作るかです。 -->

---

## 組み立て直すと Y コンビネータ

<div class="steps">

| | |
|---|---|
| | $\mathrm{FACT} = \mathrm{FACT\_GEN}\;\mathrm{FACT\_GEN}$ |
| $=_\beta$ | $(\lambda s.\,F\,(s\,s))\;(\lambda s.\,F\,(s\,s))$ |

</div>

F を引数 f にすると（ついでに s を x に α変換）

$$Y = \lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x)) \qquad \mathrm{FACT} = Y\,F$$

**ふつうの再帰の形 F を渡すと、再帰する関数が返ってくる**

<p class="note">コンビネータ (combinator)：自由変数のない λ 項。Y も、この後の Z も、<a href="#ch8">8 章</a>の S・K・I もこれ。</p>

<!-- 目安 1 分。さっきの結果を使って組み立て直します。FACT は FACT_GEN を FACT_GEN に渡したもので、FACT_GEN は λs. F (s s) と β同値でした。これを 2 つ並べるだけです。ここで F は階乗に限らず何でもよいので、F を引数 f にくくり出します。変数名 s は x に付け替えました。これが Y コンビネータです。コンビネータとは、2 章の自由変数を 1 つも含まない λ 項のことです。ふつうの再帰の形をした関数を渡すと、再帰する関数を作ってくれます。天下りに覚える式ではなく、自分を引数でもらう工夫から出てきた式だ、というのがこの章の一番伝えたいことです。 -->

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

<!-- _class: twocol -->

## Python で Y を使うと……

<div class="cols">
<div>

$$
\begin{aligned}
Y = \lambda f.\,&(\lambda x.\,f\,(x\,x))\\
&(\lambda x.\,f\,(x\,x))
\end{aligned}
$$

</div>
<div>

```python
Y = lambda f: (
    (lambda x: f(x(x)))
    (lambda x: f(x(x))))
```

```python
>>> Y(FACT_BODY)
Traceback (most recent call last):
  ...
RecursionError: ...
```

</div>
</div>

数を渡す前、`Y(FACT_BODY)` を **作るだけで** 落ちる

<!-- 目安 0.5 分。理屈は完成したので Python で書いてみます。Y の定義はそのまま写せます。ところが Y(FACT_BODY) は RecursionError になります。数を渡して計算させる前、関数を作る段階で落ちています。理屈は正しいはずなのに、なぜでしょうか。 -->

---

## なぜ？ Python は引数を先に計算する

- 正規順序 (normal order)：いちばん外側・左の簡約基から
- 適用順序 (applicative order)：いちばん内側・左（引数）から
- Python は値呼び (call by value)：引数を値まで計算してから呼ぶ（正格評価）。ただし lambda の中身は呼ばれるまで計算しない

```text
W = lambda x: F(x(x))      Y(F) は W(W)
W(W) -> F(W(W))            F を呼ぶ前に引数 W(W) を計算
     -> F(F(W(W))) -> ...  F は一度も呼ばれず、スタックが尽きる
```

正規順序なら `Y F ZERO` は fact を使わずに `ONE` まで簡約できる
FACT_GEN では `self(self)` がサンクの中にあった。**追い出して包みが外れた**

<!-- 目安 1.5 分。3 章の落とし穴と同じ原因です。評価の順番に名前を付けておきます（2 章の発展を見た人には復習です）。簡約できる場所が複数あるとき、いちばん外側・左から簡約するのが正規順序、いちばん内側、つまり引数から先に簡約するのが適用順序です。Python は値呼びで、引数を値まで計算してから関数を呼びます。3 章で正格評価と呼んだものです。適用順序に近いのですが、lambda の中身は呼ばれるまで計算しない点が違います。Y(F) は W を W に渡したものです。W(W) を計算すると F(W(W)) になりますが、Python は F を呼ぶ前に引数の W(W) を計算しようとします。それがまた F(W(W)) になり……と、F が一度も呼ばれないまま展開が続きます。正規順序なら、Y F に ZERO を渡した項は外側の F、つまり FACT_BODY から簡約されるので、fact を使わずに ONE まで行けます。では、なぜ FACT_GEN は動いたのか。FACT_GEN では self(self) が lambda _: のサンクの中にあったので、呼ばれるまで計算されませんでした。外へ追い出したときに、その包みも一緒に外れてしまったのです。 -->

---

## 包んで遅らせる：η展開

$$\lambda v.\,M\,v \quad\text{と}\quad M \quad\text{は、呼べば同じ結果}$$

- これを η展開 (eta expansion) という（v は M に出てこないとする）
- ただし違いが 1 つ：Python は lambda の **中身を呼ばれるまで計算しない**
- [3 章](#ch3)のサンク `lambda _: A` と同じ発想：必要になるまで計算しない

```python
>>> lambda v: omega(omega)(v)    # 包むだけなら落ちない
<function <lambda> at ...>
```

<!-- 目安 1 分。解決策は 3 章のサンクと同じ発想です。M を lambda v: M(v) で包んでも、v を渡して呼べば結果は同じです。これを η展開と呼びます。2 章の発展で η変換を見た人は、その逆向きです。ただし違いが 1 つあって、Python では lambda の中身は呼ばれるまで計算されません。実際 omega(omega) は落ちましたが、それを lambda で包んだだけなら落ちません。同じ値を表しつつ、計算のタイミングだけを遅らせられるわけです。サンクとの違いは、サンクは ID を渡して開けるのに対し、η展開した関数は本物の引数 v をそのまま M に渡す点です。だから再帰の相手として、そのまま n を渡して呼べます。 -->

---

<!-- _class: twocol -->

## Z コンビネータ：Y の x x を包む

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

Y との違いは x x → λv. x x v の 2 か所だけ。

**追い出したときに外れた包みを、付け直した**

<!-- 目安 1 分。Y の中で問題だった x(x) を、lambda v: x(x)(v) で包んだものが Z コンビネータです。Y との違いはこの 2 か所だけです。FACT_GEN では self(self) がサンクの中にあって守られていましたが、外へ追い出したときにその包みが外れました。Z はその包みを付け直しただけです。今度は f に渡るのは計算済みの値ではなく「呼ばれたら x(x) を計算する関数」なので、f を呼ぶ前に無限に展開することはありません。ラムダ計算の中では、Z F も η変換を許せば F の不動点です。正格評価の言語で使える Y、と覚えてください。 -->

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

- fact が実際に呼ばれるのは n ≠ 0 のときだけ。そのとき初めて 1 段展開
- IF の枝がサンクだから止まる。包まないと n = 0 でも else 側を計算する
- **自分の名前を使わずに再帰できた**

<!-- 目安 0.5 分。いよいよです。Z に FACT_BODY を渡すと、今度は落ちずに 1、6、120 と階乗が返ってきます。包んだ自分が fact として渡され、n が 0 でないときに初めて 1 段だけ展開されます。IF の枝もサンクで包んであるので、n が 0 なら else 側は計算されません。包まないと 3 章の落とし穴に戻ります。自分の名前を使わずに再帰できました。 -->

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

- FACT_BODY の `ONE` を `ZERO` に、`MUL` を `ADD` に変えただけ

<!-- 目安 0.5 分。解答です。FACT_BODY の ONE を ZERO に、MUL を ADD に変えるだけでした。Z に渡すのは、ふつうの再帰の形そのものです。一度 Z を作ってしまえば、再帰はいくらでも書けます。 -->

---

<!-- _class: optional -->

## `FIB`：再帰呼び出しが 2 つ

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

- n ≤ 1（PRED n が 0）なら n そのもの。それ以外は前 2 つの和

<!-- 目安 2 分。発展です。フィボナッチ数も同じ形で書けます。PRED(n) が 0、つまり n が 0 か 1 なら n そのものを返し、それ以外は fib(n−1) と fib(n−2) を足します。再帰呼び出しが 2 つあっても、Z に渡す形は変わりません。10 番目のフィボナッチ数は 55 です。FIB は 16 まで動き、17 で RecursionError になります（9 章の表）。講習中にその場で試すなら、FACT は 5、FIB は 10 程度が安心です。 -->


---

<!-- _class: chapter optional -->

# <span class="num" id="ch7">7</span>リスト

発展 12 分（FizzBuzz +5.5 分）

[Colab §7 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec7)

<!--
目安 0.25 分。ここから発展の章です。5 章のペアを入れ子にしてリストを作り、最後は数も文字列もない世界で FizzBuzz を動かします。5 章発展の LEQ と SUB を使うので、5 章発展を飛ばした場合はこの章も飛ばします。
-->

---

<!-- _class: optional -->

## リストの表現：ペアの入れ子

```text
CONS(h)(t)   ┌───────┬───┐    ┌───┬───┐
             │ FALSE │ ●─┼───>│ h │ t │
             └───────┴───┘    └───┴───┘
              空でない         先頭 残り

NIL          ┌──────┬──────┐
             │ TRUE │ TRUE │
             └──────┴──────┘
              空

[a, b]  =  (FALSE, (a, (FALSE, (b, (TRUE, TRUE)))))
```

- 1 つ目は **「空か？」の旗**。中身は 2 つ目のペアに入れる

<!--
目安 1.5 分。リストは「先頭」と「残り」のペアとして作るのが定番です。ただ、空のリストと空でないリストを見分ける必要があるので、外側にもう 1 段ペアをかぶせて、1 つ目に「空か？」の旗を立てます。空でないリストは旗が FALSE で、2 つ目に先頭と残りのペアが入ります。空のリスト NIL は旗が TRUE で、2 つ目は使わないので何でもよく、ここでは TRUE を詰めておきます。下の行は [a, b] を展開したものです。旗と中身が交互に出てきて、最後が NIL です。
-->

---

<!-- _class: optional -->

## `NIL`、`CONS`、`IS_NIL`、`HEAD`、`TAIL`

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

<!--
目安 1.5 分。前の図をそのまま 5 章の PAIR、FIRST、SECOND で書いただけです。CONS は名前を Lisp から借りています（construct の略）。IS_NIL は旗を取り出すだけなので FIRST そのものです。HEAD と TAIL は、まず SECOND で中身のペアを取り出し、そこから FIRST か SECOND を取ります。旗が真偽値そのものなので、IS_NIL の結果はそのまま IF に渡せます。
-->

---

<!-- _class: optional -->

## 窓その3：`to_list`

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

- `def` と `while` を使うが、**観測用の窓** なので可
- `conv` で各要素も窓に通す（`to_int` など）

<!--
目安 1.25 分。3 つ目の窓です。旗が TRUE になるまで先頭を取り出しては残りに進み、Python のリストに詰めます。def も while も講習のルールでは使わないものですが、これは純粋な世界の外側から中をのぞくための窓なので例外です。要素はチャーチ数などのままなので、2 つ目の引数 conv で要素ごとの窓を指定します。
-->

---

<!-- _class: optional -->

## `RANGE`：m から n までのリスト

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

- [6 章](#ch6)の Z と、いつもの `IF(c)(lambda _: A)(lambda _: B)(ID)`
- m ≤ n なら「m を先頭に、残りは m+1 から」

<!--
目安 1.5 分。最初の再帰的なリスト関数です。形は 6 章の FACT や SUM_TO_N と同じで、Z に「自分自身」を引数として渡してもらいます。range_ の下線は Python 組み込みの range と名前がぶつからないようにするためだけのものです。5 章発展の LEQ を使って、m が n 以下なら m を先頭にして残りを m+1 から作り、そうでなければ NIL を返します。
-->

---

<!-- _class: optional -->

## 畳み込み (fold) のアイデア

リストの `CONS` を `f` に、`NIL` を `z` に **置き換える**

```text
CONS(a)(CONS(b)(CONS(c)(NIL)))
 ▼       ▼       ▼       ▼
 f  (a)( f  (b)( f  (c)( z  )))
```

- 右から順にまとめる **右畳み込み** (right fold)
- `f` を `CONS`、`z` を `NIL` にしたら……？

<!--
目安 1 分。リストを 1 つの値にまとめる一番基本的な道具が畳み込みです。リストは CONS と NIL でできているので、CONS を 2 引数関数 f に、NIL を初期値 z にそっくり置き換えると考えます。いちばん内側、つまりリストの右端から計算が進むので右畳み込みと呼びます。では f を CONS、z を NIL にしたら何が起きるか。次のスライドで確かめます。
-->

---

<!-- _class: optional -->

## `FOLD`

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

- 空なら `z`、そうでなければ `f(先頭)(残りを畳んだもの)`

<!--
目安 1 分。空なら z、そうでなければ先頭と「残りを畳み込んだ結果」に f を適用します。前の図をそのまま再帰にしただけです。例の 1 つ目は CONS を CONS に、NIL を NIL に置き換えるので、元と同じリストが返ります。これは後で FizzBuzz の文字列連結に使います。2 つ目は要素を無視して 1 ずつ足すので、長さを数えています。
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

- `CONS` を「`f` を通してから `CONS`」に置き換えるだけ
- `MAP` 自身は再帰しない。再帰は `FOLD` の中に 1 回だけ

<!--
目安 1 分。各要素に f を適用したリストを作る MAP です。先ほどの FOLD(CONS)(NIL) はリストを写すだけでしたが、CONS の前に f を挟めば MAP になります。acc は「残りを処理し終えたリスト」です。ここで MAP 自身は Z を使っていない点に注目してください。再帰は FOLD に閉じ込めたので、以降は FOLD を部品として使えます。
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

- 使ってよい：`FOLD`、`ADD`、`ZERO`
- 余裕があれば：何行で書ける？

<p class="note">ヒント：CONS を何に、NIL を何に置き換える？</p>

<!--
目安 2 分。演習です。FOLD の図を思い出して、CONS と NIL をそれぞれ何に置き換えればよいか考えてもらいます。6 章の SUM_TO_N では Z を使って数行書きましたが、今回はもっと短くなります。2 分ほど待ちます。
-->

---

<!-- _class: answer optional -->

## `SUM` の解答：1 行

```python
SUM = FOLD(ADD)(ZERO)
```

```python
>>> to_int(SUM(RANGE(ONE)(FOUR)))
10
```

- `CONS` → `ADD`、`NIL` → `ZERO` に置き換えると
  `ADD(ONE)(ADD(TWO)(ADD(THREE)(ADD(FOUR)(ZERO))))`
- `l` すら書かない。`FOLD(ADD)(ZERO)` は「リストを待つ関数」

<!--
目安 1 分。答えは 1 行です。CONS を ADD に、NIL を ZERO に置き換えれば足し算になります。しかも引数の l を書く必要すらありません。カリー化のおかげで、FOLD に f と z だけ渡したものが、すでに「リストを受け取って合計を返す関数」になっています。6 章で Z と IF を手で組んだ SUM_TO_N が、RANGE と組み合わせて SUM(RANGE(ONE)(n)) と書けるわけです。部品がそろうと、関数だけの世界でも普通のプログラミングらしくなってきます。
-->

---

<!-- _class: optional -->

## FizzBuzz を関数だけで

```text
1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz,
11, Fizz, 13, 14, FizzBuzz
```

- 必要な部品：割り算の余り、数を数字の並びに、**文字**、連結
- 数も文字列も `if` もない世界で、ここまで作った部品だけで書く
- 定義は多いので、**形を眺める** ペースで進む

<p class="note">Tom Stuart「Programming with Nothing」（Ruby の lambda（proc）だけで FizzBuzz）へのオマージュ</p>

<!--
目安 0.75 分。ここから FizzBuzz です。3 の倍数で Fizz、5 の倍数で Buzz、両方なら FizzBuzz、それ以外は数を出す、という定番の課題です。Tom Stuart さんが Ruby の lambda（proc）だけで同じことをした「Programming with Nothing」という有名な記事と講演があり、今回はその Python 版のオマージュです。定義の数が多いので、1 行ずつ読むより「どこかで見た形だな」と眺めていきます。
-->

---

<!-- _class: optional -->

## `MOD`：引けるだけ引く

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

- 10 → 7 → 4 → 1：3 が引けなくなった残りが余り

<p class="note">前提：除数 n は 1 以上。n = ZERO は未定義で、この実装では止まらない。</p>

<!--
目安 0.5 分。割り算の余りです。n が m 以下である限り、m から n を引いて繰り返します。引けなくなったときの m が余りです。形はもう見慣れた Z と IF の組み合わせです。除数が 0 だと、いくら引いても減らないので止まりません。除数は 1 以上が前提です。
-->

---

<!-- _class: optional -->

## `DIV`：引けた回数を数える

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

- 10 → 7 → 4 → 1：引けた回数 3 が商。違いは 2 つの枝だけ

<p class="note">前提：除数 n は 1 以上。n = ZERO は未定義で、この実装では止まらない。</p>

<!--
目安 0.5 分。割り算の商は、MOD とほぼ同じ形で、引けるたびに SUCC で 1 を数えます。違いは 2 つの枝の中身だけです。前提も MOD と同じで、除数は 1 以上です。
-->

---

<!-- _class: optional -->

## `PUSH` と `TO_DIGITS`：数を数字の並びに

```python
PUSH = lambda l: lambda x: FOLD(CONS)(CONS(x)(NIL))(l)

TO_DIGITS = Z(lambda digits: lambda n: (
    IF(LEQ(n)(NINE))
      (lambda _: CONS(n)(NIL))
      (lambda _: PUSH(digits(DIV(n)(TEN)))
                       (MOD(n)(TEN)))
      (ID)
))
```

```python
>>> to_list(TO_DIGITS(POW(TEN)(TWO)), to_int)
[1, 0, 0]
```

- `PUSH`：`FOLD(CONS)` で写し、`NIL` を `[x]` に替える → 末尾に追加

<!--
目安 0.75 分。PUSH はリストの末尾に 1 つ足します。FOLD(CONS) で写しながら、NIL を「x だけのリスト」に置き換えるだけです。TO_DIGITS は 10 進の各桁のリストを作ります。9 以下なら 1 桁、そうでなければ 10 で割った商の桁を作ってから、末尾に余りを足します。100 は POW(TEN)(TWO) で作っています。
-->

---

<!-- _class: optional -->

## 文字の表現：0〜14 の数で

| 数 | 0〜9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|
| 文字 | 0〜9 | B | F | i | u | z |

```python
ELEVEN = SUCC(TEN)
TWELVE = SUCC(ELEVEN)
THIRTEEN = SUCC(TWELVE)
FOURTEEN = SUCC(THIRTEEN)
```

- Fizz と Buzz に要る文字は B、F、i、u、z の **5 つだけ**
- 文字列 ＝ 文字（数）のリスト

<!--
目安 0.5 分。文字列は文字のリストにします。では文字は何で表すか。数字の 0 から 9 はそのまま数で、Fizz と Buzz に必要な文字は B、F、i、u、z の 5 つしかないので、10 から 14 を割り当てます。このずらし方も Tom Stuart さんの記事と同じです。そのために TEN の続きを 14 まで作っておきます。
-->

---

<!-- _class: optional -->

## 窓その4：`to_str`

```python
to_str = lambda l: "".join(
    to_list(l, lambda c: "0123456789BFiuz"[to_int(c)])
)
```

```python
>>> to_str(TO_DIGITS(FOURTEEN))
'14'
```

- 各要素を `to_int` で数にし、表で 1 文字に読み替えるだけ
- 文字列リテラルが出てくるのは、この **窓の中だけ**

<!--
目安 0.5 分。最後の窓です。to_list で取り出した各要素を to_int で数にして、"0123456789BFiuz" の何文字目かを引きます。文字列のリテラルが登場するのはこの窓の中だけで、純粋な世界の中ではあくまで数のリストです。
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

- 連結：`FIZZ` の `NIL` を `BUZZ` に置き換える（`PUSH` と同じ発想）

<!--
目安 0.5 分。Fizz は F、i、z、z なので 11、12、14、14 のリストです。Buzz も同様です。FizzBuzz はこの 2 つの連結で、FOLD(CONS) で FIZZ を写しながら、末尾の NIL を BUZZ に置き換えると連結になります。PUSH と同じ発想です。
-->

---

<!-- _class: optional -->

## `FIZZBUZZ_ITEM`：1 つの数を文字列に

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

## `FIZZBUZZ`：動かす

```python
FIZZBUZZ = lambda n: MAP(FIZZBUZZ_ITEM)(RANGE(ONE)(n))
FIFTEEN = MUL(THREE)(FIVE)
```

```python
>>> to_list(FIZZBUZZ(FIFTEEN), to_str)
['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8',
 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']
```

- 1〜15 で約 3 ms。再帰上限 1000 のままで **240 程度まで** 動く

<p class="note">実測（入力は SUCC の鎖）：通常実行で 247、検証スクリプト経由で 246 まで完走。</p>

<!--
目安 1 分。1 から n までの RANGE に FIZZBUZZ_ITEM を MAP するだけです。15 は MUL(THREE)(FIVE) で作りました。窓を通すと、ちゃんと FizzBuzz が出てきます。数も文字列も if も使わず、1 引数の lambda と適用だけで書けました。手元の計測では 1 から 15 で約 3 ミリ秒、Python の再帰上限を変えずに 240 程度まで動きます。入力を SUCC の鎖で作った実測では、ふつうに実行して 247、検証用のスクリプト経由では 246 まで完走し、その次で RecursionError でした。実行のしかたや数の作り方で、境界は少し変わります。
-->

---

<!-- _class: chapter optional -->

# <span class="num" id="ch8">8</span>SKI コンビネータ

発展 10 分

[Colab §8 で試す](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec8)

<!--
目安 0.25 分。最後の発展章です。ここまでは 1 引数の lambda と適用だけで計算してきましたが、この章ではその lambda すら消してしまいます。
-->

---

<!-- _class: twocol optional -->

## lambda すら消す：`S`、`K`、`I`

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
# I は次で S と K から作る
```

</div>
</div>

- $S$：$z$ を $x$ と $y$ の両方に配る　$K$：2 つ目を捨てる　$I$：そのまま
- この 3 つ（実は 2 つ）を **適用するだけ** で計算する

<!--
目安 1 分。コンビネータ論理 (combinatory logic) の 3 つの基本部品です。K は 2 引数のうち 1 つ目を返し、2 つ目を捨てます。I は恒等関数です。S が一番わかりにくいのですが、3 つ目の引数 z を x と y の両方に配って、x(z) に y(z) を適用します。Schönfinkel が 1924 年に導入し、Curry が発展させました。カリー化の名前の由来の Curry です。Python では S と K だけ lambda で定義し、I は次のスライドで S と K から作ります。
-->

---

<!-- _class: optional -->

## `I = S K K` を確かめる

<div class="cols">
<div>

<div class="steps">

| | |
|---|---|
| | $S\,K\,K\,x$ |
| $\twoheadrightarrow_\beta$ | $K\,x\,(K\,x)$ |
| $\twoheadrightarrow_\beta$ | $x$ |

</div>

</div>
<div>

```python
I = S(K)(K)
```

```python
>>> to_int(I(THREE))
3
>>> to_bool(I(TRUE))
True
```

</div>
</div>

- $S$ が $x$ を 2 つの $K$ に配り、外側の $K$ が 2 つ目を **捨てる**
- 捨てられる 2 つ目の $K$ は何でもよい：$S\,K\,S$ も $I$

<!--
目安 1.5 分。S K K を x に適用すると、S の定義により x が 2 つの K に配られて K x (K x) になります。矢印は 3 章で見た ↠β で、各行は数ステップの β簡約をまとめて書いています。次に外側の K x が 2 つ目の引数 K x を捨てて、x が残ります。つまり S K K は恒等関数 I と同じふるまいです。だから I は部品として要らず、S と K の 2 つで足ります。Python でも数や真偽値をそのまま返すことが確かめられます。
-->

---

<!-- _class: exercise optional -->

## `K` と `K I` は何に見える？

2 つの引数 $a$、$b$ を与えて簡約してみる

$$K\,a\,b \;\to\; ?$$

$$K\,I\,a\,b \;\to\; ?$$

- どちらも、[3 章](#ch3)で見たものと同じふるまい

<p class="note">ヒント：2 つから 1 つを選んでいる</p>

<!--
目安 2 分。演習です。K に a と b を、K I に a と b を順に適用すると何が残るかを考えてください。答えはこれまでの章に出てきた、ある 2 つの関数です。2 分ほど待ちます。
-->

---

<!-- _class: answer optional -->

## 解答：`TRUE` と `FALSE`

<div class="cols">
<div>

<div class="steps">

| | |
|---|---|
| | $K\,a\,b$ |
| $\twoheadrightarrow_\beta$ | $a$ |

</div>

<div class="steps">

| | |
|---|---|
| | $K\,I\,a\,b$ |
| $\twoheadrightarrow_\beta$ | $I\,b$ |
| $\twoheadrightarrow_\beta$ | $b$ |

</div>

</div>
<div>

```python
>>> to_bool(K), to_bool(K(I))
(True, False)
```

</div>
</div>

- `K` は 1 つ目を選ぶ：**TRUE**。式も同じ形
- `K I` は 2 つ目を選ぶ：**FALSE**

<!--
目安 1 分。K a b は a なので、2 つから 1 つ目を選ぶ TRUE です。定義 λx.λy.x は TRUE の λt.λf.t と変数名が違うだけです。K I a b は、まず K が a を捨てて I が残り、I b で b になります。2 つ目を選ぶので FALSE と同じです。to_bool の窓に通しても、確かに True と False が見えます。
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
- λ が入れ子なら内側から。λ のない部分はそのまま

<!--
目安 1.5 分。λ項から λ を消して、S、K、I の式に書き換える変換がブラケット抽象です。自由変数はそのまま残るので、S、K、I だけになるのは自由変数のない閉じた項です。ここでは雰囲気だけ紹介します。λx の本体が x そのものなら I。本体に x が自由に出てこなければ、引数は捨ててよいので K。本体が適用 E1 E2 なら、引数 x を両側に配る S を使い、それぞれの側で同じ変換を続けます。引数を「そのまま返す」「捨てる」「配る」の 3 通りしかない、というのがポイントです。λ が入れ子のときは内側の λ から順に消していきます。
-->

---

<!-- _class: optional -->

## 例：$\lambda x.\,x\,x$ → $S\,I\,I$

<div class="steps">

| | |
|---|---|
| | $\mathcal{T}[\lambda x.\,x\,x]$ |
| $=$ | $S\,\mathcal{T}[\lambda x.\,x]\,\mathcal{T}[\lambda x.\,x]$ |
| $=$ | $S\,I\,I$ |

</div>

$S\,I\,I\,a \twoheadrightarrow_\beta I\,a\,(I\,a) \twoheadrightarrow_\beta a\,a$：**ω と同じふるまい**

```python
>>> to_int(S(I)(I)(ID)(THREE))
3
>>> S(I)(I)(S(I)(I))
Traceback (most recent call last):
  ...
RecursionError: maximum recursion depth exceeded
```

<!--
目安 1.25 分。6 章の ω、つまり λx.x x を変換してみます。本体は x と x の適用なので S で配り、両側は λx.x なので I。結果は S I I です。S I I a は I a (I a)、つまり a a になるので ω と同じふるまいです。ID を渡すと ID(ID) で ID が返り、3 にそのまま効きます。そして S I I を自分自身に適用すると、6 章の omega(omega) と同じく止まらず、RecursionError になります。
-->

---

<!-- _class: optional -->

## 例：$\lambda x.\,\mathrm{SUCC}\,x$ → $S\,(K\,\mathrm{SUCC})\,I$

<div class="steps">

| | |
|---|---|
| | $\mathcal{T}[\lambda x.\,\mathrm{SUCC}\,x]$ |
| $=$ | $S\,\mathcal{T}[\lambda x.\,\mathrm{SUCC}]\,\mathcal{T}[\lambda x.\,x]$ |
| $=$ | $S\,(K\,\mathrm{SUCC})\,I$ |

</div>

```python
>>> to_int(S(K(SUCC))(I)(TWO))
3
```

- 3 つの規則がすべて登場。η変換を使えばただの $\mathrm{SUCC}$

<!--
目安 0.5 分。3 つの規則がすべて出てくる例です。本体は SUCC と x の適用なので S で配ります。左の SUCC には x が出てこないので K、右は x そのものなので I です。S (K SUCC) I に 2 を渡すと、ちゃんと 3 になります。η変換を使えばただの SUCC ですが、規則どおり機械的に変換するとこうなります。
-->

---

<!-- _class: optional -->

## SKI だけでチューリング完全

- どんな λ 項も、ブラケット抽象で $S$・$K$・$I$ と**元の自由変数**だけの式になる
- **閉じた項**（自由変数のない項）なら、残るのは **適用だけ**。変数も λ もいらない
- $I = S\,K\,K$ なので、本当は **$S$ と $K$ の 2 つ** で足りる
- ラムダ計算と同じ計算能力：**チューリング完全** (Turing complete)

<p class="note"><a href="#ch6">6 章</a>の Z も、FizzBuzz も、原理的には S と K の適用だけで書ける（とても長くなる）。</p>

<!--
目安 1 分。まとめです。ブラケット抽象を使えば、どんな λ 項からも λ を消せます。自由変数はそのまま残りますが、自由変数のない閉じた項なら、S、K、I の適用だけの式になります。しかも I は S K K なので、S と K の 2 つだけで足ります。ラムダ計算と同じ計算能力を持つので、チューリング機械とも同じ、つまりチューリング完全です。この章で見た Z や FizzBuzz も、原理的には S と K を並べた式で書けます。1 章で「計算に本当に必要なものは？」と問いましたが、極端に言えば答えは「2 つの部品と適用」です。
-->


---

<!-- _class: chapter -->

# <span class="num" id="ch9">9</span>まとめと先へ

目安 3 分（発展 +1 分）

[Colab §9 で試す（性能の実験も）](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb#scrollTo=sec9)

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
目安 0.5 分。今日は lambda だけで、真偽値、自然数と四則の一部、ペアと引き算、そして再帰を作りました。冒頭で予告した FACT に FIVE を渡すと、ちゃんと 120 が出ます。数値リテラルも if も def も使っていません。使ったのは、関数を作ることと関数を呼ぶことだけです。発展まで進んだ場合は、リストや FizzBuzz、SKI コンビネータも作りました。
-->

---

<!-- _class: optional -->

## 型を付けると Y は書けない

単純型付きラムダ計算 (simply typed lambda calculus)：どの項にも型 $A \to B$ などが付く。

自己適用 $x\;x$ に型を付けようとすると

$$x : A \to B \quad\text{かつ}\quad x : A \qquad\Rightarrow\qquad A = A \to B$$

- これを満たす型 $A$ はない → $\omega$、$Y$、$Z$ は型が付かない
- **強正規化** (strong normalization)：型の付く項はすべて停止する
- だから一般の再帰は書けない。実用言語は再帰を別に用意する

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

## 性能の話：遅い・すぐ溢れる

- チャーチ数は**一進法** (unary)：$n$ は「$f$ を $n$ 回」
- `SUCC`・`ADD` の鎖は、`to_int` で見るときスタックが深くなる
- `MUL`・`POW` の合成では、値の大きさと深さは比例しない
- 実測（CPython 3.14、再帰上限 1000 の既定値）：

| 計算 | 最後まで動いた最大の $n$ | 次の値 |
|---|---:|---|
| `FIB`（[6 章](#ch6)発展） | 16 | RecursionError |
| `SUM_TO_N` | 44 | RecursionError |
| `FACT` | 11（約 10 秒） | 15 秒で打ち切り（時間切れ） |

<!--
目安 1 分。正直に言うと、この方法はとても遅く、すぐに溢れます。チャーチ数は一進法で、n を表すのに f を n 回使うので、整数に直す仕事は数に比例して大きくなります。SUCC や ADD でつないだ数は、見るときにスタックも深く使います。ただし MUL や POW で作った数は関数の合成なので、値が大きくても深さはそれほどではありません。実測では、FIB（6 章の発展）は 16、SUM_TO_N は 44 まで動き、その次で RecursionError でした。FACT は 11 で約 10 秒かかり、12 は 15 秒で打ち切りました。FACT の境界はスタックではなく時間です。実用ではなく、計算の仕組みを見るための道具だと思ってください。
-->

---

## 参考文献

<div class="small">

- A. Church. An Unsolvable Problem of Elementary Number Theory. American Journal of Mathematics 58(2), 1936.
- A. M. Turing. On Computable Numbers, with an Application to the Entscheidungsproblem. Proc. London Math. Soc. s2-42, 1936–37.
- A. M. Turing. Computability and λ-Definability. Journal of Symbolic Logic 2(4), 1937.
- H. P. Barendregt. The Lambda Calculus: Its Syntax and Semantics. North-Holland, 1981; revised ed. 1984.
- B. C. Pierce. Types and Programming Languages. MIT Press, 2002.
- 高橋正子『計算論 計算可能性とラムダ計算』近代科学社, 1991.
- T. Stuart. Programming with Nothing. Ruby Manor 3 での講演と同名の記事, 2011.
- T. Stuart. Understanding Computation. O'Reilly, 2013.

</div>

<!--
目安 0.25 分。映すだけにします。日本語なら高橋正子さんの『計算論』、手を動かすなら Tom Stuart さんの Programming with Nothing（Ruby の lambda（proc）だけで FizzBuzz まで書く講演と記事）がおすすめです。
-->

---

<!-- _class: title -->
<!-- _paginate: false -->

# おわり

## 計算の最小単位は「関数を作る」と「関数を呼ぶ」

質問をどうぞ。

<div class="small">

スライドとコードはここにあります：[github.com/elle-et-noire/lambda-talk](https://github.com/elle-et-noire/lambda-talk)

参照実装 [code/lambda_core.py](https://github.com/elle-et-noire/lambda-talk/blob/main/code/lambda_core.py) ・ [Colab で開く](https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb)

</div>

<!--
目安 0.25 分。今日のまとめは一言です。計算の最小単位は、関数を作ることと、関数を呼ぶこと。それだけで真偽値も数も再帰も作れました。スライドと今日のコードは GitHub の elle-et-noire/lambda-talk に置いてあります。Colab でもそのまま動かせるので、家で続きを試してみてください。ありがとうございました。質問があればどうぞ。
-->
