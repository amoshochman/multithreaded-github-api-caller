# multithreaded-github-api-caller
### A Python script that receives a list of queries, performs the respective queries using github api and returns the total amount of results.

**Running Instructions**: create a copy of config-example.py under the name config.py and fill the values as desired.

_Stuff which can be further improved_:

1. Using a pool for the threads. Right now, there's just a loop when the amount of available threads is too small.</br>
This is eventually a waste of CPU processing capacity
2. For the results, use some data structure more suitable to multi-threading. Or another mechanism.
3. There is no retry mechanism in case of a failure
4. There is no use of the information in case of a failure. 
For example, the information can be potentially used to quit all threads or to set a time for the next try.
5. Make the code more OO
6. Validate the content of the config file
7. Manage errors that could arise from writing to log
8. Implement some kind of pagination