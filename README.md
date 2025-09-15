# Backend Engineer Assessment
## Overview
This is a Django + DRF backend service for managing:
- Customers
- Categories (with nested hierarchy)
- Products
- Orders

It will support authentication (OpenID Connect), APIs for product/category management, ordering, and notifications via SMS + email.

## Tech Stack
- Python 3.11
- Django + Django REST Framework
- PostgreSQL
- Docker & docker-compose
- GitHub Actions (CI/CD)

## Setup
```bash
git clone <repo>
cd sil-backend
docker-compose up --build
