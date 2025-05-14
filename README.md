# rainbow-pyv

this monorepo contains games that are compatible with `pyved-engine` version `25.4a1` and above


## special features

Remarkable changes if we compare to previous
`pyved-engine` versions are:

- for regular game bundles (non frozen), the ability to run the game without embedding a `launch_game.py` redundant script
- the ability to use letterbox auto-scaling
- *(most importantly)* the ability to run a server+a game client.

For example, one can use:

```
pyv-cli serve TheGrid --host=localhost --port=12881
```

And then:
```
pyv-cli play TheGrid --host=localhost --port=12881 --player=1
```

## future games: what to expect?

In the long run, we hope producing 15 games:

| game name          | multiplayer | real-time | localStorage | story/solo campaign | monetization | tournament mode |
|:-------------------|:-----------:|:---------:|:------------:|:-------------------:|:------------:|:---------------:|
| 2048               |             |           |      x       |                     |              |                 |
| Blokuman           |             |           |      x       |                     |              |                 |
| Bomberman 2030     |      x      |     x     |              |                     |     prem     |                 |
| Dice Dominion      |      x      |           |              |                     |    stake     |        x        |
| Lucky Stamps       |             |           |              |                     |     gmbl     |                 |
| Mythrandian Guard  |      x      |           |              |          x          |     prem     |                 |
| Neon Samurai       |      x      |     x     |              |                     |    stake     |        x        |
| Neurochrome        |             |     x     |      x       |          x          |     DLC      |                 |
| Py Chess Online    |      x      |           |              |                     |    stake     |        x        |
| Ravenous Caves     |             |           |      x       |          x          |              |                 |
| Retro Starfighter  |             |     x     |      x       |                     |    stake     |        x        |
| Skyforce Combatant |             |     x     |      x       |          x          |     DLC      |                 |
| UTH Poker          |             |           |              |                     |     gmbl     |                 |
| Wheel Spinner      |             |           |              |                     |     gmbl     |                 | 
| Zombie Survivor    |             |           |      x       |                     |              |                 |          

- **gmbl:** gambling
- **stake:** tournament fee
- **prem:** premium in-game items or cosmetics

Connecting games to the challenge system (rankings+specific API) will be done later.
We will need to track the MAU (monthly active user) per game.
