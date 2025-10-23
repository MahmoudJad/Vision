# Vision
Vision is the Product Information Management (PIM) microservice in the e-commerce ecosystem. It serves as the single source of truth for product-related data — defining, structuring, and maintaining the attributes, categories, and hierarchies that shape every product in the catalog. 

# 🧠 Vision — Product Information Management (PIM) Microservice

> “To see the world as it truly is.” — *Vision*

**Vision** is the PIM (Product Information Management) microservice responsible for defining, structuring, and managing all product information in the e-commerce ecosystem.

It acts as the *core intelligence layer* — ensuring every product is enriched with accurate attributes, properly categorized, and ready to be consumed by other services such as **Thiderman**, **Dragon**, and **Gachanger**.

---

## 🚀 Features

- 🗂 **Category Management**  
  Maintain a hierarchical product category tree with parent-child relationships.

- 🧱 **Attribute Management**  
  Define and manage attribute metadata such as name, type, scopable/localizable flags, and allowed options.

- 🧬 **Family & Variant Structures**  
  Create product families and family variants to define attribute sets and variant configurations.

- 📦 **Product Model Management**  
  Store and manage base product models used as templates for variant products.

- 🔍 **Validation Layer**  
  Ensure every product and variant fits within its assigned family and category rules.

- 🌐 **API-First Design**  
  Built with **FastAPI**, fully documented and OpenAPI-compliant.

- 🧾 **Database**  
  Supports both **PostgreSQL** (production) and **SQLite** (development/testing).

---

## 🏗️ Architecture Overview

Vision fits into the distributed system as follows:

