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

## Notes
**inesctec_mrdt_slam_distmap_2d/include/inesctec_mrdt_slam_distmap_2d/slam/slam.hpp**
```cpp
{
  // ...

  updateKeyframeFactors(m_keyframe_, true);

  v1->measurement()->getDistanceMap()->free();  // uncomment this line to have multiple SLAM nodes running at same time
                                                // CONSIDERING ONLY TRACKER, NO LOOP CLOSURE!

  m_keyframe_ = new_keyframe.get();
}  // void SLAM_::addOdomKeyframe()
```

**inesctec_mrdt_slam_distmap_2d_ros/src/inesctec_mrdt_slam_distmap_2d_ros1/slam_ros1_offline.cpp**
```cpp
  // setupTerminal();

  for (rosbag::MessageInstance const& msg : view)
  {
    /* while (true)
    {
      char key = readTerminalKey();

      if (key == ' ')
      {
        m_paused_ = !m_paused_;

        // could disable ECHO in termios terminal settings
        // but when Ctrl+C, the original settings may not be restored...
        std::cout << std::endl << std::flush;

        printTime(msg.getTime(), msg.getTime() - initial_time, bag_length);

        ROS_INFO(
            "[%s][%s] Press SPACE to pause/resume processing, 'q' to quit... "
            "(+/- to change sleep time between msg -- %ld ms)",
            m_name_.c_str(), m_paused_ ? "PAUSED " : "RESUMED", m_sleep_ms);
      }
      else if (key == 'q' || key == 'Q')
      {
        std::cout << "Processing stopped by user" << std::endl;
        goto exit_loop;
      }
      else if (key == '+')
      {
        // could disable ECHO in termios terminal settings
        // but when Ctrl+C, the original settings may not be restored...
        std::cout << std::endl << std::flush;

        m_sleep_ms += 10;

        ROS_INFO(
            "[%s][%s] Press SPACE to pause/resume processing, 'q' to quit... "
            "(+/- to change sleep time between msg -- %ld ms)",
            m_name_.c_str(), m_paused_ ? "PAUSED " : "RESUMED", m_sleep_ms);
      }
      else if (key == '-')
      {
        // could disable ECHO in termios terminal settings
        // but when Ctrl+C, the original settings may not be restored...
        std::cout << std::endl << std::flush;

        m_sleep_ms = std::max(m_sleep_ms - 10, static_cast<int64_t>(0));

        ROS_INFO(
            "[%s][%s] Press SPACE to pause/resume processing, 'q' to quit... "
            "(+/- to change sleep time between msg -- %ld ms)",
            m_name_.c_str(), m_paused_ ? "PAUSED " : "RESUMED", m_sleep_ms);
      }

      if (!m_paused_)
      {
        break;
      }

      ros::spinOnce();

      std::this_thread::sleep_for(std::chrono::milliseconds(50));
    } */

     // ...
  }
  // restoreTerminal();
```

## Run
```sh
cd data/distance-maps/iilabs3d/

python3 -m venv .
source bin/activate

pip install iilabs3d-toolkit

python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-10.0m/nav_a_diff/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-10.0m/nav_a_omni/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-10.0m/loop/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-10.0m/slippage/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-20.0m/nav_a_diff/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-20.0m/nav_a_omni/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-20.0m/loop/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-20.0m/slippage/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-25.0m/nav_a_diff/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-25.0m/nav_a_omni/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-25.0m/loop/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-25.0m/slippage/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-30.0m/nav_a_diff/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-30.0m/nav_a_omni/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-30.0m/loop/
python3 eval_iilabs3d.py --dir res-0.03m_dmax-0.50m_rmax-30.0m/slippage/
```
