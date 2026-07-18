class Game:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]
        ]
        self.white_castling = False # рокировка белого
        self.black_castling = False # и черного королей

        print('Ход белых!')
        self.moveLog = []
        self.whiteToMove = True

        self.runTrue = True

    def get_pawn_moves(self, r, c):
        # return возможные ходы пешки

        # возвращаемое значение
        m = []

        if self.board[r][c][1] == 'p':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                # ходит белая пешка
                
                # если белая пешка каким-то образом находиться
                # на своём первом поле, где она не может находиться
                if r == 7:
                    return False
                elif r == 1:
                    # поле, перед взятием фигуры вместо пешки
                    return False
                    # TODO: добавить фигуру вместо пешки
                else:
                    # ходы пешки
                    if r == 6:
                        if self.board[r - 2][c] == '--' and self.board[r - 1][c] == '--':
                           m.append(['get', r - 2, c])
                    
                    if self.board[r - 1][c] == '--':
                        m.append(['get', r - 1, c])

                    if 0 <= c + 1 <= 7:
                        if self.board[r - 1][c + 1][0] == 'b':
                            m.append(['att', r - 1, c + 1])

                    if 0 <= c - 1 <= 7:
                        if self.board[r - 1][c - 1][0] == 'b':
                            m.append(['att', r - 1, c - 1])

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                # ходит черная пешка

                # если черная пешка каким-то образом находиться
                # на своём первом поле, где она не может находиться
                if r == 0:
                    return False
                elif r == 6:
                    # поле, перед взятием фигуры вместо пешки
                    return False
                    # TODO: добавить фигуру вместо пешки
                else:
                    # ходы пешки
                    if r == 1:
                        if self.board[r + 2][c] == '--' and self.board[r + 1][c] == '--':
                           m.append(['get', r + 2, c])
                    
                    if self.board[r + 1][c] == '--':
                        m.append(['get', r + 1, c])

                    if 0 <= c + 1 <= 7:
                        if self.board[r + 1][c + 1][0] == 'w':
                            m.append(['att', r + 1, c + 1])

                    if 0 <= c - 1 <= 7:
                        if self.board[r + 1][c - 1][0] == 'w':
                            m.append(['att', r + 1, c - 1])

        if m == []:
            return False
        return m

    def get_rook_moves(self, r, c):
        # return возможные ходы ладьи

        # возвращаемое значение
        m = []
        
        if self.board[r][c][1] == 'R':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                # ходит белая ладья
                d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                m.append(['att', r + n[0], c + n[1]])
                                break

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                # ходит черная ладья
                d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                m.append(['att', r + n[0], c + n[1]])
                                break
        
        if m == []:
            return False
        return m
    
    def get_knight_moves(self, r, c):
        # return возможные ходы коня

        # возвращаемое значение
        m = []
        
        if self.board[r][c][1] == 'N':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                d = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
                for i in d:
                    if 0 <= r + i[0] <= 7 and 0 <= c + i[1] <= 7:
                        if self.board[r + i[0]][c + i[1]] == '--':
                            m.append(['get', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'b':
                            m.append(['att', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'w':
                            continue

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                d = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
                for i in d:
                    if 0 <= r + i[0] <= 7 and 0 <= c + i[1] <= 7:
                        if self.board[r + i[0]][c + i[1]] == '--':
                            m.append(['get', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'w':
                            m.append(['att', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'b':
                            continue

        if m == []:
            return False
        return m

    def get_bishop_moves(self, r, c):
        # return возможные ходы слона

        # возвращаемое значение
        m = []
        
        if self.board[r][c][1] == 'B':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                # ходит белый слон
                d = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                m.append(['att', r + n[0], c + n[1]])
                                break

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                # ходит черный слон
                d = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                m.append(['att', r + n[0], c + n[1]])
                                break
        if m == []:
            return False
        return m

    def get_queen_moves(self, r, c):
        # return возможные ходы королевы

        # возвращаемое значение
        m = []

        if self.board[r][c][1] == 'Q':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                m.append(['att', r + n[0], c + n[1]])
                                break
                ########################
                # ВЫШЕ ладья НИЖЕ СЛОН #
                ########################
                d = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                m.append(['att', r + n[0], c + n[1]])
                                break

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                m.append(['att', r + n[0], c + n[1]])
                                break
                ########################
                # ВЫШЕ ладья НИЖЕ СЛОН #
                ########################
                d = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
                for i in d:
                    for j in range(1, 8):
                        n = [i[0] * j, i[1] * j]
                        if 0 <= r + n[0] <= 7 and 0 <= c + n[1] <= 7:
                            if self.board[r + n[0]][c + n[1]] == '--':
                                m.append(['get', r + n[0], c + n[1]])
                            if self.board[r + n[0]][c + n[1]][0] == 'b':
                                break
                            if self.board[r + n[0]][c + n[1]][0] == 'w':
                                m.append(['att', r + n[0], c + n[1]])
                                break
        if m == []:
            return False
        return m

    def get_king_moves(self, r, c):
        # return возможные ходы короля

        # возвращаемое значение
        m = []
        
        if self.board[r][c][1] == 'K':
            if self.whiteToMove and self.board[r][c][0] == 'w':
                d = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
                for i in d:
                    if 0 <= r + i[0] <= 7 and 0 <= c + i[1] <= 7:
                        if self.board[r + i[0]][c + i[1]] == '--':
                            m.append(['get', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'w':
                            continue
                        if self.board[r + i[0]][c + i[1]][0] == 'b':
                            m.append(['att', r + i[0], c + i[1]])

            elif not self.whiteToMove and self.board[r][c][0] == 'b':
                d = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
                for i in d:
                    if 0 <= r + i[0] <= 7 and 0 <= c + i[1] <= 7:
                        if self.board[r + i[0]][c + i[1]] == '--':
                            m.append(['get', r + i[0], c + i[1]])
                        if self.board[r + i[0]][c + i[1]][0] == 'b':
                            continue
                        if self.board[r + i[0]][c + i[1]][0] == 'w':
                            m.append(['att', r + i[0], c + i[1]])

        if m == []:
            return False
        return m

    def get_checking_king(self, white=True):
        g = "wK" if white else "bK"
        gg = "w" if white else "b"
        g_anti = "b" if white else "w"
        row, col = -1, -1
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] == g:
                    row, col = j, i
        if row == -1 or col == -1: return False
        ########################################
        d = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        h = "bN" if white else "wN"
        for i in d:
            m_row = row + i[0]
            m_col = col + i[1]
            if 0 <= m_row <= 7 and 0 <= m_col <= 7:
                if self.board[m_col][m_row] == h:
                    return True
        ########################################
        d = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for i in d:
            for j in range(1, 8):
                m_row = row + (i[0] * j)
                m_col = col + (i[1] * j)
                if 0 <= m_row <= 7 and 0 <= m_col <= 7:
                    if self.board[m_col][m_row][0] == gg:
                        break
                    elif self.board[m_col][m_row] == "--":
                        continue
                    elif self.board[m_col][m_row][0] == g_anti:
                        #TODO скан на короля
                        if self.board[m_col][m_row] == (g_anti + "B") or self.board[m_col][m_row] == (g_anti + "Q"):
                            return True
                        break
        #########################################
        d = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in d:
            for j in range(1, 8):
                m_row = row + (i[0] * j)
                m_col = col + (i[1] * j)
                if 0 <= m_row <= 7 and 0 <= m_col <= 7:
                    if self.board[m_col][m_row][0] == gg:
                        break
                    elif self.board[m_col][m_row] == "--":
                        continue
                    elif self.board[m_col][m_row][0] == g_anti:
                        #TODO скан на короля
                        if self.board[m_col][m_row] == (g_anti + "R") or self.board[m_col][m_row] == (g_anti + "Q"):
                            return True
                        break
        #########################################
        return False

    def make_move(self, start_sq, end_sq): # совершение хода
        self.startRow = start_sq[0]
        self.startCol = start_sq[1]
        self.endRow = end_sq[0]
        self.endCol = end_sq[1]
        self.pieceMoved = self.board[self.startRow][self.startCol]
        self.pieceCaptured = '--'
        if self.pieceMoved[0] != '-':
            self.pieceCaptured = self.board[self.endRow][self.endCol]
        elif self.pieceMoved[0] == '-':
            self.runTrue = False
        
        if self.runTrue and self.pieceMoved[0] != '-':
            if self.whiteToMove and self.pieceMoved[0] == 'w':
                # ход белых
                r = self.get_checking_king(white=False)
                if r:
                    print('Белые выиграли!')
                else:
                    h = False
                    match self.pieceMoved[1]:
                        case 'p':
                            h = self.get_pawn_moves(self.startRow, self.startCol)
                        case 'R':
                            h = self.get_rook_moves(self.startRow, self.startCol)
                        case 'N':
                            h = self.get_knight_moves(self.startRow, self.startCol)
                        case 'B':
                            h = self.get_bishop_moves(self.startRow, self.startCol)
                        case 'Q':
                            h = self.get_queen_moves(self.startRow, self.startCol)
                        case 'K':
                            h = self.get_king_moves(self.startRow, self.startCol)
                    #############
                    if not h:
                        pass
                    else:
                        for i in h:
                            if i[0] == 'get':
                                if self.pieceCaptured == '--':
                                    if self.endRow == i[1] and self.endCol == i[2]:
                                        self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                            elif i[0] == 'att':
                                if self.pieceCaptured != '--':
                                    if self.endRow == i[1] and self.endCol == i[2]:
                                        self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                    # self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                
                r0 = self.get_checking_king(white=False)
                if r0:
                    self.black_castling = True
                    print('Шах черному королю!')

                r2 = self.get_checking_king()
                if r2:
                    self.undo_move()
                    print('Внимание! Шах белому королю!')
                    self.white_castling = True
            if not self.whiteToMove and self.pieceMoved[0] == 'b':
                # ход черных
                r = self.get_checking_king()
                if r:
                    print('Черные выиграли!')
                else:
                    h = False
                    match self.pieceMoved[1]:
                        case 'p':
                            h = self.get_pawn_moves(self.startRow, self.startCol)
                        case 'R':
                            h = self.get_rook_moves(self.startRow, self.startCol)
                        case 'N':
                            h = self.get_knight_moves(self.startRow, self.startCol)
                        case 'B':
                            h = self.get_bishop_moves(self.startRow, self.startCol)
                        case 'Q':
                            h = self.get_queen_moves(self.startRow, self.startCol)
                        case 'K':
                            h = self.get_king_moves(self.startRow, self.startCol)
                    #############
                    if not h:
                        pass
                    else:
                        for i in h:
                            if i[0] == 'get':
                                if self.pieceCaptured == '--':
                                    if self.endRow == i[1] and self.endCol == i[2]:
                                        self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                            elif i[0] == 'att':
                                if self.pieceCaptured != '--':
                                    if self.endRow == i[1] and self.endCol == i[2]:
                                        self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                    # self.make(self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured)
                
                r0 = self.get_checking_king()
                if r0:
                    self.white_castling = True
                    print('Шах белому королю!')

                r2 = self.get_checking_king(white=False)
                if r2:
                    self.undo_move()
                    print('Внимание! Шах черному королю!')
                    self.black_castling = True
        self.runTrue = True

    def make(self, startRow, startCol, endRow, endCol, pieceMoved, pieceCaptured):
        self.board[startRow][startCol] = "--"
        self.board[endRow][endCol] = pieceMoved
        self.moveLog.append([startRow, startCol, endRow, endCol, pieceMoved, pieceCaptured])
        self.whiteToMove = not self.whiteToMove
        # print(self.get_chessnotation())
        if self.whiteToMove:
            print('Ход белых!')
        elif not self.whiteToMove:
            print("Ход чёрных!")

    def undo_move(self):
        if len(self.moveLog) != 0:
            last = self.moveLog.pop()
            self.board[last[0]][last[1]] = last[4]
            self.board[last[2]][last[3]] = last[5]
            self.whiteToMove = not self.whiteToMove

    def get_chessnotation(self):
        return self.get_rankfile(self.startRow, self.startCol) + self.get_rankfile(self.endRow, self.endCol)

    def get_rankfile(self, r, c):
        return Game.colsToFiles[c] + Game.rowsToRanks[r]
