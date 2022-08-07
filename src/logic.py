from copy import copy
import random
from statistics import mean

def get_info():

    return {
        "apiversion": "1",
        "author": "NickSquiggles",
        "color": "#ffd533",
        "head": "snail",
        "tail": "snail",
    }

def choose_move(data):
    print(f"--- start of turn {data['turn']} (i am snake {data['you']['id']}) ---")
    
    # My data
    my_snake = data["you"]
    my_head = my_snake["head"]
    my_body = my_snake["body"]
    my_neck = my_body[1]
    comfort_level = 30

    # Board data
    board = data["board"]
    board_height = board["height"]
    board_width = board["width"]
    all_snakes = data["board"]["snakes"]

    # Move tiers
    preferred_moves = []
    possible_moves = ["up", "down", "left", "right"]
    risky_moves = []

    # Behaviour functions
    avoid_walls(my_head, board_height, board_width, possible_moves)
    avoid_bodies(my_head, all_snakes, possible_moves)
    head_to_head(my_snake, my_head, all_snakes, possible_moves, risky_moves, preferred_moves)
    risky_tails(my_head, all_snakes, possible_moves, risky_moves)

    if len(possible_moves) > 1:
        tunnel_detection(my_head, board, all_snakes, preferred_moves, possible_moves, risky_moves)

    if board["food"]:
        rasp(my_snake, my_head, board, preferred_moves, all_snakes, comfort_level)

    # Choose direction to move
    for move in copy(preferred_moves):
        if move not in possible_moves:
            delete_move(move, preferred_moves)

    print(f"Pref: {preferred_moves} | Pos: {possible_moves} | Risky: {risky_moves}")

    if len(preferred_moves) != 0:
        move = random.choice(preferred_moves)
    elif len(possible_moves) != 0:
        move = random.choice(possible_moves)
    elif len(risky_moves) != 0:
        move = random.choice(risky_moves)
    else:
        move = snail_squish(my_head, my_neck)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move

# Utility functions
def delete_move(move, possible_moves):

    if move in possible_moves:
        possible_moves.remove(move)

def tuple_me(square):

    return (square["x"], square["y"])

# If all else fails, hide inside your own shell
def snail_squish(my_head, my_neck):

    if my_neck["x"] < my_head["x"]:
        return "left"
    elif my_neck["x"] > my_head["x"]:
        return "right"
    elif my_neck["y"] < my_head["y"]:
        return "down"
    elif my_neck["y"] > my_head["y"]:
        return "up"

# Avoidance functions
def avoid_walls(my_head, board_height, board_width, possible_moves):

    if my_head["x"] == 0:
        delete_move("left", possible_moves)
    if my_head["x"] == board_width - 1:
        delete_move("right", possible_moves)
    if my_head["y"] == 0:
        delete_move("down", possible_moves)
    if my_head["y"] == board_height - 1:
        delete_move("up", possible_moves)

def avoid_bodies(my_head, all_snakes, possible_moves):

    for snake in all_snakes:
        body = snake["body"][:-1]

        if {"x": my_head["x"]-1, "y": my_head["y"]} in body:
            delete_move("left", possible_moves)
        if {"x": my_head["x"]+1, "y": my_head["y"]} in body:
            delete_move("right", possible_moves)
        if {"x": my_head["x"], "y": my_head["y"]-1} in body:
            delete_move("down", possible_moves)
        if {"x": my_head["x"], "y": my_head["y"]+1} in body:
            delete_move("up", possible_moves)

# Risky move functions
def head_to_head(my_snake, my_head, all_snakes, possible_moves, risky_moves, preferred_moves):

    for move in possible_moves:
        new_head = adjacent_square(my_head, move)

        for snake in all_snakes:
            head = snake["head"]
            move_tier = risky_moves

            if head == my_head:
                continue
            if snake["length"] < my_snake["length"]:
                move_tier = preferred_moves

            if{"x": new_head["x"]-1, "y": new_head["y"]} == head:
                move_tier.append(move)
                break
            if{"x": new_head["x"]+1, "y": new_head["y"]} == head:
                move_tier.append(move)
                break
            if{"x": new_head["x"], "y": new_head["y"]-1} == head:
                move_tier.append(move)
                break
            if{"x": new_head["x"], "y": new_head["y"]+1} == head:
                move_tier.append(move)
                break

    for move in risky_moves:
        delete_move(move, possible_moves)

