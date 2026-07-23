# AI Prompts & Workflow Log

This document serves to log the high-level prompts, instructions, and iterative steps used alongside an AI coding assistant (Antigravity/DeepMind) to build this project from scratch using Test-Driven Development (TDD).

## Core Directives

The AI was instructed to follow a strict workflow:
1. **Tech Stack**: FastAPI, PostgreSQL, React, Tailwind CSS v4.
2. **Workflow Preference**: "Do only 1 task at a time and start the next task only when I type next."
3. **TDD & Git Commits**: "After every red do a commit and then after every green and also after refactoring."
4. **Git Attribution**: "Whenever commit or push is required Pls give me the commit message... I want the co authored by antigravity part but I dont want to show commits in their name [on GitHub]."

---

## Phase 1: Foundation (PostgreSQL & Models)
**Prompts/Steps:**
- "Set up a FastAPI project connected to PostgreSQL using SQLAlchemy."
- "Create Pydantic and SQLAlchemy models for User and Vehicle. User needs email, username, hashed password, and role (USER/ADMIN). Vehicle needs make, model, year, price, quantity, and category."
- "Setup pytest with an isolated SQLite in-memory database for testing."

## Phase 2: Authentication (TDD)
**Prompts/Steps:**
- "Write failing tests for user registration (`POST /api/auth/register`)." -> *[RED Commit]*
- "Implement the `/register` endpoint so the tests pass." -> *[GREEN Commit]*
- "Write a failing test for duplicate email registration." -> *[RED Commit]*
- "Implement the duplicate email check." -> *[GREEN Commit]*
- "Write failing tests for `/login` returning a JWT." -> *[RED Commit]*
- "Implement JWT generation using `python-jose` and the `/login` endpoint." -> *[GREEN Commit]*

## Phase 3: Vehicle CRUD & Inventory (TDD)
**Prompts/Steps:**
- "Write failing tests for Vehicle CRUD endpoints. Add vehicle, get all vehicles, search by make/price, update vehicle, delete vehicle. Ensure delete and update are Admin-only." -> *[RED Commit]*
- "Implement the vehicle CRUD endpoints." -> *[GREEN Commit]*
- "Write failing tests for inventory actions: `POST /vehicles/{id}/purchase` (decrements stock, auth required) and `POST /vehicles/{id}/restock` (increments stock, admin only)." -> *[RED Commit]*
- "Implement the inventory endpoints." -> *[GREEN Commit]*
- "Fix Pydantic V2 deprecation warnings in schemas." -> *[REFACTOR Commit]*

## Phase 4: Frontend Development
**Prompts/Steps:**
- "Scaffold a React + Vite + Tailwind CSS v4 Single Page Application. It needs a Login page, Register page, and a Dashboard displaying vehicles."
- "Use Axios to proxy requests to the backend (`/api`). Store JWT in localStorage."
- "Design must be premium: use dark mode, glassmorphism, Lucide icons, and modern typography."
- "Ensure Admin-only features (Add Vehicle, Edit, Delete, Restock) are conditionally rendered based on the logged-in user's role."
- *[GREEN Commit for Frontend scaffolding]*

## Phase 5: Admin Panel & Git History Fix
**Prompts/Steps:**
- "Git history is showing real GitHub users for the AI's email. Rewrite git history using filter-branch to change the `Co-authored-by` email to a dummy `.invalid` domain." -> *[Executed via filter-branch scripts]*
- "I think there should be one admin user right that can promote other users to admin too with their email id?"
- "Write failing tests for `POST /api/admin/promote-user`." -> *[RED Commit]*
- "Implement the promote-user endpoint and a startup event to seed `FIRST_ADMIN_EMAIL` from `.env`." -> *[GREEN Commit]*
- "Refactor `@app.on_event('startup')` to use FastAPI lifespan." -> *[REFACTOR Commit]*
- "Build the frontend `AdminUsersPage` to list users and promote them. Add a link in the Dashboard header." -> *[GREEN Commit]*

## Phase 6: Documentation
**Prompts/Steps:**
- "Document the Project: Create `README.md` and `PROMPTS.md`."

---

*End of Development Log*
