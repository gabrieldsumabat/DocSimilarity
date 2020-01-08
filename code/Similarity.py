import math

import luigi

from code.ComputeTFIDF import ComputeTFIDF
from code.Config import DELIMITER, NAMESPACE, DOC_DELIMITER, DEFAULT_OUTPUT, DEFAULT_PATH, DEFAULT_DOC_NAME


def find_euclidean_distance(term_dict1: dict, term_dict2: dict):
    """
    Formula: distance = sqrt( (a1-a2)**2 + (b1-b2)**2 + (c1-c2)**2 )
    :param term_dict1: string -> float, TF-IDF float value for each term
    :param term_dict2: string -> float, TF-IDF float value for each term
    :return: float, euclidean distance between the two vectors
    """
    all_term_set = term_dict1.keys() | term_dict2.keys()
    distance_squared = 0
    for term in all_term_set:
        distance_squared += (term_dict1.get(term, 0) - term_dict2.get(term, 0)) ** 2
    eucl_distance = math.sqrt(distance_squared)
    return eucl_distance


def sort_sublist_by_element_desc(element_index: int, list_of_lists: list):
    """
    Sorts a list of lists according to an element index
    :param element_index: int -> sublist index element to sort by
    :param list_of_lists: list[list] -> a list containing sub lists of equal size
    :return: list[list] -> a list of lists sorted by a specific element in descending order
    """
    sorted_list = sorted(list_of_lists, key=lambda sublist: sublist[element_index], reverse=True)
    return sorted_list


def get_doc_distance_list(doc_term_nested_dict: dict):
    """
    Calculates the similarity between the different documents and returns a nested list
    :param doc_term_nested_dict: Dict of Dict [int][string][float] -> Dictionary Number, Term, TFIDF Flat Value
    :return: List of list -> List [[doc_id,doc_id,distance],...] -> list of list representing the similarity
    """
    # Sublist [ doc_id_1, doc_id_2, similarity ]
    doc_distance_list = []
    num_docs = len(doc_term_nested_dict)
    for doc_id_1 in range(0, num_docs - 1):
        for doc_id_2 in range(doc_id_1 + 1, num_docs):
            eucl_dist = find_euclidean_distance(doc_term_nested_dict[doc_id_1], doc_term_nested_dict[doc_id_2])
            doc_distance_list.append([doc_id_1, doc_id_2, eucl_dist])
    return doc_distance_list


def build_nested_dict_docs_terms(in_file):
    """
    Converts the input file into a nested dictionary to represent all documents and terms
    :param in_file: file -> contains the tfidf mapping to each term and document
    :return: doc_term_nested_dict: Dict of Dict [int][string][float] -> Dictionary Number, Term, TFIDF Flat Value
    """
    # Document Int, Term String, TFIDF Float Value
    doc_counter = 0
    doc_term_nested_dict = {doc_counter: {}}
    for line in in_file:
        if DOC_DELIMITER in line:
            doc_counter += 1
            doc_term_nested_dict[doc_counter] = {}
        else:
            if DELIMITER in line:
                term, tfidf_float = line.split(DELIMITER)
                doc_term_nested_dict[doc_counter][term] = float(tfidf_float)
    return doc_counter, doc_term_nested_dict


class Similarity(luigi.Task):
    """
    Calculates the Similarity between different documents and returns a CSV with the result in the CWD by default
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    final_report_path = luigi.Parameter(default=DEFAULT_OUTPUT)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)

    task_namespace = NAMESPACE

    def requires(self):
        return ComputeTFIDF(input_path=self.input_path, doc_path=self.doc_path)

    def output(self):
        return luigi.LocalTarget("{}/similarity.csv".format(self.final_report_path))

    def run(self):
        with self.input().open('r') as in_file:
            num_docs, doc_term_nested_dict = build_nested_dict_docs_terms(in_file)
        doc_distance_list = get_doc_distance_list(doc_term_nested_dict)
        doc_distance_list = sort_sublist_by_element_desc(2, doc_distance_list)
        with self.output().open('w') as out_file:
            for doc_id_1, doc_id_2, eucl_dist in doc_distance_list:
                out_file.write(str(doc_id_1) + DELIMITER + str(doc_id_2) + DELIMITER + str(eucl_dist) + "\n")


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.Similarity', '--workers', '1', '--local-scheduler'])
