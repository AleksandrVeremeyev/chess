import pygame as p
import engine

# ширина и длина окна
WIDTH = HEIGHT = 512
# 8 клеток
DIMENSION = 8
# размер одной квадратной клетки в пикселях
SQ_SIZE = HEIGHT // DIMENSION # = 64
MAX_FPS = 15
IMAGES = {}

#############
# отрисовка выделенной клетки row, col - координаты; bool - флаг
sq_row, sq_col, sq_bool = 0, 0, False

# загрузка фигур шахмат
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    global sq_row, sq_col, sq_bool

    # pygame
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    # создание шахматной партии
    gs = engine.Game()

    load_images()
    running = True

    sq_selected = () # текущая выбранная клетка
    player_clicks = [] # выбранные клетки

    row, col = 0, 0
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                # при нажатии на КРЕСТИК игра завершается
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                # сохранение позиции мыши, при нажатии на экран
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # если выделенная ячейка ужа нажата
                if sq_selected == (row, col):
                    # то мы отменяем выделение
                    sq_selected = ()
                    player_clicks = []

                    # флаг выделения клетки
                    sq_row, sq_col, sq_bool = 0, 0, False

                else:
                    # записываем координаты сюда:
                    sq_selected = (row, col)
                    # и сюда:
                    player_clicks.append(sq_selected)

                    sq_row, sq_col, sq_bool = row, col, True

                # если выбранны две клетки:
                if len(player_clicks) == 2:
                    # выполняем ход
                    gs.make_move(player_clicks[0], player_clicks[1])

                    # после совершения хода очищаем переменные:
                    sq_selected = ()
                    player_clicks = []

                    # отменяем выделение
                    sq_row, sq_col, sq_bool = 0, 0, False

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    # при нажатии на "Z" - отменяем ход
                    gs.undo_move()
                    
        draw_game(screen, gs, row, col)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_game(screen, gs, r, c):
    draw_board(screen, gs, r, c) # доска
    draw_pieces(screen, gs.board) # фигуры

def draw_board(screen, _gs, row, col):
    global sq_row, sq_col, sq_bool

    colors = [p.Color("gray"), p.Color("white")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    if sq_bool:
        p.draw.rect(screen, p.Color("blue"), p.Rect(sq_col * SQ_SIZE, sq_row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    match _gs.board[sq_row][sq_col][1]:
        case 'p':
            n = _gs.get_pawn_moves(sq_row, sq_col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        case 'R':
            n = _gs.get_rook_moves(row, col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        case 'N':
            n = _gs.get_knight_moves(sq_row, sq_col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        case 'B':
            n = _gs.get_bishop_moves(sq_row, sq_col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        case 'Q':
            n = _gs.get_queen_moves(sq_row, sq_col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

        case 'K':
            n = _gs.get_king_moves(sq_row, sq_col)
            if n != False:
                for i in n:
                    if i[0] == 'get':
                        p.draw.rect(screen, p.Color("green"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif i[0] == 'att':
                        p.draw.rect(screen, p.Color("red"), p.Rect(i[2] * SQ_SIZE, i[1] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# метод отрисовки фигур
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()