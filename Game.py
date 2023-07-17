import json


class Thing:
    def __init__(self, name, description, location, color, item, status):
        self.name = name
        self.description = description
        self.location = location
        self.color = color
        self.item = item
        self.status = status
        self.children = []

    def __str__(self):
        return f"A {self.name}; {self.description}; {self.location}; {self.color}"

    def __unicode__(self):
        return f"A {self.name}; {self.description}; {self.location}; {self.color}"

    def __repr__(self):
        return f"A {self.name}; {self.description}; {self.location}; {self.color}"


class Town:
    def __init__(self, data_source):
        self.minutes = 0


        with open(data_source) as f:
            town = json.load(f)
        main_town = Thing(town['name'], town['description'], ((town['location']['top_left']), (town['location']['bottom_right'])), town['color'], town['item'], None)

        stack = [(town, main_town)]

        while stack:
            node = stack.pop()
            raw = node[0]
            processed = node[1]

            if "children" in raw:
                if len(raw["children"]) > 0:
                    for child in raw["children"]:
                        location = ((child['location']['top_left']), (child['location']['bottom_right']))
                        color = child['color']
                        item = child['item']
                        status = child['status'] if item else None
                        thingified_child = Thing(child['name'], child['description'], location, color, item, status)
                        stack.append((child, thingified_child))
                        processed.children.append(thingified_child)

        print()
        print()

        self.tree = main_town

    def step(self):
        self.minutes += 1



