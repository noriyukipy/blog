# GPUサーバの新調

GPUを使った学習でのGPUメモリ不足を解消するためにGPUサーバを新調した。

予算は30万円で次のスペックを持つものを探した。
- GPU RTX 2080Ti
- メモリ 32GB

結果、ツクモのBTOパソコン[G-GEAR GA7J-F194/T](https://www.tsukumo.co.jp/bto/pc/game/2019/GA7J-F194T.html)を購入した。
他社と比較してツクモのBTOは価格を低く抑えながらも、「ASUS PRIME H370-A (ATX)」のようにスペック表からマザーボードのメーカがわかるのがいい。

## OSインストール

OSはUbuntu Server 18.04.3 LTSをインストールする。

### インストールメディアの作成

MacOSでUbuntuのインストーラを作成する。
Ubuntu Server 18.04.3 LTSを https://ubuntu.com/download/server からダウンロードしてから、次のコマンドで作成する。

```
$ diskutil unmountDisk /dev/disk2
Unmount of all volumes on disk2 was successful
$ sudo dd if=./ubuntu-18.04.3-live-server-amd64.iso of=/dev/rdisk2 bs=1m
Password:
848+0 records in
848+0 records out
889192448 bytes transferred in 33.384081 secs (26635223 bytes/sec)
```

### インストール

インストーラメディアからインストーラを起動して設定していく。

- Language
  - English
- Keyboard configuration
  - Layout: Japanese
  - Variant: Japanese
- Network connections
  - Subnet: 192.168.0.0/24
  - Address: 192.168.0.3
  - Gateway: 192.168.0.1
  - Name servers: 192.168.0.1
  - Search domains: なし
- Configure proxy
  - 設定しない
- Configure Ubuntu archive mirror
  - http://jp.archive.ubuntu.com/ubuntu （デフォルトで設定されているものをそのまま使う）
- Filesystem setup
  - Use entire disk
  - 使うディスクを選択する
  - File system summary
    - / ext4
    - /boot/efi fat32
- Profile setup
  - Your name: xxxx
  - Your server’s name: xxxx
  - Pick a username: xxxx
- SSH Setup
  - Install OpenSSH server にチェック
- Featured Server Snaps
  - 何もインストールしない
- Rebootする

## 設定

Ansibleで必要な設定を行う。

**サーバ上で** Ansibleをインストールする。

```sh
$ sudo apt install ansible
```

ローカルから公開鍵をコピーする。

```sh
$ ssh-copy-id -i /path/to/your_public_key 192.168.0.3
```

ローカルからAnsible Playbookを実行してDockerとGPU関連の設定を行う。

```sh
$ git clone https://github.com/noriyukipy/gpu_server_setup
$ cd gpu_server_setup
```

inventory.ini を自分の環境設定に書き換えた上でPlaybookを実行する。

```
$ ansible -i inventory.ini all -m ping
192.168.0.3 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
$ ansible-playbook -i inventory.ini main.yml --become --ask-become-pass
```
