
# Hacking Version 9
# This is a text-based password guessing game that displays a 
# list of potential computer passwords. The player is allowed 
# 1 attempt to guess the password. The game indicates that the 
# player failed to guess the password correctly.

import pygame, sys, string
from pygame.locals import *
from random import randint
from time import sleep

# state
attempts = 4
black = (0, 0, 0)
green = (0, 255, 0)
padding = 10
game_title = 'HACKING'
random_characters = '!@#$%^*()-+=~[]{}'
header_strings = ['DEBUG MODE', str(attempts) + ' ATTEMPT(S) LEFT', '']
password_strings = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE', 'HEARING', 'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING']
lockout_warning_string = '*** LOCKOUT WARNING ***'
password_prompt_string = 'Enter a password >'

ctx = {
  "attempts": attempts,
  "font_name": 'courier',
  "font_size": 18,
  "font_color": green,
  "bg_color": black,
  "password": 'HUNTING',
  "guess_list": []
}

def create_window(ctx):
  pygame.display.init()
  pygame.font.init()
  pygame.display.set_caption(game_title)
  window = pygame.display.set_mode((600, 500), 0, 0)
  window.fill(ctx["bg_color"])
  font = pygame.font.SysFont(ctx["font_name"], ctx["font_size"], True)
  pygame.display.update()
  return (window, font)

def write_string(ctx, string, x_pos, line_y):
  y_pos = (ctx["font"].size('')[1] * line_y)
  ctx["window"].blit(
    ctx["font"].render(string, True, ctx["font_color"], ctx["bg_color"]),
    (x_pos, y_pos)
  )
  pygame.display.update()

def display_header(ctx, header_strings, y_start = 0):
  for string in header_strings:
    write_string(
      ctx,
      string,
      x_pos = 0 + padding,
      line_y = y_start
    )
    y_start += 1
  write_string(ctx, '', x_pos = 0 + padding, line_y = y_start)

def obfuscate_string(string):
  output = ''
  split_before_index = randint(0, 12)
  for _ in range(split_before_index):
    random_char_index = randint(0, len(random_characters) - 1)
    output += random_characters[random_char_index]
  output += string
  for _ in range(13 - split_before_index):
    random_char_index = randint(0, len(random_characters) - 1)
    output += random_characters[random_char_index]
  return output

def display_passwords(ctx, password_strings, y_start = 3):
  for password in password_strings:
    obfuscated_password = obfuscate_string(password)
    write_string(
      ctx,
      obfuscated_password,
      x_pos = 0 + padding,
      line_y = y_start
    )
    y_start += 1
    write_string(ctx, '', x_pos = 0 + padding, line_y = y_start)

def prompt_user(ctx, prompt_string, x_pos, line_y):
  user_input = []
  write_string(ctx, prompt_string, x_pos = x_pos, line_y = line_y)
  key_index = -1
  while True:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        # return key
        if event.unicode == "\r":
          return ''.join(user_input)
        # right key
        elif (event.key == 275) & (key_index < len(user_input) - 1):
          key_index += 1
        # left key
        elif (event.key == 276) & (key_index > -1):
          key_index -= 1
        # delete key
        elif (event.key == 8) & (len(user_input) > 0) & (key_index > -1):
          if key_index == len(user_input) - 1:
            user_input = user_input[:-1]
          else:
            del user_input[key_index:key_index + 1]
          key_index -= 1
        elif (event.unicode in string.printable) & (len(user_input) < 7) & (event.key not in (8, 42, 275, 276, 304)):
          user_input.insert(key_index + 1, event.unicode)
          key_index += 1
        write_string(ctx, prompt_string + '       ', x_pos = x_pos, line_y = line_y)
        write_string(ctx, str(prompt_string + ''.join(user_input)), x_pos = x_pos, line_y = line_y)

def update_header_attempts(ctx):
    write_string(ctx, str(ctx["attempts"]) + ' ATTEMPT(S) LEFT', x_pos = 0 + padding, line_y = 1)

