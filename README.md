# Cloud-Native Crypto Market ETL & Relational Data Pipeline

## 🚀 Project Overview
This repository features an end-to-end cloud-native data pipeline that ingests semi-structured market telemetry data, streams it into cloud storage infrastructure, and executes an automated transformation layer to generate a fully normalized relational data model (Star Schema). 

Designed to simulate an enterprise-grade data warehouse ingestion engine, this pipeline bypasses localized data constraints by utilizing a local cloud storage emulator to model real-world cloud operations.

---

## 📐 Data Architecture & Model
The pipeline shifts away from inefficient "wide-table" layouts, leveraging advanced data modeling to isolate entities and reduce data redundancy. Raw nested JSON payloads are parsed and structured into a high-performance **Star Schema** consisting of a centralized Fact table linked to independent Dimension lookup tables via deterministic cryptographic surrogate keys.

### Architectural Blueprint