*This project has been created as part of the 42 curriculum by todina-r.*

# Fly-in

## Description

Fly-in is a Python project for routing a fleet of drones through a network of zones. Maps describe zones, their coordinates and types, and the connections between them. The goal is to find efficient routes while respecting blocked zones and movement costs.

This repository contains the project foundation: a typed map model, a validating map-file parser, a weighted shortest-path planner, and a command-line entry point. Turn-by-turn fleet scheduling, capacity-aware conflict resolution, and animated simulation are the next implementation steps; they are not yet provided by this foundation.

## Instructions

Python 3.13 or later and [uv](https://docs.astral.sh/uv/) are used by the current project configuration.

```sh
make install
make run MAP=maps/easy/01_linear_path.txt
```

The CLI prints a shortest route and its movement cost. A restricted destination costs two turns; normal and priority destinations cost one. Blocked zones cannot be entered. Among routes with the same movement cost, the planner prefers routes passing through more priority zones.

Useful development commands:

```sh
make lint
make lint-strict
make clean
```

The program can also be run directly:

```sh
uv run python -m fly_in maps/easy/01_linear_path.txt
```

## Map Format

Maps are UTF-8 text files. Comments begin with `#`. Zone declarations must precede connections, and connection names use a dash-separated pair of zone names.

```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint 1 0 [zone=priority max_drones=2]
end_hub: goal 2 0
connection: start-waypoint
connection: waypoint-goal
```

Zone metadata supports `zone=normal|blocked|restricted|priority`, `color=<word>`, and `max_drones=<positive integer>`. Connection metadata supports `max_link_capacity=<positive integer>`. Start and end zone occupancy is unlimited.

## Algorithm


## Visual Representation


## Resources

- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
