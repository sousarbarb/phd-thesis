# distance-maps/iilabs3d/README.md

## IILABS3D Dataset

```py
MAX_TIME_SYNC_DIFF = 0.01
DELTA = 10
DELTA_UNIT = metrics.Unit.meters
```

## Evaluation
```sh
evo_rpe tum ground_truth.tum <odom trajectory file>.tum --align --pose_relation trans_part --delta 10.0 --delta_unit m --t_max_diff 0.01 --save_results <results log file>.zip
evo_rpe tum ground_truth.tum <odom trajectory file>.tum --align --pose_relation angle_deg --delta 10.0 --delta_unit m --t_max_diff 0.01 --save_results <results log file>.zip
```
