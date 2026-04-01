# 🛒 E-Commerce Cross-Selling Engine

![Status: Frontend Pending](https://img.shields.io/badge/Status-Frontend_Integration_Pending-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Machine Learning](https://img.shields.io/badge/Algorithm-FP_Growth-success)

## Project Overview
This project implements a highly optimized, memory-efficient Market Basket Analysis recommendation engine. Using the **FP-Growth** algorithm, it mines over 3.2 million Instacart grocery orders to generate high-confidence "Frequently Bought Together" recommendations. 

The system architecture is decoupled: heavy offline data processing is separated from a lightweight online query engine, making it perfectly suited for a modern React + REST API web stack.

---

## System Architecture & Handoff

The core Machine Learning and Data Engineering phases are **100% complete**. The engine's logic has been compressed into a lightweight lookup table (`association_rules.csv`) that the backend can query in milliseconds.

### Completed (Data & ML Layer)
- [x] **Data Downcasting:** Optimized Pandas memory consumption.
- [x] **Statistical Sampling & Pruning:** Extracted 100k carts and removed long-tail items to allow local CPU execution.
- [x] **FP-Growth Rule Mining:** Generated Support, Confidence, and Lift metrics.
- [x] **Query Engine (`model.py`):** Wrote the Python logic to parse the rules and return top recommendations based on Lift.

### Pending Tasks (Frontend & API Layer)
The following tasks represent the current roadmap for the Full-Stack / Frontend team to bring this engine to production.

#### 1. Backend API Wrapper (FastAPI / Flask)
- [ ] Initialize a web server using FastAPI or Flask.
- [ ] Import the `get_recommendations()` function from `model.py`.
- [ ] Create a `GET` endpoint (e.g., `/api/recommend?item=Limes`).
- [ ] Ensure the API loads `association_rules.csv` into memory *once* on server startup (caching) rather than on every request.
- [ ] Format the Python list response into a clean JSON array to send to the client.

#### 2. React Frontend Interface
- [ ] **UI Layout:** Build a mock e-commerce shopping grid showing available groceries.
- [ ] **State Management:** Implement a "Virtual Cart" state in React to track items the user clicks.
- [ ] **Recommendation Component:** Build a dynamic "Frequently Bought Together" carousel or sidebar.

#### 3. Integration & Connecting the Stack
- [ ] Set up Axios or the native Fetch API in React to call the Python backend endpoint whenever a new item is added to the cart.
- [ ] Map over the returned JSON array to render the recommended product cards dynamically.
- [ ] Handle edge cases (e.g., UI behavior when the API returns an empty array for items with no strong recommendations).

---

## File Directory Guide

**Files for the Frontend/API Team:**
* `association_rules.csv`: The pre-computed "brain" of the engine. Load this into your API server.
* `model.py`: Contains the `load_engine()` and `get_recommendations()` logic to integrate into your API routes.

**Offline Files (Do Not Deploy to Web Server):**
* `dataHandling.py`: Initial data exploration.
* `modelBuilder.py`: The heavy ML pipeline used to create the CSV.
* `/data/`: Raw Instacart datasets (gigabytes in size).

---

## How to Test the Python Logic Locally

If the frontend team wants to verify the Python logic before building the API, run the following command in the terminal:

```bash
python model.py
