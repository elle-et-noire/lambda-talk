# 引き継ぎメモ（2026-10-16、`c8440f6` ＋未コミットの変更）

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
5. **`79b34cb` タイトルと用語・数式の整備**
   - タイトルを「Lambda Calculus in Python」に変え、サブタイトルとリード文を削除した。
   - 用語を「無名関数（lambda 式）」「関数呼び出し」「評価する」にそろえた。lambda を「関数定義」とは呼ばない。
   - 句点で細切れになった文をつなぎ、スライドの箇条書き・本文・注記は末尾の句点なしで統一した（ノートブックはです・ます調なので句点あり）。
   - λ の本体の約束（$\lambda x.\,M\,N$ の本体は $M\,N$ 全体）を、カリー化のスライドから λ 記法のスライドへ移した。
   - 簡約表（`<div class="steps">`）を 11 個すべて KaTeX の `aligned` に置き換え、関係記号を揃えた。
   - FACT_GEN の引数名 `self` を `s` に変えた（参照実装 `code/lambda_core.py`、スライド、ノートブック）。`code/tests/test_rules.py` は `plan/outline.md` の定義とも照合しているので、`self` を `s` と読み替える処理を加えた。
   - 引き継ぎ資料（`CLAUDE.md`、`docs/handoff.md`、`tools/check_overflow.js`）を追加した。

## 未コミット（`c8440f6` の上）

- `slides/_sample.md` の h2 を、3 つ並べの旧サブタイトルから「見出し 2 の見本」に変えた。
- 和名と英語名の併記を、初出だけに変えた（CLAUDE.md の「表記」も更新）。もともと重複は少なく、外したのはスライドの 2 か所（4 章のチャーチ数、6 章の η展開）だけ。ノートブックは変更なし。
- 1 章「1930 年代」のスピーカーノートを約 590 字から 401 字に縮め、`tally_time.py -v` の警告を消した。目安 1.5 分は変えていない。

## ユーザーの判断待ち

- **η展開の併記**：初出の併記を 2 章の発展スライドに残し、6 章の Z コンビネータのスライドからは外した。発展を飛ばして話すと、聞き手が最初に見るのは 6 章になる。
- **右畳み込み (right fold)**：英語名はスピーカーノートにしかなく、7 章の見出しは和名だけ。見出しに英語名を移すかどうか。

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
