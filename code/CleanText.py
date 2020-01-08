import re

import luigi

from code.Config import NAMESPACE, ALLOWED_CHARACTERS, DEFAULT_PATH, DEFAULT_DOC_NAME


def clean_text(text):
    """
    Returns a string without any non-allowed characters
    :param text: string
    :return: string
    """
    regex = re.compile(ALLOWED_CHARACTERS)
    return regex.sub('', text)


class CleanText(luigi.Task):
    """
    Cleans the input text of any unwanted characters and normalizes all characters to lowercase
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)

    task_namespace = NAMESPACE

    def output(self):
        return luigi.LocalTarget('{}/document_cleaned.txt'.format(self.doc_path))

    def run(self):
        out_file = self.output().open('w')
        with open(str(self.input_path), 'r') as file:
            for line in file:
                cleaned_line = clean_text(line)
                cleaned_lowercase_line = cleaned_line.lower()
                out_file.write(cleaned_lowercase_line)
        out_file.close()


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.CleanText', '--workers', '1', '--local-scheduler'])
