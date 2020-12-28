import socket

UP, LEFT, FRONT, RIGHT, BACK, DOWN = range(6)
dic = {'U': UP, 'D':DOWN, 'L':LEFT, 'F':FRONT, 'R':RIGHT, 'B':BACK}

class Cube:
    def __init__(self, cube):
        self.cube = []
        for i in range(6):
            self.cube.append([list(cube[i*9:i*9+9])[x:x+3] for x in range(0, 9, 3)])
    def rotate_opp(self, side):
        for i in range(3):
            self.rotate(side)
    def is_solved(self):
        for i in self.cube:
            if i[0] != i[1] or i[1] != i[2]:
                return False
            for j in i:
                if j.count(j[0]) != 3:
                    return False
        return True
    def rotate_one_side(self, side):
        new_list = []
        for i in range(3):
            new_list.append([self.cube[side][2-j][i] for j in range(3)])
        self.cube[side] = new_list
    def rotate_first_line(self, side):
        if side == UP:
            self.cube[FRONT][0], self.cube[LEFT][0], self.cube[BACK][0], self.cube[RIGHT][0] = self.cube[RIGHT][0], self.cube[FRONT][0], self.cube[LEFT][0], self.cube[BACK][0]
        elif side == LEFT:
            sides = list()
            sides.append([self.cube[UP][i][0] for i in range(3)])
            sides.append([self.cube[FRONT][i][0] for i in range(3)])
            sides.append([self.cube[DOWN][i][0] for i in range(3)])
            sides.append([self.cube[BACK][2-i][2] for i in range(3)])
            for i in range(3):
                self.cube[FRONT][i][0] = sides[0][i]
            for i in range(3):
                self.cube[DOWN][i][0] = sides[1][i]
            for i in range(3):
                self.cube[BACK][i][2] = sides[2][i]
            for i in range(3):
                self.cube[UP][i][0] = sides[3][i]
        elif side == FRONT:
            sides = list()
            sides.append(self.cube[UP][2])
            sides.append([self.cube[RIGHT][i][0] for i in range(3)])
            sides.append(self.cube[DOWN][0])
            sides.append([self.cube[LEFT][i][2] for i in range(3)])
            for i in range(3):
                self.cube[RIGHT][i][0] = sides[0][i]
            self.cube[DOWN][0] = sides[1][::-1]
            for i in range(3):
                self.cube[LEFT][i][2] = sides[2][i]
            self.cube[UP][2] = sides[3]
        elif side == RIGHT:
            sides = list()
            sides.append([self.cube[UP][2-i][2] for i in range(3)])
            sides.append([self.cube[BACK][i][0] for i in range(3)])
            sides.append([self.cube[DOWN][i][2] for i in range(3)])
            sides.append([self.cube[FRONT][i][2] for i in range(3)])
            for i in range(3):
                self.cube[BACK][i][0] = sides[0][i]
            for i in range(3):
                self.cube[DOWN][2-i][2] = sides[1][i]
            for i in range(3):
                self.cube[FRONT][i][2] = sides[2][i]
            for i in range(3):
                self.cube[UP][i][2] = sides[3][i]
        elif side == BACK:
            sides = list()
            sides.append(self.cube[UP][0])
            sides.append([self.cube[LEFT][i][0] for i in range(3)])
            sides.append(self.cube[DOWN][2][::-1])
            sides.append([self.cube[RIGHT][i][2] for i in range(3)])
            for i in range(3):
                self.cube[LEFT][i][0] = sides[0][i]
            self.cube[DOWN][2] = sides[1]
            for i in range(3):
                self.cube[RIGHT][i][2] = sides[2][i]
            self.cube[UP][0] = sides[3]
        else:
            self.cube[FRONT][2], self.cube[RIGHT][2], self.cube[BACK][2], self.cube[LEFT][2] = self.cube[LEFT][2], self.cube[FRONT][2], self.cube[RIGHT][2], self.cube[BACK][2]
    def print(self):
        for i in range(3):
            print(' ' * 15, self.cube[BACK][2-i][::-1])
        print()
        for i in range(3):
            print([self.cube[LEFT][2-j][i] for j in range(3)],
            [self.cube[UP][i][j] for j in range(3)],
            [self.cube[RIGHT][j][2-i] for j in range(3)])
        print()
        for i in range(3):
            print(' ' * 15, self.cube[FRONT][i])
        print()
        for i in range(3):
            print(' ' * 15, self.cube[DOWN][i])
        print('\n\n\n')
    def rotate(self, side):
        self.rotate_one_side(side)
        self.rotate_first_line(side)
    def solve(self, moves):
        curr = ''
        for j in moves:
            if j == "'":
                self.rotate(dic[curr])
                self.rotate(dic[curr])
            else:
                self.rotate(dic[j])
            curr = j

CONNECTION_INFO = ('challenges.cyber.org.il', 10505)

def get_startup_info(server_socket):
    data = ''
    while 'Send the correct line:' not in data:
        data += server_socket.recv(1024).decode()

    return data

def main():
    answer = ''

    server_socket = socket.socket()
    server_socket.connect(CONNECTION_INFO)
    
    while 'Wrong!' not in answer and 'MUCH' not in answer:
        data = get_startup_info(server_socket)
        
        # This is how you should talk with the server.
        # The data is printed to the screen and the user needs to input the answer manualy.
        # Feel free to use the manual version or implement your own.
        cube = Cube(data[data.index('Shuffled')+10:data.index('Options')-1])
        cube.print()
        tmp_cube = cube
        data = data[data.index('Options') + 9 : data.index('Send the correct line') - 2]
        data_list = [i[i.index(' ')+1:] for i in data.split('\n')]
        curr = ''
        for i in data_list:
            for j in i:
                if j == "'":
                    tmp_cube.rotate(dic[curr])
                    tmp_cube.rotate(dic[curr])
                else:
                    tmp_cube.rotate(dic[j])
                curr = j
            if tmp_cube.is_solved():
                tmp_cube.print()
                print(data_list.index(i), i)
                line_number = str(data_list.index(i) + 1).encode()
            tmp_cube.print()
            tmp_cube = cube
        #
        line_number = b'1'

        server_socket.send(line_number)

        answer = server_socket.recv(100).decode()
        print(answer)


if __name__ == '__main__':
    #main()
    #c = Cube('y'*9+'r'*9+'g'*9+'o'*9+'b'*9+'w'*9)
    #c.print()
    c = Cube('wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby')
    c.print()
    s = "L', F, B2, R', B, R', L, B, D', F', U, B2, U, F2, D', R2, L2, U, F2, D'".replace(", ","")
    update = ''
    tmp = ''
    for i in s:
        if i == ',' or i == ' ':
            continue
        if i == '2':
            update += tmp
            continue
        update += i
        tmp = i
    c.solve(update)
    c.print()