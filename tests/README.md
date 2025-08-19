# Tests

* `dev`: tests that use `fakeserver.py` to emulate the Minecraft Java server. The tests are responsible for checking the flow of operation. Designed for the development of new features and quick access to a "server".

* `integration`: tests that use a real Minecraft Java server. The workflow is tested in a real scenario with a real server.


## How to tests

* `dev`

```bash
$ python -m unittest discover tests/dev
```

* `integration`

```bash
$ python -m unittest discover tests/integration
```
