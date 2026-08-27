# USER STORIES
## Feature 1: Selected feature: Tags/labels

### Feature 1.1: prompt to generate stories using ChatGPT
Generate user stories related to tags for the mid-course-project for Task Tracker in the same format and quality as this example.

Example:
Story: As a team member, I want to add a tag to a task so that I can filter tasks. 

Acceptance Criteria:
-	Tags as list or normalized comma-separated field. 
-	Tags are mandatory; missing or blank title returns HTTP 422.
-	A created task appears in the task list with title, id, status, priority, description, assignee, and tags. 
Now generate five more stories in the same format.

Constraints:
-	Use "team member" as the user role.
-	Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.
-	Include at least one failure case across the generated stories.


Output format:
Return each story with ID, Story and Acceptance Criteria headings.


### Feature 1.2: initial user stories (generated from ChatGPT)
Here are five tag-focused user stories with IDs, matching the requested format and level of detail.
ID: TAG-002
Story:
As a team member, I want to edit the tags on a task so that I can keep task categories accurate.
Acceptance Criteria:
•	A team member can add, remove, or replace tags on an existing task.
•	Tags are stored as a list or normalized comma-separated field.
•	Updated tags are persisted and displayed with the task.
•	Updating tags for a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-003
Story:
As a team member, I want to filter tasks by tag so that I can quickly find related tasks.
Acceptance Criteria:
•	A team member can filter the task list using a tag.
•	Only tasks containing the selected tag are returned.
•	The filtered task list includes title, id, status, priority, description, assignee, and tags.
•	Filtering by a tag that does not exist returns an empty task list.
________________________________________
ID: TAG-004
Story:
As a team member, I want to remove a tag from a task so that outdated categories are no longer associated with it.
Acceptance Criteria:
•	A team member can remove an existing tag from a task.
•	The removed tag no longer appears in the task's tag list. Other task tags remain unchanged.
•	Removing a tag from a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-005
Story:
As a team member, I want to prevent duplicate tags on a task so that task categorization remains consistent.
Acceptance Criteria:
•	A task cannot contain the same tag more than once.
•	Adding an existing tag does not create a duplicate entry.
•	Tags are compared consistently when checking for duplicates.
•	A blank tag value returns HTTP 422.
________________________________________
ID: TAG-006
Story:
As a team member, I want to search tasks by tag so that I can find tasks belonging to a specific category.
Acceptance Criteria:
•	A team member can search for tasks using a tag value.
•	Search results include title, id, status, priority, description, assignee, and tags.
•	Tasks containing the requested tag are included in the results.
•	A blank tag search returns HTTP 422.

### Feature 1.3: needed correction
TAG-004: to correct (historical)
Earlier correction required at least one tag per task. That rule was later reversed: tags are optional, including an empty tag list.

TAG-004: current correction
Rewrite TAG-004 so a team member can replace or remove tags, including clearing all tags. Blank or whitespace-only tag values are ignored (not stored).

TAG-006: to remove
Similar to story TAG-003 

### Feature 1.4: final user-stories 
ID: TAG-002
Story:
As a team member, I want to edit the tags on a task so that I can keep task categories accurate.
Acceptance Criteria:
•	A team member can add, remove, or replace tags on an existing task.
•	Tags are stored as a list or normalized comma-separated field.
•	Updated tags are persisted and displayed with the task.
•	Updating tags for a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-003
Story:
As a team member, I want to filter tasks by tag so that I can quickly find related tasks.
Acceptance Criteria:
•	A team member can filter the task list using a tag.
•	Only tasks containing the selected tag are returned.
•	The filtered task list includes title, id, status, priority, description, assignee, and tags.
•	Filtering by a tag that does not exist returns an empty task list.
________________________________________
ID: TAG-004
Story:
As a team member, I want to replace or remove tags from a task so that I can keep its categorization accurate, including clearing all tags when none apply.
Acceptance Criteria:
•	A team member can remove an existing tag from a task.
•	A team member can remove the last remaining tag, leaving the task with an empty tag list.
•	A team member can replace existing tags with another valid set of tags (including replacing with an empty list).
•	Tags remain normalized (trimmed, lowercased, de-duplicated) when updated.
•	Blank or whitespace-only tag values in a submitted list are ignored (not stored).
•	Other task fields remain unchanged when tags are removed or replaced.
•	Updating tags for a task that does not exist returns HTTP 404.
________________________________________
ID: TAG-005
Story:
As a team member, I want to prevent duplicate tags on a task so that task categorization remains consistent.
Acceptance Criteria:
•	A task cannot contain the same tag more than once.
•	Adding an existing tag does not create a duplicate entry.
•	Tags are compared consistently when checking for duplicates.
•	Blank or whitespace-only tag values are ignored (not stored).

## Feature 2: Selected feature: Task comments

