# AnkiIn

[![Release][release-shield]][release-url]
[![MIT License][license-shield]][license-url]
[![Issues][issues-shield]][issues-url]
[![Stargazers][stars-shield]][stars-url]
[![Forks][forks-shield]][forks-url]
[![Contributors][contributors-shield]][contributors-url]
[![CodeFactor][codefactor-shield]][codefactor-url]

See [AnkiLink Project](https://github.com/users/Clouder0/projects/1) for future plans.

## Introduction

AnkiIn is a Python Package that enables you to generate Anki cards from markdown text.  
It is easy to use and powerful.

**ATTENTION! This repo is for developers, so if you just want to use an Anki Importer, please check [AnkiLink](https://github.com/Clouder0/AnkiLink)**

Features:

- Directly Import into Anki via anki-connect
- Directly Export to `apkg` file with Anki offline via genanki
- Inline Configuration
- Human-Friendly Syntax
- Markdown Rendering Support
- Html Support
- Cross-Platform
- Many Useful built-in Note Types:
  - Q&A
  - Cloze
  - Choices
  - ListCloze
  - TableCloze
- Easy to Extend

---

To use this lib, you are not required to sacrifice your note readability for compatibility with Anki.

Here is a quick example:

```markdown
This is a question.
This is an answer.

Single line question.
Multiple line answer.
The first line of this block is recognized as the question.

Multiple line question is <br> possible somehow.
too hacky maybe.

markdown rendering is supported.
- use a list!
    - or something like that.

Clozes are **easy** to **create** too.
```

## Installation

You can install by pip:

```bash
pip install AnkiIn
```

### install Anki Connect

To use the lib, you need to install [AnkiConnect](https://github.com/FooSoft/anki-connect) extension.  
Code:`2055492159`  
For detailed installation guide, please visit the [anki-connect repo](https://github.com/FooSoft/anki-connect).

## Usage

You can review [AnkiLink](https://github.com/Clouder0/AnkiLink) to understand how this works.

Also, [AnkiIn Wiki](https://github.com/Clouder0/AnkiIn/wiki) is under construction.

For more syntax examples, see [tests](https://github.com/Clouder0/AnkiIn/tree/main/tests).

## Applications

I'd like to list some applications using AnkiIn here.  
If you want to add yours, please create an issue/pull request.

- [AnkiLink](https://github.com/Clouder0/AnkiLink)

## Credit

- [anki](https://github.com/ankitects/anki)
- [anki-connect](https://github.com/FooSoft/anki-connect)
- [genanki](https://github.com/kerrickstaley/genanki)
- [markdown2](https://github.com/trentm/python-markdown2)

## License

The source code is licensed under MIT.
License is available [here](https://github.com/Clouder0/AnkiIn/blob/main/LICENSE).

[contributors-shield]: https://img.shields.io/github/contributors/Clouder0/AnkiIn.svg
[contributors-url]: https://github.com/Clouder0/AnkiIn/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Clouder0/AnkiIn.svg
[forks-url]: https://github.com/Clouder0/AnkiIn/network/members
[stars-shield]: https://img.shields.io/github/stars/Clouder0/AnkiIn.svg
[stars-url]: https://github.com/Clouder0/AnkiIn/stargazers
[issues-shield]: https://img.shields.io/github/issues/Clouder0/AnkiIn.svg
[issues-url]: https://github.com/Clouder0/AnkiIn/issues
[license-shield]: https://img.shields.io/github/license/Clouder0/AnkiIn.svg
[license-url]: https://github.com/Clouder0/AnkiIn/blob/main/LICENSE
[release-shield]: https://img.shields.io/github/release/Clouder0/AnkiIn.svg
[release-url]: https://github.com/Clouder0/AnkiIn/releases
[codefactor-shield]: https://www.codefactor.io/repository/github/clouder0/AnkiIn/badge/main
[codefactor-url]: https://www.codefactor.io/repository/github/clouder0/AnkiIn/overview/main
