Verification

# 1. Feature: TAG/Labels

## 1.1 Baseline check	
Asking the agent to summarize the application and to read and summarize specific files.

## 1.2 Backend check	Testing the end point and the expected response (status and timestamp)
Opening the browser

Testing with the updated verify_a.py 

Testing with the updated test_tasks.py

Testing specific test in test_tasks.py: test_patch_blank_tag_returns_422. It passed. Breaking: changing the tag to optional (in models.py). The test failed. Then restoring the test and it passed.

Testing with command line - adding a task with tag: passed. 
Invoke-RestMethod -Method POST -Uri http://localhost:8001/tasks -ContentType "application/json" -Body '{"title":"Task A","status":"ToDo","priority":"High","assignee":"Alice","tags":["Keyword1"]}'

Testing with command line - adding a task without tag: failed.
Invoke-RestMethod -Method POST -Uri http://localhost:8001/tasks -ContentType "application/json" -Body '{"title":"Task A","status":"ToDo","priority":"High","assignee":"Alice"}'


## 1.3 Manual browser check	
Adding a task with tag

Adding a task without tag

Emptying tag in task

Updating tag in task not null

Updating task without updating the tag

Filter with tag


## 1.4 Behavior contract before refactor	
Optimized tool selection## Module 3 Kanban Behavior Contract

| ID | Behavior | How to check manually | Pass/Fail notes |
|---|---|---|---|
| 1 | Three status columns render with correct counts | Load the board and verify there are exactly three columns (e.g. To Do, In Progress, Done) and each header shows the correct number of tasks in that column 

| 2 | Cards sort by priority inside each column | Confirm tasks within each column are ordered from highest priority to lowest priority after the board loads 

| 3 | Loading state appears before tasks load | Refresh the page or start with a slow network and verify a loading indicator displays before the task cards appear 

| 4 | Empty columns remain visible | Ensure columns with no tasks still render as empty placeholders rather than disappearing | |
| 5 | Error state appears when the backend is stopped | Stop or disconnect the backend and refresh the board to verify a visible error message appears instead of the normal board 

| 6 | Valid drag sends PATCH and updates the board | Drag a task from one valid column to another, check the network request is PATCH, and confirm the board updates to reflect the move 

| 7 | Invalid drag/server 422 reverts and shows the server message | Force an invalid drag or simulate a server 422 response, then verify the card returns to its original column and a server error message is shown 

| 8 | New Task and Edit modal flows still work, including title validation and dismissal | Open New Task and Edit modals, verify title validation prevents invalid submission, submit valid data, and confirm the modal can be dismissed correctly 


## 1.5 Behavior contract after refactor	
Re-run behavior-contract items:
- 1: Three status columns render with correct counts
- 3: Loading state appears before tasks load
- 4: Empty columns remain visible
- 8: New Task and Edit modal flows still work, including title validation and dismissal

## 1.6 Break test 1	
Test: pytest tests/test_tasks.py -k test_patch_blank_tags_are_ignored -v

Testing before breaking: passed

Breaking the code (returns 422) and testing after breaking: failed

Restoring (returns 200) as initially: passed

## 1.7 Break test 2	
Test: pytest tests/test_tasks.py -k test_patch_remove_only_tag_returns_422 -v

Testing before breaking: passed

Breaking the code (returns 200) and testing after breaking: failed

Restoring (returns 422) as initially: passed




# 2. Feature: Task comment

## 2.1 Baseline check	
The agent is able to read and summarize the application

## 2.2 Backend check
CRUD endpoint tests: POST, GET, PATCH, DELETE

Transitions: todo to inprogress (200), inprogress to done (200), done to inprogress (200), todo to done (422),  done to todo (422), todo to todo (200), inprogress to inprogress (200), done to done (200)


## 2.3 Frontend check
•	Adding task with comment
•	Adding task without comment
•	Deleting comment in 1 task
•	Updated comment in 1 task
•	Deleting comments in 1 task
•	Task transition
•	Modal form 


## 2.4 Testing via py files 
•	Verify_a
•	Confest
•	Test_tasks


## 2.5 Break test 1
•	Test: test_patch_comment_not_found_returns_404 
•	Initially: it passed.
•	Altered: change the status in main.py (clearest). •	In patch_comment, use 400 or 422 instead of 404 when comment is None. It failed.
•	Then restored: it passed.


## 2.6 Break test 2
•	Test: test_patch_status_keeps_comment_unchanged 
•	Initially: it passed.
•	Alteration: Make ToDo → InProgress invalid so the PATCH returns 422 — the 200 assert fails (less about comments). The test failed.
•	Restoration: it passed.	

 
