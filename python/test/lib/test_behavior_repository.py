import unittest

from lib.behaviors import behavior, repository


class BehaviorRepositoryTests(unittest.TestCase):
    def test_should_find_behavior_pre(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-PRE"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 1)

    def test_should_not_find_behavior_pre(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-POST"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 0)

    def test_should_find_behavior_app_id(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-PRE-TEST"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 1)

    def test_should_not_find_behavior_app_id(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-PRE-OTHER"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 0)

    def test_should_find_behavior_post(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-POST"] = 1
      found_behaviors = list(repo.get_by_request(headers, "POST"))
      self.assertEqual(len(found_behaviors), 1)

    def test_should_not_find_behavior_post(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-POST"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 0)

    def test_should_not_find_behavior_unsupported(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-FAKEBEHAVIOR-PRE"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 0)

    def test_should_find_many_behaviors_general(self):
      repo = createRepo(["SOMETHING", "SOMETHINGELSE"])
      headers = {}
      headers["X-DEMO-SOMETHING-PRE"] = 1
      headers["X-DEMO-SOMETHINGELSE-PRE"] = 1
      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 2)

    def test_targeted_should_override_general_behavior(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-PRE"] = 1
      headers["X-DEMO-SOMETHING-PRE-TEST"] = 2

      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 1)
      self.assertEqual(found_behaviors[0].get_value(), 2)

    def test_targeted_should_override_general_behavior_different_order(self):
      repo = createRepo()
      headers = {}
      headers["X-DEMO-SOMETHING-PRE-TEST"] = 2
      headers["X-DEMO-SOMETHING-PRE"] = 1

      found_behaviors = list(repo.get_by_request(headers, "PRE"))
      self.assertEqual(len(found_behaviors), 1)
      self.assertEqual(found_behaviors[0].get_value(), 2)

def createRepo(behaviors_arr = None):
  factory = lambda n, value: behavior.Behavior("SOMETHING", value)
  behaviors_arr = behaviors_arr if behaviors_arr is not None else ["SOMETHING"]
  return repository.Repository(behaviors_arr, factory, app_id="TEST")

if __name__ == '__main__':
    unittest.main()            
