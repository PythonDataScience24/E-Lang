We used pylint to help make the code more readable and to follow PEP8.
Below are a few messages that we fixed with its use:

main.py on the line `@app.shell_context_processor` gave error `E306 expected 1 blank line before a nested definition, found 0`, fixed by inserting a blank line

`config.py` in the `Config` class had the line `SQLALCHEMY_TRACK_MODIFICATIONS =config('SQLALCHEMY_TRACK_MODIFICATIONS',cast=bool)`, which made pylint show 3 messages at once:
- `E225 missing whitespace around operator`
- `E231 missing whitespace after ','`
- `E501 line too long (86 > 79 characters)`

also in `config.py`, on the line defining class `TestConfig` was the error `E302 expected 2 blank lines, found 1`, fixed by adding an additional blank line

`auth.py` had another `E501 line too long` message fixed by splitting up a very long `import` statement, with another such message in `language_ns.py`
`language_ns.py` also contained an `E302 expected 2 blank lines, found 1` message, alongside a `E501 line too long (118 > 79 characters` message

`models.py` contained multiple `W293 blank line contains whitespace` messages
