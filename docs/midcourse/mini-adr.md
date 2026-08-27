Mini ADR

# 1. Selected feature: Tags/labels (required feature)

## 1.1 Preparing the setting
-	Starting with the user-stories and correction with ChatGPT. Stories were inspected and 3 was revised.
-	Asking for 2 light weight architecture proposals from ChatGPT. Option A: json file local storage. Option B: SQLite local database. Options were inspected and I selected option was A as simpler and less complex. Option A requires limited set up, no need to external database, query can be done with python, no need for SQL knowledge. 
-	Asking for ADR from ChatGPT. ADR was inspected. It included the context, the decision, the tree of files, the reasoning, the consequences. I approved it.
-	Asking for skeleton from Claude. Code was inspected. I did not find new items compared to the previous skeleton. The comparison between initial skeleton and later one shows no difference: same folders, same files. 

## 1.2 Backend
-	Working the backend. Asking Claude to revise the initial prompts related to models.py, storage.py, verify_a.py, conftest.py, test_task.py. Codes were inspected: they included how to integrate the feature (tag). Here I approved them and updated the application files.  
-	Working the application with Cursor IDE. First, I asked the agent to summarize application. Then I used the prompts updated by Claude to update the files: models.py, storage.py, verify_a.py, conftest.py, test_task.py
-	Checking the CRUD endpoints 
-	Testing the application from the backend using curl command lines. First I tried adding a task with tag: it passed. Then trying to add a task without a tag: it failed. 
-	Testing the application with test_tasks.py. All passed. 
-	Breaking one test: test_patch_blank_tag_returns_422). Initially it passed. I changed the models to have the tag optional. Retesting with the modification: the test failed. Restorating the initial version: it passed.

## 1.3 Frontend
-	Working the frontend. I used VS code. 
-	Updating the kanban board to make visible the “tag” and later the “search”. The agent suggested the modifications. I inspected them and then approved them. 
-	Running the application from the frontend.
-	Testing the frontend using curl command lines: Adding a new task with or without tags. 
-	Updating the modal form. 
-	Fixing the modal form. I had errors initially when updating the tasks in same status: an error when updating a task and keeping it in same status. I tried to fix the valid transitions to include (todo -> todo, inprogress -> inprogress, done-> done in the business_rules.py). With VS code, the errors remained. I asked Claude to correct the file, the code was fixed and the application worked. 
-	Testing the modal form: new task, empty tag, preserve tag after unrelated update, filter. For filtering, Claude suggesting several options, I selected the simplest one “text search box”.
-	Refactoring. I prepared a repo for the application (before refactoting) in github under mid-course-project (add, commit, push). I asked the agent to write a kanban behavior contract, the contract was inspected and approved. I focused on style, asking the agent to improve the style and use the green color instead of blue. I tested later and the kanban turned green.
-	Testing and debugging.  I asked the agent for 5 edge cases. The cases were inspected, they were similar to each other, and similar to the ones in the test_tasks.py. I selected two tests from the test_tasks.py: they passed. I changed the code (breaking it). The tests failed. Then the tests were restored. I tried one test after one test. 
-	Updating the application on github (mid-course-project-after-refactor). 


# 2 Selected feature: Task comment (required feature)

## 2.1 Preparing the setting
-	Generating user-stories from ChatGPT. I inspected the user stories, and asked for correction, before approval. 
-	Architecture proposals, ADR were kept without modification.

## 2.2 Backend
-	Working the backend with Cursor IDE.
-	Updating the application py files: main, models, storage, verify_a, conftest, test_tasks… The agent suggested the modifications,  I inspected them and then approved them.
-	Checking the CRUD endpoints 
-	Testing the backend manually with command line: for each CRUD endpoints (POST, GET, GET/tasked, PATCH, DELETE), for comments operations (present or missing)
-	Fixing an error: the backend was not allowing transition in same status (todo to todo, done to done, inprogress to inprogress). I asked the agent to suggest solutions. I checked them and selected the simplest ones (updating the business_rules and the test_tasks). Also the comment field was not mandatory. For that, the solution was to update the models.py, storage.py, main.py, and the tests.
-	Testing the backend with command line to test the comment field: empty or filled.
-	Testing with test files: verify_a.py, conftest.py, and test_tasks.py. All passed.
-	Breaking the codes for 2 tests from test_tasks.py: they passed before breaking, failed when breaking and passed after restoration

## 2.3 Frontend
-	Moving to the frontend with VS Code/GitHub Copilot
-	Checking the application with VS code. 
-	Updating the kanban board to make visible the “comment” in the task box. 
-	Testing the frontend using curl command lines: Adding a new task with comment and without comment. Emptying comment. Updating fields not comment. Transitions between status.
-	Updating the modal form with the support of the agent.
-	Testing the modal form. 
-	Fixing the modal form: I had errors initially when updating the tasks in same status: an error when updating a task and keeping it in same status. I tried to fix the valid transitions to include (todo -> todo, inprogress -> inprogress, done-> done in the business_rules.py). With VS code, the errors remained. I asked Claude to correct the files, the code was fixed and the application worked. 
-	Testing the modal form manually: new task, empty comment, preserve comment after unrelated update, reject blank comment, delete comment, 404 for missing comment... 
-	Testing and debugging via command lines.  I asked the agent for 5 edge cases. For 2 tests, I asked the agent to prepare tests. Tests were checked and added to the test_tasks.py. Then each test was tested (passed), altered (failed) and then restored (pass): test_patch_comment_not_found_returns_404 and test_patch_status_keeps_comment_unchanged
-	Then I updated the application on github. 

# 3. Corrections
The application was revised in order to:
- Have the new features "tag" and "task comment" as optional
- Have the task title as required.
The agent suggested the updates for the files (main, models, storage, verify_a, test_tasks, index...). They were inspected and then approved.