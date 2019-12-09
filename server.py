import collections
import random

from model import SiteModel
import matplotlib.pyplot as plt
from config import NUMBER_OF_STEPS, NUMBER_OF_USERS

model = SiteModel(NUMBER_OF_USERS)
for _ in range(NUMBER_OF_STEPS):
    model.step()


def check_influence_distribution():
    agent_data = [a.get_influence() for a in model.schedule.agents]
    plt.hist(agent_data)
    plt.title("User influence")
    plt.show()


def check_total_tags_distribution():
    agents_dicts = [a.get_interests() for a in model.schedule.agents]
    agents_dicts_sum = {}
    for tag in SiteModel.tags:
        agents_dicts_sum[tag] = sum(abs(d[tag]) for d in agents_dicts)
    plt.title("Sum of tag interests (abs)")
    plt.bar(agents_dicts_sum.keys(), agents_dicts_sum.values())
    plt.show()


def check_distribution_by_tag():
    agents_dicts = [a.get_interests() for a in model.schedule.agents]
    dict_all = collections.defaultdict(list)
    for tag in SiteModel.tags:
        dict_all[tag] = []
        for d in agents_dicts:
            dict_all[tag].append(d[tag])
        plt.title(tag)
        plt.hist(dict_all[tag])
        plt.show()


def check_random_user_tags_distribution(number_of_users_to_display):
    for _ in range(number_of_users_to_display):
        agent_dict = random.choice(model.schedule.agents).get_interests()
        plt.bar(agent_dict.keys(), agent_dict.values())
        plt.title("Random user interests")
        plt.show()


def check__total_user_actions_probabilities():
    agents_dicts = [a.get_actions_probabilities()
                    for a in model.schedule.agents]
    dict_all = collections.defaultdict(list)
    for action in SiteModel.actions:
        dict_all[action] = []
        for d in agents_dicts:
            dict_all[action].append(d[action])
        plt.title(action)
        plt.hist(dict_all[action])
        plt.show()


# check_influence_distribution()
# check_total_tags_distribution()
# check_random_user_tags_distribution(2)
# check_distribution_by_tag()
# check__total_user_actions_probabilities()
