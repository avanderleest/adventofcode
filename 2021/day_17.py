import re
from xxlimited import new

with open('day_17_input_test.txt') as f:
  coordinates = []
  for line in f:
    line = line.split()
    for word in line:
      if word != 'target' and word != 'area:':
        value = re.split('\..|\,|\=', word)
        coordinates.append(value)

for list in coordinates:
  for item in list:
    if item == '':
      list.remove('')
print(coordinates)

class Target:
  def __init__(self, list_of_coordinates: list):
      self.min_x = int(list_of_coordinates[0][1])
      self.max_x = int(list_of_coordinates[0][2])
      self.min_y = int(list_of_coordinates[1][1])
      self.max_y = int(list_of_coordinates[1][2])

  def __get_distance(self, value: int, target_min, target_max):
    if target_min <= value <= target_max:
      return 0
    if value < target_min:
      return target_min - value
    if value > target_max:
      return value - target_max

  def distance_from_target(self, probe):
    x_distance = self.__get_distance(probe.current_position.x, self.min_x, self.max_x)
    y_distance = self.__get_distance(probe.current_position.y, self.min_y, self.max_y)
    return x_distance + y_distance

  def is_in_target(self, x_coord: int, y_coord: int):
    within_x = self.min_x <= x_coord <= self.max_x
    within_y = self.min_y <= y_coord <= self.max_y
    return within_x == True and within_y == True

class Coordinates:
  def __init__(self, x: int, y: int):
      self.x = x
      self.y = y

  def new_by_adding(self, v):
    return Coordinates(self.x + v.x, self.y + v.y)

class Velocity(Coordinates):
  def __init__(self, x: int, y: int):
      super().__init__(x, y)

  def apply_drag(self):
    x_is_negative = self.x < 0
    new_y_velocity = self.y - 1
    if x_is_negative:
      new_x_velocity = self.x + 1
    else:
      new_x_velocity = self.x - 1
    return Velocity(new_x_velocity, new_y_velocity)


class Probe:
  def __init__(self, initial_velocity_x, initial_velocity_y):
      self.initial_velocity = Velocity(initial_velocity_x, initial_velocity_y)
      # self.list_of_positions = [(0, 0)]
      # self.list_of_velocities = []
      self.current_velocity = self.initial_velocity
      self.current_position = Coordinates(0, 0)

  # This returns 0 if it hits the target otherwise returns the closest distance to the target
  def launch_towards(self, target: Target):
    last_distance_to_target = target.distance_from_target(self)
    while True:
      self.current_position = self.current_position.new_by_adding(self.current_velocity)
      print('Probe position is: ', self.current_position.x, ', ', self.current_position.y)
      new_distance_to_target = target.distance_from_target(self)
      print('New distance to target is: ', new_distance_to_target)
      self.current_velocity = self.current_velocity.apply_drag()
      # Check to see if we hit
      if new_distance_to_target == 0:
        return 0
      # are we still ascending to high point?
      if self.current_velocity.y > 0:
        continue
      # Have we passed it?
      if new_distance_to_target > last_distance_to_target:
        return last_distance_to_target
      last_distance_to_target = new_distance_to_target



class Simulator:
  def __init__(self) -> None:
      pass

target = Target(coordinates)
probe = Probe(7, 2)
print('The closest we got was', probe.launch_towards(target))