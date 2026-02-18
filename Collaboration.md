# Contributing to the Course Collaboration Repository

This repository is a shared academic workspace for course projects and collaborations. Proper structure and Git discipline are required to maintain a clean, professional, and scalable codebase.

Please read this document fully before making your first contribution.

---

# Repository Structure

All student work must be placed inside:

```
collaborations/
```

---

## Student Folder Naming (Required)

Create a folder using the format:

```
netid-firstname
```

### Example

```
collaborations/k_b459-keshav
```

### Rules

* Use lowercase only
* No spaces
* No special characters
* Must match your NetID

---

# Project Structure

Inside your folder, create one directory per project.

### Example

```
collaborations/k_b459-keshav/customer-data-management
```

Prefer meaningful project names over generic ones like `project1`.

---

## Required Project Layout

Every project **must contain**:

```
project-name/
 ├── README.md
 ├── src/        (recommended)
 ├── data/       (if applicable)
 └── docs/       (optional)
```

---

# README Requirements (Mandatory)

Your README must clearly explain:

* Project objective
* Problem being solved
* Approach / architecture
* Technologies used
* How to run the project
* Example output (recommended)

A reviewer should understand your project without reading your code.

---

# Academic Integrity

You are free to design your project creatively **as long as it:**

* Is related to the course
* Does not violate academic ethics
* Does not contain plagiarized code
* Properly cites external sources

Violations will be treated seriously.

---

# Git Workflow (STRICT)

## Always Start Clean

Before beginning **any work**:

```bash
git switch main
git pull
```

Failing to pull is the #1 cause of merge conflicts.

---

## Never Work Directly on `main`

**Direct commits to `main` are not allowed.**

Always create a branch.

---

# Branch Naming Convention (Required)

```
netid-firstname-projectname-mode
```

### Example

```
k_b459-keshav-customer-data-management-dev
```

### Modes

| Mode     | Purpose            |
| -------- | ------------------ |
| dev      | active development |
| feature  | new feature        |
| fix      | bug fixes          |
| refactor | restructuring code |

---

# Creating a Branch

```bash
git switch -c branch_name
```

If the branch already exists:

```bash
git switch branch_name
```

---

# Commit Standards

Poor commits make collaboration painful. Write meaningful messages.

## Good Examples

```
add data preprocessing pipeline
implement REST endpoint for user service
fix memory bug in training loop
```

## Avoid

```
update
stuff
final
changes
```

---

# Push Your Work

```bash
git push -u origin branch_name
```

After the first push, simply use:

```bash
git push
```

---

# Pull Request Process (Mandatory)

When your work is ready:

1. Open a Pull Request.
2. Add reviewers (example: `keshavsbhandari` or collaborators).
3. Wait for feedback.
4. Address requested changes.
5. Push updates.

### Do NOT:

* Merge your own PR
* Ignore comments
* Resolve conversations without fixing issues

---

# PR Checklist (Students Should Verify)

Before requesting review:

✅ Project builds/runs
✅ README is complete
✅ Folder structure is correct
✅ No unnecessary files
✅ No large datasets committed
✅ No secrets or API keys
✅ Branch name follows convention

---

# After Approval

Once your PR is merged:

### Delete the remote branch (recommended via GitHub UI)

Then locally:

```bash
git switch main
git pull
git branch -d branch_name
```

---

# Large Files Policy

Do NOT commit:

* Large datasets
* Model weights
* Virtual environments
* `.DS_Store`
* `node_modules`
* `.venv`

Use `.gitignore`.

For large research artifacts, use cloud storage and link them in the README.

---

# Conflict Prevention Rule

Every time you begin work:

```bash
git switch main
git pull
```

No exceptions.

---

# Forbidden Actions

These create serious problems in shared repositories:

❌ Force pushing
❌ Deleting others' files
❌ Modifying another student's directory
❌ Committing directly to main
❌ Renaming top-level folders

---

# Professional Expectations

This repository mirrors real-world engineering collaboration.

Treat it as professional experience.

Employers care deeply about Git competency.

---

# Learn GitHub (Strongly Encouraged)

If you are not comfortable with Git:

Official guide:

[https://docs.github.com/en/get-started](https://docs.github.com/en/get-started)

Recommended topics:

* branching
* pull requests
* rebasing vs merging
* resolving conflicts

Learning this now will save you significant time in your career.

---

# Example Directory Tree

```
collaborations/
 ├── k_b459-keshav/
 │    ├── customer-data-management/
 │    │     ├── README.md
 │    │     ├── src/
 │    │     └── data/
 │
 ├── ab1234-jane/
 │    └── fraud-detection/
```

---

# Final Advice

Pull often.
Commit clearly.
Name things properly.
Document your work.

Good engineering habits start here.
