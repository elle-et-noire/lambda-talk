# 構成案：Python からクラスも数も消す（ラムダ計算）

## 時間の型

| 版 | 内容 | 想定 |
|---|---|---|
| 必須のみ | 必須スライドだけ | 約 57.5 分（＋予備 2.5 分で 60 分枠） |
| 標準 | 必須 ＋ 2章発展・3章 XOR・4章 IS_EVEN と MUL_BY_ADD・5章発展・6章 FIB・7章リスト（FizzBuzz 除く） | 約 88.5 分 |
| 全部入り | 標準 ＋ FizzBuzz ＋ 8章 SKI ＋ 9章 型（発展） | 約 105 分（＋質疑バッファで 120 分枠） |

依存関係の注意：7章（リスト）の `RANGE` は 5章発展の `LEQ`/`SUB` を使う。7章を入れるなら 5章発展も入れる。

## 章ごとの計画

凡例：［必］必須、［発］発展（`optional` クラス）、［演］演習、［解］解答

### 0. タイトルとルール（必須 2.5 分）
0-1 タイトル［必］
0-2 今日作るもの（真偽値・自然数・足し算・再帰）［必］
0-3 ルール：使ってよいもの／使わないもの［必］
0-4 例外：観測用関数＝「純粋な世界の外側にある窓」［必］
0-5 時間割（章一覧と必須／発展）［必］

### 1. 導入（必須 3.5 分）
1-0 章扉
1-1 計算に本当に必要なものは？［必］
1-2 1930 年代：Church のラムダ計算と Turing の機械［必］
1-3 チャーチ＝チューリングのテーゼ（一言）［必］
1-4 λ記法と Python の lambda の対応（2 カラム）［必］

### 2. 文法と評価（必須 9.5 分 ＋ 発展 5 分）
2-0 章扉
2-1 項は 3 種類：変数・抽象・適用（BNF）［必］
2-2 Python に写すと（2 カラム）［必］
2-3 表記の約束：適用は左結合、抽象は右へ伸びる［必］
2-4 自由変数と束縛変数［必］
2-5 α変換［必］
2-6 β簡約の定義［必］
2-7 β簡約を 1 ステップずつ（図）［必］
2-8 カリー化：`f(a)(b)` の読み方［必］
2-9 ［演］手で簡約する［必］
2-10［解］［必］
2-11 η変換［発］
2-12 評価戦略：正規順序 vs 適用順序［発］
2-13 Python は適用順序（正格）。これが後で効いてくる（伏線）［発］

### 3. チャーチ真偽値（必須 8 分 ＋ 発展 2 分）
3-0 章扉
3-1 真偽値＝2 択から選ぶ関数：`TRUE`、`FALSE`（2 カラム）［必］
3-2 窓その1：`to_bool`［必］
3-3 `IF`［必］
3-4 `NOT`、`AND`［必］
3-5 ［演］`OR` を書く［必］
3-6 ［解］［必］
3-7 落とし穴：正格評価で `IF` が両方の枝を評価する［必］
3-8 サンク `lambda _: ...` で包む（Z の伏線）［必］
3-9 ［演］`XOR`［発］
3-10［解］［発］

### 4. チャーチ数（必須 9.5 分 ＋ 発展 4 分）
4-0 章扉
4-1 数 n ＝ f を n 回適用する関数［必］
4-2 `ZERO`、`ONE`（2 カラム）［必］
4-3 窓その2：`to_int`［必］
4-4 `SUCC` と `TWO`〜`TEN`［必］
4-5 `ADD`（m 回 `SUCC`）［必］
4-6 `MUL`（関数合成。短い）［必］
4-7 ［演］`POW` を書く（`EXP` とも）［必］
4-8 ［解］`POW = lambda m: lambda n: n(m)`。なぜ動くか［必］
4-9 `IS_ZERO`［必］
4-10［演］`IS_EVEN`［発］
4-11［解］［発］

