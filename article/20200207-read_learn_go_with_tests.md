# 2020/02/07 - 「Learn Go with Tests」を読んだ

最近仕事でも趣味でもGoを書く機会が多い。
Go を習得するために [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests/) という記事を読んだところとてもよく、Goをこれから学びはじめる方におすすめできる内容だったので紹介したい。

自分がGoを始めるにあたり読んだのは [A Tour of Go](https://tour.golang.org/) や [はじめてのGo言語](http://cuto.unirita.co.jp/gostudy/) 程度で、あとはGoの[公式ドキュメントサイト](https://golang.org/doc/)や各ライブラリのGoDocを読んで使い方を学んだ。
そんな中で、Goでテストの書き方を調べたときに出会ったのが今回紹介する [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests/) だ。

Learn Go with Tests では著者の今までの Go 導入経験を元に、Go の基本文法やアプリケーションの作り方を学んでいくのだが、面白いのがテスト駆動開発を初めから導入していることだ。
Go の機能を紹介する際は、テストを書きながら紹介した Go の機能が動いているのかを検証する形をとっている。
これによって、読者は Go 言語の機能と共にテスト駆動開発も習得できるようになっている。

テスト駆動開発にあたっては「Red-Green-Refactor」の流れを守りながらコーディングを進めていく。本文にしたがってコーディングを進めていくと、「Red-Green-Refactor」のリズムを自分の中に取り入れることができるだろう。

本文ではステップ「Red」を重要視する記述が多くでてくる。「Red」のステップでは

1. テストを書く
2. コンパイルを通す
3. テストが失敗することを確認する

という流れでコーディングを行うのだが、現実には面倒で 3. のステップをスキップしてしまう人も多いのだろう。
Learn Go with Test では、はじめの数章ではこれでもかということ「Red」をスキップしないように毎回注意書きが書かれているので、本文に従って進めていけば「Red」のステップも意識できるようになるだろう。
当然意味があるから「Red」のステップが存在しており、その意味を本文では

1. エラーが発生することを確認する（何もしていないテストではないことを確認する）
2. エラー発生時に意味のあるコメントを出力することを確認する

としている。1. はよく言われる内容なのだが、2. は自分にとって新しい知見だった。
たしかに今まで自分が書いたテストはエラー時のコメントがわかりにくく、テストコードを見にいくまでどんな原因でエラーが発生したかわからないことが多かったと反省した。

Learn Go with Tests では、現実的なアプリケーションのテストの書き方も学ぶことができる。
[Dependency Injection](https://quii.gitbook.io/learn-go-with-tests/go-fundamentals/dependency-injection) と [Mocking](https://quii.gitbook.io/learn-go-with-tests/go-fundamentals/mocking) では、標準出力へ値を表示するコマンドラインプログラムを通して副作用を伴うプログラムへのテスト手法である依存注入やモックといった方法を学ぶことができる。
さらに [後半の章](pplication/app-intro) では、テストを書きながらAPIサーバを構築する。
現実では Go を使って API サーバを構築することも多いと思うので、後半の章を読むことで現実の課題にすぐに取り入れる形でテスト手法を学ぶことができる内容になっている。

以上、簡単だが Learn Go with Tests の概要を紹介した。
他言語の経験がある方ならばはじめに読む解説としてもとてもお勧めできる内容となっている。
最後に、表紙にも採用されている [Red-Green-Refactor の Gopher](https://github.com/quii/learn-go-with-tests/blob/master/red-green-blue-gophers-smaller.png) がすごく可愛いのでぜひ一度見てもらうとよいかと思う。
疲れたときはこの Gopher たちを眺めて気合いを入れなおそう！