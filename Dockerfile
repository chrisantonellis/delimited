
# debian & python3.6
FROM python:3.6

# delimited package
ADD ./delimited/ /delimited/delimited
ADD ./setup.py /delimited/setup.py
WORKDIR /delimited
RUN pip install --editable .[test,docs]

# tests
ADD ./test /test

# run
WORKDIR /
CMD ["tail", "-f", "/dev/null"]
