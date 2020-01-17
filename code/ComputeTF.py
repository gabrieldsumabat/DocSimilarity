import collections

import luigi

from code.CleanText import CleanText
from code.Config import DELIMITER, NAMESPACE, DOC_DELIMITER, DEFAULT_PATH, DEFAULT_DOC_NAME


class ComputeTF(luigi.Task):
    """
    Using the cleaned text, calculates the term frequency
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)

    task_namespace = NAMESPACE

    def requires(self):
        return CleanText(input_path=self.input_path, doc_path=self.doc_path)

    def output(self):
        return luigi.LocalTarget('{}/document_tf.txt'.format(self.doc_path))

    def run(self):
        with self.output().open('w') as out_file:
            with self.input().open('r') as file:
                term_dict = collections.Counter()
                for line in file:
                    if DOC_DELIMITER in line:
                        # Supposed to be the total sum of terms
                        num_terms = sum(term_dict.values())
                        tf_dict = {term: term_count / num_terms for term, term_count in term_dict.items()}
                        for term, term_freq in tf_dict.items():
                            out_file.write(term + DELIMITER + str(term_freq) + "\n")
                        out_file.write(DOC_DELIMITER + "\n")
                        term_dict = collections.Counter()
                    else:
                        for word in line.strip().split():
                            term_dict[word] = term_dict.get(word) + 1


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.ComputeTF', '--workers', '1', '--local-scheduler'])
