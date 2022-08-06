import random

"""
This file can be a nice home for your Battlesnake's logic and helper functions.

We have started this for you, and included some logic to remove your Battlesnake's 'neck'
from the list of possible moves!
"""

def delete_move(move, possible_moves):

    if move in possible_moves:
        possible_moves.remove(move)


def get_info():
    """
    This controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "NickSquiggles",
        "color": "#ffd533",
        "head": "snail",
        "tail": "snail",
    }


def choose_move(data):
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_snake = data["you"]      # A dictionary describing your snake's position on the board
    my_head = my_snake["head"]  # A dictionary of coordinates like {"x": 0, "y": 0}
    my_body = my_snake["body"]
    my_neck = my_body[1]  # A list of coordinate dictionaries like [{"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0}]
    all_snakes = data["board"]["snakes"]

    # Uncomment the lines below to see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnake this turn is: {my_snake}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # TODO: Step 1 - Don't hit walls.
    # Use information from `data` and `my_head` to not move beyond the game board.
    board = data["board"]
    board_height = board["height"]
    board_width = board["width"]
    possible_moves = avoid_walls(my_head, board_height, board_width, possible_moves)

    # TODO: Step 2 - Don't hit yourself.
    # Use information from `my_body` to avoid moves that would collide with yourself.
    possible_moves = avoid_my_body(my_head, my_body, possible_moves)

    # TODO: Step 3 - Don't collide with others.
    # Use information from `data` to prevent your Battlesnake from colliding with others.
    possible_moves = avoid_other_lads(my_head, all_snakes, possible_moves)

    # TODO: Step 4 - Find food.
    # Use information in `data` to seek out and find food.
    # food = data['board']['food']

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    if len(possible_moves) != 0:
        move = random.choice(possible_moves)
    else:
        move = snail_squish(my_head, my_neck)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def snail_squish(my_head, my_neck):

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        return "left"
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        return "right"
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        return "down"
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        return "up"

def avoid_walls(my_head, board_height, board_width, possible_moves):

    if my_head["x"] == 0:
        delete_move("left", possible_moves)
    if my_head["x"] == board_width - 1:
        delete_move("right", possible_moves)
    if my_head["y"] == 0:
        delete_move("down", possible_moves)
    if my_head["y"] == board_height - 1:
        delete_move("up", possible_moves)

    return possible_moves

def avoid_my_body(my_head, my_body, possible_moves):

    if {"x": my_head["x"]-1, "y": my_head["y"]} in my_body:
        delete_move("left", possible_moves)
    if {"x": my_head["x"]+1, "y": my_head["y"]} in my_body:
        delete_move("right", possible_moves)
    if {"x": my_head["x"], "y": my_head["y"]-1} in my_body:
        delete_move("down", possible_moves)
    if {"x": my_head["x"], "y": my_head["y"]+1} in my_body:
        delete_move("up", possible_moves)

    return possible_moves

def avoid_other_lads(my_head, all_snakes, possible_moves):

    for snake in all_snakes:
        body = snake["body"]

        if {"x": my_head["x"]-1, "y": my_head["y"]} in body:
            delete_move("left", possible_moves)
        if {"x": my_head["x"]+1, "y": my_head["y"]} in body:
            delete_move("right", possible_moves)
        if {"x": my_head["x"], "y": my_head["y"]-1} in body:
            delete_move("down", possible_moves)
        if {"x": my_head["x"], "y": my_head["y"]+1} in body:
            delete_move("up", possible_moves)

    return possible_moves