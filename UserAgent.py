import random
from mesa import Agent
from essential_generators import DocumentGenerator

from Actions import Post
import model


class UserAgent(Agent):
    INITIAL_RELATION_VALUE = 1
    RELATION_DECAY_PER_CYCLE = 0.9
    gen = DocumentGenerator()

    def __init__(self, unique_id, interests, actions_probabilities, influence, model):
        super().__init__(unique_id, model)
        self._relations = {}  # weights determining the relationship with users
        self._interests = interests
        self._posts = []  # written _posts
        self._performed_actions = []
        self._actions_probabilities = actions_probabilities
        self._influence = influence
        self._friends = []
        self._actions = {"write_comment": self.write_comment_to_post,
                         "write_post": self.write_post,
                         "react": self.react_to_post,
                         "share_post": self.share_post}
        self._action_relation_values = {
            "write_comment": 1,
            "react": 0.5,
            "share_post": 2
        }

    def update_relation(self, user, action_type):
        self._relations[user] += self._action_relation_values[action_type]

    def decrease_connections(self):
        for user in self._relations.keys():
            self._relations[user] *= UserAgent.RELATION_DECAY_PER_CYCLE

    def add_friend(self, user):
        self._friends.append(user)
        self._relations[user] = UserAgent.INITIAL_RELATION_VALUE

    def add_random_friends(self, num_of_friends):
        new_friends = random.choices(self.model.users, k=0)  # TODO: Why is num_of_friends float?
        for friend in new_friends:
            self.try_to_become_friends(friend)

    def try_to_become_friends(self, user):
        # TODO check if user become friend with given user, use add_friend
        #   gaining new _friends depends on mutual _friends,
        #   probability of becoming _friends is always higher than 0
        pass

    def write_comment_to_post(self):
        # TODO add comment to selected post, update relation
        generated_comment = UserAgent.gen.sentence()
        print(self.unique_id, "write comment")

    def write_post(self):
        # TODO select topics, send to _friends and to some random users if _influence is high enough
        #   post is sent to everyone if user _influence is equal to 1
        #   post is sent to half of users if user _influence is equal to 0.5 etc
        generated_text = UserAgent.gen.paragraph()
        new_post = Post(attitude=['?'], author=self,
                        tags=random.choices(model.SiteModel.tags, k=random.randint(0, len(model.SiteModel.tags))),
                        text=generated_text)  # TODO: Random tags, what about attidute?
        self._posts.append(new_post)
        print(self.unique_id, "write post")

    def react_to_post(self):
        # TODO react to selected post, update relation
        print(self.unique_id, "react")

    def share_post(self):
        # TODO share selected post, update relation
        print(self.unique_id, "share post")

    def append_react(self, post_id, reaction):
        self._posts[post_id].add_reaction(reaction)

    def append_comment(self, post_id, comment):
        self._posts[post_id].add_comment(comment)

    def append_observer(self, post_id, user):
        self._posts[post_id].add_observer(user)

    def step(self):
        for action in self._actions_probabilities:
            probability = self._actions_probabilities[action]
            r = random.random()
            if r <= probability:
                self._actions[action]()
        for user in self.model.schedule.agents:
            self.try_to_become_friends(user)
        self.decrease_connections()
