from ai_default_tables import *
import chess_pieces as cp
import numpy as n

class calc_rule:
    def __init__(self):
        self.calc_level = False


    def calc(self, cb):
        pass

    def calc_diff(self, cb, move):
        return 0

class cr_piece_value(calc_rule):
    def __init__(self):
        super().__init__()
        self.values = DEFAULT_PIECE_VALUES
        self.calc_level = 99
    def calc(self, cb, BW):
        """
        Calculates the total piece value of 1 colour
        """
        value = 0
        for square in cb.allsquares:
            if square.piece and BW == square.piece.BW: 
                ID = square.piece.ID
                value += self.values[ID]
        return value

    def calc_diff(self, cb, BW, move):
        startsquare, endsquare = move
        taken_piece = endsquare.piece
        
        if taken_piece:
            ID = taken_piece.ID
            if BW != taken_piece.BW: 
                return self.values[ID]
            else:
                return -self.values[ID]
        return 0
    
class cr_piece_position_value(calc_rule):
    def __init__(self):
        super().__init__()
        self.values = []
        self.values.append(PAWN_TABLE)
        self.values.append(KNIGHT_TABLE)
        self.values.append(BISHOP_TABLE)
        self.values.append(ROOK_TABLE)
        self.values.append(QUEEN_TABLE)
        self.values.append(KING_TABLE)
    def calc(self, cb, BW):
        value = 0
        for square in cb.allsquares:
            if square.piece and BW == square.piece.BW:
                ID = square.piece.ID
                if BW == cp.CP_BLACK:
                    value += self.values[square.piece.ID][square.y][square.x]
                else:
                    value += self.values[square.piece.ID][7 - square.y][square.x]
        return value

class ai_rule:
    def __init__(self, rule, weight):
        self.rule = rule
        self.weight = weight
class ai:
    def __init__(self):
        self.rules = []
        self.rules.append(ai_rule(cr_piece_value(), 1))
        self.rules.append(ai_rule(cr_piece_position_value(), 1))
        self.transpostable = []
        self.transposvalue = []

    def calc_board(self, cb, BW):
        value = 0
        for ai_rule in self.rules:
            value += ai_rule.rule.calc(cb, BW) * ai_rule.weight
        return value

    def transposcode(self, cb):
        strcode = ""
        for square in cb.allsquares:
            if square.piece:
                strcode = strcode + square.code + square.piece.code
        return strcode
        
    def alpha_beta_search(self, board, rule_eval, depth, alpha, beta, player, maximizing_player):
        returnVal = 0
        #TODO: is_game_over
        if depth == 0 or board.isCheckmate(player):
            if maximizing_player:
                return self.calc_board(board, player) - board.opponent(board.opponent(player))
            else:
                return self.calc_board(board, board.opponent(player)) - board.opponent(player)
            
        transposcode = self.transposcode(board)
        if transposcode in self.transpostable:
            return self.transposvalue[self.transpostable.index(transposcode)]
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in board.possible_moves(player):
                self.calc_rule_eval(board, rule_eval, player, move, depth - 1)
                startsquare, endsquare = move
                p1, p2 = startsquare.piece, endsquare.piece
                endsquare.piece, startsquare.piece = p1, None
                eval = self.alpha_beta_search(board, rule_eval, depth - 1, alpha, beta, board.opponent(player), False)
                startsquare.piece, endsquare.piece = p1, p2
                max_eval = max(max_eval, eval)
                #fail-soft set alpha before break
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            returnVal = max_eval
        else:
            min_eval = float('inf')
            for move in board.possible_moves(player):
                self.calc_rule_eval(board, rule_eval, player, move, depth - 1)
                startsquare, endsquare = move
                p1, p2 = startsquare.piece, endsquare.piece
                endsquare.piece, startsquare.piece = p1, None
                eval = self.alpha_beta_search(board, rule_eval, depth - 1, alpha, beta, board.opponent(player), True)
                startsquare.piece, endsquare.piece = p1, p2
                min_eval = min(min_eval, eval)
                #fail-soft beta before break
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            returnVal = min_eval
        self.transpostable.append(transposcode)
        self.transposvalue.append(returnVal)
        return returnVal
    
    def calc_rule_eval(self, cb, rule_eval, BW, move, depth, isTopLevel=False):
        for i in range(len(self.rules)):
            ai_rule = self.rules[i]
            if isTopLevel and ai_rule.rule.calc_level == 99:
                rule_eval[i][depth-1] = ai_rule.rule.calc(cb, BW)
            elif ai_rule.rule.calc_level == depth:
                rule_eval[i][depth-1] = ai_rule.rule.calc(cb, BW)
            elif ai_rule.rule.calc_level > depth:
                rule_eval[i][depth-1] = rule_eval[i][depth] + ai_rule.rule.calc_diff(cb, BW, move)
    
    def find_best_move(self, board, depth, player):
        rule_eval = n.zeros((len(self.rules), depth))
        self.calc_rule_eval(board, rule_eval, player, None, depth, True)
        self.transpostable = []
        self.transposvalue = []
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in board.possible_moves(player):
            self.calc_rule_eval(board, rule_eval, player, move, depth - 1)
            startsquare, endsquare = move
            p1, p2 = startsquare.piece, endsquare.piece
            endsquare.piece, startsquare.piece = p1, None
            eval = self.alpha_beta_search(board, rule_eval, depth - 1, alpha, beta, board.opponent(player), False)
            startsquare.piece, endsquare.piece = p1, p2
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move
