import luigi

from code.ComputeIDF import ComputeIDF
from code.ComputeTF import ComputeTF
from code.Config import DELIMITER, NAMESPACE, DOC_DELIMITER, DEFAULT_PATH, DEFAULT_DOC_NAME


def idf_file_to_dict(idf):
    """
    Parses input idf file into a term dictionary
    :param idf: file -> idf produced file
    :return: dict -> {string, float} for term, idf value
    """
    idf_dict = {}
    for line in idf:
        if DELIMITER in line:
            term, idf_val = line.split(DELIMITER)
            idf_dict[term] = float(idf_val)
    return idf_dict


class ComputeTFIDF(luigi.Task):
    """
    Using TF and IDF documents, returns the TF document with the TF values multiplied by the corresponding IDF value
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)

    task_namespace = NAMESPACE

    def requires(self):
        return [
            ComputeIDF(input_path=self.input_path, doc_path=self.doc_path),
            ComputeTF(input_path=self.input_path, doc_path=self.doc_path)
        ]

    def output(self):
        return luigi.LocalTarget('{}/document_tfidf.txt'.format(self.doc_path))

    def run(self):
        [idf_file, tf_file] = self.input()
        with idf_file.open('r') as idf:
            idf_dict = idf_file_to_dict(idf)

        with self.output().open('w') as out_file:
            with tf_file.open('r') as tf:
                for line in tf:
                    if DOC_DELIMITER in line:
                        out_file.write(DOC_DELIMITER + "\n")
                    else:
                        if DELIMITER in line:
                            term, tf_str = line.split(DELIMITER)
                            tf_float = float(tf_str) * idf_dict[term]
                            out_file.write(term + DELIMITER + str(tf_float) + "\n")


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.ComputeTFIDF', '--workers', '1', '--local-scheduler'])
