import numpy as np

from http_utils import get_embedding, get_importance, reflect_on_memories
from params import ALPHA_RECENCY, ALPHA_IMPORTANCE, ALPHA_RELEVANCE
from utils import cos_sim


class Memory:
    def __init__(self, description, t, citations=None, override_importance=-1):
        self.description = description
        self.created_timestamp = t
        self.most_recent_access_timestamp = t
        self.embedding = get_embedding(description)
        if override_importance > -1:
            self.importance = override_importance
        else:
            self.importance = get_importance(description)
        if citations is not None:
            self.citations = citations
        else:
            self.citations = []

    def __str__(self):
        return f"A {self.description}"

    def __unicode__(self):
        return f"A {self.description}"

    def __repr__(self):
        return f"A {self.description}"


class Agent:
    def __init__(self, name, age, innate_tendencies, initial_memories, starting_location):
        self.name = name
        self.memories = []
        for memory_string in initial_memories:
            if len(memory_string) > 0:
                self.memories.append(Memory(memory_string, 0, override_importance=6))
        self.innate_tendencies = innate_tendencies
        self.age = age
        self.current_location = starting_location

    def retrieve_memories(self, query_memory, t, top_k=10):
        query_embedding = get_embedding(query_memory)

        memory_recencies = []
        memory_importances = []
        memory_relevances = []

        for idx, memory in enumerate(self.memories):
            recency = 0.99 ** ((t - memory.most_recent_access_timestamp) / 60)
            importance = memory.importance
            relevance = cos_sim(query_embedding, memory.embedding)

            memory_recencies.append(recency)
            memory_importances.append(importance)
            memory_relevances.append(relevance)

        memory_recencies = np.array(memory_recencies)
        memory_importances = np.array(memory_importances)
        memory_relevances = np.array(memory_relevances)

        # Normalize each row of scores to [0, 1]
        memory_recencies = np.interp(memory_recencies, (memory_recencies.min(), memory_recencies.max()), (0, 1))
        memory_importances = np.interp(memory_importances, (memory_importances.min(), memory_importances.max()), (0, 1))
        memory_relevances = np.interp(memory_relevances, (memory_relevances.min(), memory_relevances.max()), (0, 1))

        memory_scores = ALPHA_RECENCY * memory_recencies + ALPHA_IMPORTANCE * memory_importances + ALPHA_RELEVANCE * memory_relevances

        # Get the top k memories
        top_ten_indices = np.argpartition(memory_scores, -top_k)[-top_k:]

        memories_to_return = []

        for i in top_ten_indices:
            memories_to_return.append(self.memories[i])

        return memories_to_return

    def add_memory(self, memory):
        self.memories.append(memory)

    def get_most_recent_memories(self, n):
        return self.memories[-n:]

    def reflect(self, t):
        # Get 100 most recent records from the memory stream
        last_100 = self.get_most_recent_memories(100)

        reflections = reflect_on_memories(self.name, last_100, t)

        for reflection in reflections:
            self.add_memory(Memory(reflection[0], t, citations=reflection[1]))

