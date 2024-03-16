from real_time_builder import RealTimeGraph
import argparse

parser = argparse.ArgumentParser(description='Real Time Graph')
parser.add_argument('--name', type=str, default='superflat', help='file path')
args = parser.parse_args()

if args.name == 'superflat':
    rtb = RealTimeGraph('benchmark/superflat/world-dump.txt', position=(288, -464, -61), target=(313, -404, -61), view=5)
    rtb_static = RealTimeGraph('benchmark/superflat/world-dump.txt', position=(288, -464, -61), target=(313, -404, -61), update=False)

    path, cost = rtb.control_agent()
    print('------update-----------')
    print('path', path)
    print('cost', cost)

    path, cost = rtb_static.a_star_search()
    print('------static-----------')
    print('path', path)
    print('cost', cost)
elif args.name == 'simple':
    rtb = RealTimeGraph('benchmark/simple/world-dump.txt', position=(0, 0, 0), target=(2, 2, 0), view=1)
    rtb_static = RealTimeGraph('benchmark/simple/world-dump.txt', position=(0, 0, 0), target=(2, 2, 0), update=False)

    path, cost = rtb.control_agent()
    print('------update-----------')
    print('path', path)
    print('cost', cost)

    path, cost = rtb_static.a_star_search()
    print('------static-----------')
    print('path', path)
    print('cost', cost)
elif args.name == 'bridge':
    rtb = RealTimeGraph('benchmark/bridge/world-dump.txt', position=(-6, 0, 60), target=(6, 6, 0), view=3)
    rtb_static = RealTimeGraph('benchmark/bridge/world-dump.txt', position=(-6, 0, 0), target=(6, 6, 0), update=False)

    path, cost = rtb.control_agent()
    print('------update-----------')
    print('path', path)
    print('cost', cost)

    path, cost = rtb_static.a_star_search()
    print('------static-----------')
    print('path', path)
    print('cost', cost)
elif args.name == 'skyblock':
    rtb = RealTimeGraph('benchmark/skyblock/world-dump.txt', position=(5, 5, 60), target=(0, 0, 60), view=3)
    rtb_static = RealTimeGraph('benchmark/skyblock/world-dump.txt', position=(5, 5, 60), target=(0, 0, 60), update=False)

    path, cost = rtb.control_agent()
    print('------update-----------')
    print('path', path)
    print('cost', cost)

    path, cost = rtb_static.a_star_search()
    print('------static-----------')
    print('path', path)
    print('cost', cost)