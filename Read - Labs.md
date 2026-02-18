# Database Lab Setup Guide

Welcome to the Database Lab environment.

This repository is designed to help you learn how to:

* Run databases using Docker
* Connect using DBeaver (GUI)
* Use CLI tools
* Understand storage and volumes
* Experiment safely in a local lab environment

All hands-on work will happen inside the `db_lab/` folder.

---

# 1. Required Software

Install the following tools before starting.

---

## 1.1 Install Docker

Download Docker Desktop:

[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

Install for your operating system:

* Windows
* macOS
* Linux (Ubuntu users can install Docker Engine)

After installation, verify:

```bash
docker --version
docker compose version
```

Docker must be running before starting the lab.

---

## 1.2 Install VS Code

Download:

[https://code.visualstudio.com/](https://code.visualstudio.com/)

Recommended extensions:

* Docker
* SQL
* Markdown Preview

VS Code will be used to:

* Edit SQL files
* Edit docker-compose files
* Read lab instructions

---

## 1.3 Install Git (Windows Only: Git Bash)

### Windows users:

Install Git from:

[https://git-scm.com/downloads](https://git-scm.com/downloads)

During installation, enable:

* Git Bash

Use Git Bash instead of Command Prompt for running Docker commands.

Mac/Linux users already have terminal access.

Verify:

```bash
git --version
```
#### Change your VSCode default terminal to GitBash
- Open VSCode and type `Ctrl+Shift+p`
- Then in search bar type: `Terminal: Select Default Profile`
- Then select `Git Bash` from the list (Note. You may not see `Git Bash` if you have not installed it. Install GitBash, restart VSCode and switch) 

### Mac Users:
Open **Terminal** and run:

```bash
git --version
```

If a version number appears, Git is already installed. If macOS prompts you to install developer tools, click **Install** - this installs Git through Apple’s Command Line Tools (works natively on Apple Silicon).

If you want to install manually, run:

```bash
xcode-select --install
```

Alternatively, download the official macOS installer from [https://git-scm.com/download/mac](https://git-scm.com/download/mac), run the `.dmg`, and complete the setup.

### Linux Users
I love you guys 💕.

### Configure
After installation, configure Git:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

### Local Setup
Now open VSCode and clone (`ctrl+shift+p'-> Search: 'Git Clone') a repo: https://github.com/TXSTCODEPLAYGROUND/CS4332SPRING2026.git
This will prompt you to authenticate. Authenticate via browser loging.
Note: Some folks might have other browser as default browser, but you might be logged in your GitHub account in different browser. Make sure this is not happening.

---

## 1.4 Install DBeaver (Community Edition)

Download from:

[https://dbeaver.io/download/](https://dbeaver.io/download/)

Choose:

**DBeaver Community Edition (Free)**

Install using default settings.

DBeaver will be used to:

* Connect to MySQL
* View tables
* Run queries
* Generate ER diagrams

---

# 2. Self-Study: Basic Docker Concepts

Before running the lab, understand these concepts:

* What is a container?
* What is an image?
* What is a volume?
* What is port mapping?
* What is docker-compose?

You are expected to read:

* `Readme00 – Docker Basics.md`
* `Readme01 – Set up.md`
* `Readme03 – Storage and Volumes.md`
* `Readme04 – DBeaver Setup.md`

These are located inside the `db_lab/` folder.

---

# 3. Getting Started

Navigate into the lab directory:

```bash
cd db_lab
```

Start containers:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

You should see:

* MySQL
* (Other databases if configured)

---

# 4. Lab Structure

Inside `db_lab/` you will find:

* Docker configuration files
* SQL scripts
* Markdown instructions
* Setup guides

Use these files to:

* Experiment with creating tables
* Insert data
* Study relationships
* Explore physical storage
* Practice using DBeaver

---

# 5. Learning Workflow

Recommended order:

1. Read Docker basics
2. Start containers
3. Connect via CLI
4. Create tables
5. Insert data
6. Connect using DBeaver
7. View data and diagrams
8. Experiment and break things safely

---

# 6. Important Notes

* Always make sure Docker is running before connecting.
* If ports are already in use, stop old containers.
* Save SQL scripts inside the project folder.
* Do not rely only on GUI tools — practice CLI usage.

---

# 7. Objective

By completing this lab, you should understand:

* How databases run inside containers
* How to connect via CLI and GUI
* How foreign keys work
* How storage behaves physically
* How volumes persist data

---

This lab is meant for experimentation.
Break things. Restart. Rebuild. Learn.
