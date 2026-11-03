# ManicMinelayers

---

Make AI playing ManicMinelayers with each others !

## Usage

---

### Run main python file
#### Using make
```shell
make up
```

#### Using docker compose
````shell
docker compose run --rm app python3 -m src.main
````

#### Result exemple (Could change depending on the project version):
```shell
Player 1: human   |   Player 2: stupidbot
```

## Structure

```shell
.
├── .github/workflows/
├── src/
│    ├── main.py
│    ├── cli/*.py
│    ├── classes/
│    │      ├─── players/
│    │      └───  *.py
│    └── ui/*.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
└── requirements.txt
```


### Use it using CLI

---

The project should entirely work using CLI command. Commands should only take "user inputs" and use game / analytic services.

#### Example

- You have created the play method for a human, for a stupidbot in ``src/classes``
- You have created a display method taking a game in ``src/ui/main.py`` (in the ManicMinelayers class)
- You entered the following command and need to generate a ManicMinelayers instance, a human instance and a stupidbot instance, then make them play:
```shell
make play human stupidbot
## Or
docker compose run --rm app python3 -m cli.main play human stupidbot
```

The command role is to generate the 3 instances you need and start a game using a static method in ManicMinelayers. This method can render a game, or not.
This method also allow to control game speed if there are on human playing.

In this exemple, the command should open a ``pygame`` interface and start running the game with "human" and "stupidbot"
