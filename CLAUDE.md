# CLAUDE.md

講義スライド「Lambda Calculus in Python」のリポジトリ。いまの作業状況は [docs/handoff.md](docs/handoff.md) を参照。

## 概要

- 日本語の Marp スライドで、Python の 1 引数 lambda だけでラムダ計算を書く入門講義（真偽値・チャーチ数・ペア・Y/Z コンビネータ・リスト・SKI）。
- 対応する Colab ノートブックがあり、§N が N 章に対応する。
- `main` に push すると GitHub Actions が HTML / PDF をビルドし、GitHub Pages に公開する。
- リポジトリ: https://github.com/elle-et-noire/lambda-talk
- 公開先: https://elle-et-noire.github.io/lambda-talk/ （PDF は `lambda.pdf`）
- Colab: https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb

## ディレクトリ

| パス | 役割 |
|---|---|
| `slides/lambda.md` | 本体。スピーカーノートは `<!-- 目安 N 分。… -->` の HTML コメント |
| `slides/_sample.md` | テーマ確認用の見本（`make sample`） |
| `theme/quiet.css` | Marp テーマ `quiet` |
| `theme/quiet-webfonts.css` | **生成物**（`make webfonts`）。手で編集しない |
| `notebooks/lambda.ipynb` | Colab 用ノートブック。自己完結で `code/` を import しない |
| `code/lambda_core.py` | 定義の参照実装。スライドとノートブックの定義はこれと AST が一致する必要がある |
| `code/tests/` | pytest（check_slides・参照実装・ノートブックのテスト） |
| `tools/check_slides.py` | スライドのコードを実行して検証する（`make check`） |
| `tools/tally_time.py` | 「目安 N 分」を章ごとに集計する（`make time`） |
| `tools/gen_webfonts.py` | Google Fonts から `theme/quiet-webfonts.css` を生成する |
| `tools/check_overflow.js` | headless Chromium でスライドのはみ出しを検出する |
| `tools/measure_limits.py` | 再帰の深さと実行時間の限界を実測する（9 章の表の根拠） |
| `plan/` | 企画・レビューの経緯の記録。古い用語が残っていてよく、更新しない |
| `out/` | ビルド成果物（git 管理外） |
| `.github/workflows/pages.yml` | check → HTML/PDF ビルド → Pages へデプロイ |

## 環境構築

- **Python 3.14**：uv で `.venv` を作る。依存は pytest だけ（ツールは標準ライブラリのみ）。
  ```sh
  uv venv --python 3.14 .venv
  uv pip install --python .venv/bin/python pytest
  ```
- **Node 22**：marp-cli は `npx --yes @marp-team/marp-cli@4.5.1` で都度取得する（Makefile の `MARP`）。
- **Chromium / Chrome**：PDF・PNG の出力と `tools/check_overflow.js` で使う。
  - 自動で見つからないときは `CHROME_PATH=/path/to/chrome make pdf` のように指定する。
- **フォント**：PDF をきれいに出すには Noto Sans CJK JP / Noto Sans Mono / Noto Sans Mono CJK JP を入れる（Debian/Ubuntu なら `fonts-noto-cjk fonts-noto-mono`）。HTML は Web フォントで代替される。

## コマンド

| コマンド | 内容 |
|---|---|
| `make check` | スライドのコードブロックを上から実行し、doctest・ルール・参照実装との一致・ページ内リンクを検査 |
| `make test` | pytest（`code/tests`） |
| `make time` | 発表時間の集計（必須／標準／全部入り） |
| `make html` / `make pdf` / `make png` | `out/` に書き出す |
| `make webfonts` | `theme/quiet-webfonts.css` を作り直す（ネットワークが必要） |
| `node tools/check_overflow.js [out/lambda.html]` | はみ出しの検出（先に `make html`） |

## 守るべき制約

- **check_slides**（`make check`）
  - ` ```python ` ブロックは上から順に実行される。コードは 1 行 64 桁以内（全角は 2 桁）、1 ブロック 12 行以内で、超えると警告になる。
  - 定義の右辺は、名前・1 引数 lambda・1 引数の呼び出しだけで書く。数値リテラルや演算子は使えない。結果を確かめるための変換関数（`to_int` など）は例外。
  - `code/lambda_core.py` にある名前を定義するときは、AST が一致すること。
  - 実行しないブロックは 1 行目を `# 実行しない` にする。
  - ページ内リンク（`[N 章](#chN)`、`<a href="#chN">`）の行き先 `id` が存在すること。数字だけの行き先は Marp のスライド番号とみなし、検査しない。
- **ノートブック**（`code/tests/test_notebook.py`）
  - 出力は空で保存する。セル id は一意で、`sec0`〜`sec9` の見出しセルがあること。
  - Python 3.10 の文法で書き、`lambda_core` は import しない。
  - 定義は `code/lambda_core.py` と AST が一致すること。上から全部実行して通ること。
  - 演習の `MY_X = None` に正解を入れると、`check` が通ること。
