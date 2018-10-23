#!/usr/bin/env python3

def initial_health():
    health_points = 125
    return health_points

def fight_monster(health_points):
    health_points -= 25
    return health_points

def add_health(health_points):
    health_points += 25
    return health_points