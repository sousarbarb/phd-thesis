include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",                      -- mapping global frame
  tracking_frame = "eve/base_footprint",  -- robot tracking frame (base_footprint|base_link)
  published_frame = "eve/odom",           -- target frame for robot's pose w.r.t. map_frame
  odom_frame = "eve/odom",                -- odometry frame (external|internal)
  provide_odom_frame = false,             -- enable Cartographer odom publisher
  publish_frame_projected_to_2d = true,   -- restrict published pose to 2D
  use_pose_extrapolator = true,
  use_odometry = false,                   -- consume external /eve/odom
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,                    -- one LaserScan topic (/eve/scan)
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 1.0,        -- interval in seconds at which to publish the submap poses (e.g. 0.3s)
  pose_publish_period_sec = 10e-3,        -- interval in seconds at which to publish poses (e.g. 5e-3 = 200 Hz)
  trajectory_publish_period_sec = 100e-3, -- interval in seconds at which to publish the trajectory markers (e.g. 30e-3 = 30ms)
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D.submaps.num_range_data = 35
TRAJECTORY_BUILDER_2D.use_imu_data = false            -- disable IMU data for 2D localization
TRAJECTORY_BUILDER_2D.min_range = 0.1                 -- sensor minimum range (m)
TRAJECTORY_BUILDER_2D.max_range = 30.0                -- sensor maximum range (m)
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 25.0  -- when maximum range, mark as empty area up to (m)
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = false
-- TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.linear_search_window = 0.1
-- TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.translation_delta_cost_weight = 10.
-- TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.rotation_delta_cost_weight = 1e-1
TRAJECTORY_BUILDER_2D.motion_filter.max_distance_meters = 0.5
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = 0.5

POSE_GRAPH.optimization_problem.huber_scale = 1e2
POSE_GRAPH.optimize_every_n_nodes = 35
POSE_GRAPH.constraint_builder.min_score = 0.65

return options
