class Piece:
    def _init_(self, color, name):
        self.color = color
        self.name = name   

    def _repr_(self):
        return f'{self.color[0]}{self.name[0]}'

class Pawn(Piece):
    def _init_(self, color):
        super()._init_(color, 'pawn')

    def valid_moves(self, x, y, board):
        #pawn valid moves
        moves = []
        direction = -1 if self.color == 'white' else 1
      
        if board[x + direction][y] is None:
            moves.append((x + direction, y))
    
        if (self.color == 'white' and x == 6) or (self.color == 'black' and x == 1):
            if board[x + direction][y] is None and board[x + 2 * direction][y] is None:
                moves.append((x + 2 * direction, y))
  
        for dy in [-1, 1]:
            if 0 <= y + dy < 8 and board[x + direction][y + dy] is not None:
                if board[x + direction][y + dy].color != self.color:
                    moves.append((x + direction, y + dy))
        return moves

class Knight(Piece):
    def _init_(self, color):
        super()._init_(color, 'knight')

    def valid_moves(self, x, y, board):
        #knight valid moves
        moves = []
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dx, dy in directions:
            if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                if board[x + dx][y + dy] is None or board[x + dx][y + dy].color != self.color:
                    moves.append((x + dx, y + dy))
        return moves

class Bishop(Piece):
    def _init_(self, color):
        super()._init_(color, 'bishop')

    def valid_moves(self, x, y, board):
        #bishop Valid moves
        return self._generate_moves(x, y, board, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def _generate_moves(self, x, y, board, directions):
        moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    moves.append((nx, ny))
                elif board[nx][ny].color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return moves

class Rook(Piece):
    def _init_(self, color):
        super()._init_(color, 'rook')
        self.has_moved = False

    def valid_moves(self, x, y, board):
        #Rook valid moves
        return self._generate_moves(x, y, board, [(1, 0), (-1, 0), (0, 1), (0, -1)])

    def _generate_moves(self, x, y, board, directions):
        moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    moves.append((nx, ny))
                elif board[nx][ny].color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return moves

class Queen(Piece):
    def _init_(self, color):
        super()._init_(color, 'queen')

    def valid_moves(self, x, y, board):
        #queen valid moves
        return self._generate_moves(x, y, board, [
            (1, 1), (1, -1), (-1, 1), (-1, -1),
            (1, 0), (-1, 0), (0, 1), (0, -1)
        ])

    def _generate_moves(self, x, y, board, directions):
        moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if board[nx][ny] is None:
                    moves.append((nx, ny))
                elif board[nx][ny].color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return moves

class King(Piece):
    def _init_(self, color):
        super()._init_(color, 'king')
        self.has_moved = False

    def valid_moves(self, x, y, board):
        #king valid moves
        moves = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dx, dy in directions:
            if 0 <= x + dx < 8 and 0 <= y + dy < 8:
                if board[x + dx][y + dy] is None or board[x + dx][y + dy].color != self.color:
                    moves.append((x + dx, y + dy))
        # Castling moves
        if not self.has_moved:
            if isinstance(board[x][0], Rook) and not board[x][0].has_moved and \
                    all(board[x][i] is None for i in range(1, 4)):
                moves.append((x, 2))
            if isinstance(board[x][7], Rook) and not board[x][7].has_moved and \
                    all(board[x][i] is None for i in range(5, 7)):
                moves.append((x, 6)) 
        return moves

class ChessBoard:
    def _init_(self):
        self.board = self.create_board()
        self.turn = 'white'
        self.history = []

    def create_board(self):
        #Creating a 8*8 chess board and place pieces in initial positions
        board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            board[1][i] = Pawn('black')
            board[6][i] = Pawn('white')

        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for i, piece in enumerate(piece_order):
            board[0][i] = piece('black')
            board[7][i] = piece('white')

        return board

    def display_board(self):
        for row in self.board:
            print(' '.join([str(piece) if piece else '--' for piece in row]))
        print()

    def move_piece(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        piece = self.board[start_x][start_y]

        if piece is None:
            raise ValueError("starting position")
        if piece.color != self.turn:
            raise ValueError(f"It's {self.turn}'s turn")
        if (end_x, end_y) not in piece.valid_moves(start_x, start_y, self.board):
            raise ValueError("Invalid move")

        self.history.append((start, end, self.board[end_x][end_y]))

        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = None

        if isinstance(piece, (King, Rook)):
            piece.has_moved = True

        if isinstance(piece, King) and abs(start_y - end_y) == 2:
            if end_y == 2:
                self.board[start_x][3] = self.board[start_x][0]
                self.board[start_x][0] = None
            elif end_y == 6:
                self.board[start_x][5] = self.board[start_x][7]
                self.board[start_x][7] = None

        if isinstance(piece, Pawn) and (end_x == 0 or end_x == 7):
            self.board[end_x][end_y] = Queen(piece.color)

        self.turn = 'black' if self.turn == 'white' else 'white'

    def undo_move(self):
        if not self.history:
            raise ValueError("No moves to undo")
        last_move = self.history.pop()
        start, end, captured_piece = last_move
        start_x, start_y = start
        end_x, end_y = end
        self.board[start_x][start_y] = self.board[end_x][end_y]
        self.board[end_x][end_y] = captured_piece

        self.turn = 'black' if self.turn == 'white' else 'white'

    def is_check(self, color):
        king_position = None
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.name == 'king' and piece.color == color:
                    king_position = (x, y)
                    break
            if king_position:
                break

        if not king_position:
            raise ValueError(f"No {color} king found on the board")

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.color != color:
                    if king_position in piece.valid_moves(x, y, self.board):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color):
            return False
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.color == color:
                    for move in piece.valid_moves(x, y, self.board):
                        temp_board = [row[:] for row in self.board]
                        temp_board[move[0]][move[1]] = piece
                        temp_board[x][y] = None
                        if not self.is_check(color):
                            return False
        return True

    def is_stalemate(self, color):
        if self.is_check(color):
            return False
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.color == color:
                    if piece.valid_moves(x, y, self.board):
                        return False
        return True

    def is_draw(self):
        
        if self.is_stalemate(self.turn):
            return True
        return False

def main():
    game = ChessBoard()
    game.display_board()

    game.move_piece((6, 0), (4, 0))  
    game.display_board()
    game.move_piece((1, 0), (3, 0))
    game.display_board()

if __name__ == "_main_":
    main()