# Code Review of build.py

* What do the different status numbers mean? (line 42)

* Should error be a required field? (line 59)

* In __init__ there should be an exception raised for providing neither argument (line 107)

* Safe variable in save never declared (line 123)


#Code Review of build_test.py

* no assertions in first three tests, counting on raising uncaught exceptions but not asserting it (line 72)

* test_build_insertion is depending on an empty DB, but you don't initialize a new DB for testing (line 82)

* typo "fake_json" spelled "jake_json" (line 116)
