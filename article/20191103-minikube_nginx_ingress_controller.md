# minikube で nginx ingress controller の設定

minikube の nginx ingress controller の設定を調査したので参照先とともに方法を書きます。

## アドオンの有効化

minikube で ingress addon を有効にする

    $ minikube addons enable ingress

## Ingress controller の設定ファイルの確認

Ingress controller の nginx の設定には [ConfigMap を使う](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/)。
そのために、まずは ingress contoller がどの ConfigMap を参照しているか確認する。

nginx ingress controller のポッド名を確認する。

    $ kubectl -n kube-system get pod  | grep nginx
    nginx-ingress-controller-57bf9855c8-9kbhc   1/1     Running   0          86m

ポッドの設定を確認することで、参照している ConfigMap を調べる。

    $ kubectl -n kube-system get pod nginx-ingress-controller-57bf9855c8-9kbhc -o yaml | grep configmap
        - --configmap=$(POD_NAMESPACE)/nginx-load-balancer-conf
        - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
        - --udp-services-configmap=$(POD_NAMESPACE)/udp-services

`--configmap=$(POD_NAMESPACE)/nginx-load-balancer-conf` で指定されている ConfigMap に設定が記述されている。

## 設定

[ConfigMap で設定できるオプション](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/) に従って設定する。

[](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/)例えば、 `server_tokens` を設定したければ次のように ConfigMap に `server_tokens` の設定を追加する。

    # nginx-lb-conf.yml
    apiVersion: v1
    data:
      # Minikube default parameters
      hsts: "false"
      map-hash-bucket-size: "128"
      # Set your custom parameters below
      server-tokens: "false"
    kind: ConfigMap
    metadata:
      name: nginx-load-balancer-conf

  `metadata.name` には先ほど調べた ConfigMap の名前を設定すること。

## 設定の反映

作成した ConfigMap を apply する。

    $ kubectl -n kube-system apply -f nginx-lb-conf.yml

[ConfigMap を apply すると nginx ingress controller も再起動して設定が反映される](https://kubernetes.github.io/ingress-nginx/examples/customization/custom-configuration/)。
ingress controller のログを見て設定が反映されたことを確認する

    $ stern -n kube-system nginx
    ...
    nginx-ingress-controller-57bf9855c8-9kbhc nginx-ingress-controller I1102 01:43:29.052643       6 controller.go:133] Configuration changes detected, backend reload required.
    nginx-ingress-controller-57bf9855c8-9kbhc nginx-ingress-controller I1102 01:43:29.055002       6 event.go:258] Event(v1.ObjectReference{Kind:"ConfigMap", Namespace:"kube-system", Name:"nginx-load-balancer-conf", UID:"a86f84b8-d227-4806-a5a6-263f27fe02d3", APIVersion:"v1", ResourceVersion:"298106", FieldPath:""}): type: 'Normal' reason: 'UPDATE' ConfigMap kube-system/nginx-load-balancer-conf
    nginx-ingress-controller-57bf9855c8-9kbhc nginx-ingress-controller I1102 01:43:29.150700       6 controller.go:149] Backend successfully reloaded.

オプション名や設定値が誤っている場合はこのログにリロードに失敗したことが出るので、対応すること。

## 参考

記事の中で参照しているページ

- https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/
- https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/
- https://kubernetes.github.io/ingress-nginx/examples/customization/custom-configuration/

パラメータごとの設定コード。例えば `server-tokens` は次のコードになる

- https://github.com/kubernetes/ingress-nginx/blob/master/test/e2e/settings/server_tokens.go

