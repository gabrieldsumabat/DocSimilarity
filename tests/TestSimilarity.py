import unittest

from code.Similarity import find_euclidean_distance, get_doc_distance_list, sort_sublist_by_element_desc


class TestSimilarity(unittest.TestCase):

    def test_find_euclidean_distance(self):
        dummy_dict1 = {
            "a": 1,
            "b": 2,
            "c": 3
        }
        dummy_dict2 = {
            "a": 1,
            "c": 2,
            "d": 3
        }
        distance = find_euclidean_distance(dummy_dict1, dummy_dict2)
        self.assertEqual(distance, 3.7416573867739413)

    def test_get_doc_distance_list(self):
        dummy_dict = {
            0: {
                "a": 1,
                "b": 2,
                "c": 3
            }, 1: {
                "a": 1,
                "c": 2,
                "d": 3
            }
        }
        dummy_list = get_doc_distance_list(dummy_dict)
        self.assertEqual(dummy_list, [[0, 1, 3.7416573867739413]])

    def test_sort_sublist_by_distance(self):
        dummy_list = [[0, 1, 3.7416573867739413], [0, 2, 5.7416573867739413], [0, 1, 4.7416573867739413]]
        sorted_list = sort_sublist_by_element_desc(1, dummy_list)
        self.assertEqual(sorted_list[0][1], 2)
