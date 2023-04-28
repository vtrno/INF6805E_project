# INF6805E
Work done :
 - [x] Simulate surrounding a target (robot 0) with up to 8 robots for now
 - [x] We need to get independant from the hardcoded number of robots at the start to ensure resistance to failure. The system put in place to count the number of robots in the swarm currently uses a leader. This makes the system not fully decentralized.
 - [x] The robots should consider the obastacles in his path choices (it shouldn't just keep going straight into an obstacle)
 - [x] The robots should handle the situtation where it losts connection to the group
   - [x] if it losts all connection to the group :
     - [x] if it sees the beacon it follows it (with obstacle avoidance)
     - [x] if it doesn't see the beacon but has seen it, it goes to the last seen position of the beacon (with obstacle avoidance) during a certain number of step
     - [x] else it does a random walk (with obstacle avoidance)
   - [x] if has just one neighbor it prioritizes to follow its neighbor (with obstacle avoidance), instead of going to the beacon of forming a surrounding to the beacon
   - [x] else : it goes too the position (considering lennard jones forces and beacon position) (with obstacle avoidance)
 - [x] lost_connection TODO 1  : optimize the obstacle avoidance so it's coherent with the target position of the robot(may it be the beacon or another position (ex: the unique neighbor if the robot is connected to only one neighbor))
 - [x] lost_connection TODO 2 : create a counter for the case where a robot has a unique neighbor which has a unique neighbor
 - [x] lost_connection TODO 3 : not sure to understand the LKP and check if we correctly implemented the last seen position code
 - [x] Other Ideas : create a queue that saves the last 5 positions of either the last neighbor seen, the centroid of the swarm, the centroid of the 3 nearest neighbors last seen or directly the beacon

# Credits
[Buzz programming language](https://github.com/buzz-lang/Buzz)  
[ARGoS 3 simulator](https://github.com/ilpincy/argos3)  