def check_warning(ctx, warning_string):
  if ctx["attempts"] == 1:
    x_pos = ctx["window"].get_width() - (ctx["font"].size(warning_string)[0] + padding)
    line_y = (ctx["window"].get_height() // ctx["font"].size('')[1]) - 1.2
    write_string(ctx, warning_string, x_pos = x_pos, line_y = line_y)

def display_hint(ctx, guess):
    line_y = (len(ctx["guess_list"]) * 2)
    ctx["guess_list"].append(guess)
    first_string = guess + ' INCORRECT'
    letters_correct = 0
    for index in range(min(len(guess), len(ctx["password"]))):
      if guess[index] == ctx["password"][index]:
        letters_correct += 1
    second_string = str(letters_correct) + '/' + str(len(ctx["password"])) + ' IN MATCHING POSITIONS'
    x_pos = ctx["window"].get_width() - (ctx["font"].size(second_string)[0] + padding)
    write_string(ctx, first_string, x_pos = x_pos, line_y = line_y)
    write_string(ctx, second_string, x_pos = x_pos, line_y = line_y + 1)

def handle_guesses(ctx, prompt_string, warning_string):
  y_start = 18
  guess = prompt_user(ctx, prompt_string, x_pos = 0 + padding, line_y = y_start)
  while guess != ctx["password"]:
    ctx["attempts"] -= 1
    update_header_attempts(ctx)
    display_hint(ctx, guess)
    y_start += 1
    pygame.display.update()
    if ctx["attempts"] == 0:
      break
    check_warning(ctx, warning_string)
    guess = prompt_user(ctx, prompt_string, x_pos = 0 + padding, line_y = y_start)
  return guess

def compute_outcome_width_coordinate(ctx, string):
  x_space = ctx["window"].get_width() - ctx["font"].size(string)[0]
  return x_space // 2

def compute_outcome_height_coordinate(ctx):
  num_of_outcome_lines = 7
  y_space = (ctx["window"].get_height() // ctx["font"].size('')[1]) - num_of_outcome_lines
  line_y = y_space // 2
  return line_y

def prompt_to_exit(ctx, prompt_string, x_pos, line_y):
  write_string(ctx, prompt_string, x_pos = x_pos, line_y = line_y)
  while True:
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.unicode == "\r":
          pygame.quit()
          sys.exit()

def display_outcome(ctx, guess):
  ctx["window"].fill(ctx["bg_color"])
  won_game = (guess == ctx["password"])
  if won_game:
    outcome_line2 = 'EXITING DEBUG MODE'
    outcome_line3 = 'LOGIN SUCCESSFUL - WELCOME BACK'
    prompt_string = 'PRESS ENTER TO CONTINUE'
  else: 
    outcome_line2 = 'LOGIN FAILURE - TERMINAL LOCKED'
    outcome_line3 = 'PLEASE CONTACT AN ADMINISTRATOR'
    prompt_string = 'PRESS ENTER TO EXIT'
  
  outcome_strings = [guess, outcome_line2, outcome_line3]

  y_start = compute_outcome_height_coordinate(ctx)

  for string in outcome_strings:
    x_pos = compute_outcome_width_coordinate(ctx, string)
    write_string(ctx, string, x_pos = x_pos, line_y = y_start)
    y_start += 1
    write_string(ctx, '', x_pos = x_pos, line_y = y_start)
    y_start += 1

  x_pos = compute_outcome_width_coordinate(ctx, prompt_string)
  prompt_to_exit(ctx, prompt_string, x_pos, y_start)

def main():
  (ctx["window"], ctx["font"]) = create_window(ctx)
  display_header(ctx, header_strings)
  display_passwords(ctx, password_strings)
  final_guess = handle_guesses(ctx, password_prompt_string, lockout_warning_string)
  display_outcome(ctx, final_guess)

main()
