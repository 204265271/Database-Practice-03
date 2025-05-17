# Introduction 
- This project is the 3rd practice lab for PKU 2025 spring - semester lecture Introduction to Database. 
- See this project also at 204265271@github. 

# Explanation to Some Details 
- [q1] We choose the first problem for Question 1: find all son - relations and all ancestor - relations. 
- [q2] As for the query part (part I) of Question 2: we choose to print all section - titles and count the number of qa structures. 
- [q2] For part II in Question 2, it's hard to flatten the "section" part and the "question - bank" part at the same time, 
    because these 2 parts are not formed in the same way. As a result, we choose to flatten the section part because it has more layers. 
- [q3] This time, in the third part, we choose SQLite instead of MySQL. The loading time may be long, especially the first time you load it. 
- [q3] There is no need to save the vectors of the sentences in the db, however, it takes a huge amount of space.
    But still we do this because of the requirement of the lab doc. 