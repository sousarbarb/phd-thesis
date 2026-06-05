# data/slam/README.md
```sh
pip install scipy matplotlib pillow numpy iilabs3d-toolkit

# IILABS3D W/ EVO: (nav_a_diff)
# RicoSLAM
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_diff/ground_truth.tum \
  iilabs3d/scan-based/iilabs3d_nav_a_diff_ricoslam_slam_pose.tum                            \
  iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam_pose.tum           \
  iilabs3d/local-map/iilabs3d_nav_a_diff_ricoslam_slam_pose.tum                             \
  iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_diff_ricoslam_slam_pose.tum            \
  iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam_pose.tum            \
  iilabs3d/scan-based/iilabs3d_nav_a_diff_ricoslam_slam_pose_corrected.tum                  \
  iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam_pose_corrected.tum \
  iilabs3d/local-map/iilabs3d_nav_a_diff_ricoslam_slam_pose_corrected.tum                   \
  iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_diff_ricoslam_slam_pose_corrected.tum  \
  iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam_pose_corrected.tum

# Gmapping
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_diff/ground_truth.tum \
  iilabs3d/gmapping_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_diff_gmapping_pose.tum \
  iilabs3d/gmapping_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_diff_gmapping_pose.tum \
  iilabs3d/gmapping_lin-1.00m_ang-1.00rad/iilabs3d_nav_a_diff_gmapping_pose.tum

# IILABS3D W/ EVO: (nav_a_omni)
# RicoSLAM
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_omni/ground_truth.tum \
  iilabs3d/scan-based/iilabs3d_nav_a_omni_ricoslam_slam_pose.tum                            \
  iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam_pose.tum           \
  iilabs3d/local-map/iilabs3d_nav_a_omni_ricoslam_slam_pose.tum                             \
  iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_omni_ricoslam_slam_pose.tum            \
  iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam_pose.tum            \
  iilabs3d/scan-based/iilabs3d_nav_a_omni_ricoslam_slam_pose_corrected.tum                  \
  iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam_pose_corrected.tum \
  iilabs3d/local-map/iilabs3d_nav_a_omni_ricoslam_slam_pose_corrected.tum                   \
  iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_omni_ricoslam_slam_pose_corrected.tum  \
  iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam_pose_corrected.tum

# Gmapping
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_omni/ground_truth.tum \
  iilabs3d/gmapping_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_omni_gmapping_pose.tum \
  iilabs3d/gmapping_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_omni_gmapping_pose.tum \
  iilabs3d/gmapping_lin-1.00m_ang-1.00rad/iilabs3d_nav_a_omni_gmapping_pose.tum

# IILABS3D W/ EVO: (loop)
# RicoSLAM
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/loop/ground_truth.tum \
  iilabs3d/scan-based/iilabs3d_loop_ricoslam_slam_pose.tum                            \
  iilabs3d/scan-based_w-relocalization/iilabs3d_loop_ricoslam_slam_pose.tum           \
  iilabs3d/local-map/iilabs3d_loop_ricoslam_slam_pose.tum                             \
  iilabs3d/local-map_w-factors-update/iilabs3d_loop_ricoslam_slam_pose.tum            \
  iilabs3d/local-map_w-relocalization/iilabs3d_loop_ricoslam_slam_pose.tum            \
  iilabs3d/scan-based/iilabs3d_loop_ricoslam_slam_pose_corrected.tum                  \
  iilabs3d/scan-based_w-relocalization/iilabs3d_loop_ricoslam_slam_pose_corrected.tum \
  iilabs3d/local-map/iilabs3d_loop_ricoslam_slam_pose_corrected.tum                   \
  iilabs3d/local-map_w-factors-update/iilabs3d_loop_ricoslam_slam_pose_corrected.tum  \
  iilabs3d/local-map_w-relocalization/iilabs3d_loop_ricoslam_slam_pose_corrected.tum

# Gmapping
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/loop/ground_truth.tum \
  iilabs3d/gmapping_lin-0.30m_ang-0.30rad/iilabs3d_loop_gmapping_pose.tum \
  iilabs3d/gmapping_lin-0.50m_ang-0.50rad/iilabs3d_loop_gmapping_pose.tum \
  iilabs3d/gmapping_lin-1.00m_ang-1.00rad/iilabs3d_loop_gmapping_pose.tum

# IILABS3D W/ EVO: (slippage)
# RicoSLAM
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/slippage/ground_truth.tum \
  iilabs3d/scan-based/iilabs3d_slippage_ricoslam_slam_pose.tum                            \
  iilabs3d/scan-based_w-relocalization/iilabs3d_slippage_ricoslam_slam_pose.tum           \
  iilabs3d/local-map/iilabs3d_slippage_ricoslam_slam_pose.tum                             \
  iilabs3d/local-map_w-factors-update/iilabs3d_slippage_ricoslam_slam_pose.tum            \
  iilabs3d/local-map_w-relocalization/iilabs3d_slippage_ricoslam_slam_pose.tum            \
  iilabs3d/scan-based/iilabs3d_slippage_ricoslam_slam_pose_corrected.tum                  \
  iilabs3d/scan-based_w-relocalization/iilabs3d_slippage_ricoslam_slam_pose_corrected.tum \
  iilabs3d/local-map/iilabs3d_slippage_ricoslam_slam_pose_corrected.tum                   \
  iilabs3d/local-map_w-factors-update/iilabs3d_slippage_ricoslam_slam_pose_corrected.tum  \
  iilabs3d/local-map_w-relocalization/iilabs3d_slippage_ricoslam_slam_pose_corrected.tum

# Gmapping
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/slippage/ground_truth.tum \
  iilabs3d/gmapping_lin-0.30m_ang-0.30rad/iilabs3d_slippage_gmapping_pose.tum \
  iilabs3d/gmapping_lin-0.50m_ang-0.50rad/iilabs3d_slippage_gmapping_pose.tum \
  iilabs3d/gmapping_lin-1.00m_ang-1.00rad/iilabs3d_slippage_gmapping_pose.tum


## SLAM Toolbox
# preprocessing
# roscore on another terminal
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_diff.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_diff.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_omni.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_omni.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_loop.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_loop.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_slippage.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_slippage.tum_slam_toolbox.tum

python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_diff.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_diff.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_omni.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_omni.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_loop.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_loop.tum_slam_toolbox.tum
python3 sync_tf_scan.py --base eve/base_footprint --map map --scan /eve/scan iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_slippage.tum_slam_toolbox.bag iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_slippage.tum_slam_toolbox.tum

# Benchmark
python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_diff/ground_truth.tum \
  iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_diff.tum_slam_toolbox.tum \
  iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_diff.tum_slam_toolbox.tum

python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/nav_a_omni/ground_truth.tum \
  iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_nav_a_omni.tum_slam_toolbox.tum \
  iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_nav_a_omni.tum_slam_toolbox.tum

python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/loop/ground_truth.tum \
  iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_loop.tum_slam_toolbox.tum \
  iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_loop.tum_slam_toolbox.tum

python3 eval_iilabs3d.py \
  /mnt/data/datasets/paper_slam_2d/distance-maps-eval/iilabs3d/iilabs3d_dataset/benchmark/livox_mid-360/slippage/ground_truth.tum \
  iilabs3d/slam-toolbox_lin-0.30m_ang-0.30rad/iilabs3d_slippage.tum_slam_toolbox.tum \
  iilabs3d/slam-toolbox_lin-0.50m_ang-0.50rad/iilabs3d_slippage.tum_slam_toolbox.tum


################################################################################
## GRAPH RESULTS
################################################################################
# IILABS3D: RicoSLAM (nav_a_diff)
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json

grep --count -o -w "range_max" iilabs3d/scan-based/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json

grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_diff_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_diff_ricoslam_slam.json

# IILABS3D: RicoSLAM (nav_a_omni)
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json

grep --count -o -w "range_max" iilabs3d/scan-based/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json

grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-factors-update/iilabs3d_nav_a_omni_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-relocalization/iilabs3d_nav_a_omni_ricoslam_slam.json

# IILABS3D: RicoSLAM (loop)
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based_w-relocalization/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-factors-update/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-relocalization/iilabs3d_loop_ricoslam_slam.json

grep --count -o -w "range_max" iilabs3d/scan-based/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/scan-based_w-relocalization/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-factors-update/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-relocalization/iilabs3d_loop_ricoslam_slam.json

grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based_w-relocalization/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-factors-update/iilabs3d_loop_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-relocalization/iilabs3d_loop_ricoslam_slam.json

# IILABS3D: RicoSLAM (slippage)
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/scan-based_w-relocalization/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-factors-update/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "VariableSE2DistanceMapStaticPointNormal2fVectorCloudRight" iilabs3d/local-map_w-relocalization/iilabs3d_slippage_ricoslam_slam.json

grep --count -o -w "range_max" iilabs3d/scan-based/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/scan-based_w-relocalization/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-factors-update/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "range_max" iilabs3d/local-map_w-relocalization/iilabs3d_slippage_ricoslam_slam.json

grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/scan-based_w-relocalization/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-factors-update/iilabs3d_slippage_ricoslam_slam.json
grep --count -o -w "SE2DistanceMapStaticPointNormal2fVectorCloudRightPosePoseGeodesicErrorFactor" iilabs3d/local-map_w-relocalization/iilabs3d_slippage_ricoslam_slam.json


################################################################################
## DYNAMICS REMOVAL MAPPING RESULTS
################################################################################
# RicoSLAM
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/scan-based/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/scan-based/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/scan-based/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/scan-based/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/scan-based/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/scan-based/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/scan-based/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/scan-based/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/scan-based/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/scan-based/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/scan-based/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/scan-based/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/scan-based/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/local-map/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/local-map/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/local-map/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 iilabs3d/local-map/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/local-map/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/local-map/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/local-map/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 iilabs3d/local-map/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/local-map/std/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_diff_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/local-map/std/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_nav_a_omni_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/local-map/std/iilabs3d_loop_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_loop_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 iilabs3d/local-map/std/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff iilabs3d/local-map/dyn-rmv/iilabs3d_slippage_ricoslam_slam_occ_mat.tiff

# Avantgarde
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run0_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run0_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run1_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run1_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run2_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run2_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run3_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run3_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run4_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run4_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run5_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run5_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 avantgarde/scan-based/std/avantgarde_run6_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run6_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run0_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run0_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run1_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run1_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run2_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run2_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run3_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run3_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run4_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run4_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run5_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run5_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 avantgarde/scan-based/std/avantgarde_run6_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run6_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run0_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run0_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run1_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run1_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run2_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run2_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run3_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run3_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run4_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run4_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run5_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run5_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 avantgarde/scan-based/std/avantgarde_run6_ricoslam_slam_occ_mat.tiff avantgarde/scan-based/dyn-rmv/avantgarde_run6_ricoslam_slam_occ_mat.tiff

# Cappero
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 cappero/scan-based_rmax-25.0m_res-0.03m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/scan-based_rmax-25.0m_res-0.03m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 cappero/scan-based_rmax-25.0m_res-0.03m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/scan-based_rmax-25.0m_res-0.03m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 cappero/scan-based_rmax-25.0m_res-0.03m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/scan-based_rmax-25.0m_res-0.03m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/std/cappero_ricoslam_slam_occ_mat.tiff cappero/local-map-wo-factors-update_rmax-25.0m_res-0.03m_trans-2.50m/dyn-rmv/cappero_ricoslam_slam_occ_mat.tiff

# Flowbotic
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 flowbotic/local-map/std/flowbotic_20251024_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251024_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 flowbotic/local-map/std/flowbotic_20251027_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251027_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 flowbotic/local-map/std/flowbotic_20251028_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251028_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 flowbotic/local-map/std/flowbotic_20251024_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251024_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 flowbotic/local-map/std/flowbotic_20251027_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251027_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 flowbotic/local-map/std/flowbotic_20251028_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251028_ricoslam_slam_occ_mat.tiff

python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 flowbotic/local-map/std/flowbotic_20251024_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251024_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 flowbotic/local-map/std/flowbotic_20251027_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251027_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 flowbotic/local-map/std/flowbotic_20251028_ricoslam_slam_occ_mat.tiff flowbotic/local-map/dyn-rmv/flowbotic_20251028_ricoslam_slam_occ_mat.tiff

# Kuka
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.05 kuka/local-map-wo-factors-update/std/kuka_ricoslam_slam_occ_mat.tiff kuka/local-map-wo-factors-update/dyn-rmv/kuka_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.10 kuka/local-map-wo-factors-update/std/kuka_ricoslam_slam_occ_mat.tiff kuka/local-map-wo-factors-update/dyn-rmv/kuka_ricoslam_slam_occ_mat.tiff
python3 analyse_occupancy_maps_modified.py --labels std dyn-rmv --tau 0.20 kuka/local-map-wo-factors-update/std/kuka_ricoslam_slam_occ_mat.tiff kuka/local-map-wo-factors-update/dyn-rmv/kuka_ricoslam_slam_occ_mat.tiff

```
