# Project 4 Post Mortem

## Implementation of Component Design and Code Quality:

One of the complicated things about doing this project through from beginning to end with the same small team is that assignments from early in the course on project1 stuck through project4. This means that as we designed Rosie and eventually divided it into pieces that we would each work on, we were making the decision about one step in the process without much knowledge of how that decision would stand later in the process.

The components were well designed and broken into discreet chunks that were well ordered and well documented, but the complexity involved in implementing each component was less consistent than we had consisted when we originally divided responsibilities. This meant that as we began working on component implementation, some of us were faced with much more work than others. We rebalanced our roles part way through the process, but the workload was still uneven as a result of our decisions in much earlier projects.
In terms of code quality, the pair programming produced the highest quality code, though it is hard to say how much higher or lower the quality would have been with double time spent by one person. The reviewed code was also very clean at the end of the process, but the constraint that it could not be tested before it was reviewed felt arbitrary and detracted from our review and our code quality unnecessarily.

## Implementation of Test Plan

Our test plan ended up being a more problematic ambition than any of our other code. It was very easy for us to write the ideas for which things could be tested, but when we started writing the tests we realized that many were somewhat redundant or were not particularly useful, but would still be time consuming to write. We adjusted well as we wrote them, and we were very happy with the coverage we ultimately achieved and have a high degree of confidence in our code as a result, but in the future we would definitely not be quite so free with the number of tests we let ourselves plan for.
For the test driven development section of the code, this burden was greatest, but the coverage was ultimately the best. In terms of how confident we are in the restults, there is no doubt this section was the highest.

## Efficacy of Development Processes

By far the least efficient process for development was the code reviewed section. Arranging for the three of us to meet for half an hour to talk about the code was exponentially more difficult than scheduling all of the time for just two of us to meet for pair programming. This might be exacerbated by the general student schedule during finals, but it took the longest for us to produce quality code with this process.

Pair programming was very efficient when it was happening, but some time passed in between sessions because schedules are hard to coordinate. This is much less likely to be a problem in a more professional setting, but on the academic schedule it definitely hindered our efficiency.
The test driven development was the slowest process because our test plan was very thorough and introduced extra overhead. However, it produced the code which we have the highest degree of confidence in.

Working alone was very efficient because we had implemented our designs very well, but time spent on referring to pieces owned by other team members kept it from being as efficient as pair programming.

## Integration of the Components

Because we were working with in a well defined web framework, and because our design had been well layed out, integrating the components was a relative breeze. The integration of the pair programmed sections with the other sections worked on by the pair was easiest because there was the most shared knowledge, though the reviewed code, which was the only other section of code, was also easy to integrate because we had all read and discussed it. This was not a problem for our team.

## Preparation of the Release Review/Demo

Rosie is a tool to help develop other programs, so the real demo would be to see it work during a development process.Because we don't have time to set up an entire second project which uses Rosie, our demo really consists of flexing the muscles and showing the joints move. Since we had a thorough test plan and had been doing rigorous testing throughout the development process, this was a fairly simple thing for us to demonstrate. We knew which pieces needed to work and how to demonstrate that they did.

## The Overall Project as an Educational Exercise

Having finally implemented most of the features we originally imagined for Rosie, it was definitely rewarding to have seen the process through to the end. There was a lot learned from each of the individual methods for writing code, but it was hard to communicate the lessons learned to one another after the fact. We were all involved in the review process, and most of us were in the pair programming session, but especially the test driven development section was really only educational for one of us. It would certainly have been painful for each of us to have had to do each type, so we're not sure what we would suggest as an alternative, but we definitely didn't each get the full experience of each type of development.
