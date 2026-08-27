Reflection - Tag

## 1. AI tools	
The 4 tools were used: ChatGPT, Claude, Cursor IDE and VS code with GitHub copilot.

With ChatGPT and Claude, we need to specify the role, the context, the needed tasks, the requirements and constraints. 
ChatGPT was used to create user stories. Claude was used for generation of skeletons, and revision of structured prompts for feature 1.  

Using Cursor IDE and VS Code/GitHub Copilot, we benefit from the ability of these programs to read the application and files. Here the agent is able to read, summarize the content of the application and suggest solutions. The prompts are usually inline prompt.
Cursor IDE was used for the backend. Also I used it to update the structured prompts for feature 2. VS Code/GitHub Copilot was used for the frontend.


## 2. AI helped	
AI helped in the following:
-	Creation of user stories
-	Reading my file and application
-	Updating the structured prompts and inline prompts
-	Generation of new tests
-	Checking for errors and suggesting solutions
-	Preparing the backend and the frontend
-	Updating the modal form

The most help was in updating the application files (main, models, storage…) to integrate the new features, and in creating the tests (verify_a, conftest, test_tasks).



## 3. AI failed	
AI had some failure in the following:
-	Creation of redundant scenarios
-	Suggestion of solutions that are not solving the errors…
-	Maintain the valid transitions in business_rules

One moment AI slowed it down for both features (tag and comment), is when I could not update the task in frontend due to invalid transitions in same status. The error mentioned that status transitions in same status was not valid. I have tried to add manually the needed status transitions in the business_rules.py (todo -> todo inprogress -> inprogress, done -> done). I have asked the VS Code agent to find the error. But it failed. He was suggesting removing the added transitions (todo -> todo inprogress -> inprogress, done -> done). Finally, I moved to Claude and asked it to provide me with the needed solutions including the needed status transitions.


## 4. My review
One place where my review changed the result was when I requested to include in the business_rules the transitions in same status (todo -> todo inprogress -> inprogress, done -> done).