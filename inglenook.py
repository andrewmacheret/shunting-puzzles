from random import shuffle
from itertools import *
from collections import *
from heapq import *
import sys

track_sizes = (5,3,3)
move_size = 3
goal_size = 5
valid_destinations = [[j for j in range(len(track_sizes)) if j != i] for i in range(len(track_sizes))]

def is_goal(tracks, goal):
  return goal in tracks

def produce_move(tracks, from_index, to_index, amount):
  tracks = list(map(list, tracks))
  shunt = []
  for _ in range(amount):
    shunt.append(tracks[from_index].pop())
  for _ in range(amount):
    tracks[to_index].append(shunt.pop())
  return tuple(map(tuple, tracks))

def get_next_tracks(tracks):
  move_from = next(([(i, len(t) - s)] for i,t,s in zip(count(), tracks, track_sizes) if len(t) > s), zip(range(len(tracks)), repeat(1)))
  for i, min_move in move_from:
    max_move = min(move_size, len(tracks[i]))
    for j in valid_destinations[i]:
      for m in range(min_move, max_move+1):
        yield produce_move(tracks, i, j, m), (i, j, m)


def bfs(tracks, goal):
  seen = set()
  q = [(0, tracks, tuple())]

  while q:
    r, tracks, path = heappop(q)
    if is_goal(tracks, goal):
      print(r, 'moves' + '\n')
      return path

    seen.add(tracks)

    for next_tracks, move in get_next_tracks(tracks):
      if next_tracks not in seen:
        cost = (4 if path[-1][1] != move[0] else 2) if path else 3
        heappush(q, (r + cost, next_tracks, path + (move,)))

COLOR_RESET = '\33[0m'
COLORS = [
  '\33[30m', # loco
  '\33[31m',
  '\33[32m',
  '\33[33m',
  '\33[34m',
  '\33[35m',
  '\33[36m',
  '\33[92m',
  '\33[94m'
]

def colored_wagon(index):
  return f"{COLORS[0 if index == 'L' else index]}[{index}]{COLOR_RESET}"

def draw_tracks(tracks, loco, shunt):
  if loco >= 0:
    tracks = list(map(list, tracks))
    tracks[loco].append('L')
    tracks = tuple(map(tuple, tracks))
  else:
    shunt.append('L')

  t0,t1,t2 = tracks
  rails = [
    ['═══', '═══', '═══', '═══', '═══', '══╦', '╦══', '═══', '═══', '═══', '═══'],
    ['   ', '   ', '═══', '═══', '═══', '══╝', '║'],
    ['   ', '   ', '═══', '═══', '═══', '═══', '╝']
  ]
  for i,t in enumerate(tracks):
    for j,x in enumerate(t, 2 if i > 0 else 0):
      k = i if j < 6 else 0
      rails[k][j] = colored_wagon(x)
  for j,x in enumerate(shunt, 7):
    rails[0][j] = colored_wagon(x)
  return '\n'.join(''.join(r) for r in rails) + '\n'




def simulate(tracks, path):
  loco = -1
  shunt = []
  last_tracks = None
  last_shunt = None
  last_loco_to = None
  for i,j,m in path:
    last_tracks = tracks
    tracks = produce_move(tracks, i, j, m)
    loco_from = next(i for i, t1, t2 in zip(count(), last_tracks, tracks) if len(t1) > len(t2))
    loco_to = next(i for i, t1, t2 in zip(count(), last_tracks, tracks) if len(t1) < len(t2))
    diff = len(last_tracks[i]) - len(tracks[i])
    last_shunt = shunt
    shunt = list(last_tracks[i][-diff:])

    if last_loco_to != loco_from:
      print(draw_tracks(last_tracks, -1, []))
      print(draw_tracks(last_tracks, loco_from, []))


    last_tracks = list(map(list, last_tracks))
    for _ in shunt: last_tracks[loco_from].pop()
    last_tracks = tuple(map(tuple, last_tracks))

    print(draw_tracks(last_tracks, -1, shunt))

    print(draw_tracks(tracks, loco_to, []))

    last_loco_to = loco_to


def set_zeros(tracks):
  it = count(6)
  return tuple(tuple(x if x else next(it) for x in t) for t in tracks)



if __name__ == "__main__":
  goal = (1,2,3,4,5)

  if len(sys.argv) > 1:
    arrangement = tuple(map(int, sys.argv[1:]))
  else:
    # random
    arrangement = [1,2,3,4,5,0,0,0]
    shuffle(arrangement)
    arrangement = tuple(arrangement)
  initial_tracks = (
    arrangement[:track_sizes[0]],
    arrangement[track_sizes[0]:],
    tuple()
  )

  # initial_tracks = ((1, 2, 3, 4, 5), (6, 7, 8), ())
  filled_initial_tracks = set_zeros(initial_tracks)
  # print('initial_tracks:', filled_initial_tracks)
  # print()

  path = bfs(initial_tracks, goal)

  simulate(filled_initial_tracks, path)


