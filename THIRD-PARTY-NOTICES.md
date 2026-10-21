# 出典と第三者の権利表示

このリポジトリの skill が元にした資料と、そのライセンスの扱いを記す。各 skill の SKILL.md 末尾にある「出典」の節は、この一覧の要約である。

## japanese-refinement

| 出典 | 取り込んだもの | 取り込み方 | ライセンス |
|---|---|---|---|
| k16shikano の gist「日本語技術文書の文章規範」 https://gist.github.com/k16shikano/fd287c3133457c4fd8f5601d34aa817d | 文章規範の各節（段落と論証の構成、論証の厳密さ、読み手の負荷の管理、視点と語り、演出の抑制、LLM っぽい表現の禁止、翻訳調の比喩と擬人化の禁止、冗長の排除、見出しの付け方、読者への誠実さ） | 書籍原稿に固有の整形規則を除いて汎用化 | Unlicense |
| kotek-7/dotfiles の sanitize-artifacts https://github.com/kotek-7/dotfiles/blob/main/dot_agents/skills/sanitize-artifacts/SKILL.md | 「生成残渣の除去」「推敲時の点検」「出力の作法」の着想（依頼や会話を製造過程として扱い、その痕跡を成果物から除く考え方、記述の三分類、制約を断り書きではなく書き方に反映する考え方） | 着想のみ。表現と例は原典を参照せずに独立に書き起こした | 表記なし |
| nanaism/yomiyasu https://github.com/nanaism/yomiyasu | 比喩動詞と術語の直訳の語彙、話し言葉の範囲、擬人化の境界、言い換えで含みを残す規則、定型の導入と結び、数の宣言、「〜ためです」の切り出し、間を作るだけの読点、太字が表示されない書き方、補助動詞と形式名詞の表記 | 規則を参考にし、文面と例文はこの skill の粒度で書き起こした | MIT（Copyright (c) 2026 nanaism） |
| coji/natural-japanese https://github.com/coji/natural-japanese | 英語に訳し戻す判定、エンジニアの話し言葉と定着の判定基準、チャット応答の名残、先回りの打ち消し、動作の名詞化、条件の消えた結論、二重否定と条件の入れ子、同じ型の反復、演出語は削るだけにする規則 | 規則を参考にし、文面と例文はこの skill の粒度で書き起こした | MIT（Copyright (c) 2026 coji） |

## ライセンスの全文

出典ごとに、その出典が配布している LICENSE ファイルを原文のまま記す。

### nanaism/yomiyasu

https://github.com/nanaism/yomiyasu/blob/main/LICENSE

```
MIT License

Copyright (c) 2026 nanaism

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### coji/natural-japanese

https://github.com/coji/natural-japanese/blob/main/LICENSE

```
MIT License

Copyright (c) 2026 coji

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
