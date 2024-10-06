```markdown
# Weekly Progress Reports and Useful Commands

## Summary
This note consolidates weekly progress reports and useful commands documentation. It includes a detailed breakdown of the author's activities and strategies for Week 3, such as the use of a learning rate scheduler and early stopping criteria to improve model convergence. It also addresses problems encountered, such as potential overfitting, and the resolutions implemented, including lowering the learning rate and introducing gradient clipping. Additionally, the note provides guidelines on useful commands and chunk formatting, emphasizing the importance of including an <info> tag at the top of each chunk.

## Justification
The title 'Weekly Progress Reports and Useful Commands' captures the essence of the content provided. The chunks include both weekly progress updates (Week 3 Report and Week 2 Report) and useful commands documentation, ensuring the title accurately reflects the dual focus of the note.

## Useful Commands

### Introduction to Useful Commands
**Note Path:** Useful Commands.md
**Author:** rifaat

# Useful Commands

### Reminder to Include Info Tag
**Note Path:** Useful Commands.md
**Author:** rifaat

Remember to include an <info> tag at the top of each chunk.

### Example of Chunk Format
**Note Path:** Useful Commands.md
**Author:** rifaat

For example:
```markdown
<chunk>
<info>
</info>
</chunk>
```

## Weekly Progress Reports

### Week 3 Report

#### How I Did:
**Note Path:** Week 3 Report.md
**Author:** rifaat

* I used an initial learning rate of 1e-4, with weight decay to prevent overfitting. Based on training observations, I experimented with a **learning rate scheduler** and **early stopping criteria** to improve convergence stability.

#### Problems:
**Note Path:** Week 3 Report.md
**Author:** rifaat

* Noticed that the model was converging too quickly, potentially overfitting to early stages of training, with validation performance plateauing.

#### Resolution:
**Note Path:** Week 3 Report.md
**Author:** rifaat

* Lowered the learning rate and introduced **gradient clipping** to stabilize the training process. Early stopping was used to prevent overfitting. I also increased the number of training epochs to allow for more robust convergence.

### Week 2 Report

#### Introduction
**Note Path:** Week 2 Report.md
**Author:** rifaat

# Week 2 Report

## Links
- [[Useful Commands]]
- [[Week 3 Report]]
- [[Week 2 Report]]
```

This structured markdown note consolidates the progress reports and useful commands, ensuring clarity and ease of reference for the team.