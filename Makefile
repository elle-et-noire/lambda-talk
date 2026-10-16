# 講義スライド「Lambda Calculus in Python」のビルド
#   make html | pdf | pdf-notes | png | check | test | all | sample | webfonts | clean
# ブラウザを変えたいときは CHROME_PATH=/path/to/chrome make pdf

MARP    ?= npx --yes @marp-team/marp-cli@4.5.1
PY      ?= .venv/bin/python
SRC     := slides/lambda.md
SAMPLE  := slides/_sample.md
OUT     := out
DEPS    := $(SRC) theme/quiet.css theme/quiet-webfonts.css .marprc.yml

MARP_OPTS := --config-file .marprc.yml --no-stdin
ifneq ($(strip $(CHROME_PATH)),)
BROWSER_OPTS := --browser-path "$(CHROME_PATH)"
endif

.PHONY: all html pdf pdf-notes png check test time sample webfonts clean

all: check html pdf

html: $(OUT)/lambda.html
pdf: $(OUT)/lambda.pdf
pdf-notes: $(OUT)/lambda-notes.pdf

$(OUT)/lambda.html: $(DEPS)
	@mkdir -p $(OUT)
	$(MARP) $(MARP_OPTS) $(SRC) --html -o $@

$(OUT)/lambda.pdf: $(DEPS)
	@mkdir -p $(OUT)
	$(MARP) $(MARP_OPTS) $(BROWSER_OPTS) $(SRC) --pdf -o $@

$(OUT)/lambda-notes.pdf: $(DEPS)
	@mkdir -p $(OUT)
	$(MARP) $(MARP_OPTS) $(BROWSER_OPTS) $(SRC) --pdf --pdf-notes -o $@

png: $(DEPS)
	@rm -rf $(OUT)/png && mkdir -p $(OUT)/png
	$(MARP) $(MARP_OPTS) $(BROWSER_OPTS) $(SRC) --images png -o $(OUT)/png/lambda.png

check:
	$(PY) tools/check_slides.py $(SRC)

test:
	$(PY) -m pytest code/tests -q

# テーマ確認用：slides/_sample.md を out/sample/ に PNG で書き出す
sample: $(SAMPLE) theme/quiet.css .marprc.yml
	@rm -rf $(OUT)/sample && mkdir -p $(OUT)/sample
	$(MARP) $(MARP_OPTS) $(BROWSER_OPTS) $(SAMPLE) --images png -o $(OUT)/sample/sample.png

clean:
	rm -rf $(OUT)/lambda.html $(OUT)/lambda.pdf $(OUT)/lambda-notes.pdf $(OUT)/png $(OUT)/sample

# スピーカーノートの「目安 N 分」を集計（必須／標準／全部入り）
time:
	$(PY) tools/tally_time.py $(SRC)

# テーマの Web フォント定義 theme/quiet-webfonts.css を Google Fonts から作り直す
webfonts:
	$(PY) tools/gen_webfonts.py
