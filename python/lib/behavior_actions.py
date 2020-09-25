'''This module provides functions to execute behaviors during http requires'''

def handle_behaviors(instance, headers, step):
  '''Takes in an instance of the behavior Repository, the headers as a dict, and the current step'''
  behaviors = instance.get_by_request(headers, step)

  for b in behaviors:
    b.execute()

def handle_behaviors_pre(instance, headers):
  '''Takes in an instance of the behavior Repository and the headers as a dict'''
  handle_behaviors(instance, headers, "PRE")

def handle_behaviors_post(instance, headers):
  '''Takes in an instance of the behavior Repository and the headers as a dict'''
  handle_behaviors(instance, headers, "POST")
  