# build.py

* where does the safe variable come from on line 123

* for update with results, what if it is a passed test? I think you need to check whether the result is of type success or type fail and act accordingly (look at my _build function in worker_thread.py)

# build_test.py

* where are your assertions in `test_empty_build_creation`, `test_build_from_bad_json`

* do you need to call save after line 67?

* I think you may need to import the Connection from the build.py file? Also, I don't think you need to reference the db and collection on line 37 because you specified them in the Build class

* `jake_json` -> `fake_json` on line 116

* what happened to all of your black box tests? a lot of them got deleted?