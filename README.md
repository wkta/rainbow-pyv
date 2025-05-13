# rainbow-pyv

this monorepo contains games that are compatible with `pyved-engine` version `25.4a1` and above


## special features

The big change if we compare to previous `pyved-engine` versions is:
- the ability to use letterbox auto-scaling
- the ability to run a server+a game client.
To do so, for example one could use:

```
pyv-cli serve TheGrid --host=localhost --port=12881
```

And then:
```
pyv-cli play TheGrid --host=localhost --port=12881 --player=1
```
