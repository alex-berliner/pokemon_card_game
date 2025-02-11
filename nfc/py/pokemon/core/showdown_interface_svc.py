# node pokemon-showdown start --no-security
from poke_env.teambuilder import Teambuilder
from poke_env.player import Player, RandomPlayer
import asyncio
# import signal
import sys
sys.path.append('../build/proto')
import pokemon_interface_pb2
import socket
import sys
import time
from hardware_listener import *
from gen1teamgen import *

from poke_env.player.battle_order import (
    BattleOrder,
    DefaultBattleOrder,
    DoubleBattleOrder,
)

class MaxDamagePlayer(Player):
    def __init__(self, battle_format, name, queue, evl, team):
        super().__init__(battle_format=battle_format, team=team)
        self.name = name
        self.queue = queue
        self.evl = evl

# self._data = GenData.from_gen(gen)

# # Species related attributes
# self._ability: Optional[str] = None
# self._active: bool
# self._base_stats: Dict[str, int]
# self._current_hp: Optional[int] = 0
# self._effects: Dict[Effect, int] = {}
# self._first_turn: bool = False
# self._gender: Optional[PokemonGender] = None
# self._heightm: int
# self._item: Optional[str] = self._data.UNKNOWN_ITEM
# self._last_details: str = ""
# self._last_request: Optional[Dict[str, Any]] = {}
# self._level: int = 100
# self._max_hp: Optional[int] = 0
# self._moves: Dict[str, Move] = {}
# self._must_recharge: bool = False
# self._possible_abilities: List[str]
# self._preparing_move: Optional[Move] = None
# self._preparing_target = None
# self._protect_counter: int = 0
# self._revealed: bool = False
# self._shiny: Optional[bool] = False
# self._species: str = ""
# self._status_counter: int = 0
# self._status: Optional[Status] = None
# self._terastallized_type: Optional[PokemonType] = None
# self._terastallized: bool = False
# self._type_1: PokemonType
# self._type_2: Optional[PokemonType] = None
# self._weightkg: int
    # TODO: utility NFCs stored in hand that let you poll for stats of pokemon
    def pokemon_status(self, pokemon, available_moves):
        o = ""
        # /home/pi/code/pokemon/poke-env/src/poke_env/environment/pokemon.py

        o += ("Active" if pokemon._active else "Inactive").ljust(10)

        status_cond = ""
        if pokemon._status:
            status_cond = f"({pokemon._status.name.capitalize()})"
        o += f"{pokemon._species.capitalize()} {status_cond} ".ljust(18)

        # hp
        hp  = f"{pokemon._current_hp}".ljust(3) + " / "
        hp += f"{pokemon._max_hp}".ljust(6)
        o += hp
        if pokemon._current_hp > 0:
            if pokemon._active:
                move_names = "".join([str(x).split(" ")[-1].capitalize().ljust(16) for x in available_moves])
                o += f"{move_names} "
            else:
                move_name_arr = [(f"{pokemon._moves[x]._id},").ljust(16) for x in pokemon._moves]
                move_names = "".join(move_name_arr).ljust(16)
                o += f"{move_names} "
            for e in pokemon._effects:
                o += f"{e.name}, ".ljust(16)
        return o

    def get_pokemon_active(self, battle):
        return [battle.team[x] for x in battle.team if battle.team[x]._active][0]

    def get_pokemon_inactive(self, battle):
        return sorted([battle.team[x] for x in battle.team if not battle.team[x]._active], key=lambda x: x._species)

    def display_turn_start(self, battle, available_moves):
        print("\n"*30)
        print(f"Player {self.name}'s turn")
        print("Opponent's Pokemon:")
        print(self.pokemon_status(battle.opponent_active_pokemon, available_moves))
        print()
        print(f"Your Pokemon:{' '*27}Red{' '*13}Yellow{' '*10}Blue{' '*12}Grey")
        print(self.pokemon_status(self.get_pokemon_active(battle), available_moves))
        # print("Inactive:")
        for e in self.get_pokemon_inactive(battle):
            print(self.pokemon_status(e, available_moves))
        for i in range(self.name):
            print("="*30)

    def choose_move(self, battle):
        available_switches = [BattleOrder(available_switches) for available_switches in battle.available_switches]
        available_moves = [BattleOrder(move) for move in battle.available_moves]
        self.evl.switch_player(self.name-1)
        self.display_turn_start(battle, available_moves)
        for _ in range(self.queue.qsize()):
            self.queue.get()
        # print(self.queue.qsize())
        # for e in available_moves:
        #     print(e)
        # failsafe for continuing game when no moves are available
        if not any(available_switches + available_moves):
            print("jumpstarting game state after disconnect. sorry!")
            return self.choose_random_move(battle)
        while True:
            for i in range(self.queue.qsize()):
                # print(self.queue.qsize())
                message = self.queue.get()
                if len(message.pokemon_name) > 0:
                    for e in battle.available_switches:
                        if e._species.lower() == message.pokemon_name.lower() and e._current_hp > 0: # TODO: change to faint check
                            print(f"switching to {message.pokemon_name.capitalize()}")
                            time.sleep(2)
                            return BattleOrder(e)
                elif self.get_pokemon_active(battle)._current_hp < 1:
                    print("Your pokemon has fainted!")
                    time.sleep(0.5)
                    for _ in range(self.queue.qsize()):
                        self.queue.get()
                    time.sleep(0.5)
                elif self.get_pokemon_active(battle)._current_hp > 0:
                    move_id = message.attack
                    if move_id >= len(available_moves):
                        print(f"Invalid move id! {move_id}")
                        for e in available_moves:
                            print(e)
                        time.sleep(0.5)
                        for _ in range(self.queue.qsize()):
                            self.queue.get()
                        time.sleep(0.5)
                        input()
                        continue
                    move = str(available_moves[move_id]).split(" ")[-1]
                    print(f"Using {move}")
                    time.sleep(1)
                    return available_moves[move_id]

        return self.choose_random_move(battle)

class PlayerTeamManager(Teambuilder):
    def __init__(self, teams):
        self.team = self.join_team(self.parse_showdown_team(teams.pop()))

    def yield_team(self):
        return self.team

async def main():
    print("?")
    start = time.time()
    event_listener = HardwareListener()

    teams = genteams()
    print(teams[0])
    max_damage_player_1 = MaxDamagePlayer(
        name = 1,
        battle_format = "gen1ou",
        team = PlayerTeamManager(teams),
        queue = event_listener.queue,
        evl = event_listener
    )
    # max_damage_player_2 = MaxDamagePlayer(
    #     name = 2,
    #     battle_format = "gen1ou",
    #     team = PlayerTeamManager(teams),
    #     queue = event_listener.queue,
    #     evl = event_listener
    # )
    max_damage_player_2 = RandomPlayer(
        # name = 2,
        battle_format = "gen1ou",
        team = PlayerTeamManager(teams),
        # queue = event_listener.queue,
        # evl = event_listener
    )

    await max_damage_player_1.battle_against(max_damage_player_2, n_battles=1)

    print(
        "Max damage player won %d / 1 battles [this took %f seconds]"
        % (
            max_damage_player_1.n_won_battles, time.time() - start
        )
    )
    # TODO: removing this causes the interpreter to shut down without the
    # HL server shutting down. These should be shutting down at the same time.
    while True:
        time.sleep(0.1)
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
