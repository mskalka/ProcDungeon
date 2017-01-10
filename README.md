# ProcDungeon
Tinkering with procedural generation with a roguelike in mind.

Current focus is on map generation combining a number of common and not so common roguelike methods to generate circular,
"tower like" maps:

1. First generates a number of rooms in a radius around a point and checks for intersections
2. When room count is satisfied, populate map with "Cell" objects, adding a buffer around the map
3. Mark each Cell in a larger radius around the rooms as carveable
4. Generate a maze (or mazes) inside that carveable space, ignoring the rooms
5. Ensure each room is connected to every maze it touches

TODO:
* More robust camera
* Reimpliment the player and other creatures.
* Pathfinding AI (partially implimented)
* Impliment DM system to coordinate creature movement, combat, loot, etc.

# Example Map:
![Alt text](/map_example.png?raw=true "Example Map")
