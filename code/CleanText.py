import re

import luigi

from code.Config import NAMESPACE, ALLOWED_CHARACTERS, DEFAULT_PATH, DEFAULT_DOC_NAME

regex = re.compile(ALLOWED_CHARACTERS)


def clean_text(text):
    """
    Returns a string without any non-allowed characters
    :param text: string
    :return: string
    """
    return regex.sub('', text)


class CleanText(luigi.Task):
    """
    Cleans the input text of any unwanted characters and normalizes all characters to lowercase
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default='/'.join([DEFAULT_PATH, DEFAULT_DOC_NAME]))

    task_namespace = NAMESPACE

    def output(self):
        return luigi.LocalTarget('{}/document_cleaned.txt'.format(self.doc_path))

    def run(self):
        with open(str(self.output().open('w')))as out_file:
            with open(str(self.input_path), 'r') as in_file:
                for line in in_file:
                    cleaned_line = clean_text(line)
                    cleaned_lowercase_line = cleaned_line.lower()
                    out_file.write(cleaned_lowercase_line)


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.CleanText', '--workers', '1', '--local-scheduler'])
