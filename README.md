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

## games: what to expect?

In the long run, we may achieve running 14 games:

- 2048
- Blokuman
- Bomberman 2030
- Dice Dominio
- Lucky Stamps
- Mythrandian Guard
- Neon Samurai
- Py Chess Online
- Ravenous Caves
- Retro Starfighter
- Skyforce Combatant
- Wheel Spinner
- Zombie Survivor
