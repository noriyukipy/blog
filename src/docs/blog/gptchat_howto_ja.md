# 2020/01/13 - 最新のニューラル会話モデルでおしゃべりしよう！ - GPT-2でチャットボット作成

記事作成日 2020/01/13, 記事更新日 2020/04/29

## 概要

- [GPTChat](https://github.com/noriyukipy/gptchat) という、日本語向けの GPT-2 言語モデル、およびそれをベースとした会話モデルの学習・生成 CLI を作成しました。
- GPTChat を使って日本語 Wikipedia で GPT-2 を学習し、ファインチューニングして日本語の会話モデルを作成しました。

## あらすじ

2018-2019 年は [GPT](https://openai.com/blog/language-unsupervised/) とその後継である [GPT-2](https://openai.com/blog/better-language-models/) が話題になりました。
GPT および GPT-2は、大規模なウェブテキストから事前学習した言語モデルで、特定のタスクにファインチューニングすることで多くのベンチマークタスクでSOTAを達成しました。

では、GPT や GPT-2 をチャットボット向けにファインチューニングすることは可能でしょうか？
チャットボットへの適用手法は [1] で提案されており、2018年に開催された[ConvAI2](http://convai.io/)という対話コンペティションの自動評価部門にて一位に輝いています。
この手法に興味がある方は、 [1] の他に著者本人が解説した [2] があるので合わせて参照してください。

- [1] *TransferTransfo: A Transfer Learning Approach for Neural Network Based Conversational Agents* by Thomas Wolf et al. ([https://arxiv.org/abs/1901.08149](https://arxiv.org/abs/1901.08149))
- [2] *How to build a State-of-the-Art Conversational AI with Transfer Learning* by Thomas Wolf. ([https://medium.com/huggingface/how-to-build-a-state-of-the-art-conversational-ai-with-transfer-learning-2d818ac26313](https://medium.com/huggingface/how-to-build-a-state-of-the-art-conversational-ai-with-transfer-learning-2d818ac26313))

こうなってくると、日本語のチャットボットを作成できないかと期待しますね！
しかし、GPT-2を使って日本語でチャットボットを作ろうとした時、立ちはだかる壁があります。

一つ目は、GPT-2の公開されている事前学習モデルは英語を中心に学習されていることです。
GPT-2は事前学習モデルをファインチューニングしてタスクを解きます。
例えばチャットボットを作ろうとすると、GPT-2の事前学習モデルを「入力発話」から「応答発話」を生成するようにファインチューニングするわけです。
そのファインチューニングに必要な GPT-2 の事前学習モデルは公開されているのですが、英語を中心に学習されているため日本語には適していません。
そのため、日本語用の GPT-2 の事前学習モデルを作成する必要があります。

二つ目は、トークナイザの問題です。
GPT-2 のトークナイザは、入力文をスペース単位で単語に分割し、単語にバイト単位で多く共通する部分をまとめてトークンとして表現する Byte Pair Encoding という手法を用います。
この手法で学習したトークナイザの事前学習モデルは提供されいるのですが、こちらも英語を主に学習されているため日本語には不向きです。
後ほど改めて紹介する [🤗 Transformers](https://github.com/huggingface/transformers) が提供している学習済みトークナイザで日本語をトークナイズすると次のようになります。

```sh
>>> import transformers
>>> tokenizer = transformers.GPT2Tokenizer.from_pretrained("gpt2")
>>> tokenizer.tokenize("お腹が空いた")
['ãģ', 'Ĭ', 'è', 'ħ', '¹', 'ãģĮ', 'ç', '©', 'º', 'ãģĦ', 'ãģŁ']
```

日本語はスペースで単語が分けられていないため、トークナイザは文「お腹が空いた」を一単語として認識し、その後あらかじめ学習しておいたトークン単位に分割しています。
バイト単位での分割のため、入力した文字数よりも多くのトークンが出現していることもわかります。

このような観点から、GPT-2 を日本語で使おうとしたとき、

1. 日本語用のトークナイザに変更する
2. その上で、GPT-2 を事前学習する

必要があります。

以上を踏まえて、 [GPTChat](https://github.com/noriyukipy/gptchat) という GPT-2 の学習・生成 CLI を作成しました。
GPTChatではトークナイザを日本語向けに変更をした上で、GPT-2 の事前学習モデルの学習スクリプトと、[1] [2] を元にした手法で GPT-2 の事前学習モデルをチャットボット向けにファインチューニングする学習スクリプトを提供しています。

まず、GPTChat の GPT-2 モデルは、先ほどトークナイザの実例で使った HuggingFaceの [🤗 Transformers](https://github.com/huggingface/transformers) を使っています。

次にトークナイザは、GPT-2 のデフォルトのトークナイザ `transformers.GPT2Tokenizer` ではなく、BERT 用の日本語向けのトークナイザ `transformers.BertJapaneseTokenizer` とその学習済みモデルを用いています。
`transformers.BertJapaneseTokenizer` は transformers に [v2.3.0](https://github.com/huggingface/transformers/releases/tag/v2.3.0) より導入されたトークナイザで、東北大学により公開されていたものがマージされました。
詳しくは次を参照ください。

- [https://www.nlp.ecei.tohoku.ac.jp/news-release/3284/](https://www.nlp.ecei.tohoku.ac.jp/news-release/3284/)
- [https://github.com/cl-tohoku/bert-japanese](https://github.com/cl-tohoku/bert-japanese)

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">おはようござえます、日本の友達<br><br>Hello, Friends from Japan 🇯🇵! <br><br>Thanks to <a href="https://twitter.com/NlpTohoku?ref_src=twsrc%5Etfw">@NlpTohoku</a>, we now have a state-of-the-art Japanese language model in Transformers, `bert-base-japanese`.<br><br>Can you guess what the model outputs in the masked LM task below? <a href="https://t.co/XIBUu7wrex">pic.twitter.com/XIBUu7wrex</a></p>&mdash; Hugging Face (@huggingface) <a href="https://twitter.com/huggingface/status/1205283603128758277?ref_src=twsrc%5Etfw">December 13, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

`transformers.BertJapaneseTokenizer` は、[GitHubのリポジトリ](https://github.com/cl-tohoku/bert-japanese)によると、文を MeCab で分かち書きしたのち、SentencePieceの Byte Pair Encoding によってトークナイズを行います。
実際に使って挙動を確かめてみましょう。

```sh
>>> import transformers
>>> tokenizer = transformers.BertJapaneseTokenizer.from_pretrained("bert-base-japanese")
>>> tokenizer.tokenize("お腹が空いた")
['お', '##腹', 'が', '空い', 'た']
```

結果をみると、まず MeCab で「お腹」「が」「空い」「た」と分割され、その後 Byte Pari Encoding で「お」「##腹」「が」「空い」「た」と分割されたことが見えますね。

最後に、GPTChat の会話モデルは [1] [2] を参考に、一問一答型の会話を行うモデルとして実装しました。
[1] [2] では、対話に個性や履歴を考慮していますが、GPTChatでは個性や履歴は考慮せずシンプルに一問一答を行う会話を対象とします。

以上で、GPTChat を作成したあらすじと概略は終わりです！
この後は、 GPTChat の使い方を説明します。
今回は日本語 Wikipedia で GPT-2 を学習して事前学習モデルを作成したのち、そのモデルをチャットボット向けにファインチューニングして実際に会話するところまで行ってみたいと思います。

## GPTChatのインストール

Docker イメージをビルドするのが簡単です。

```sh
$ git clone -b v0.1.2 https://github.com/noriyukipy/gptchat
$ cd gptchat
$ docker image build -t gptchat .
```

ソースからインストールすることも可能です。
この場合は、必要な環境設定を [Dockerfile](https://github.com/noriyukipy/gptchat/blob/v0.1.1/Dockerfile) で確認してください。

```sh
$ pip install git+https://github.com/noriyukipy/gptchat
```

## GPT-2 モデル

### 学習データの作成

はじめに、日本語 Wikipedia のダンプデータをダウンロードして学習データとして使えるように整形します。

```sh
$ mkdir corpus
$ cat 20191201/jawiki-20191201-pages-articles.txt | grep -v doc | perl -wlp -e 's/。/。\n/g' | perl -wln -e '/^$/ or print'  >corpus/raw.txt
$ head -n100000 corpus/raw.txt >corpus/val.txt
$ head -n200000 corpus/raw.txt | tail -n+100001 >corpus/test.txt
$ tail -n+200001 corpus/raw.txt >corpus/train.txt
```

### GPT-2 モデルの学習

それでは `gptchat.gpt.train` を使って BaseModel の GPT-2 を学習してみましょう。


```sh
$ docker container run --gpus all --rm -d -v $(pwd):/work gptchat python -m gptchat.gpt.train --output_dir=output --data=corpus/train.txt --tokenizer_model=bert-base-japanese --num_epochs=10 --batch_size=2 --checkpoint_steps=50000 --seed=0 --shuffle=True --gpu
```

`--tokenizer_model=bert-base-japanese` というパラメータを指定していることに注意してください。
`bert-base-japanese` を指定することで `transformers.BertJapaneseTokenizer` を利用します。
日本語モデルを学習する場合は指定するようにしてください。

`--data` で先ほど作成した学習データを指定しましょう。

`--gpu` オプションで学習に GPU を利用するように設定しています。
今回は学習には RTX 2080 Ti を用いました。
学習中はだいたい 10GB 程度 GPU メモリを使用していることがわかります。

```sh
$ nvidia-smi
Wed Jan  8 15:00:06 2020
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.33.01    Driver Version: 440.33.01    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 208...  On   | 00000000:01:00.0 Off |                  N/A |
| 69%   82C    P2   249W / 250W |  10411MiB / 11019MiB |     99%      Default |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0     24986      C   python                                     10399MiB |
+-----------------------------------------------------------------------------+
```

`--checkpoint_steps` ごとに、 `--output_dir` 以下にモデルが保存されます。

```sh
$ tree output
output
├── step_0
│   ├── added_tokens.json
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── vocab.txt
└── step_50000-epoch_1-batch_50000
    ├── added_tokens.json
    ├── config.json
    ├── pytorch_model.bin
    ├── special_tokens_map.json
    ├── tokenizer_config.json
    └── vocab.txt
```

モデルのパラメータを確認したい場合は、各モデルのディレクトリ以下の `config.json` を確認してください。

### モデルの評価

学習したモデルに対して `gptchat.gpt.evaluate` を使ってテストセットに対してパープレキシティを計算できます。
70万ステップ後の学習モデルをテストセット `corpus/test.txt` で評価してみましょう。

```sh
$ docker container run --gpus all --rm -it -v $(pwd):/work gptchat python -m gptchat.gpt.evaluate --model=output/step_700000-epoch_3-batch_89716 --data=corpus/test.txt --batch_size=2 --gpu
Perplexity 18.0370
```

### 文生成

文を生成するには `gpchat.gpt.generate` を用います。

```sh
$ docker container run --rm -it -v $(pwd):/work gptchat python -m gptchat.gpt.generate --model=output/step_700000-epoch_3-batch_89716
>>> 奈良時代には
奈良 時代 に は 実在 し た 。 「 埴生 の 説 」 や 「 プルースト の 説 」 の よう な 記述 が み られる 。 初期 王朝 ( 13 世紀
>>> 車社会では
車 社会 で は 、 車両 の 性能 向上 の ため 、 頻繁 に 動力 車 を する 場合 が ある 。 たとえば 、 フォード ・ X 1 と の 交差点 の 際 の
```

Wikipediaにのっているような文章が生成されていますね！

## 会話モデル

GPT-2 の事前学習モデルができたので、次はそれをファインチューニングして会話モデルを学習してみましょう。

GPT-2 を対話モデルとして使うためには、「入力発話」と「応答発話」の間にセパレータを入れてモデルに入力します。

|           | 1       | 2       | 3       | 4       | 5       | 6       | 7      | 8   | 9 |
| ---       | ---     | ---     | ---     | ---     | ---     | ---     | ---    | --- | --- |
| 単語     | \<bos\>  | 餃子    | が      | 食べ    | たい    | \<sep\> | 美味し | そう   | \<eos\> |

そして学習時には「応答発話」の言語モデルを学習するようにします。

それに加えて、 [1] [2] での手法にならい、生成した応答発話が応答として適切かどうか分類するタスクも同時に学習します。
一単語ごとに生成してできた文が全体として応答発話に適切かどうかを判定しようというわけです。
この学習を行うために、学習データには事前に distractor と呼ばれる入力発話に対して適切でない応答発話を複数個付与しておき、学習時に分類します。

### 学習データの準備

用意する学習データセットは入力発話と応答発話をタブで区切ったデータです。
このデータは各自準備してください。
今回は、70万ペア程度の会話データを学習に用いました。

このデータを `chat/train.txt` として用意します。

```sh
$ head -n1 chat/train.txt
何が食べたい？      餃子が食べたいです。
```

このデータに対して、 `gptchat.chat.add_distructors` で distractor を付与します。

```sh
$ cat chat/train.txt | python -m gptchat.chat.add_distractors --num_distractors=2 >chat/train_dist.txt
```

すると、応答発話の後にタブ区切りで `--num_distractors` で指定した数の distractor が付与されます。
distractor は応答発話中からランダムで `--num_distractors` 個選ばれます。
今回は `--num_distractors=2` と指定しているので、二つの発話が新たに付与されているのがわかります。

```sh
$ head -n1 chat/train_dist.txt
何が食べたい？      餃子が食べたいです。    おはよう〜   勉強中です。
```

### 会話モデルの学習

データの準備ができたら、 `gptchat.chat.train` で学習します。

```sh
$ docker container run --gpus all -d -v $(pwd):/work gptchat python -m gptchat.chat.train --output_dir=chat_output --model=output/step_700000-epoch_3-batch_89716 --data=chat/train_dist.txt --batch_size=16 --num_distructors=2 --checkpoint_steps=50000 --num_epochs=10 --gpu
```

先ほど学習した GPT-2 の事前学習モデルを `--model` で指定してください。
BaseModel と同様に、 `--checkpoint_steps` ステップごとにモデルが`--output_dir` 以下に保存されます。

### 応答生成

学習が完了したら、 `gpchat.chat.generate` で応答生成してみましょう。
`--model` に学習したモデルを指定します。
今回は35万ステップ後の学習モデルを利用します。

```sh
$ docker container run --rm -it -v $(pwd):/work gptchat python -m gptchat.chat.generate --model=chat_output/step_350000-epoch_10-batch_12500
>>> おはよう
<bos> おはよう <sep> おはよう ござい ます ー! <eos>
>>> お腹減った
<bos> お腹 減っ た <sep> ご飯 か! <eos>
>>> 一緒に食べる？
<bos> 一緒 に 食べる? <sep> とっくに 食べ て まし た! <eos>
```

おおおー！いい感じですね！

APIとして利用するために、HTTP サーバとして提供するための `gptchat.chat.serve` も用意しています。

```sh
$ docker container run --rm -it -v $(pwd):/work -p 8080:8080 gptchat python -m gptchat.chat.serve --address=0.0.0.0 --port=8080 --model=chat_output/step_350000-epoch_10-batch_12500
```

`/generate` エンドポイントに対して `{"text": "こんにちは"}` のようにリクエストを送るとレスポンスとしてモデルの出力が得られます。

```sh
$ curl localhost:8080/generate -d '{"text": "元気？"}' -H "content-type:application/json" | jq
{
  "text": "元気？",
  "model_output": "<bos> 元気? <sep> 元気 だ よー!!! <eos>",
  "reply": "元気だよー!!!"
}

```

## まとめ

- 日本語向けの GPT-2 の言語モデルおよび会話モデルの学習・生成 CLI である GPTChat を作成しました。
- GPTChat を日本語 Wikipedia で事前学習し、ファインチューニングすることで日本語の会話モデルが作成できることを確認しました。
