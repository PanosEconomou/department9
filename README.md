# Department 9

Be a bureaucrat the way you want to! In this indie game you get the chance to explore your life as a bureaucrat with choices that matter and have real effect in the story. No more preset responses, you can interact with your environment the way you want to and at the length you want to, how much of the world you get to explore is completely up to you!

## Development

To get started clone this repository and then crete a python environment directly.

``` shell
python -m venv env
sh ./env/bin/activate
pip install requirements.txt
```

Now you should have a local python environment set up with all the necessary packages. In addition you will need to install [Hermes 3](https://ollama.com/library/hermes3) which is the LLM that the NPCs use for their interaction it is running locally through [Ollama](https://ollama.com). To install in linux run

```shell
curl -fsSL https://ollama.com/install.sh | sh
```

or just check their downloand instructions. Once it is installed do 

```shell
ollama run hermes3
```

to downloand and install the model and make sure it works. That should be all the setup!



