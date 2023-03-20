from projen.python import PythonProject

project = PythonProject(
    author_email="nicolas.byl@nexineer.io",
    author_name="Nicolas Byl",
    module_name="taskman",
    name="taskman",
    version="0.1.0",
)

project.synth()