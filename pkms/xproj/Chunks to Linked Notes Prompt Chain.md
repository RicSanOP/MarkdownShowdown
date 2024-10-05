# Chunks to Linked Notes

- basket of chunks containing metadata
	- filename (can associate with other chunks)
	- author
	- summary (maybe contextual)
	- sequence id in note?

### Context Prompt

We are a team working on an AI project together. As is common, we take notes to manage information pertaining to our jobs. Each team member is maintains their own notebase of markdown files which use wikilinks to link to each other. Various markdown editors leverage linking in markdown such as:
	- [Obsidian](https://obsidian.md/)
	- [Dendron](https://www.dendron.so)
	- [LogSeq](https://logseq.com)

The fact that each team member has their own personal notebase has some advantages and disadvantages. While a team member has the freedom to draft markdown notes and structure the notebase in whichever way they see fit, they miss out on the potentially valuable information that exists within the notebases of their teammates. This means that a given team member can comfortably manage their tasks, draft project documentation and develop their personal knowledge database without concern for how they structure their writing and organize their markdown files, which may not suit the preferences of their teammates. However, there is a lack of a centralized notebase structure where the team can productively share and compare notes on project tasks, project documentation and knowledge on the problem domain.

Therefore we need your help! You will help us merge our individual notebases into a unified, centralized and structured notebase. In general, here are the steps you will take:
- process our markdown files
- break them down into chunks
- tag our files and chunks based on their function
- cluster the tagged chunks and markdown files into new potential markdown file candidates
- suggest wikilink style links to connect the note files semantically
- draft the new notes taking into consideration the relevant markdown file contents

### Centralized Notebase Structure

##### General Description

The centralized notebase which you will be generating by merging our individual notebases together will follow a mutally agreed upon structure. Each note in this new notebase will fall into one of 3 note types:
- task management: contains information on what the author has done or ought to do next
- project documentation: contains information on how the project will be desgined, implemented or operated
- knowledge database: contains information that is helpful for understanding the problem space and solving challenges in the project

##### Task Management Notes

Task Management Notes are markdown files containing information on actions that the author has taken in the past, is currently undertaking and/or will take in the future. Task Management Notes can take on many different styles such as:
- a devlog where the author describes what they have done in a journaling writing style which includes self reflections on their work
- a checklist where the author determines what they have to do and check off items when completed
- a table containing tasks on each row along with metadata on the team member responsible, the task priority, expected deadline and/or task priority
##### Project Documentation Notes

Project Documentation Notes are markdown files containing information on the project deliverable itself. These notes usually focus on a specific part of the project, describing one 
##### Knowledge Database Notes