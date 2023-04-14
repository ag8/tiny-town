import tomllib

from Agents import Agent

with open("initial_setup.toml", "rb") as f:
    data = tomllib.load(f)

print()

characters = []

for character_name in data['characters'].keys():
    name = data['characters'][character_name]['name']
    age = data['characters'][character_name]['age']
    innate_tendencies = data['characters'][character_name]['innate_tendencies']
    initial_memories = data['characters'][character_name]['initial_memories']
    starting_location = tuple(data['characters'][character_name]['starting_location'])
    yesterday = tuple(data['characters'][character_name]['yesterday'])

    characters.append(Agent(name, age, innate_tendencies, initial_memories.split(";"), starting_location, yesterday))

print()