- **リンクの目印**
  - 章扉の見出しは `# <span class="num" id="chN">N</span>…`。本文の「N 章」は `#chN` へのリンクにする。
  - Colab へのリンクは `…/lambda.ipynb#scrollTo=secN`。
  - ノートブックの「（スライド：「…」）」は、スライドの見出しと文字列を一致させる。
- **時間**
  - `tools/tally_time.py` は、見出しに「FizzBuzz を関数だけで」を含むかどうかで 7 章後半の区分を決めている。この見出しは変えない。
  - 時間割の表、冒頭の「必須のみ約 N 分」、`make time` の結果を一致させる。
- **Web フォント**
  - インストール済みの Noto を優先し、ない環境では Google Fonts を使う。
  - Google 版の Noto Sans Mono には罫線文字がない。同名で読み込むとローカル版を上書きして図が崩れるため、Web 版は別名 `Quiet Web Mono` で定義し、フォント指定でローカル版の後ろに置いている。
  - コード中の日本語は、別名フォント `Quiet Code CJK`（Noto CJK を `size-adjust: 120%`）で半角 2 文字幅にそろえている。Web 版は Noto Sans JP の woff2 サブセットを同じ別名で再定義している。
- **公開**：`main` への push で Pages が更新される（対象パスは workflow の `paths`）。

## 文体の基準（ユーザーの指摘）

スライド・スピーカーノート・ノートブックのすべてに適用する。

- **造語・比喩を使わない**：一般名詞に文脈上の意味を持たせない。
  - 例：「窓」→「変換関数」、「純粋な世界」→「lambda と関数呼び出しだけで書いたコード」
  - ほかにも「包み」「伏線」「鍵」「山場」「旗」「選び手」「略記」「ルール」を使わない。
- **主語・目的語を省かない**：そのスライドだけで分かるように書く。
  - 例：「IS_ZERO：1 回でも適用されたら偽」→「IS_ZERO：n が f を 1 回でも適用すれば FALSE」
- **前提のない問いや煽りを置かない**：見出しや導入に、聞き手がまだ共有していない前提の問いを置かない。順を追って説明すれば、面白さは自然に伝わる。
  - 例：「引き算はなぜ難しいか」→「前者関数 PRED：1 つ前の値もペアで持ち歩く」
  - 「実は」「驚くほど」「面白い」「いよいよ」も使わない。
- **親しげな演出をしない**：ラベルは中立にする。
  - 例：「Colab §6 で試す」→「コード：Colab §6」
  - 「〜してみよう」、感嘆符、絵文字、決め台詞、3 つ並べの列挙を使わない。
  - スピーカーノートのです・ます調はよい。
- **聞き手はプログラマー**：自由変数・束縛変数・α/β/η などは丁寧に定義せず、Python コードとの対応で示す。冗長なスライドは統合する。
- **「ルール」という設定を作らない**：子供扱いになる。制約は実際の理由で動機づける。
  - 例：再帰定義は、名前を定義の右辺に置き換えると FACT が現れ続けて置き換えが終わらない。
- **標準用語を使う**：
  - lambda 式は「無名関数（lambda 式）」と呼ぶ。`def` を連想させるので「関数定義」とは呼ばない。適用は「関数呼び出し」。
  - `ADD = …` のように名前を付ける操作は「定義」と呼ぶ。名前は「定義の右辺に置き換えられる」と説明する。
- **句点で細切れにしない**：論理的につながる短文は、接続助詞でつなぐ。
- **数式**：簡約や等式の列は KaTeX の `aligned` で関係記号（`=`、`=_\beta`、`\twoheadrightarrow_\beta`）を揃える。`<div class="steps">` の表は使わない。
- **表記**：Church–Turing thesis は英語名だけ。ほかの用語は和名（英語名）の併記を現状維持する。
- **タイトル**：「Lambda Calculus in Python」。スタイリッシュにし、サブタイトルやリード文で内容を列挙しない。

## 作業の進め方

- **作業の割り振り**：作業は background のサブエージェントに任せ、メインのセッションは新しい指示を受けられるよう空けておく。難しさでモデルと effort を選ぶ（言い回しや構成の判断は opus/high、機械的な修正は opus/medium）。
- **並行作業の衝突を避ける**：同じファイルを複数のエージェントが触るときは、担当範囲を分け、Edit で局所的に変更させる。時間割の更新が絡む作業は 1 つのエージェントにまとめる。
- **commit / push**：ユーザーの了承を得てから行う。commit メッセージは日本語。push 後は Pages のデプロイ結果（`gh run watch`）を確認する。
- **公開前の検証**：`make check`・`make test`・`make time` が通り、時間の記述と一致していること。`make html` の後、`node tools/check_overflow.js` ではみ出しが 0 であること。見た目は PNG で確認する。
