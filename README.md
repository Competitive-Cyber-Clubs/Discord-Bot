<!-- markdownlint-disable MD001 -->
# CCC-Bot

## This bot is still in alpha stages

Good coding practices and version will be implemented on its completion.

[![Maintainability](https://api.codeclimate.com/v1/badges/027b6135ce0965aa69c1/maintainability)](https://codeclimate.com/github/Cyb3r-Jak3/CCC-Bot/maintainability)

## About

This is a bot for the CCC Discord. It is made specifically for it, so it has been highly tailored to meet the unique requirements of it.
As such it is not recommended for most other discord channels, however it is something that you should be able to learn from to create your own.

### To add

Please visit this [link](https://discordapp.com/api/oauth2/authorize?client_id=643200662045458444&permissions=268443648&scope=bot)

#### To Do

- Sync admin role with bot admins.
- Format joinable schools better.

## Security Notice

Bandit is will warn about a possible SQL injection with the select SQL queries. However, I am using sqlite the recommended way to prevent injection attacks and the end users do not have direct access to be able to craft their own queries.  
If you are able to preform an SQL injection or other attack please contact me so that I can look into it.