### Feature 2.1: Prompt
Generate user stories related to task comment for the mid-course-project for Task Tracker in the same format and quality as this example.

Example:
Story: As a team member, I want to add a comment so that I can update the status and the priority. 

Acceptance Criteria:
-	Support list/add/delete behavior
-	Non-blank text validation
-	Not-found handling
-	
Now generate five more stories in the same format.

Constraints:
-	Use "team member" as the user role.
-	Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.
-	Include at least one failure case across the generated stories.


Output format:
Return each story with ID, Story and Acceptance Criteria headings.


### Feature 2.2: Initial user stories
ID: COMMENT-002
Story:
As a team member, I want to edit a comment on a task so that I can correct or update information I previously added.
Acceptance Criteria:
•	Support comment update behavior.
•	Comment text must not be blank.
•	Updating a comment for a task that does not exist returns HTTP 404.
•	Updating a comment that does not exist returns HTTP 404.
________________________________________
ID: COMMENT-003
Story:
As a team member, I want to view comments on a task so that I can review information related to the task.
Acceptance Criteria:
•	Support list comments behavior.
•	Each comment includes an id, task id, text, and creation date.
•	Comments are returned only for the requested task.
•	Requesting comments for a task that does not exist returns HTTP 404.
________________________________________
ID: COMMENT-004
Story:
As a team member, I want to delete a comment from a task so that I can remove information that is no longer relevant.
Acceptance Criteria:
•	Support comment delete behavior.
•	A successfully deleted comment is no longer included in the task's comments.
•	Deleting a comment that does not exist returns HTTP 404.
•	Deleting a comment from a task that does not exist returns HTTP 404.
________________________________________
ID: COMMENT-005
Story:
As a team member, I want to add multiple comments to a task so that I can keep track of different updates and decisions.
Acceptance Criteria:
•	Support adding multiple comments to the same task.
•	Each comment has a unique id and is associated with the correct task.
•	Comment text must not be blank.
•	Adding a comment to a task that does not exist returns HTTP 404.
________________________________________
ID: COMMENT-006
Story:
As a team member, I want to retrieve a specific comment from a task so that I can review its exact content.
Acceptance Criteria:
•	Support retrieving a single comment by its id.
•	The returned comment includes its id, task id, text, and creation date.
•	Requesting a comment that does not exist returns HTTP 404.
•	Requesting a comment for a task that does not exist returns HTTP 404.


### Feature 2.3: needed correction
Thank you. For ID: COMMENT-005 I want one comment per task, that can be updated. Non need to have multiple comments for a task. One is enough.   

For ID: COMMENT-006 There is no need to retrieve specific comment. To remove this story. 

Rewrite all stories taking into considerations my note. I want the team member to be able to update the comments.


### Feature 2.4: Final stories
Understood. Since each task should have exactly one comment, the stories should focus on creating, viewing, updating, and deleting that single comment rather than managing multiple comments or retrieving individual comments.
ID: COMMENT-002
Story:
As a team member, I want to add a comment to a task so that I can provide additional information about the task.
Acceptance Criteria:
•	Support adding one comment to a task.
•	A comment must contain non-blank text.
•	A task can have no more than one comment.
•	Adding a comment to a task that does not exist returns HTTP 404.
•	Attempting to add a second comment to a task returns HTTP 422.
________________________________________
ID: COMMENT-003
Story:
As a team member, I want to view the comment on a task so that I can review the additional information associated with it.
Acceptance Criteria:
•	Support viewing the comment associated with a task.
•	The returned comment includes its text and creation date.
•	A task without a comment returns an empty or null comment value.
•	Requesting the comment for a task that does not exist returns HTTP 404.
________________________________________
ID: COMMENT-004
Story:
As a team member, I want to delete the comment from a task so that I can remove information that is no longer relevant.
Acceptance Criteria:
•	Support deleting the comment associated with a task.
•	A successfully deleted comment is no longer associated with the task.
•	Deleting a comment from a task that does not exist returns HTTP 404.
•	Attempting to delete a comment when the task has no comment returns HTTP 404.
________________________________________
ID: COMMENT-005
Story:
As a team member, I want to update the comment on a task so that I can keep the task information accurate.
Acceptance Criteria:
•	Support updating the existing comment on a task.
•	A comment must contain non-blank text.
•	Updating a comment for a task that does not exist returns HTTP 404.
•	Updating a task that does not have a comment returns HTTP 404.
•	The updated comment is persisted and displayed with the task.
________________________________________
ID: COMMENT-006
Story:
As a team member, I want to replace the existing comment on a task so that I can keep only the most current information.
Acceptance Criteria:
•	A task can contain only one comment at a time.
•	Replacing the comment updates the existing comment text rather than creating a second comment.
•	The replacement comment must contain non-blank text.
•	The updated comment is persisted and displayed with the task.
•	Attempting to replace a comment for a task that does not exist returns HTTP 404.

