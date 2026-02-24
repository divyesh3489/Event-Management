# Event Management System - Development Task

## 🎯 Objective

Build a Django-based event management system with:

- Functional UI
- REST API backend
- Recurring events support
- Calendar view showing all occurrences

---

# ✅ Core Requirements

## 1️⃣ Event Management (CRUD)

Implement via:

- API (Django REST Framework)
- Functional UI (Django Templates)

Features:

- Create Event
- Update Event
- Delete Event
- List Events

Event Fields:

- Title
- Description (optional)
- Start datetime
- End datetime
- Recurrence (optional)

---

## 2️⃣ Recurring Events

Supported recurrence types:

- Daily
- Weekly
- Monthly

Recurrence must support:

- End date OR
- Number of occurrences

System must generate event occurrences automatically.

---

## 3️⃣ Functional UI

User should be able to:

- Create events via form
- Edit events
- Delete events
- View event list
- Configure recurrence
- View event details

Requirements:

- Fully connected to backend API
- Responsive and clean UI

---

## 4️⃣ Calendar View

Use:

- FullCalendar.js

Features:

- Month view
- Show recurring occurrences
- Click event to view details

---

## 5️⃣ Backend Integration

Frontend must:

- Load events from API
- No mock/static data

API must:

- Return events within date range
- Return expanded recurring occurrences

---

# 🧱 Technical Architecture

## Models

- Event
- Recurrence
- EventOccurrence

## Backend

- Django
- Django REST Framework

## Frontend

- Django Templates
- FullCalendar.js

---

# 📁 Implementation Steps

## Step 1

- Create project + app
- Setup DRF

## Step 2

- Create models
- Run migrations

## Step 3

- Implement recurrence logic

## Step 4

- Create API endpoints

## Step 5

- Build template UI

## Step 6

- Integrate FullCalendar

## Step 7

- Connect calendar to API

---

# ✅ Definition of Done

- Event CRUD works via UI and API
- Recurring events generated correctly
- Calendar displays all occurrences
- Frontend connected to backend
- Project runs locally without errors

---

# ⏱ Expected Time

Approx: 8 hours

---

# ⭐ Optional Bonus

- Edit single occurrence
- Exclude specific dates
- Week/day calendar view
- Drag & drop events
- Docker setup