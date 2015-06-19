venv:
    virtualenv venv

install: venv
    . venv/bin/activate; pip install -r requirements.txt

tests:
    . venv/bin/activate; nosetests

clean:
    rm -rf venv
    rm *.pyc
