update-requirements:
  pip-compile --no-annotate requirements.in > requirements.txt
  pip-compile --no-annotate requirements_dev.in > requirements_dev.txt
