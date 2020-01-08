import math

import luigi

from code.ComputeTF import ComputeTF
from code.Config import DELIMITER, NAMESPACE, DOC_DELIMITER, DEFAULT_PATH, DEFAULT_DOC_NAME


class ComputeIDF(luigi.Task):
    """
    Using the TF Document, calculates the IDF Value for each term
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)

    task_namespace = NAMESPACE

    def requires(self):
        return ComputeTF(input_path=self.input_path, doc_path=self.doc_path)

    def output(self):
        return luigi.LocalTarget('{}/document_idf.txt'.format(self.doc_path))

    def run(self):
        term_count_dict = {}
        doc_count = 0
        with self.input().open('r') as in_file:
            for line in in_file:
                if DOC_DELIMITER in line:
                    doc_count += 1
                else:
                    term, _ = line.split(DELIMITER)
                    term_count_dict[term] = term_count_dict.get(term, 0) + 1

        tf_dict = {term: math.log(doc_count / term_count) for term, term_count in term_count_dict.items()}

        with self.output().open('w') as out_file:
            for term, term_idf_float in tf_dict.items():
                out_file.write(term + DELIMITER + str(term_idf_float) + "\n")


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.ComputeIDF', '--workers', '1', '--local-scheduler'])
