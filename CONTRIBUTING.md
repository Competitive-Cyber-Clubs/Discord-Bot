# CONTRIBUTING

<!-- markdownlint-disable MD024 -->

## How to contribute

---

Thanks for reading this because I am always looking to collaborate with other people to see their ideas.

Currently all development is done on [GitLab](https://gitlab.com/Cyb3r-Jak3/ccc-bot) and mirror to other repositories. I recommend checking to project out there because it has all the issues and requests.
If you are looking to submit a pull request then please do so on [GitLab](https://gitlab.com/Cyb3r-Jak3/ccc-bot) because all development is done there. Any pull request that is opened on GitHub will be closed and I mirror it on GitLab.  

Please open issues on [GitLab](https://gitlab.com/Cyb3r-Jak3/ccc-bot/issues). if you do not have a GitLab account, send then please email service desk([incoming+cyb3r-jak3-ccc-bot-15469862-issue-@incoming.gitlab.com](mailto:incoming+cyb3r-jak3-ccc-bot-15469862-issue-@incoming.gitlab.com)).


## Documentation

---

All of the cog, functions, etc should be documented in a way that allows for people with an understanding of python to get how the information flows through the bot. If you would like easier understanding, then I recommend checking out the project on [sourcegraph](https://sourcegraph.com/gitlab.com/Cyb3r-Jak3/ccc-bot).

## Commands

---

When adding a new command the format should be `verb-noun`, i.e. `search-school`, `add-school`.

### Cogs

When adding a new cog make sure that it is added to [cogs/__init__.py](cogs/\_\_init\_\_.py) and documented there. A good example cog to copy and get started with is [cog/regions.py](cogs/regions.py).

## Testing

---

There no current methodology for writing tests for discord.py, thus all tests have to be run manually when the bot is online.

### Cogs/Commands

All commands need to be tested to ensure that nothing changes.
For simplicity sake, all cogs will be given a check box and once all commands for that cog are tested then it can be checked.

### Tables

It is important the all tables in the database are build correctly. All tables need to be dropped then rebuilt and test populated.  
This test is not mandatory based on the changes implemented.
