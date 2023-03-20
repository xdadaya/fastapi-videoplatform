from enum import Enum


class ReactionType(str, Enum):
    LIKE = "like"
    DISLIKE = "dislike"
