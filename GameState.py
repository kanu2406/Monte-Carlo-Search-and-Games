import math
import random
from collections import defaultdict
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import random
from collections import deque
import copy
from Card_and_Deck import *
from Game_and_Player import *

class GameState:
    def __init__(self, game):
        
        self.game = game
        self.current_player_index = game.current_player_index  
        self.players = game.players
        self.hands = {}  
        for player in game.players:
            self.hands[player.name]=list(player.hand)
            
        self.table_cards = game.cards_on_table  
        
        self.tricks_won = {player.name: player.tricks_won for player in game.players}
        self.trump_suit = game.trump_suit
        self.table_color = game.table_color
        self.have_suits =  {}
        

    def apply_move(self, card,verbose=False):

        player_names = ["Alice", "Bob", "Charlie"]        
        new_hands = {p: h[:] for p, h in self.hands.items()}
        player_name = self.players[self.current_player_index].name 
        if card in self.hands[player_name]:
            self.hands[player_name].remove(card)  
        b1=False
        b2=False
        for c in new_hands[self.players[self.current_player_index].name]:
            if c == card or (c.suit==card.suit and c.rank==card.rank): 
                new_hands[self.players[self.current_player_index].name].remove(c)
                # print(f"removed card {c}")
                b1=True
                break
            

        # self.game.players[self.current_player_index].hand.remove(card)
        for c in self.game.players[self.current_player_index].hand:
            if c == card or (c.suit==card.suit and c.rank==card.rank):  # Compare by value, not reference
                self.game.players[self.current_player_index].hand.remove(c)
                # print(f"removed card {c}")
                b2=True
                break

        if verbose:
          if b1==True:
              print("card removed")
          else:
              print("couldn't found card")
            

        

        # print(f" hand of current player after removal {self.hands[self.players[self.current_player_index].name]}")
        # print(f" hand of current player after removal {self.game.players[self.current_player_index].hand}")

        # self.hands = new_hands

        new_table_cards = self.table_cards[:] + [[self.current_player_index, card]]
        self.game.cards_on_table = new_table_cards

        if len(new_table_cards) == 1:
            self.table_color = card.suit  
            new_table_color=card.suit
            self.game.table_color = new_table_color
        else:
            new_table_color=self.table_color
            self.game.table_color = new_table_color

        if len(new_table_cards) == 3:
            _,winner = self.get_winner(new_table_cards)

            next_turn = winner  
            for player in self.players:
              if player.index == winner:
                self.tricks_won[player.name] += 1
                # player.tricks_won += 1
            # self.tricks_won[self.players[winner].name] += 1
            # self.players[winner].tricks_won += 1
            new_table_cards = []  
            new_table_color = None
            self.game.cards_on_table = []
            self.game.table_color = None
            self.game.cards_on_table = new_table_cards
            self.game.table_color = new_table_color
        else:
            next_turn = (self.current_player_index + 1) % len(self.hands)  

        self.game.current_player_index = next_turn

        self.current_player_index = next_turn
        self.hands = new_hands
        self.table_cards = new_table_cards
        self.table_color = new_table_color
        return self



    # def is_terminal(self):
    #     return all(len(hand) == 0 for hand in self.hands.values())

    def is_terminal(self):
        # if all(len(hand) == 0 for hand in self.hands.values()):
        #     return True

        # if len(self.players[self.current_player_index].hand) == 0:
        #     return True
        
        total_tricks = sum(self.tricks_won.values())
        if total_tricks >= 10:
              # print(f"tricks_won:{sum(self.tricks_won.values())}")
              return True

        return False

    def get_winner(self,new_table_cards):
        lead_suit = self.table_color  
        trump_suit = self.trump_suit

        
        winning_card = max(new_table_cards, key=lambda card:
                          (card[1].suit == trump_suit, card[1].suit == lead_suit, card[1].value))

        winning_player_index = winning_card[0]
        return winning_card, winning_player_index

    def get_legal_moves(self):
        lead_suit = self.table_color  
        trump_suit = self.trump_suit  
        player = self.players[self.current_player_index]

        if lead_suit is None:
            legal_moves = list(player.hand)

        elif lead_suit!=trump_suit:
            lead_suit_cards = [card for card in player.hand if card.suit == lead_suit]
            has_lead_suit = len(lead_suit_cards) > 0

            if has_lead_suit:
                legal_moves = lead_suit_cards


            else:
                trump_cards = [card for card in player.hand if card.suit == trump_suit]

                if trump_cards:
                    trumps_in_play = [card[1].value for card in self.table_cards if card[1].suit == trump_suit]

                    if trumps_in_play:
                        max_trump = np.max(trumps_in_play)
                        higher_trumps = [card for card in trump_cards if card.value > max_trump]

                        if higher_trumps:
                            legal_moves = higher_trumps 
                        else:
                            legal_moves = list(player.hand)  

                    else:
                        legal_moves = trump_cards 

                else:
                    
                    legal_moves = list(player.hand)

        else:
            trump_cards = [card for card in player.hand if card.suit == trump_suit]
            if trump_cards:
                trumps_in_play = [card[1].value for card in self.table_cards if card[1].suit == trump_suit]
                if trumps_in_play:
                    max_trump = np.max(trumps_in_play)
                    higher_trumps = [card for card in trump_cards if card.value > max_trump]
                    if higher_trumps:
                        return higher_trumps
                    else:
                        return trump_cards
                else:
                    return trump_cards
            else:
                return player.hand

        return legal_moves
        # return self.players[self.current_player_index].legal_moves(game)
    
    # def redistribute(self):

    #     redistributed_state = copy.deepcopy(self)  

    #     current_player = redistributed_state.players[redistributed_state.current_player_index]
    #     known_cards = self.hands[current_player.name]  
    #     played_cards = self.table_cards 
    #     played_cards = [card[1] for card in played_cards]
    #     full_deck = Deck()
    #     all_cards = full_deck.cards  
            
    #     unknown_cards = [card for card in all_cards if card not in known_cards and card not in played_cards]

    #     random.shuffle(unknown_cards)

    #     for player in redistributed_state.players:
    #         if player != current_player:
    #             num_cards = len(redistributed_state.hands[player.name])
    #             redistributed_state.hands[player.name] = unknown_cards[:num_cards]
    #             # unknown_cards = unknown_cards[num_cards:] 
    #             del unknown_cards[:num_cards]

    #     return redistributed_state
    def redistribute(self):
          redistributed_state = copy.deepcopy(self)
          # redistributed_state = self

          current_player = redistributed_state.players[redistributed_state.current_player_index]
          current_player_name = current_player.name

          # Step 1: Collect all cards from the other players' hands
          unknown_cards = []
          for player in redistributed_state.players:
              if player.name != current_player_name:
                  unknown_cards.extend(redistributed_state.hands[player.name])
          

          # Step 2: Shuffle the collected cards
          random.shuffle(unknown_cards)

          # Step 3: Redistribute the cards back to the other players
          for player in redistributed_state.players:
              if player.name != current_player_name:
                  num_cards = len(redistributed_state.hands[player.name])
                  redistributed_state.hands[player.name] = unknown_cards[:num_cards]
                  del unknown_cards[:num_cards]

          return redistributed_state
    
    def redistribute_with_inference(game_state, trick_history):
        if not trick_history:
          return game_state.redistribute()
        redistributed_state = copy.deepcopy(game_state)
        players = redistributed_state.players
        hands = redistributed_state.hands
        current_player_name = players[redistributed_state.current_player_index].name

        # Step 1: Infer suits players don't have
        inferred_cannot_have = {p.name: set() for p in players}
        for trick in trick_history:
            if not trick:
                continue
            lead_player_idx, lead_card = trick[0]
            lead_suit = lead_card.suit
            for player_idx, card in trick[1:]:
                if card.suit != lead_suit:
                    player_name = players[player_idx].name
                    inferred_cannot_have[player_name].add(lead_suit)

        # Step 2: Collect unknown cards (from other players)
        unknown_cards = []
        for player in players:
            if player.name != current_player_name:
                unknown_cards.extend(hands[player.name])

        random.shuffle(unknown_cards)
        # print(inferred_cannot_have)
        # Step 3: Redistribute using inferred constraints
        for player in players:
            if player.name == current_player_name:
                continue

            num_cards = len(hands[player.name])
            cannot_have = inferred_cannot_have[player.name]

            # Try to assign cards not in suits the player "cannot have"
            assigned = []
            i = 0
            while len(assigned) < num_cards and i < len(unknown_cards):
                card = unknown_cards[i]
                if card.suit not in cannot_have:
                    assigned.append(card)
                    unknown_cards.pop(i)
                else:
                    i += 1

            # If still not enough cards, fill with whatever remains
            while len(assigned) < num_cards and unknown_cards:
                assigned.append(unknown_cards.pop())

            hands[player.name] = assigned

        return redistributed_state



   

        

    


