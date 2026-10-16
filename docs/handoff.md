# 引き継ぎメモ（2026-10-16）

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
6. **`745aac8` 併記の整理と 1 章のノート**
   - `slides/_sample.md` の h2 を、3 つ並べの旧サブタイトルから「見出し 2 の見本」に変えた。
   - 和名と英語名の併記を、初出だけに変えた（CLAUDE.md の「表記」も更新）。もともと重複は少なく、外したのはスライドの 2 か所（4 章のチャーチ数、6 章の η展開）だけ。ノートブックは変更なし。
   - 1 章「1930 年代」のスピーカーノートを約 590 字から 401 字に縮め、`tally_time.py -v` の警告を消した。目安 1.5 分は変えていない。
7. **1 章を決定問題からの動機付けに組み替え**（ユーザーの指摘：道具を減らす理由が不透明だった）
   - 冒頭はタイトル → 今日作るもの → 時間割だけにし、「lambda と関数呼び出しだけで書く」を 1 章の最後へ移した。
   - 1 章は、決定問題（判定する手順がないと示すには手順を数学的に定義する必要がある）→ 同値性の定理と Church–Turing thesis → lambda と関数呼び出しだけで書く、の順。
   - 「Python の道具を減らしていく」は、理由なしに問いを置いていたので削除した。
   - 参考文献に Church 1936「A Note on the Entscheidungsproblem」（DOI 10.2307/2269326）と Hilbert–Ackermann 1928（初版に DOI がないのでリンクなし、CiNii で書誌を確認）を足した。参考文献 2 枚は `.refs` クラスで行間を詰めた（`theme/quiet.css`）。
   - 時間：冒頭 2.25 → 1.25 分、1 章 2.5 → 3.5 分で、必須 46.5 分は変わらない。
8. **thesis スライドの結びと「講義」の表現**
   - 「決定問題を判定する機械的な手順はない」という結論を、thesis スライドの締めの段落から thesis の箇条書きの中へ移した（締めに置くと、次のスライドでその続きが来ると期待させるため）。
   - 「講義」という語をスライド・ノートブック・Makefile・CSS・CLAUDE.md から外し、CLAUDE.md の文体の基準に「講義という体にしない」を足した。
9. **ページ内リンクをスライド単位に**
   - 章の中の特定のスライドを指す 14 か所を、見出しの先頭の空の span に付けた id（`strict-eval`、`not-and`、`thunk`、`church-num`、`add`、`fact-gen`、`y-strict`、`z-comb`、`fib`、`ski`）へのリンクに変えた。時間割の表は `#chN` のまま。
   - ノートブックの「（スライド：「…」）」と見出しの一致を検査するテスト `test_slide_references_match_titles` を足した（見出しは HTML タグを除いて比べる）。

未コミットの変更はない。

## ユーザーの判断待ち

なし。η展開の併記を 6 章に戻すこと、右畳み込みの英語名を 7 章の見出しに移すことは、どちらもしないと決まった。

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
  - この環境には Chrome が入っておらず、`/tmp/penrose-playwright-browsers/chromium-1248/chrome-linux64/chrome` を `CHROME_PATH` に指定して使った（/tmp なので消えることがある）。marp-cli で使うときは「No usable sandbox」になるので、`--no-sandbox` を付けるラッパーを `--browser-path` に渡す。
  - 見た目は `make png` で確かめる。1 枚だけなら marp-cli の `--images png` を一時ディレクトリに出す。
- **PDF の内部リンク**：`make pdf` の後に pypdf で確かめる。各ページの注釈の `/Dest` が、すべて `named_destinations` に存在すればよい（章扉の `/ch1`〜`/ch9` と、スライドに付けた id）。
  ```sh
  uv run --no-project --with pypdf python -c "import pypdf; r=pypdf.PdfReader('out/lambda.pdf'); nd=set(r.named_destinations); ds={a.get_object().get('/Dest') for p in r.pages for a in (p.get('/Annots') or []) if a.get_object().get('/Dest')}; print(sorted(nd)); print('missing:', sorted(d for d in ds if d not in nd))"
  ```
- **PDF のフォント**：`pdffonts out/lambda.pdf` で Noto 系が埋め込まれていることを見る。罫線が DejaVu に化けていないか（7 章のリストの図）も見る。
- **デプロイ**：push 後、`gh run list --workflow pages.yml --limit 1` で run を探し、`gh run watch <id> --exit-status` で結果を待つ。
