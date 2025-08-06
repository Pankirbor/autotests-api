from enum import Enum


class AllureFeature(str, Enum):
    USERS = "Users"
    COURSES = "Courses"
    FILES = "Files"
    EXERCISES = "Exercises"
    AUTHENTICATION = "Authentication"
