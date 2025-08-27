import argparse
from lib.CHaser import * # lib/CHaser.py

"""
【ライブラリの配置方法】
    同じフォルダ内に「lib」フォルダを作成し、その中に「CHaser.py」ファイルを配置してください。

【サーバーとの接続方法】
    Client クラスの引数に port, name, host を指定します。
    指定しない場合は、実行時に入力を求められます。
    例： player = Client(2010, "Cool", "localhost")

    プログラムの末尾にある以下の記述により、コマンドライン引数を使って接続情報を指定できます。

        parser.add_argument('-p', '--port', default=2010)
        parser.add_argument('-n', '--name', default='sample')
        parser.add_argument('-i', '--host', default='localhost')

    default の値を変更することで、引数を省略した場合に使用される初期値を変更できます。

    【使用例】

        python sample.py -p 2010 -n Cool -i localhost
        python sample.py --port 2010 --name Cool --host localhost
        python sample.py -n Cool


【行動関数の記述形式】
    行動関数は「行動(方向)」の形式で記述します。
     行動は「walk」「look」「search」「put」の4種類
     方向は「Right」「Up」「Left」「Down」の4種類
    例： walk(Up), search(Right) など

【マスの情報】
    行動関数が返すマップ情報は、以下のいずれかの種類です。
    「Floor」:なしもない
    「Enemy」:相手
    「Block」:ブロック
    「Item」 :アイテム

【マップ情報の構造】
    行動関数は、行動後の周囲9マスの情報を以下の順番でリストとして返します。

    「UpLeft」  |  「Up」   |「UpRight」
    -----------+-----------+-----------
    「Left」    |「Center」 |  「Right」
    -----------+-----------+-----------
    「DownLeft」| 「Down」  |「DownRight」
"""

player = None
map_info = [] # 周辺情報を保存するリスト
look_info = [] # 近隣情報を保存するリスト
search_info = [] # 遠方情報を保存するリスト

def main(port, name, host):
    global player, map_info, look_info, search_info
    
    # サーバーと接続
    player = Client(port=port, name=name, host=host)

    while True:
        # ターン１
        # 準備完了
        player.get_ready()
        # 左遠方探査
        player.search(Left)

        # ターン２
        # 準備完了 & 自己周辺探査
        map_info = player.get_ready()
        # 下がブロックでなければ
        if map_info[Down] != Block:
            # 下移動
            player.walk(Down)
        else:
            # 上設置
            player.put(Up)

        # ターン３
        # 準備完了
        player.get_ready()
        # 上近隣探査
        player.look(Up)

        # ターン４
        # 準備完了
        player.get_ready()
        # 右設置
        player.put(Right)




"""
python sample.py のようにこのファイルを直接実行すると，
__name__ は "__main__" となる．これを利用して main() を実行する．
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=2010)
    parser.add_argument('-n', '--name', default='sample')
    parser.add_argument('-i', '--host', default='localhost')
    
    args = parser.parse_args()

    main(port=args.port, name=args.name, host=args.host)