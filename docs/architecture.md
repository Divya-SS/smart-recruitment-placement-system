# System Architecture Documentation
## Smart Recruitment & Placement Management System (SRPMS)

### 1. High-Level Architecture Overview
The system follows a modern, decoupled client-server architecture:
- **Frontend:** Single Page Application (SPA) built with React.js and Vite.
- **Backend:** Modular REST API built with Python, Flask, and SQLAlchemy ORM.
- **Database:** Normalized Relational Database on MySQL 8.0 (InnoDB).
- **Authentication:** Stateless JSON Web Token (JWT) with Role-Based Access Control (RBAC).

```
[ React 18 Frontend ] <──(HTTPS / JSON REST API)──> [ Flask Backend API ] <──(PyMySQL / Pool)──> [ MySQL 8.0 Database ]
```

### 2. Backend Design Patterns
1. **Application Factory Pattern (`create_app`):** Enables isolated application configurations for development, testing, and production.
2. **Service Layer Pattern:** Routes/controllers parse HTTP requests and delegate business logic to dedicated services.
3. **Database Repository/ORM Pattern:** SQLAlchemy 2.0 ORM manages relational persistence, constraints, and eager loading.
4. **Standardized API Response Envelope:**
   ```json
   {
     "status": "success | error",
     "message": "Human-readable description",
     "data": { ... },
     "errors": null
   }
   ```
