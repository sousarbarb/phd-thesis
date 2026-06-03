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




python3 analyse_occupancy_maps.py \
    /home/sousarbarb97/dev/phd/phd-thesis/data/slam/tests/local-map/standard/flowbotic_20251024_ricoslam_slam_occ_mat.tiff \
    /home/sousarbarb97/dev/phd/phd-thesis/data/slam/tests/local-map/dyn-rmv/flowbotic_20251024_ricoslam_slam_occ_mat.tiff \
    --labels "With dynamics" "Without dynamics"

```
