Now for the experimental setup of the mapping with dynamics removal section, let me give you more context for you to present a more thorough explanation:

* Flowbotic: dataset provided by Flowbotic in an industrial case, the location cannot be disclosure for annonimity of Flowbotic's industrial partner
   * 33Hz, range max 200.0m, range min 0.0m, angle min -3.140000104904175rad, angle max 3.140000104904175rad, angle increment 0.008726646192371845rad
   * 20251024
      * duration of 943 seconds, equivalent to 15 minutes and 43 seconds
      * 31800 laser scan messages
      * 31800 poses, 289.548m path length, 943.899s duration (evo_traj, odom)
   * 20251027
      * duration of 648 seconds, equivalent to 10 minutes and 48 seconds
      * 21945 laser scan messages
      * 21945 poses, 199.165m path length, 648.914s duration (evo_traj, odom)
   * 20251028
      * duration of 687 seconds, equivalent to 11 minutes and 27 seconds
      * 23044 laser scan messages
      * 23044 poses, 205.322m path length, 687.134s duration (evo_traj, odom)
* cappero: dataset provided by Prof. Dr. Giorgio Grisetti during my stay at the Sapienza University of Rome. This dataset is an indoor data acquisition within the Department of Computer, Control and Management Engineering (DIAG) from the Sapienza University
   * duration of 1065 seconds, equivalent to 17 minutes and 45 seconds
   * 42680 laser scan messages, 40Hz, range max 30m, range min 0.03m, angle max 2.3518311977386475rad, angle min -2.356194496154785rad, angle increment 0.004363323096185923rad
   * 42680 poses, 592.945m path length, 1065.521s duration (evo_traj, odom from scan variant)
* kuka: another dataset provided by Prof. Dr. Giorgio Grisetti during my stay, suppossedly in an industrial logisitcs case
   * duration of 4699 seconds, equivalent to 1 house 18 minutes and 19 seconds
   * 29833 laser scan messages, 6.3Hz (reported by rosbag info, validated with rostopic hz with simulated time), range max 30.0m, range min 0.0m, angle max 2.365112543106079rad, angle min -2.3474674224853516rad, angle increment 0.008727000094950199rad
   * 29832 poses, 2610.199m path length, 4699.457s duration (evo_traj, odom)
* avantgarde
   * 25hz, angle min -3.1415927410125732rad, angle max 3.1415927410125732rad, angle increment 0.0026179938577115536rad, range min 0m, range max 200m
   * run0
      * duration of 3573 seconds
      * 89254 laser scan messages
      * 89254 poses, 1210.492m path length, 3571.744s duration (evo_traj, odom)
   * run1
      * duration of 4237 seconds
      * 105845 laser scan messages
      * 105845 poses, 630.015m path length, 4235.752s duration (evo_traj, odom)
   * run2
      * duration of 1477 seconds
      * 36865 laser scan messages
      * 36865 poses, 298.218m path length, 1475.348s duration (evo_traj, odom)
   * run3
      * duration of 1377 seconds
      * 34374 laser scan messages
      * 34374 poses, 293.656m path length, 1375.645s duration (evo_traj, odom)
   * run4
      * duration of 2689 seconds
      * 67145 laser scan messages
      * 67145 poses, 420.562m path length, 2687.568s duration (evo_traj, odom)
   * run5
      * duration of 2296 seconds
      * 57322 laser scan messages
      * 57322 poses, 481.840m path length, 2294.067s duration (evo_traj, odom)
   * run6
      * duration of 1502 seconds
      * 37483 laser scan messages
      * 37483 poses, 342.210m path length, 1500.188s duration (evo_traj, odom)