### 5. ペアと引き算（必須 5 分 ＋ 発展 6 分）
5-0 章扉
5-1 `PAIR`、`FIRST`、`SECOND`［必］
5-2 引き算はなぜ難しいか［必］
5-3 Kleene のトリック（ペアをずらす図）［必］
5-4 `SHIFT` と `PRED`、歯医者の逸話（伝わっている話）［必］
5-5 ［演］`SUB` を書く［発］
5-6 ［解］［発］
5-7 `LEQ`、`EQ`［発］

### 6. 再帰と Y コンビネータ（必須 16.5 分 ＋ 発展 2 分）山場
6-0 章扉
6-1 階乗を書きたい。でも自分の名前は呼べない［必］
6-2 自己適用 `ω = λx.x x` と `Ω = ω ω`（RecursionError）［必］
6-3 アイデア：自分自身を引数でもらう［必］
6-4 `FACT_GEN`：`self(self)` で再帰する［必］
6-5 動いた：`FACT_GEN(FACT_GEN)`［必］
6-6 `self(self)` を外へ追い出す：`FACT_BODY`［必］
6-7 抽象化すると Y：`Y F = F (Y F)`［必］
6-8 Python で Y を使うと RecursionError［必］
6-9 なぜ？ 正格評価が `x(x)` を先に計算し続ける［必］
6-10 η展開で包む：Z コンビネータ［必］
6-11 Z で `FACT`［必］
6-12［演］Z で `SUM_TO_N`［必］
6-13［解］［必］
6-14 `FIB` と、扱える最大値（実測）［発］

### 7. リスト（発展 12 分 ＋ FizzBuzz 5.5 分）
7-0 章扉
7-1 リストの表現（ペアの入れ子、図）［発］
7-2 `NIL`、`CONS`、`IS_NIL`、`HEAD`、`TAIL`［発］
7-3 窓その3：`to_list`［発］
7-4 `RANGE`（Z）［発］
7-5 `FOLD`［発］
7-6 `MAP`（`FOLD` で書く）［発］
7-7 ［演］`SUM` を `FOLD` で書く［発］
7-8 ［解］［発］
7-9 FizzBuzz 準備：`MOD`、`DIV`［発］
7-10 文字の表現と `TO_DIGITS`、窓その4：`to_str`［発］
7-11 `FIZZBUZZ` 本体［発］
7-12 実行結果［発］

### 8. SKI コンビネータ（発展 10 分）
8-0 章扉
8-1 lambda すら消す：`S`、`K`、`I`［発］
8-2 `I = S K K` を確かめる（手で簡約 ＋ Python）［発］
8-3 ［演］`K` と `K I` は何に見える？［発］
8-4 ［解］`TRUE` と `FALSE`［発］
8-5 ブラケット抽象：変数を消す 3 つの規則［発］
8-6 例：`λx.x x` → `S I I`［発］
8-7 SKI だけでチューリング完全［発］

### 9. まとめと先へ（必須 3 分 ＋ 発展 1 分）
9-0 章扉
9-1 今日作ったもの［必］
9-2 型付きラムダ計算では Y が型付けできない（停止性）［必］
9-3 実用言語とのつながり：クロージャ、Haskell、Lisp［必］
9-4 性能の話：一進法、再帰上限（実測値）［必］
9-5 参考文献（実在確認済みのみ）［必］
9-6 おわり／質問［必］

## 演習一覧

スライドのノートの「目安」と一致させる。出題の欄の括弧内は、ノートで指示している考える時間。

