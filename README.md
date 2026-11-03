# ManicMinelayers

---

Make AI playing ManicMinelayers with each others !

## Available players

---

- stupidbot ( play with random choices )
- human ( You play )
- minmax
- MCTS

## Usage

---

### Using make :
#### Make play 2 players and look at the game in live ( at a humain speed )
```sh
make play <player_1> <player_2>
```

Example:
```sh
make play stupidbot minmax
```

---

#### Make play 2 players and get statistics ( Games are played as fast as possible )
```sh
make statistics <player_1> <player_2> <iterations> <optionnal_json_config_file>
```

Example:
```sh
make statistics minmax stupidbot 10 ./hyper_parameters_config.json
```

## Configure hyperparameters

---

You can use a configuration file to adjust hyperparameters. It can be usefull to make play 2 players with each others,
and get statistics using those hyperparameters. Then, You will be able to analyse AI performance according to their
hyperparameters. AI analytics are then generated and saved each time you run statistics, you can retrieve a report
telling which parameters were most performing (with some performance indicators). Another history file is available to 
retrieve past game analytics.

### File format
You must use a **json** file. Here are the available keys to configure your hyperparameters. Each value in this exemple
is the configuration default value if no file is provided.

// TODO
```json
{
  
}
```