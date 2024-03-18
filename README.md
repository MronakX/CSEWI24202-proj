# CSE202WI24-proj

This is a project repo for CSE202, winter 2024.

We focus on solving pathfinding problems in Minecraft, a well-known sandbox game.

## Benchmark

credit: Yuchen, [https://github.com/DuckDuckWhaleUCSD](https://github.com/DuckDuckWhaleUCSD)

The Minecraft map data is under the `benchmark` folder. We have a manually designed `simple` which consists of 11 blocks, and four other benchmarks `bridge`, `road`, `skyblock`, `superflat` imported from real Minecraft maps by using a custom Minecraft client. The client prefers not to be open-sourced and thereby not presented here.

#### Example

|            simple            |            bridge            |           road           |             skyblock             |             superflat             |
| :--------------------------: | :--------------------------: | :----------------------: | :------------------------------: | :--------------------------------: |
| ![simple](./assets/simple.png) | ![bridge](./assets/bridge.png) | ![road](./assets/road.png) | ![skyblock](./assets/skyblock.png) | ![superflat](./assets/superflat.png) |

## Stateful A* pathfinding

credit: Dawei Guo, [https://github.com/MronakX](https://github.com/MronakX)


The modified A* algorithm with resource constraint is implemented in `stateful-pathfind.ipynb`, where we also implemented a baseline ordinary A* algorithm.


Modify the following line to whatever benchmark you want to test. Also, customize the starting point and goal point to adapt the data.

```
world_txt_filename = 'benchmark/superflat/world-dump.txt'
```

#### Path Example (on x-y plane)

##### Simple

|           A*           |       Stateful A*       |
| :---------------------: | :---------------------: |
| ![](./assets/ord_sqr.png) | ![](./assets/res_sqr.png) |

##### superflat

|            A*            |       Stateful A*       |
| :----------------------: | :----------------------: |
| ![](./assets/ord_path.png) | ![](./assets/res_path.png) |

## Realtime update

credit: Yulin Liu [Yulin Liu&#39;s github page](https://github.com/liuyulinn)

We implement a mimic "real-time update" in RealTimeGraph class in real_time_builder.py and test cases in plot_path.py

Results:

| ![bridge](./assets/plot_bridge.png)     | ![skyblock](./assets/plot_skyblock.png)    |
| ------------------------------------- | ---------------------------------------- |
| ![super flat](./assets/plot_simple.png) | ![super flat](./assets/plot_superflat.png) |