def risky_tails(my_head, all_snakes, possible_moves, risky_moves):

    for move in possible_moves:
        new_head = adjacent_square(my_head, move)

        for snake in all_snakes:
            tail = snake["body"][-1]

            if{"x": new_head["x"], "y": new_head["y"]} == tail:
                risky_moves.append(move)
                break

    for move in risky_moves:
        delete_move(move, possible_moves)

def adjacent_square(my_head, direction):

    match direction:
        case "left": return {"x": my_head["x"]-1, "y": my_head["y"]}
        case "right": return {"x": my_head["x"]+1, "y": my_head["y"]}
        case "down": return {"x": my_head["x"], "y": my_head["y"]-1}
        case "up": return {"x": my_head["x"], "y": my_head["y"]+1}

def tunnel_detection(my_head, board, all_snakes, preferred_moves, possible_moves, risky_moves):

    tunnel_lengths = []
    for move in possible_moves:
        tunnel_lengths.append(flood_fill(my_head, board, all_snakes, move))
    cutoff = mean(tunnel_lengths)
    print(f"Average length: {cutoff}")

    for move, tunnel_length in zip(possible_moves, tunnel_lengths):
        print(f"Move: {move} | Length: {tunnel_length}")
        if tunnel_length < cutoff:
            print(f"Risky direction: {move} | Length: {tunnel_length}")
            risky_moves.append(move)
    
    for move in risky_moves:
        delete_move(move, possible_moves)
    

def flood_fill(my_head, board, all_snakes, move):
    
    target = adjacent_square(my_head, move)
    to_visit = [target]
    visited = set()

    while to_visit:
        current_square = to_visit.pop()
        visited.add(tuple_me(current_square))

        for direction in ["left", "right", "down", "up"]:
            next_target = adjacent_square(current_square, direction)

            if tuple_me(next_target) not in visited:
                if empty_square_check(next_target, board["width"], board["height"], all_snakes):
                    to_visit.append(next_target)
    
    return len(visited)


def empty_square_check(square, board_width, board_height, all_snakes):

    #Check if square is out of bounds
    if square["x"] < 0 or square["x"] >= board_width or square["y"] < 0 or square["y"] >= board_height:
        return False
    
    #Check if square is inside a snake
    for snake in all_snakes:
        body = snake["body"]

        if square in body:
            return False

    return True

# Preferable move functions
def rasp(my_snake, my_head, board, preferred_moves, all_snakes, comfort_level):

    my_health = my_snake["health"]
    food = board["food"]
    crumb_map = sorted(food, key=lambda crumb: (abs(my_head["x"] - crumb["x"]) + abs(my_head["y"] - crumb["y"])))

    # Display locations of all food on map
    """
    for crumb in food:
        crumb_dist = (abs(my_head["x"] - crumb["x"]) + abs(my_head["y"] - crumb["y"]))
        print(f"Crumb Map: {crumb_dist}{crumb_map}")
    """

    nearest_crumb = crumb_map[0]


    snake_lengths = sorted(all_snakes, key=lambda snake: snake["length"])
    shortest_snake = snake_lengths[0]
    print(f"Shortest Snake: {shortest_snake['name']} | Health: {shortest_snake['health']}")

    if (len(all_snakes) > 1 and shortest_snake == my_snake) or my_health < comfort_level:
        if my_head["x"] > nearest_crumb["x"]:
            preferred_moves.append("left")
        if my_head["x"] < nearest_crumb["x"]:
            preferred_moves.append("right")
        if my_head["y"] > nearest_crumb["y"]:
            preferred_moves.append("down")
        if my_head["y"] < nearest_crumb["y"]:
            preferred_moves.append("up")
