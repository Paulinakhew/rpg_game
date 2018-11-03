#!/usr/bin/env python3

import view as v
import os
from random import randint
import model as m

def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Inventory : ' + str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  #display the user's current health points
  print('Your current HP: ' + str(health_points))
  print("---------------------------")

#an inventory, which is initially empty
inventory = []

#a dictionary linking a room to other rooms
rooms = {
  'Hall' : { 
        'south' : 'Kitchen',
        'east' : 'Dining Room',
        'item' : 'key',
        'north' : 'Office',
        'west' : 'Closet'
      },
  'Office' : {
        'south' : 'Hall',
        'east' : 'Living Room',
        'up' : 'Attic',
        'item' : 'ladder',
        'west' : 'Bedroom'
      },
  'Kitchen' : {
        'north' : 'Hall',
        'item' : 'monster',
        'east' : 'Games Room'
      },
  'Dining Room' : {
        'west' : 'Hall',
        'south' : 'Games Room',
        'north' : 'Living Room',
        'east' : 'Washroom'
      },
  'Living Room' : {
        'south' : 'Dining Room',
        'item' : 'monster',
        'west' : 'Office',
        'item' : 'monster',
        'gift' : 'health potion'
      },
  'Games Room' : {
        'north' : 'Dining Room',
        'west' : 'Kitchen',
        'item' : 'potion',
        'east' : 'Garden'
      }, 
  'Washroom' : {
        'west' : 'Dining Room',
        'south' : 'Garden'
      },
  'Garden' : {
        'west' : 'Games Room',
        'north' : 'Washroom'
      },
  'Closet' : {
        'east' : 'Hall',
        'north' : 'Bedroom'
      },
  'Attic' : {
        'down' : 'Office',
        'item' : 'sword'
      },
  'Bedroom' : {
        'south' : 'Closet',
        'east' : 'Office',
        'item' : 'monster',
        'north' : 'Cellar'
      },
  'Cellar' : {
        'south' : 'Bedroom',
        'item' : 'monster',
        'gift' : 'health potion'
  }
}

#start the player in the Hall
currentRoom = 'Hall'

v.clear_screen()
v.showInstructions()

health_points = 25

#loop forever
while health_points > 0:
  showStatus()
  #get the player's next 'move'
  #.split() breaks it up into an list array
  #eg typing 'go east' would give the list:
  #['go','east']
  move = ''
  while move == '':  
    move = input('>')
    move = move.lower().split()

  #if they type 'go' first
  if move[0] == 'go':
    #check that they are allowed wherever they want to go
    if move[1] in rooms[currentRoom]:
      #set the current room to the new room
      currentRoom = rooms[currentRoom][move[1]]
    #there is no door (link) to the new room
    else:
        print('can\'t go that way!')

  #if they try to drink the health potion
  if move[0] == 'drink' and move[1] == 'potion':
    #check that they have a health potion in their inventory
    if 'health potion' in inventory:
      #adds 25 HP through calling the function in model
      health_points = m.add_health(health_points)
      print('Congrats! Your health is now {} HP.'.format(health_points))
      #remove the health potion from inventory once used
      inventory.remove('health potion')
    else:
      print('can\'t drink potion!')

  #if they type 'get' first
  if move[0] == 'get' :
    #player has to solve a riddle in order to get the sword
    if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and move[1] == 'sword':
      v.riddle()
      riddle_answer = input('>')
      riddle_answer = riddle_answer.lower()
      if riddle_answer == 'silence':
        print("That is correct. Congratulations!")
        #add the item to their inventory
        inventory += [move[1]]
        #display a helpful message
        print(move[1] + ' got!')
        #delete the item from the room
        del rooms[currentRoom]['item']
        #otherwise, if the item isn't there to get
      else:
        print("That is the wrong answer.")
    #the ladder is only there to display that the user can travel up and down
    elif "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item'] and move[1] == 'ladder':
      print("can't get ladder!")
    #if the room contains an item, and the item is the one they want to get
    elif "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      #add the item to their inventory
      inventory += [move[1]]
      #display a helpful message
      print(move[1] + ' got!')
      #delete the item from the room
      del rooms[currentRoom]['item']
    #otherwise, if the item isn't there to get
    else:
      #tell them they can't get it
      print('Can\'t get ' + move[1] + '!')

  #if the user has a sword in their inventory, the game does not end right away for them
  if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item'] and 'sword' in inventory:
    showStatus()
    move = input('There is a monster in the room! \nUse your sword to fight it by typing \'fight monster.\'\n')
    if move == 'fight monster':
      while 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
      #generate a random number
        number = randint(1,2)
        if number == 1:
          health_points = m.fight_monster(health_points)
          print('The monster attacked you! You are now at {} HP.'.format(health_points))
          if health_points == 0:
            print('A monster has got you... GAME OVER!')
            os.system('cowsay -d PLEASE TRY AGAIN')
            break
            break
            break
            break
        elif number == 2:
          print('Killed the monster! ')
          del rooms[currentRoom]['item']
    #if the user inputs something other than 'fight monster'
    else:
      print('A monster has got you... GAME OVER!')
      os.system('cowsay -d PLEASE TRY AGAIN')
      break
  #player loses if they enter a room with a monster
  elif 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
    print('A monster has got you... GAME OVER!')
    os.system('cowsay -d PLEASE TRY AGAIN')
    break

  #player wins if they get to the garden with a key and a potion
  if currentRoom == 'Garden' and 'key' in inventory and 'potion' in inventory:
    print('You escaped the house... YOU WIN!')
    break

  #monster drops potion when you kill it
  if 'gift' in rooms[currentRoom] and 'item' not in rooms[currentRoom]:
    print('The monster has dropped a gift!')
    user_input = input(">")
    if user_input == 'get gift':
      inventory += ['health potion']
      print('Congrats! You now have a health potion.\nTo use it, type \'drink potion\'')
      del rooms[currentRoom]['gift']
