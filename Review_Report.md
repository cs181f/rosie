# Review Report

Linnea wrote her component for code review

The input received from the process was very valuable. As I wasn't confident
in the implementation of parts of my component, a code review helped catch
areas where my confusion had caused incorrectness. The reviewers caught
typos, oversights, and confusing or incorrectly implemented code, and they
also were able to point out areas where my interpretation of the design
did not match their interpretation.

After the review process, unfortunately a lot of errors remained. While the 
biggest errors, where I incorrectly implemented code, were caught, they were
not resolved and figuring out how to correct the errors was very difficult
due to the confusion that led to their inclusion in the first place.

Doing the code review before testing was both good and bad. It was good in
that it caught many areas of incorrect implementation etc. that I might have
edited the tests to match instead of the other way around. It was bad in that
testing might have prompted me to at least be aware of some of the mistakes,
which would have allowed the code review to focus a little more tightly on
where the errors were instead of the more general "this just doesn't make
sense" notes that I received.

Knowing that I were going to have a code review would not have altered my
test plans at all.

Next time I would make two signicant changes - I would first of all run tests
before the code review if only to catch the most basic errors. And second,
I would not use the extra mongokit library that we used. We had hoped that
mongokit would help simplify the database functions and allow us to use a
database schema. While the database schema worked, we spent a lot of time
debugging, mostly due to not-so-helpful documentation and too many shiny
features that I tried to take advantage of, to our detriment.
