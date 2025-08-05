import socket
import ipaddress
import os

import random

COOL = 2009
HOT  = 2010

Floor = 0
Enemy = 1
Block = 2
Item  = 3

UpLeft = 0
Up = 1
UpRight = 2
Left = 3
Center = 4
Right = 5
DownLeft = 6
Down = 7
DownRight = 8

UL = UpLeft
U  = Up
UR = UpRight
L  = Left
C  = Center
R  = Right
DL = DownLeft
D  = Down
DR = DownRight

F = Floor
E = Enemy
B = Block
I = Item

class Client:
    def __init__(self):
        self.port = input('ポート番号を入力してください ⇒ ')
        self.name = input('名前を入力してください ⇒ ')
        if input('ローカルに接続しますか？(y/n)') == 'y':
            self.host = '127.0.0.1'
        else:
            self.host = input('IPアドレスを入力してください ⇒ ')

        if not self.__ip_judge(self.host):
            os._exit(1)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        while True:
            try:
                self.client.connect((self.host, int(self.port)))
            except ConnectionRefusedError:
                if not self.connected:
                    self.connected = True
                    print('サーバーが起動していません')
                continue
            break

        print("port:", self.port)
        print("name:", self.name)
        print("host:", self.host)

        self.__str_send(self.name + "\r\n")

    def __ip_judge(self, host):
        try:
            ipaddress.ip_address(host)
        except Exception as e:
            print("IPアドレスの形式に誤りがあります : {0}".format(e))
            return False
        else:
            return True

    def __str_send(self, send_str):
        try:
            self.client.sendall(send_str.encode("utf-8"))
        except OSError:
            print("send error:{0}\0".format(send_str))

    def __order(self, order_str, gr_flag = False):
        try:
            if gr_flag:
                responce = self.client.recv(4096)

                if b"@" in responce:
                    pass # Connection completed.
                else:
                    print("Connection failed.")

            self.__str_send(order_str + "\r\n")

            responce = self.client.recv(4096)[0:11].decode("utf-8")

            if not gr_flag:
                self.__str_send("#\r\n")

            if responce[0] == "1":
                return [int(x) for x in responce[1:10]]
            elif responce[0] == "0":
                self.box()
                raise OSError("Game Set!")
            else:
                print("responce[0] = {0} : Response error.".format(responce[0]))
                raise OSError("Responce Error")

        except OSError as e:
            print(e)
            self.client.close()
            os._exit(0)

    def get_ready(self):
        return self.__order("gr", True)

    def walk_right(self):
        return self.__order("wr")

    def walk_up(self):
        return self.__order("wu")

    def walk_left(self):
        return self.__order("wl")

    def walk_down(self):
        return self.__order("wd")

    def look_right(self):
        return self.__order("lr")

    def look_up(self):
        return self.__order("lu")

    def look_left(self):
        return self.__order("ll")

    def look_down(self):
        return self.__order("ld")

    def search_right(self):
        return self.__order("sr")

    def search_up(self):
        return self.__order("su")

    def search_left(self):
        return self.__order("sl")

    def search_down(self):
        return self.__order("sd")

    def put_right(self):
        return self.__order("pr")

    def put_up(self):
        return self.__order("pu")

    def put_left(self):
        return self.__order("pl")

    def put_down(self):
        return self.__order("pd")
    
    ### action ###

    # 指定方向に移動
    def walk(self, direction):
        action = {
            Up    : self.walk_up,
            Down  : self.walk_down,
            Right : self.walk_right,
            Left  : self.walk_left
        }
        return action[direction]()

    # 指定方向を近隣探査
    def look(self, direction):
        action = {
            Up    : self.look_up,
            Down  : self.look_down,
            Right : self.look_right,
            Left  : self.look_left
        }
        return action[direction]()

    # 指定方向を遠方探査
    def search(self, direction):
        action = {
            Up    : self.search_up,
            Down  : self.search_down,
            Right : self.search_right,
            Left  : self.search_left
        }
        return action[direction]()
    
    # 指定方向に設置
    def put(self, direction):        
        action = {
            Up    : self.put_up,
            Down  : self.put_down,
            Right : self.put_right,
            Left  : self.put_left
        }
        return action[direction]()
    
    ### direction ###

    # 指定方向の反対方向
    def backward(self, direction):
        backward = {
            Up    : Down,
            Down  : Up,
            Right : Left,
            Left  : Right
        }
        return backward[direction]

    # 指定方向の右方向
    def rightward(self, direction):
        rightward = {
            Up    : Right,
            Down  : Left,
            Right : Down,
            Left  : Up
        }
        return rightward[direction]

    # 指定方向の左方向
    def leftward(self, direction):
        leftward = {
            Up    : Left,
            Down  : Right,
            Right : Up,
            Left  : Down
        }
        return leftward[direction]

    # 指定方向の右前方向
    def forwardRight(self, direction):
        forwardRight = {
            Up    : UpRight,
            Down  : DownLeft,
            Right : DownRight,
            Left  : UpLeft
        }
        return forwardRight[direction]

    # 指定方向の左前方向
    def fowardLeft(self, direction):
        fowardLeft = {
            Up    : UpLeft,
            Down  : DownRight,
            Right : UpRight,
            Left  : DownLeft
        }
        return fowardLeft[direction]

    # 指定方向の右後方向
    def backRight(self, direction):
        backRight = {
            Up    : DownRight,
            Down  : UpLeft,
            Right : DownLeft,
            Left  : UpRight
        }
        return backRight[direction]

    # 指定方向の左前方向
    def backLeft(self, direction):
        backLeft = {
            Up    : DownLeft,
            Down  : UpRight,
            Right : UpLeft,
            Left  : DownRight
        }
        return backLeft[direction]


    # ブロックのない方向にランダム移動
    def randomWalk(self, map_info, direction = None):
        # 可能な移動のリスト
        legalMove  = []
        
        # 上下左右のブロックを確認
        for dir in [Up, Down, Left, Right]:
            # 移動方向にブロックなし & 後退じゃない
            if map_info[dir] != Block and direction != self.backward(dir):
                legalMove.append(dir) # 移動方向を追加

        if len(legalMove) > 0:
            # 移動可能な中からランダムに選択
            selectedMove = random.choice(legalMove)
        else:
            # 迂回できないときは後退を選択
            selectedMove = self.backward(direction)

        # 選んだ方向に移動
        return self.walk(selectedMove), selectedMove


    # ブロックを避けて指定方向に移動
    def safetyWalk(self, map_info, direction):
        # 指定方向にブロックがなければそのまま移動
        if map_info[direction] != Block:
            selectedMove = direction
        else:
            # 指定方向にブロックがある時は左右に迂回
            # 可能な移動のリスト
            legalMove  = []
            for dir in [self.rightward(direction), self.leftward(direction)]:
                # 移動方向にブロックなし
                if map_info[dir] != Block:
                    # 移動方向を追加
                    legalMove.append(dir) 

            if len(legalMove) > 0:
                # 左右に迂回可能ならランダムに選択
                selectedMove = random.choice(legalMove)
            else:
                # 迂回できないときは後退を選択
                selectedMove = self.backward(direction)
                
        # 選んだ方向に移動
        return self.walk(selectedMove), selectedMove

    # 壁沿いに移動
    def alongRightHandWalk(self, map_info, direction):
        # 右、指定方向、左、後ろの順にブロックがなければ移動
        if map_info[self.rightward(direction)] != Block and map_info[self.backRight(direction)] == Block:
            selectedMove = self.rightward(direction)
        elif map_info[direction] != Block:
            selectedMove = direction
        elif map_info[self.rightward(direction)] != Block:
            selectedMove = self.rightward(direction)
        elif map_info[self.leftward(direction)] != Block:
            selectedMove = self.leftward(direction)
        else:
            selectedMove = self.backward(direction)
                
        # 選んだ方向に移動
        return self.walk(selectedMove), selectedMove