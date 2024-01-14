from typing import Tuple

def gen_state (yellow_pos: Tuple[int, int], blue_pos: Tuple[int, int]) -> str:
  yellow_x, yellow_y = yellow_pos
  blue_x, blue_y = blue_pos
  return f"X{yellow_x}Y{yellow_y}_X{blue_x}Y{blue_y}"

def prefix_if_uncontrollable(x: int, y: int, event: str) -> str:
  return "UNC_" + event if x == 1 and y == 1 else event


def generate_moves(rows: int, columns: int):
  moves = {}

  # Mosse del giallo

  for yellow_index in range(rows * columns):
    yellow_x = yellow_index % 5
    yellow_y = int(yellow_index / 5)

    for blue_index in range(rows * columns):
      if yellow_index == blue_index:
        continue
      blue_x = blue_index % 5
      blue_y = int(blue_index / 5)

      key = gen_state((yellow_x, yellow_y), (blue_x, blue_y))
      if key not in moves:
        moves[key] = []

      # Muovi verso l'alto
      if yellow_y > 0 and (blue_y != yellow_y - 1 or blue_x != yellow_x):
        moves[key].append(f"edge {prefix_if_uncontrollable(yellow_x, yellow_y, 'UP_Y')} goto {gen_state((yellow_x, yellow_y - 1), (blue_x, blue_y))}")

      # Muovi verso il basso
      if yellow_y < rows - 1 and (blue_y != yellow_y + 1 or blue_x != yellow_x):
        moves[key].append(f"edge {prefix_if_uncontrollable(yellow_x, yellow_y, 'DOWN_Y')} goto {gen_state((yellow_x, yellow_y + 1), (blue_x, blue_y))}")

      # Muovi a sinistra
      if yellow_x > 0 and (blue_x != yellow_x - 1 or blue_y != yellow_y):
        moves[key].append(f"edge {prefix_if_uncontrollable(yellow_x, yellow_y, 'LEFT_Y')} goto {gen_state((yellow_x - 1, yellow_y), (blue_x, blue_y))}")

      # Muovi a destra
      if yellow_x < columns - 1 and (blue_x != yellow_x + 1 or blue_y != yellow_y):
        moves[key].append(f"edge {prefix_if_uncontrollable(yellow_x, yellow_y, 'RIGHT_Y')} goto {gen_state((yellow_x + 1, yellow_y), (blue_x, blue_y))}")

  # Mosse del blu
        
  for blue_index in range(rows * columns):
    blue_x = blue_index % 5
    blue_y = int(blue_index / 5)

    for yellow_index in range(rows * columns):
      if yellow_index == blue_index:
        continue
      yellow_x = yellow_index % 5
      yellow_y = int(yellow_index / 5)

      key = gen_state((yellow_x, yellow_y), (blue_x, blue_y))

      # Muovi verso l'alto
      if blue_y > 0 and (blue_y - 1 != yellow_y or blue_x != yellow_x):
        moves[key].append(f"edge {prefix_if_uncontrollable(blue_x, blue_y, 'UP_B')} goto {gen_state((yellow_x, yellow_y), (blue_x, blue_y - 1))}")

      # Muovi verso il basso
      if blue_y < rows - 1 and (blue_y + 1 != yellow_y or blue_x != yellow_x):
        moves[key].append(f"edge {prefix_if_uncontrollable(blue_x, blue_y, 'DOWN_B')} goto {gen_state((yellow_x, yellow_y), (blue_x, blue_y + 1))}")

      # Muovi a sinistra
      if blue_x > 0 and (blue_x - 1 != yellow_x or blue_y != yellow_y):
        moves[key].append(f"edge {prefix_if_uncontrollable(blue_x, blue_y, 'LEFT_B')} goto {gen_state((yellow_x, yellow_y), (blue_x - 1, blue_y))}")

      # Muovi a destra
      if blue_x < columns - 1 and (blue_x + 1 != yellow_x or blue_y != yellow_y):
        moves[key].append(f"edge {prefix_if_uncontrollable(blue_x, blue_y, 'RIGHT_B')} goto {gen_state((yellow_x, yellow_y), (blue_x + 1, blue_y))}")

  return moves

if __name__ == "__main__":

  # Genera tutte le mosse possibili
  all_moves = generate_moves(3, 5)

  with open('requirement3_test.cif', 'w') as file:
    file.write('import "../plant/events.cif";\n')
    file.write('\n')
    file.write('//XYellowYYellow_XBlueYBlue\n')
    file.write('requirement Requirement3:\n')
    for key in all_moves:
      if key == gen_state((0, 0), (3, 1)):
        file.write(f"    location {key}: initial; marked;\n")
      else:
        file.write(f"    location {key}: marked;\n")
      for value in all_moves[key]:
        file.write(f"        {value};\n")
      file.write("\n")
    file.write("end\n")

