# Zinc Test Design Document

## 📋 Overview

This document outlines the technical design and architecture of the Zinc Test application, a sales data processing and management system.

## 🏗️ Architecture

### Core Components

#### 🚀 FastAPI

- Modern API design with async support
- Automatic API documentation via Swagger UI
- High performance and easy to maintain

#### 💾 SQLModel

- Combines SQLAlchemy and Pydantic
- Type-safe data validation
- Clean and intuitive ORM interface

#### 🐘 PostgreSQL

- High performance and reliable
- Rich set of features

#### 🔄 Alembic

- Database migration management
- Version control for schema changes
- Safe deployment of database updates

#### 🔍 Sentry

- Real-time error tracking
- Performance monitoring
- Distributed tracing capabilities

## 📊 Data Model

Each row in sales data is parsed into three interconnected models:

### 🏷️ Product

*Core entity representing available products*

```sql
CREATE TABLE products (
    id          INTEGER PRIMARY KEY,
    name        VARCHAR(255),
    price       FLOAT CHECK (price >= 0),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🛍️ Order

*Represents customer purchase transactions*

```sql
CREATE TABLE orders (
    id                  INTEGER PRIMARY KEY,
    client_id          INTEGER CHECK (client_id >= 0),
    sale_id            INTEGER CHECK (sale_id >= 0),
    batch_number       INTEGER CHECK (batch_number >= 0),
    sales_notes        VARCHAR(255),
    notes              VARCHAR(255),
    subtotal           FLOAT,
    total              FLOAT,
    discount_percentage FLOAT DEFAULT 0,
    discount_amount    FLOAT DEFAULT 0,
    tax                FLOAT,
    date               DATE CHECK (date <= CURRENT_DATE),
    location           VARCHAR(255) CHECK (location IN ('Online Store', 'Golf - experience')),
    created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📦 OrderItem

*Links products to orders with quantity information*

```sql
CREATE TABLE order_items (
    id          INTEGER PRIMARY KEY,
    order_id    INTEGER REFERENCES orders(id),
    product_id  INTEGER CHECK (product_id >= 0),
    quantity    INTEGER,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🛠️ Infrastructure

### Development Environment

- **Python 3.12+** - Latest stable Python version
- **Poetry** - Dependency and virtual environment management
- **Docker & Docker Compose** - Containerization and orchestration

### Production Deployment

- Containerized workloads
- Environment-based configuration
- Secure credential management

## 📈 Scaling & Resilience

### Horizontal Scaling

The application is designed for horizontal scaling:

- Stateless architecture
- Container-based deployment
- Load balancer ready

### Resilience Features

- Health checks
- Container orchestration

## 🔄 CI/CD Pipeline

### Continuous Integration

1. **Test Suite**
   - Run unit tests with pytest
   - Run migrations on a fresh database to check for syntax or logical errors

2. **Build Process**
   - Build docker image
   - Push docker image to a container registry

### Continuous Deployment

1. **Pre-deployment**
   - Database backup

2. **Deployment**
   - New version rollout
   - Migration execution
   - Health checks
   - Rollback if needed

3. **Post-deployment**
   - Verification
   - Old version cleanup

### Rollback Strategy

- Database migration rollback
- Container version reversion
- Backup restoration

## 📊 Observability

### Monitoring

- Container resource metrics
- Application performance
- Database health
- API response times

### Alerting

- Critical error notifications
- Performance degradation alerts
- Resource utilization warnings
- Service health monitoring

## ⚖️ Trade-Offs

### Technical Decisions

1. **FastAPI vs Django**
   - ✅ Modern async support
   - ✅ Automatic documentation
   - ❌ Less built-in features

2. **SQLModel vs SQLAlchemy**
   - ✅ Pydantic integration
   - ✅ Type safety
   - ❌ Less mature ecosystem
