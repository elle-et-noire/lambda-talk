---
marp: true
theme: quiet
paginate: true
math: katex
size: 16:9
---

<!-- _class: title -->
<!-- _paginate: false -->

# Lambda Calculus in Python

## 1 引数の lambda で真偽値・数・再帰を作る

2026 年 10 月　サンプル講義

<!--
テーマ確認用のタイトル。ここで自己紹介と今日のゴール（30 秒）。
-->

---

<!-- _class: chapter -->

# <span class="num">2</span>文法と評価

目安 10 分（発展 +5 分）

<!--
章扉。章の狙いを一言で（15 秒）。
-->

---

## 箇条書きと 12 行のコード

β簡約 (beta reduction) は **関数適用** を 1 ステップ *進める* こと。

```python
ID = lambda x: x                                      # 恒等関数
TRUE = lambda t: lambda f: t                          # 先を選ぶ
FALSE = lambda t: lambda f: f                         # 後を選ぶ
IF = lambda b: lambda t: lambda f: b(t)(f)            # 分岐の形
NOT = lambda b: b(FALSE)(TRUE)                        # 入れ替え
AND = lambda a: lambda b: a(b)(FALSE)                 # 両方真か
ZERO = lambda f: lambda x: x                         # f を 0 回
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))       # 1 回追加
ADD = lambda m: lambda n: m(SUCC)(n)                 # m 回 SUCC
to_int = lambda n: n(lambda k: k + 1)(0)              # 数に変換
print(to_int(ADD(SUCC(ZERO))(SUCC(SUCC(ZERO)))))   # => 3 になる
assert to_int(ZERO) == 0, "ZERO must be 0 (64 chars wide)......"
```

<!--
12 行・全幅 64 桁の上限を確認するためのスライド。行末コメントは日本語（1 分）。
-->

---

## 箇条書きだけのスライド

- 用語は初出時に英語を併記する：α変換 (alpha conversion)
- コードは上から累積実行される
  - 使う名前は、それより前のスライドで定義する
  - 結果を Python の値に変換する関数は、小文字の `to_` で始める
- 発展スライドは飛ばしても話がつながる

> 引用：計算に本当に必要なものは何か？

<p class="note">注記：.note は小さく控えめな文字。出典や補足に使う。</p>

<!--
本文の行間と引用・注記の見え方を確認（30 秒）。
-->

---

<!-- _class: twocol -->

## λ記法と Python の対応

<div class="cols">
<div>

$$\lambda x.\,x$$

$$\lambda t.\,\lambda f.\,t$$

$$\lambda n.\,\lambda f.\,\lambda x.\,f\,(n\,f\,x)$$

</div>
<div>

```python
ID = lambda x: x
TRUE = lambda t: lambda f: t
SUCC = (lambda n: lambda f:
        lambda x: f(n(f)(x)))
print(TRUE("a")("b"))  # 先を選ぶ
CHECK = "34 chars per column....."
```

</div>
</div>

<!--
左が λ 記法、右が Python。ラベルは CSS が自動で付ける（1 分）。
-->

---

<!-- _class: optional -->

## η変換 (eta conversion)：長い見出しでも発展タグに重ならない

$x$ が $M$ の自由変数でないとき

$$\lambda x.\,M\,x \;\to_\eta\; M$$

- Python では `lambda v: f(v)` と `f` は同じふるまい
- ただし **評価のタイミング** が変わる（Z コンビネータの伏線）

<!--
発展スライド。時間がなければ飛ばす（2 分）。
-->

---

<!-- _class: exercise optional -->

## `XOR` を書く

`TRUE`・`FALSE`・`NOT` だけを使って `XOR` を定義せよ。

```python
XOR = lambda a: lambda b: ...
assert to_bool(XOR(TRUE)(FALSE)) is True
assert to_bool(XOR(TRUE)(TRUE)) is False
```

<p class="note">ヒント：a が真なら NOT(b)、偽なら b。</p>

<!--
演習（発展）。2 分待つ。演習ラベルと発展タグが重ならないことを確認。
-->

---

<!-- _class: answer -->

## `XOR` の解答

```python
XOR = lambda a: lambda b: a(NOT(b))(b)
```

- `a` が `TRUE` なら第 1 引数 `NOT(b)` を選ぶ
- `a` が `FALSE` なら第 2 引数 `b` を選ぶ

<!--
解答。a で分岐しているだけ、と強調（1 分）。
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

| 名前 | λ 記法 | Python |
|---|---|---|
| 恒等 | $\lambda x.\,x$ | `lambda x: x` |
| 真 | $\lambda t.\,\lambda f.\,t$ | `lambda t: lambda f: t` |

<!--
表のスタイル確認。上は手順表（.steps）、下は通常の表（1 分）。
-->

---

## 不動点と Z コンビネータ

$$
Y \;=\; \lambda f.\,(\lambda x.\,f\,(x\,x))\,(\lambda x.\,f\,(x\,x))
$$

$$
Z \;=\; \lambda f.\,(\lambda x.\,f\,(\lambda v.\,x\,x\,v))\,(\lambda x.\,f\,(\lambda v.\,x\,x\,v))
$$

$Y\,F = F\,(Y\,F)$ が成り立つ。Python では $Z$ を使う。

<!--
ディスプレイ数式の大きさ確認（1 分）。
-->
