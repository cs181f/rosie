# build.py

* add *args and **kwargs to definition of save on line 120
    - DEFECT
    - MUST FIX

* remove safe on line 133
    - DEFECT
    - MUST FIX

* fix update_with_results to make it work without an error
    - DEFECT
    - MUST FIX
    - look at lines 90-95 in WorkerThread

* add what status numbers means
    - DEFECT
    - MUST FIX

* remove error as a require field
    - DEFECT
    - MUST FIX

# build_test.py

* import connection from the models file
    - DEFECT
    - MUST FIX

* add assertions to `test_empty_build_creation`, `test_build_from_bad_json`, `test_build_from_good_json`
    - DEFECT
    - MUST FIX

* `jake_json` to `fake_json`
    - DEFECT
    - MUST FIX

* try and save builds in `test_build_from_bad_json` and `test_build_from_good_json`
    - DEFECT
    - MUST FIX

* add clarification/explanation for why you removed a bunch of tests
    - CLARIFICATION
    - MUST FIX