| 章 | 演習 | 区分 | 出題 | 解説 | 計 |
|---|---|---|---:|---:|---:|
| 2 | 手で β簡約 | 必須 | 2 分（2 分） | 0.75 分 | 2.75 分 |
| 3 | `OR` | 必須 | 1.5 分（1 分＋ヒント 0.5 分） | 0.5 分 | 2 分 |
| 3 | `XOR` | 発展 | 1.5 分 | 0.5 分 | 2 分 |
| 4 | `POW` | 必須 | 2.5 分（2 分、途中で 2 択のヒント） | 1.25 分 | 3.75 分 |
| 4 | `IS_EVEN` | 発展 | 2 分（1.5 分） | 1 分 | 3 分 |
| 5 | `SUB` | 発展 | 2 分（1.5 分） | 2 分 | 4 分 |
| 6 | `SUM_TO_N` | 必須 | 2.5 分（2 分） | 0.5 分 | 3 分 |
| 7 | `SUM`（`FOLD`） | 発展 | 2 分（2 分） | 1 分 | 3 分 |
| 8 | `K` と `K I` | 発展 | 2 分（2 分） | 1 分 | 3 分 |

## 命名と定義の仕様（全章共通・`code/lambda_core.py` と一致させる）

- 純粋な世界の定義は大文字（`TRUE`、`SUCC` など）。例外は `omega`（小文字のギリシャ文字ωに合わせる）。
- 観測用関数（窓）は小文字の `to_` で始める：`to_bool`、`to_int`、`to_list`、`to_str`。
- サンクは `lambda _: 式`。強制するときは `(ID)` を適用する。
- 再帰の形は必ず `IF(条件)(lambda _: A)(lambda _: B)(ID)`。

```python
ID = lambda x: x
TRUE = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
IF = lambda b: lambda t: lambda f: b(t)(f)
NOT = lambda b: b(FALSE)(TRUE)
AND = lambda a: lambda b: a(b)(FALSE)
OR = lambda a: lambda b: a(TRUE)(b)
XOR = lambda a: lambda b: a(NOT(b))(b)
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
SUCC = lambda n: lambda f: lambda x: f(n(f)(x))
TWO = SUCC(ONE)  # 以下 TEN まで同様
ADD = lambda m: lambda n: m(SUCC)(n)
MUL = lambda m: lambda n: lambda f: m(n(f))
POW = lambda m: lambda n: n(m)
IS_ZERO = lambda n: n(lambda _: FALSE)(TRUE)
IS_EVEN = lambda n: n(NOT)(TRUE)
PAIR = lambda a: lambda b: lambda s: s(a)(b)
FIRST = lambda p: p(TRUE)
SECOND = lambda p: p(FALSE)
SHIFT = lambda p: PAIR(SECOND(p))(SUCC(SECOND(p)))
PRED = lambda n: FIRST(n(SHIFT)(PAIR(ZERO)(ZERO)))
SUB = lambda m: lambda n: n(PRED)(m)
LEQ = lambda m: lambda n: IS_ZERO(SUB(m)(n))
EQ = lambda m: lambda n: AND(LEQ(m)(n))(LEQ(n)(m))
omega = lambda x: x(x)
FACT_GEN = lambda self: lambda n: (IF(IS_ZERO(n))(lambda _: ONE)(lambda _: MUL(n)(self(self)(PRED(n))))(ID))
FACT_BODY = lambda fact: lambda n: (IF(IS_ZERO(n))(lambda _: ONE)(lambda _: MUL(n)(fact(PRED(n))))(ID))
Y = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))
Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))
FACT = Z(FACT_BODY)
SUM_TO_N, FIB, NIL, CONS, IS_NIL, HEAD, TAIL, RANGE, FOLD, MAP, SUM,
MOD, DIV, TO_DIGITS, FIZZBUZZ など 7 章の定義は lambda_core.py を正とする
S = lambda x: lambda y: lambda z: x(z)(y(z))
K = lambda x: lambda y: x
I = S(K)(K)
```

## スライド表記の約束

- 用語は初出時に英語を併記：β簡約 (beta reduction) など。
- コードは 1 スライド 12 行まで。1 行は全幅 64 文字、2 カラム時 34 文字まで。
- 発展スライドは `<!-- _class: optional -->`。章扉は `chapter`、演習は `exercise`、解答は `answer`、λと Python の対応は `twocol`。
- 各スライドにスピーカーノート（HTML コメント）：話す内容と目安時間。
- スライド内コードは上から累積実行される。使う名前は、それより前のスライドで必ず定義する。
