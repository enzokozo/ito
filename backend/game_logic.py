import random

class ItoGame:
    def __init__(self):
        # O baralho do Ito tem cartas de 1 a 100
        self.deck = list(range(1, 101))

        # Dicionário para guardar o nome do jogador e a carta que ele recebeu
        self.players = {}

        # O tema da rodada (ex: "O que levar para uma ilha deserta?")
        self.theme = ""

        # Cartas que foram jogadas na rodada
        self.played_cards = []

        self.is_started = False

    def add_player(self, player_name:str):
        """
        Adiciona um jogador ao jogo, caso o jogo ainda não tenha começado.
        """

        if not self.is_started and player_name not in self.players:
            # O valor None significa que o jogador ainda não recebeu uma carta
            self.players[player_name] = None
            return True
        return False
    
    def start_round(self, theme: str):
        """
        Inicia uma nova rodada, embaralha as cartas e dá 1 carta para cada jogador.
        """
        if len(self.players) < 2:
            return False, "Faltam jogadores para começar"
        
        self.is_started = True
        self.theme = theme
        self.played_cards = []

        # Re-cria e embaralha o deck
        self.deck = list(range(1, 101))
        random.shuffle(self.deck)

        # Distribui uma carta para cada jogador
        for player in self.players:
            self.players[player] = self.deck.pop()

        return True, "Rodada iniciada"

    def get_game_state(self) -> dict:
        """
        Retorna as informações do jogo (sem revelar as cartas dos jogadores).
        """
        return {
            "players": list(self.players.keys()),
            "played_cards": self.played_cards,
            "theme": self.theme,
            "is_started": self.is_started
        } 