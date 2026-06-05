#!/usr/bin/env python3
"""
Extract map -> base_link from a rosbag's TF tree, sampled at scan timestamps,
into a TUM trajectory file consumable by evo.
"""
import argparse
import rosbag
import rospy
import tf2_ros
import tf2_py


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bag')
    ap.add_argument('out_tum')
    ap.add_argument('--map',  default='map')
    ap.add_argument('--base', default='base_link')
    ap.add_argument('--scan', default='/scan')
    args = ap.parse_args()

    bag = rosbag.Bag(args.bag, 'r')

    # Cache large enough to hold the full bag's TFs
    cache_s = (bag.get_end_time() - bag.get_start_time()) + 100.0
    buf = tf2_ros.Buffer(cache_time=rospy.Duration(cache_s))

    # 1) Pre-load every TF in the bag (dynamic + static)
    print('Loading TFs...')
    for topic, msg, _ in bag.read_messages(topics=['/tf', '/tf_static']):
        is_static = (topic == '/tf_static')
        for tf in msg.transforms:
            if is_static:
                buf.set_transform_static(tf, 'rosbag')
            else:
                buf.set_transform(tf, 'rosbag')

    # 2) For each scan, look up map -> base_link at the scan's header stamp
    print(f'Sampling {args.map} -> {args.base} at {args.scan} stamps...')
    n_ok, n_fail = 0, 0
    with open(args.out_tum, 'w') as f:
        for _, msg, _ in bag.read_messages(topics=[args.scan]):
            try:
                tf = buf.lookup_transform(args.map, args.base, msg.header.stamp)
            except (tf2_py.LookupException,
                    tf2_py.ExtrapolationException,
                    tf2_py.ConnectivityException):
                n_fail += 1
                continue
            t = tf.transform.translation
            r = tf.transform.rotation
            f.write(f"{msg.header.stamp.to_sec():.9f} "
                    f"{t.x:.9f} {t.y:.9f} {t.z:.9f} "
                    f"{r.x:.9f} {r.y:.9f} {r.z:.9f} {r.w:.9f}\n")
            n_ok += 1

    bag.close()
    print(f'Wrote {n_ok} poses, skipped {n_fail}')


if __name__ == '__main__':
    main()
