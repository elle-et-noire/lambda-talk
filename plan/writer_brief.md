# スライド執筆者向け共通ブリーフ

あなたは講習会スライド「Python からクラスも数も消す（ラムダ計算）」の一部の章を書きます。
プロジェクト：/home/lomega/utmc/lambda-python/lambda-talk
必ず読むもの：plan/outline.md（全体構成・命名仕様）、code/lambda_core.py（定義の正）、plan/limits.md（実測した上限）、theme/quiet.css と slides/_sample.md（マークアップ例）。

## 聴衆と口調
- Python はある程度書ける（lambda、クロージャ、高階関数は見たことがある程度）。ラムダ計算は初見。
- 日本語。です・ます調の地の文は避け、スライド本文は体言止めや短文で簡潔に。スピーカーノートは話し言葉（です・ます）で。
- 用語は初出時に英語を併記する：β簡約 (beta reduction)、カリー化 (currying) など。初出は担当章ではなく「デッキ全体で初出」の箇所。担当外の章で既に出た用語は併記しなくてよい（outline を見て判断）。
- 天下り式にしない。「なぜそうなるか」を 1 ステップずつ。

## 講習のルール（全編で守る）
- 使ってよい：1 引数の `lambda`、関数適用、名前付け（長い式の略記）。自分自身を参照する名前付けは禁止。
- 使わない：数値リテラル、`True`/`False`、`if`、`class`、組み込み演算子、`def` による再帰。
- 例外：観測用関数 `to_bool`、`to_int`、`to_list`、`to_str`（「純粋な世界の外側にある窓」）。

## コードの約束（機械検証される）
- スライド中の ```python ブロックは、デッキ全体で上から順に同じ名前空間で累積実行される（tools/check_slides.py）。
- `>>>` を含むブロックは doctest として照合される。結果を見せたいときは doctest 形式で書く：
  ```python
  >>> to_int(ADD(TWO)(THREE))
  5
  ```
  例外は次の形で（メッセージ本文は無視される）：
  ```python
  >>> omega(omega)
  Traceback (most recent call last):
    ...
  RecursionError: maximum recursion depth exceeded
  ```
- 定義は code/lambda_core.py と同じ式・同じ引数名で書く（AST 比較される。改行位置は自由）。lambda_core.py にない名前を新たに作るのは、説明用の変種（例：`MUL_BY_ADD`）に限り可。その場合もルールを守る。
- 使う名前は、デッキ上でそれより前に定義されていなければならない。前の章の定義は再掲しない（必要なら「前の章の ○○」と言葉で触れる）。
- どうしても実行できないブロックだけ 1 行目を `# 実行しない` に（最小限）。λ記法は Python ブロックではなく KaTeX（`$...$`、`$$...$$`）で書く。
- 1 ブロック 12 行まで。1 行は全幅 64 文字、2 カラム内 34 文字まで。超えるならスライドを分ける。
- 再帰上限が関わる例の値は plan/limits.md の「スライドに載せてよい安全値」以下にする。
- 単体確認：`.venv/bin/python tools/check_slides.py <あなたのファイル> --preload-core` が通ること（前章の定義を先読みして確認するモード）。

## スライドの約束
- 1 スライド 1 メッセージ。文字は少なめ。箇条書きは 5 項目程度まで。
- 見出しは `##`（章扉とタイトルだけ `#`）。
- 各スライドの末尾にスピーカーノート（HTML コメント）を必ず付ける。形式：
  `<!-- 目安 1.5 分。話す内容…… -->`
- 章扉：`<!-- _class: chapter -->`（発展章は `chapter optional`）、本文に「目安 N 分（発展 +M 分）」。
- 発展スライド：`<!-- _class: optional -->`。演習：`exercise`、解答：`answer`（発展の演習は `exercise optional`）。演習の解答は必ず次のスライド。
- λ記法と Python の対応は `twocol` クラス。
- 絵文字・アイコン・装飾的な記号は使わない。図は表、KaTeX、または簡単なテキスト図（コードブロックは ```text）で。
- スライド区切りは `---`。front-matter は書かない（統合時に付ける）。最初のスライドの前に `---` を置かない。

## 提出前に
- check_slides が通ることを確認する。
- `npx --yes @marp-team/marp-cli@4.5.1` で、あなたのファイルに front-matter を付けた一時コピー（scratchpad などに置く）を PNG 化し、全ページを Read で目視してはみ出し・詰め込みを直す。テーマは `--theme-set theme/quiet.css`、`--html` を付ける。
- 報告：作ったスライド数、各スライドの区分（必須/発展）と目安時間の合計、lambda_core.py にない新しい名前の一覧、気になった点。

## テーマ `quiet` のマークアップ規約（テーマ担当の報告より）
- 色：背景 #fbfaf7、文字 #2b2b2b、アクセント紺 #1f3a5f、補助色レンガ #9a4b2c。`**x**` は紺の太字（主な強調）、`*x*` はレンガ色（控えめに使う）。
- 本文 30px、`##` 見出し 38px。コードは全幅 26px、2 カラム内 24px。
- 文字幅：全角 1 文字は 2 桁として数える。全幅 64 桁、2 カラムは 34 桁まで。
- 高さ：12 行のコードを置くと、残りは `##` 見出しと散文 1 行分だけ。散文を増やすならコードは 10 行以下に。
- タイトル：`<!-- _class: title -->` と `<!-- _paginate: false -->`、`# タイトル`、`## サブタイトル`、段落。
- 章扉：`<!-- _class: chapter -->`（発展章は `chapter optional`）、`# <span class="num">2</span>文法と評価`、次の段落に `目安 10 分（発展 +5 分）`。
- クラスは空白区切りで組み合わせる：`<!-- _class: exercise optional -->`。演習・解答スライドには `##` 見出しが必須。
- twocol：`<!-- _class: twocol -->`、`## 見出し`、`<div class="cols">` の中に子 `<div>` をちょうど 2 つ（左に λ記法 `$$...$$`、右に ```python）。開きタグ `<div>` の後と閉じタグ `</div>` の前には空行を入れる。
- 普通のスライドで `<div class="cols">` を使うと、ラベルなしの 2 カラムになる。
- 数式：適用の間隔は `\,` を使う（例：`\lambda x.\,f\,(x\,x)`）。ディスプレイ数式は横幅 1100px 程度まで。
- β簡約の手順表：`<div class="steps">` の中に表を置く（div の内側に空行を入れる）。ヘッダは空の `| | |` と `|---|---|`。各行は `| $\to_\beta$ | $項$ |`、1 行目の第 1 列は空。
- 補助：`<p class="note">…</p>`（小さく控えめ。出典やヒントに）、`.small`、`.muted`、`.center`。
- `section::before` と `section::after` はテーマが使うので、スライド側で上書きしない。
- marp-cli を直接呼ぶときは `--no-stdin` を付ける（付けないと非対話シェルで止まる）。例：
  `npx --yes @marp-team/marp-cli@4.5.1 --config-file .marprc.yml --no-stdin <file> --images png -o <outdir>/x.png`
- 見本：slides/_sample.md
