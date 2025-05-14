# Mythrandian Guard: game concept
the game is a mix between two game genres:
* idle game
* resource management


## Resources
There are 4 resources that the player can manage (earn, hoarding, spending):
* gold 
* reputation points
* energy (limited supply, e.g. 3 pts per 24 hours)
* mana (limited capacity)


## Collectible
Player can collect stuff from quests, or buy stuff at the shop
* Artifact parts (quests only)
* Equipment (pimp your avatar, can own 1 equipment item at a time)
* Lackeys, can own 0 to 15


## Affordances (and how to communicate possible actions)
First possible action: build structures. Benefits are:
* passive gold income
* (semi-passive) reputation income
* (semi-passive) mana regen
* increased mana supply
* new options: Pvp (attack or defend), quests
* increase number of parallel quests (1->2)


## Characters stats
Both lackeys and the avatar are game characters. So they all share 5 primitive
stats:
* level: 1-59
* endurance: 1-10
* initiative: 1-10
* shadow warrior: 0/1 (flag)
* willpower: 1-100

Secondary stats that are used in combat:
* damage, based on level (level 1 => value 5)
* max hp, based on both endurance and level (level 1 & en 1 => value: 45)
* fighter's position, based on both initiative and level


## Magic
There are 5 spells in the game that gives a temporary buff.
At the beginning only one spell is unlocked, to unlock the 4 others you
would need to collect artifact parts and complete a collection.

* initial spell
  * *Magical Workforce*: (for 5 minutes) your lackeys receive +100% willpower


* future spells
  * *Epic confidence*: (for 2 hours) you can send a minimum of 2 fighters (instead of 3) to complete a mission
  * *Mana frenzy*: (for 12 hours) your mana supply is increased by 4
  * *Overwhelming Force*: (for 2 minutes) any fighter sent on mission has level+3
  * *Glowing armor*: (for 2 minutes) any fighter sent on mission has endurance+2
  * *Lion heart*: (instant) replace a random mission by an elite one


## Missions
Three difficulty levels:
* Not too rough - low chance to get a fight (20%)
* Hurt me plenty - 50% chance to get a fight
* Ultra-violence - 100% chance to get a fight, drops an artifact part

In general sending a balanced team: DD* + Tank + Support should give a good
success rate.\
(* DD stands for Damage Dealer)

Check `fightsim_logic.py` for detailled information.
