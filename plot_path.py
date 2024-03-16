import matplotlib.pyplot as plt
import numpy as np
from real_time_builder import RealTimeGraph
import argparse

parser = argparse.ArgumentParser(description='Real Time Graph')
parser.add_argument('--name', type=str, default='superflat', help='file path')
args = parser.parse_args()

if args.name == 'bridge':
    file_path = 'benchmark/bridge/world-dump.txt'
    position = (-6, 0, 60)
    target = (6, 6, 60)
elif args.name == 'skyblock':
    file_path = 'benchmark/skyblock/world-dump.txt'
    position = (0, 0, 60)
    target = (5, 5, 60)
elif args.name == 'simple':
    file_path = 'benchmark/simple/world-dump.txt'
    position = (0, 0, 0)
    target = (2, 2, 0)
elif args.name == 'superflat':
    file_path = 'benchmark/superflat/world-dump.txt'
    position = (288, -464, -61)
    target = (313, -404, -61)


paths = []
if args.name == 'superflat':
    view_range = [5]
else:
    view_range = [1, 3, 5]
for view in view_range:
    rtb = RealTimeGraph(file_path, position=position, target=target, view=view)
    path, cost = rtb.control_agent()
    paths.append(path)

fig, ax = plt.subplots()
for i in range(len(paths)):
    if paths[i] is None:
        continue
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    ax.plot(x, y, label=f'view: {view_range[i]}')

rtb_static = RealTimeGraph(file_path, position=position, target=target, update=False)
path, cost = rtb_static.a_star_search()
ax.plot([p[0] for p in path], [p[1] for p in path], label='static')
print('static cost', cost)
# plt.title("Ordinary A*")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title(f'{args.name}')
ax.legend()



plt.savefig(f'plot_{args.name}.png', dpi=600)
plt.show()
