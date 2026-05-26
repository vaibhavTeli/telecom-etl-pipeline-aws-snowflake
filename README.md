# Enterprise Telecom Billing ETL Pipeline

## 📌 Project Overview
An automated, end-to-end Data Engineering pipeline designed to process massive volumes of telecom Call Data Records (CDRs). This project extracts raw, unstructured log data from an AWS S3 Data Lake, performs in-memory transformations using Python (Pandas) to filter and aggregate usage metrics, and executes an automated bulk-load into a Snowflake Data Warehouse.

## 🏗️ Pipeline Architecture

```mermaid
graph LR
    subgraph Extract
    A[(AWS S3 Data Lake)] 
    end
    
    subgraph Transform
    B[Python & Pandas Engine]
    end
    
    subgraph Load
    C[(Snowflake Data Warehouse)]
    end

    A -->|boto3 data stream| B
    B -->|In-memory Cleaning & Aggregation| B
    B -->|snowflake-connector bulk load| C
    
    style A fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:black
    style B fill:#3776AB,stroke:#ffd343,stroke-width:2px,color:white
    style C fill:#29B5E8,stroke:#1A237E,stroke-width:2px,color:black