# 引き継ぎメモ（2026-10-16 時点）

恒常的な指示・制約・文体の基準は [CLAUDE.md](../CLAUDE.md) にある。このファイルには、その時点の状況だけを書く。

## 公開先

- HTML スライド: https://elle-et-noire.github.io/lambda-talk/
- PDF: https://elle-et-noire.github.io/lambda-talk/lambda.pdf
- Colab: https://colab.research.google.com/github/elle-et-noire/lambda-talk/blob/main/notebooks/lambda.ipynb
- リポジトリ: https://github.com/elle-et-noire/lambda-talk

## これまでの経緯

1. **`170534c` 初期コミット**：スライド・テーマ・検証ツール・テスト・計画資料。
2. **`1237a70`**
   - Colab ノートブック `notebooks/lambda.ipynb` を追加した（§N = N 章）。
   - 本文の「N 章」を章扉へのページ内リンク（`#chN`）にし、check_slides にリンク先の検査を追加した。
   - GitHub Pages へのデプロイを設定した。
3. **`63f4f56`**
   - Google Fonts に対応した（`theme/quiet-webfonts.css`）。
   - 言い回しを見直した（「窓」などの造語、煽る見出し、親しげなラベルをやめた）。
   - 参考文献に DOI と出版社ページへのリンクを付け、Kleene の逸話の出典（Barendregt 1997、Kleene 1981、Crossley 1975）を追加した。
   - タイトルを一度「ラムダ計算を Python で動かす」に変えた。
4. **`c2e50d5` 圧縮**
   - 2 章の基本概念を、Python との対応で示す形に組み直した。
   - 重複するスライドを統合した（111 → 87 枚、必須 57.5 → 46.5 分、標準 88.5 → 71.25 分、全部入り 105 → 84 分）。
   - 「ルール」の設定をやめ、6 章で「再帰定義は置き換えが終わらない」から自己適用・Y/Z へ進む構成にした。
5. **未コミット**：タイトルを「Lambda Calculus in Python」に変え、サブタイトルとリード文を削除した。

## 作業中（未コミット）

- **タイトル変更の差分**：`slides/lambda.md`、`notebooks/lambda.ipynb`、`Makefile` の 1 行目、`slides/_sample.md` の h1。
- **サブエージェントが作業中**（この差分の上で進めている）：
  - 用語の見直し：lambda 式を「無名関数（lambda 式）」、適用を「関数呼び出し」と呼ぶ。「関数を作ること／呼ぶこと」のような言い方を直す。lambda を「関数定義」とは呼ばない。
  - 句点で細切れになった文をつなぐ。箇条書きの末尾の句点を統一する。
  - λ の本体についての約束（「$\lambda x.\,M\,N$ の本体は $M\,N$ 全体」）を、カリー化のスライドから λ 記法のスライド「λ記法と Python の lambda：項は 3 種類」へ移す。適用の左結合はカリー化のスライドに残す。
- 作業が終わったら、検証してまとめて commit・push してよいと、ユーザーの了承を得ている。
- 引き継ぎ資料（`CLAUDE.md`、`docs/handoff.md`、`tools/check_overflow.js`）も未コミット。

## ユーザーの判断待ち

- **`slides/_sample.md` の旧サブタイトル**：「1 引数の lambda で真偽値・数・再帰を作る」（3 つ並べの列挙）が、テーマの h2 の見本として残っている。消すか差し替えるか。
- **和名と英語名の併記**（約 40 語）：今は「β簡約 (beta reduction)」「チャーチ数 (Church numerals)」「サンク (thunk)」などの併記を維持している。Church–Turing thesis だけは英語名のみに変えた。ほかをどうするか。

## 未確認の事項

- **Colab の `#scrollTo=secN`**：GitHub から開いたノートブックで各 § に飛べるかは、ブラウザで確かめていない。飛べなくてもノートブックの先頭が開くだけ。
- **Kleene 1981 についてのスピーカーノート**：5 章の PRED のスライドに「Kleene 本人の 1981 年の回想には笑気ガスが出てこない」という指摘があるが、Kleene 1981 の本文では確かめていない。
- **参考文献のリンク先**：DOI は doi.org と Crossref で確かめた。ただし JSTOR・Wiley・Springer・IEEE・MIT Press・O'Reilly のページは、ボット対策で中身を直接取得できなかった（MIT Press と O'Reilly は Web アーカイブのスナップショットで存在を確認した）。
- **Python 3.10**：ノートブックは 3.10 の構文で書いていることをテストで確かめているが、3.10 の実機では実行していない（3.12 と 3.14 で実行済み）。

## 検証の方法

- **基本**：`make check && make test && make time`
  - 時間の記述は、時間割の表と冒頭の「必須のみ約 N 分」を `make time` の結果と照合する。
- **はみ出し**：`make html && node tools/check_overflow.js`
  - 各 `<section>` の padding の内側より下・右に出た要素と、`<pre>` のスクロール（コードの切れ）を数える。
  - KaTeX の MathML と SVG の `path` は誤検出になるので除いている。
  - puppeteer-core は、marp-cli が npx キャッシュ（`~/.npm/_npx/*/node_modules/puppeteer-core`）に入れたものを使う。見つからなければ `PUPPETEER_CORE` で、ブラウザは `CHROME_PATH` で指定する。
  - snap 版の Chromium は `/tmp` などを `file://` で読めないので、スクリプト内の HTTP サーバー経由で開いている。
  - 見た目は `make png` で確かめる。1 枚だけなら marp-cli の `--images png` を一時ディレクトリに出す。
- **PDF の内部リンク**：`make pdf` の後に pypdf で確かめる。各ページの注釈の `/Dest` が、`named_destinations` に `/ch1`〜`/ch9` として存在すればよい。
  ```sh
  uv run --no-project --with pypdf python -c "import pypdf; r=pypdf.PdfReader('out/lambda.pdf'); print(sorted(k for k in r.named_destinations if k.startswith('/ch')))"
  ```
- **PDF のフォント**：`pdffonts out/lambda.pdf` で Noto 系が埋め込まれていることを見る。罫線が DejaVu に化けていないか（7 章のリストの図）も見る。
- **デプロイ**：push 後、`gh run list --workflow pages.yml --limit 1` で run を探し、`gh run watch <id> --exit-status` で結果を待つ。
