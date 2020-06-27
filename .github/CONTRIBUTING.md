# CONTRIBUTING

<!-- markdownlint-disable MD024 -->

## How to contribute

---

Thanks for reading this because we are always looking to collaborate with other people to see their ideas.

To get started fork the repo and make a branch with an accurate name for the changes you are making. Once you have made the changes to your liking open a pull request and we will look it over.

## Documentation

---

All of the cog, functions, etc should be documented in a way that allows for people with an understanding of python to get how the information flows through the bot. We are using numpy's style guide. If you would like easier understanding, then I recommend checking out the project on [sourcegraph](https://sourcegraph.com/github.com/Competitive-Cyber-Clubs/Discord-Bot).

## Commands

---

When adding a new command the format should be `verb-noun`, i.e. `search-school`, `add-school`.

### Cogs

When adding a new cog make sure that it is added to [cogs/__init__.py](cogs/\_\_init\_\_.py) and documented there. A good example cog to copy and get started with is [cog/regions.py](cogs/regions.py).

## Testing

---

There no current methodology for writing tests for discord.py, thus all tests have to be run manually when the development bot is online.
All commits to branches are inspected by [GitLab CI](https://gitlab.com/Cyb3r-Jak3/Discord-Bot) using pylint, flake8, bandit and black. Tox implementation in on the road map.

### Cogs/Commands

All commands need to be tested to ensure that nothing changes.
For simplicity sake, all cogs will be given a check box and once all commands for that cog are tested then it can be checked.

### Tables

It is important the all tables in the database are build correctly. All tables need to be dropped then rebuilt and test populated.  
This test is not mandatory based on the changes implemented.
