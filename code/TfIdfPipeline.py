import luigi

from code.Config import NAMESPACE, DEFAULT_PATH, DEFAULT_DOC_NAME, DEFAULT_OUTPUT
from code.Similarity import Similarity


class TfIdfPipeline(luigi.WrapperTask):
    """
    Wrapper class for calling the entire pipeline
    Can be extended later to include several other pipelines
    """
    doc_path = luigi.Parameter(default=DEFAULT_PATH)
    input_path = luigi.Parameter(default=DEFAULT_PATH + DEFAULT_DOC_NAME)
    final_report_path = luigi.Parameter(default=DEFAULT_OUTPUT)

    task_namespace = NAMESPACE

    def requires(self):
        return Similarity(input_path=self.input_path, doc_path=self.doc_path, final_report_path=self.final_report_path)


if __name__ == '__main__':
    luigi.run([NAMESPACE + '.TfIdfPipeline', '--workers', '1', '--local-scheduler'])
