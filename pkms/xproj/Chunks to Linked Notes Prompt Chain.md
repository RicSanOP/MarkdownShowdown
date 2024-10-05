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

Project Documentation Notes are markdown files containing information on the project deliverable itself. These notes usually focus on a specific part of the project. They could focus on software aspect by describing the architecture of a software module, outlining the code structure of a class or function or listing  the dependencies of a codebase. Project documentation could also discuss machine learning processes such as results of model training, provide reasons for how learning models are architected or comment on the performance of a model during evaluation.
##### Knowledge Database Notes

Knowledge Database Notes are markdown files containing information that is meant to educate on the problem space. These are more independent from the project's development and are meant to assist the author in better understanding the problem they are trying to solve. The hope is that some of this knowledge can come in handy when justifying current approaches in the project and/or offer solutions to future potential problems.

### Markdown Candidate Proposals


### Markdown Title Suggestion

##### Task Management Notes Preamble

[[Chunks to Linked Notes Prompt Chain#Context Prompt]]
[[Chunks to Linked Notes Prompt Chain#Task Management Notes]]

##### Project Documentation Notes Preamble

[[Chunks to Linked Notes Prompt Chain#Context Prompt]]
[[Chunks to Linked Notes Prompt Chain#Project Documentation Notes]]
##### Knowledge Database Notes Preamble

[[Chunks to Linked Notes Prompt Chain#Context Prompt]]
[[Chunks to Linked Notes Prompt Chain#Knowledge Database Notes]]

You are going to help us come up with a title for a new markdown note. We are going to provide you with a collection of markdown files and chunks that have tagged with the {INSERT NOTE TYPE HERE} note type and share a strong semantic similarity. Imagine that you are about to draft a new note containing all the information found in the provided markdown files and chunks. Please suggest a title for this new markdown note and explain why you have decided to go with this title. Feel free to provide references to the provided markdown files and chunks. Please provide your answer in the following JSON format:

{
	title: "",
	justification: ""
}
