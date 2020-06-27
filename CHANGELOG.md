# Changelog

<!-- markdownlint-disable MD001 MD003 MD024 -->

<!--

[LATEST]
---

### Added

### Changed

### Removed
-->

[v0.1.1]
---

### Added

- Member join log.
- Members join schools they create.
- Added bandit testing in .gitlab-ci.yml.
- School search function now lists if a role has been created for a school.
- Added "?" as a command prefix.
- Added Python black for code scanning.
- Added Secret Scanning.
- Dependabot dependency checking

### Changed

- Fix issue where message on member leaving would not work make a log.
- Lots of formatting changes to use python black.
- School list has been moved to a separate repo for easy of updating.

### Removed

- Error message for no command found.
- Dotenv dependency.

[v0.1.0] - 05/05/2020
---

### Added

- kwargs to [utils.messages.list_message()](utils/messages.py) that gets passed to make embed.

### Changed

### Removed

- Support for Python 3.5

[v0.1.2-beta]
---

### Added

- Version number to the bot.
- More blacklisted words.
- GitHub issue and pull request templates.
- Footer ability to [utils.messages.list_message()](utils/messages.py)
- Alias for search-school

### Changed

- Updated description.
- Fixed the math in [cogs.misc.uptime](cogs/misc.py).

### Removed

- Heroku deployment through GitLab CI.
- Removed GitLab issue and pull request templates.
- Code Climate analyzing.

[v0.1.1-beta]
---

### Added

- `reload-extension` command in [cogs.admin](cogs/admin.py) to allow for extension reloading.
- `uptime` command in [cogs.misc](cogs/misc.py) that reports how long the bot has been up.
- [cogs.errors](cogs/errors.py) for all error handling.

### Changed

- Made the bot a subclass from the discord bot.
- Made cogs into extensions.
- Updated format for CHANGELOG.

[v0.1-beta]
---

### Added

- A managed role check function in [cogs.health](cogs/health.py) to reduce duplicate code

### Changed

- Fixed utils.messages.list_message to send all results.
  - Fixed Cyb3r-Jak3/ccc-bot#15
- Made it so utils.messages.make_embed will send the embed by default.
- Change deploying in [.gitlab-ci.yml](.gitlab-ci.yml) to Heroku.

[Commit: ae5d1b8c]
---

### Added

- More help and better help to commands.

### Changed

- Big rework of the list_message function in [utils.messages](utils/messages.py) to change to using embed field to make it cleaner.
  - Related to #11 & #12
- Worked on cleaning up [cogs.join_school](cogs/schools.py) for readability and complexity.

### Removed

[Commit: 0b3808aa]
---

### Added

- [utils.messages.make_embed](utils/messages.py) to make a centralized embed location.
- Made all commands use embeds return in embeds.
- Add more help and documentation for commands.
- [utils.datahandler](utils/datahandler.py) makes its own logger file.

### Changed

- Changed how schools were being searched. Using pandas searching rather then list searching.
- Made it so all returns in [utils.validate](utils/validate.py) are one line.
- Changed error reporting to make an embed and only one ctx send.
- Add cog_checks to [cogs.health](cogs/health.py) and [cog.admin](cogs/admin.py).
- Changed the strings for query_str to remove the \\.
- Changed order of the errors table.
- Fixed bug where errorID would not be set.

[Commit: 7d0ae94]
---

### Added

- `admin_log` function in [utils.messages](utils/messages.py) a function that will centralize log reporting.
- `test-log` command in [utils.health](cogs/health.py) that will test to make sure that `admin_log` is working.

### Changed

- Format of [Contributing.md](CONTRIBUTING.md).
- Date format for [Contributing.md](CONTRIBUTING.md).
- Change description for bot argument in [cogs](cogs/)

### Removed

- Debugging print statements.

[Commit: 3366269]
---

### Added

- `list_message` function in [utils.messages](utils/messages.py) to remove duplicate list message sending.
- [utils.tables](utils/tables.py) Adds tables for datahandler as separate script for easier reading.
- `get-x` function in[cogs.health](cogs/health.py) which is a combined `get-errors` and `get-reports`.
- Added changelog requirement to the [merge request template](.gitlab/merge_request_templates/default.md).

### Changed

- Swapped `school-search` and `region-select` in [utils.validate](utils/validate.py) to bring similar functions together.
- Fixed `state-search` in [utils.validate](utils/validate.py) to work with `list_message`.

### Removed

- [cogs.heath{'get-errors' & 'get-report'}](cogs/health.py) as they were combined into one command.

---
This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
