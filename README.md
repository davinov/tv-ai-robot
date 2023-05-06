To allow user access to the serial port (on debian based distribs):

```shell
sudo usermod -a -G dialout $USER
```

Install the dependencies:

```shell
pip install poetry
poetry install
```

Run:

```shell
poetry run src/main.py
```
