# Changelog

<!-- markdownlint-disable MD001 -->
<!-- markdownlint-disable MD003 -->
<!-- markdownlint-disable MD024 -->

[Latest] - 03/04/2020
---

### Added

- [utils.messages.list_message](utils/messages.py) to remove duplicate list message sending.
- [utils.tables](utils/tables.py) Adds tables for datahandler as separate script for easier reading.
- [cogs.healthy.get-x](cogs/health.py) which is a combined `get-errors` and `get-reports`.
- Added changelog requirement to the [merge request template](.gitlab/merge_request_templates/default.md).

### Changed

- Swapped `school-search` and `region-select` in [utils.validate](utils/validate.py) to bring similar functions together.
- Fixed `state-search` in [utils.validate](utils/validate.py) to work with `list_message`.

### Removed

- [cogs.heath{'get-errors' & 'get-report'}](cogs/health.py) as they were combined into one command.

---
This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
