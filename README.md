# GPT Adventure

A web-based dungeon roleplaying game programmed in Python using the FastAPI framework.

## Getting Started

To get started with the game, simply clone the repository and run the game locally.

```bash
$ git clone git@github.com:JohnnyIrvin/GPT-Adventure.git
$ cd GPT-Adventure
$ pip install -r requirements.txt
$ python adventure
```

## Using Docker

To run GPT Adventure using Docker, simply build the Docker image and run the container.

```bash
$ docker build -t gpt-adventure .
$ docker run -p 8080:8000 gpt-adventure
```

This will run the game on port 8080. You can access the game by visiting http://localhost:8080 in your web browser.

If you would like to customize the port that the game runs on, you can specify it when running the container. For example, to run the game on port 8000, use the following command:

```bash
$ docker run -p 8000:8000 gpt-adventure
```

## Configuration

You will need to provide a session token, cf_clearance, user_agent and a list of usernames and passwords to a filenamed config.json located at the root of the repository. The config.json file should have the following format:

{
  "session_token": "your-session-token-here",
  "cf_clearance": "cloudflare-clearance-token",
  "user_agent": "your-user-agent-here",
  "users": [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    ...
  ]
}

The session_token field should be a string is generated from ChatGPT, see instructions from [revChatGPT](https://github.com/acheong08/ChatGPT/wiki/Setup#access-token-authentication). This token is used to authenticate with ChatGPT.

The users field should be a list of objects, each with a username and password field. These will be used to create user accounts for the game.

## Contributing
We welcome contributions to GPT Adventure! If you have an idea for a new feature or have found a bug, please open an issue on the [GitHub Repository](https://github.com/JohnnyIrvin/GPT-Adventure)

If you would like to contribute code, please fork the repository and create a pull request with your changes.

## License

GPT Adventure is licensed under the MIT license. See [LICENSE](LICENSE) for more details.
