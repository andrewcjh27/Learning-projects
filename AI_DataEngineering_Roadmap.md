# AI & Data Engineering Knowledge Roadmap
> From fundamentals to production-grade systems — with hands-on projects at each stage.

---

## How to Use This Roadmap

- Follow the **phases in order** — each builds on the last.
- Sections marked **[PROJECT]** are hands-on milestones. Don't skip them.
- Estimated time per phase assumes ~10 hrs/week.
- Link your projects to a GitHub portfolio as you go.

---

## Phase 0 — Computer Science Fundamentals (2–3 weeks)

Before touching any tool, you need the mental model for *why* systems work the way they do.

### CPU & Memory Architecture
- **CPU**: cores, threads, clock speed, cache hierarchy (L1/L2/L3), instruction pipelines
- **RAM vs. disk**: latency differences (ns vs. μs vs. ms) — this explains why in-memory databases exist
- **Processes vs. threads**: concurrency, parallelism, the GIL in Python
- **Why this matters**: understanding CPU bottlenecks helps you know when to switch to Spark, Dask, or a GPU

### GPU Architecture
- **GPU vs. CPU**: thousands of small cores vs. a few powerful ones — GPUs win at embarrassingly parallel math
- **VRAM**: why model size is constrained by GPU memory
- **CUDA**: NVIDIA's parallel computing platform; the backbone of deep learning
- **Tensor cores**: specialized hardware for matrix multiply — used by transformers
- **When GPU > CPU**: matrix operations, neural network training, batch inference
- **Key concepts**: throughput vs. latency, kernel launches, memory bandwidth

### Networking Basics
- HTTP/HTTPS, TCP/IP, DNS — how data moves between machines
- Latency vs. throughput
- Ports, sockets, load balancers

### Resources
- *Computer Science Distilled* (book) — fast overview
- MIT 6.004 OpenCourseWare (free) for architecture depth
- 3Blue1Brown for visual math intuition

---

## Phase 1 — Linux, the Command Line & Git (2 weeks)

Almost all data infrastructure runs on Linux. Fluency here is non-negotiable.

### Linux & Shell
- File system, permissions, processes (`ps`, `top`, `htop`)
- Shell scripting: `bash`, pipes, redirects, `cron` for scheduling
- `ssh`, `scp`, `rsync` — remote access to servers and cloud instances
- `tmux` / `screen` — persistent sessions on remote machines
- Environment variables, `.bashrc`, `PATH`

### Git
- Branching, merging, rebasing
- Pull requests, code review workflows
- `.gitignore`, tagging releases
- **Why it matters**: every tool in this roadmap — dbt, Airflow, Spark jobs — is version-controlled with Git

### [PROJECT 0] Automate a Local Task with Shell
Build a shell script that:
1. Downloads a public dataset (e.g., NYC taxi data via `curl`)
2. Does basic cleaning/counting with `awk` or `python`
3. Logs output with timestamps to a file
4. Schedules itself with `cron`

**Skills locked in**: Linux fluency, scripting, scheduling basics

---

## Phase 2 — Python for Data (3–4 weeks)

Assume you know basic Python. This phase fills the gaps that matter professionally.

### What to Know Beyond Basics
- **Type hints** and readable code style (PEP 8, `ruff`)
- **Virtual environments**: `venv`, `conda`, `poetry` — isolation matters for reproducibility
- **Iterators & generators**: lazy evaluation — key for large data
- **Decorators**: used heavily in Airflow, FastAPI, pytest
- **`dataclasses`** and **`pydantic`**: typed data structures, used in APIs and pipelines
- **Async Python**: `asyncio`, `aiohttp` — needed for non-blocking API calls
- **Error handling patterns**: retries, backoff, circuit breakers

### Data Libraries
- `pandas` — tabular data, but know its memory limits (~5–10x dataset size in RAM)
- `polars` — faster, lazy evaluation, better for large files
- `numpy` — array math, backbone of ML libraries
- `pyarrow` — columnar format, bridges pandas ↔ Spark ↔ cloud storage
- `pydantic` — data validation (critical for APIs and pipeline schemas)

### [PROJECT 1] Data Pipeline in Pure Python
Build a local ETL pipeline:
1. Ingest a CSV/JSON dataset (e.g., GitHub Events API — public, free)
2. Clean and transform with `pandas` + `pydantic` for schema validation
3. Output to Parquet format using `pyarrow`
4. Write unit tests with `pytest`

**Skills locked in**: Python fluency, data types, schema validation, Parquet format

---

## Phase 3 — APIs: Building & Consuming (3–4 weeks)

APIs are how every modern system communicates. You'll use them as a consumer (calling OpenAI, AWS, databases) and as a builder (exposing your own data pipelines and models).

### What is an API?
- **REST**: stateless, HTTP-based, uses JSON — the dominant pattern
- **GraphQL**: query exactly what you need — used by GitHub, Shopify
- **gRPC**: binary protocol, fast, used in microservices and ML serving
- **WebSockets**: persistent connections — used in real-time dashboards

### HTTP Deep Dive
- Methods: GET, POST, PUT, PATCH, DELETE
- Status codes: 200, 201, 400, 401, 403, 404, 422, 500, 503
- Headers: `Authorization`, `Content-Type`, `Accept`, `Rate-Limit`
- Authentication: API keys, OAuth 2.0, JWT tokens
- **Pagination**: offset vs. cursor-based — important when pulling large datasets from APIs
- **Rate limiting**: how to handle 429 errors with exponential backoff

### Building APIs with FastAPI
- Route handlers, path/query parameters, request bodies
- Pydantic models for request/response validation
- Dependency injection, middleware
- Background tasks
- OpenAPI/Swagger auto-documentation

### Consuming APIs
- `httpx` (async) and `requests` (sync)
- Session management, connection pooling
- Streaming responses (important for LLM APIs)

### [PROJECT 2A] Build a REST API with FastAPI
Build a "Data Access API" that:
1. Has endpoints to query a local SQLite/DuckDB database
2. Accepts filters via query parameters (e.g., `?date=2024-01&city=NYC`)
3. Returns paginated JSON responses
4. Implements API key authentication
5. Includes rate limiting middleware
6. Auto-generates Swagger docs

**Skills locked in**: REST design, authentication, pagination, data access patterns

### [PROJECT 2B] Build an API Client / Data Ingestion Pipeline
Pick a real public API (GitHub, Open-Meteo weather, Alpha Vantage stocks):
1. Write a Python client class with retry logic, pagination, and rate limiting
2. Pull data on a schedule, store raw JSON to disk
3. Transform and load into a local database
4. Expose a summary endpoint via your FastAPI from 2A

**Skills locked in**: API consumption patterns, data ingestion, error handling

---

## Phase 4 — Databases (4–5 weeks)

Data engineers live in databases. You need to understand the full landscape.

### Relational Databases (SQL)
- **ACID properties**: Atomicity, Consistency, Isolation, Durability — why transactions exist
- **Indexes**: B-trees, composite indexes, covering indexes — how queries get fast
- **Query planner**: `EXPLAIN ANALYZE` — read execution plans
- **Joins**: how hash joins, nested loops, and merge joins work under the hood
- **Window functions**: `ROW_NUMBER`, `LAG`, `LEAD`, `PARTITION BY` — essential for analytics
- **CTEs and subqueries**: readable, maintainable SQL
- **Normalization vs. denormalization**: 3NF for OLTP, star schema for OLAP
- Databases to know: **PostgreSQL** (production workhorse), **SQLite** (local/embedded)

### Analytical / OLAP Databases
- **DuckDB**: in-process analytical DB — runs on your laptop, reads Parquet/CSV, SQL interface. Think "SQLite for analytics."
- **Columnar storage**: why column stores (vs. row stores) are fast for aggregations
- **Snowflake**: cloud data warehouse — covered in Phase 8
- **BigQuery**: Google's serverless warehouse (similar concept to Snowflake)

### NoSQL Databases
- **Document stores** (MongoDB): flexible schema, good for semi-structured data
- **Key-value stores** (Redis): in-memory, microsecond latency — used for caching, sessions, queues
- **Wide-column** (Cassandra): massive write throughput, eventual consistency — IoT, time-series
- **When to use what**: SQL for structured + transactions; NoSQL for scale, flexibility, or special access patterns

### Data Formats
- **CSV**: universal but slow, no schema
- **JSON**: flexible, human-readable, verbose
- **Parquet**: columnar, compressed, schema-embedded — the default for data lakes
- **Avro**: row-based, schema evolution — common in Kafka streams
- **Delta Lake / Iceberg**: table formats on top of Parquet — versioning, ACID on data lakes

### [PROJECT 3] Build a Local Data Warehouse
1. Use DuckDB as your analytical store
2. Load your Parquet files from Project 1 & 2
3. Design a star schema (fact + dimension tables)
4. Write 10 analytical SQL queries (aggregations, window functions, CTEs)
5. Add a Redis cache layer in front of your FastAPI from Project 2A for hot queries

**Skills locked in**: OLAP design, star schema, DuckDB, Redis caching, SQL mastery

---

## Phase 5 — Tokenization, Embeddings & NLP Fundamentals (2–3 weeks)

This bridges classical data work with modern AI. Essential for understanding LLMs and building RAG systems.

### Tokenization
- **What a token is**: a chunk of text (word, subword, or character) that a model processes
- **Why it matters**: LLM pricing, context window limits, and latency are all measured in tokens
- **BPE (Byte Pair Encoding)**: how GPT tokenizers work — merges frequent character pairs
- **WordPiece**: used by BERT — similar idea, different objective
- **SentencePiece**: language-agnostic tokenizer used by T5, LLaMA
- **tiktoken**: OpenAI's fast tokenizer — use this to count tokens before API calls
- **Vocabulary size**: GPT-4 ~100k tokens; affects embedding table size

### Embeddings
- **Word embeddings**: Word2Vec, GloVe — dense vector representations of words
- **Sentence/document embeddings**: encoding meaning of full passages into a vector
- **Semantic similarity**: cosine similarity between vectors
- **Embedding models**: `text-embedding-3-small` (OpenAI), `all-MiniLM-L6-v2` (sentence-transformers, free/local)
- **Dimensionality**: typical embedding vectors are 384–3072 dimensions

### Vector Databases
- **What they store**: high-dimensional vectors with metadata
- **What they do**: fast approximate nearest neighbor (ANN) search — "find the 5 most similar embeddings"
- **Algorithms**: HNSW (Hierarchical Navigable Small World), IVF — know the trade-offs
- **Tools**: **pgvector** (Postgres extension), **Pinecone** (managed), **Weaviate**, **Chroma** (local, great for dev), **Qdrant**
- **When to use**: semantic search, recommendation systems, RAG pipelines

### [PROJECT 4A] Semantic Search Engine
1. Take a dataset of documents (e.g., Wikipedia articles, your own notes, arXiv papers)
2. Chunk them into ~500 token segments (use `tiktoken` to count)
3. Embed each chunk using `sentence-transformers`
4. Store vectors in **Chroma** (local)
5. Build a FastAPI endpoint: POST a query → get top-5 most relevant chunks

**Skills locked in**: tokenization, chunking, embeddings, vector search, ANN

---

## Phase 6 — RAG (Retrieval-Augmented Generation) (3–4 weeks)

RAG is the dominant pattern for making LLMs useful on private/custom data.

### What RAG Is
- **Problem**: LLMs have a fixed knowledge cutoff and no access to your private data
- **Solution**: at query time, retrieve relevant documents from your knowledge base, inject them into the LLM prompt as context
- **Architecture**: Query → Embed → Vector Search → Retrieve Chunks → Prompt + Chunks → LLM → Answer

### RAG Components in Detail
- **Chunking strategy**: fixed-size, sentence-aware, recursive — matters more than most people think
- **Retrieval**: dense (vector search), sparse (BM25/keyword), hybrid (combine both)
- **Reranking**: after initial retrieval, use a cross-encoder to rerank by relevance (e.g., Cohere Rerank)
- **Prompt engineering**: how to structure retrieved context in the prompt without confusing the model
- **Context window management**: retrieved docs must fit; truncation and summarization strategies
- **Hallucination mitigation**: citations, faithfulness checks, grounding

### Advanced RAG Patterns
- **Multi-query retrieval**: generate multiple queries from one user question, merge results
- **HyDE (Hypothetical Document Embeddings)**: generate a hypothetical answer, embed it, search with that
- **Parent-child chunking**: store small chunks for retrieval, return larger parent chunks for context
- **Agentic RAG**: the LLM decides when and what to retrieve (tool use)

### LLM API Usage
- OpenAI API: chat completions, streaming, function calling / tool use
- Token management: system vs. user vs. assistant messages, context limits
- Cost estimation: `input_tokens × price + output_tokens × price`
- Streaming responses for better UX

### Tools
- **LangChain** / **LlamaIndex**: RAG frameworks — good for prototyping, understand what they abstract
- **DSPy**: programmatic prompt optimization — worth knowing
- Know the frameworks but be able to build RAG without them too

### [PROJECT 4B] Full RAG Application
Extend Project 4A into a complete RAG system:
1. Add an LLM response layer (OpenAI API or local model via `ollama`)
2. Implement hybrid retrieval (dense + BM25 with `rank_bm25`)
3. Add reranking step
4. Stream the LLM response through your FastAPI endpoint
5. Build a minimal chat UI (Streamlit or Gradio)
6. Track: query, retrieved chunks, latency, token count per request (log to DuckDB)

**Skills locked in**: full RAG pipeline, LLM APIs, streaming, hybrid retrieval, observability

---

## Phase 7 — Cloud Fundamentals (4–5 weeks)

Cloud is the infrastructure layer everything else runs on. Pick one provider to go deep (AWS recommended for job market), then know the patterns that transfer to all.

### Core Cloud Concepts
- **Regions and Availability Zones**: geographic redundancy
- **IAM (Identity & Access Management)**: users, roles, policies — security foundation
- **Shared responsibility model**: what the cloud secures vs. what you secure
- **Managed vs. unmanaged services**: e.g., RDS (managed Postgres) vs. EC2 + self-hosted Postgres

### Compute
- **EC2 (AWS) / Compute Engine (GCP) / VMs (Azure)**: virtual machines — full control, you manage the OS
- **Instance types**: CPU-optimized (C series), memory-optimized (R series), GPU (P/G series)
- **Auto Scaling Groups**: automatic horizontal scaling based on load
- **Lambda (AWS) / Cloud Functions (GCP)**: serverless — no servers to manage, pay per invocation
- **ECS / EKS**: container orchestration (Docker + Kubernetes) — covered more in Phase 9

### Storage
- **S3 (AWS) / GCS (GCP)**: object storage — infinitely scalable, cheap, stores Parquet/CSV/JSON
- **Storage classes**: hot (frequent access) vs. cold (archival) — cost trade-off
- **EBS**: block storage attached to EC2 instances (like a hard drive)
- **EFS**: network file system, shared across instances

### Networking
- **VPC**: your private network in the cloud
- **Subnets**: public (internet-accessible) vs. private
- **Security Groups**: firewall rules
- **Load Balancers**: ALB (application layer), NLB (network layer)

### Managed Data Services
- **RDS**: managed relational DB (Postgres, MySQL, etc.)
- **DynamoDB**: managed NoSQL key-value/document store
- **ElastiCache**: managed Redis
- **Kinesis**: managed real-time streaming (like Kafka)
- **Glue**: managed ETL + data catalog
- **Athena**: SQL on S3 using Presto — serverless, pay per query

### [PROJECT 5A] Deploy Your API to the Cloud
Take your FastAPI from Project 2A:
1. Containerize it with **Docker**
2. Push the image to **ECR** (Elastic Container Registry)
3. Deploy to **AWS App Runner** or **ECS Fargate** (serverless containers)
4. Set up an **Application Load Balancer**
5. Store your DuckDB data files in **S3**
6. Add environment-based config via **AWS Secrets Manager**
7. Set up **CloudWatch** logging and basic alarms

**Skills locked in**: Docker, ECR, cloud deployment, load balancing, secrets management, observability

### [PROJECT 5B] Build a Cloud Data Lake
1. Create an S3 bucket as your data lake
2. Write a Lambda function that triggers on S3 upload (new raw data file arrives)
3. Lambda cleans/transforms and writes Parquet to a processed/ prefix
4. Register the Parquet tables in **AWS Glue Data Catalog**
5. Query with **Athena** — write 5 analytical queries
6. Visualize with a simple dashboard (use Streamlit querying Athena via `boto3`)

**Skills locked in**: event-driven pipelines, Glue catalog, Athena, S3 data lake patterns

---

## Phase 8 — The Modern Data Stack (4–5 weeks)

This is the toolchain used by virtually every data team: Fivetran → Snowflake → dbt → visualization.

### Snowflake
- **Architecture**: separates storage (S3) from compute (virtual warehouses) — scale each independently
- **Virtual warehouses**: compute clusters you turn on/off, size up/down
- **Micro-partitioning**: automatic data clustering — how Snowflake achieves fast queries without manual indexes
- **Time Travel**: query data as it existed at a past point in time
- **Zero-copy cloning**: instant copies of tables/schemas for dev/test
- **Data sharing**: share live data with other Snowflake accounts without copying
- **Stages**: internal/external — loading data from S3 into Snowflake
- **Snowpipe**: auto-ingest data as it lands in S3
- **Cost model**: storage (cheap) + compute (by second) + data transfer

### Fivetran
- **What it does**: managed EL (Extract + Load) — connectors to 300+ sources (Salesforce, Postgres, GA, Shopify, etc.)
- **What it doesn't do**: transform — that's dbt's job
- **Incremental sync**: tracks what's changed since the last sync (CDC or timestamp-based)
- **Schema migration**: handles upstream schema changes automatically
- **When to use vs. custom pipelines**: Fivetran wins when a connector exists; custom wins for unusual sources or cost sensitivity at scale

### dbt (data build tool)
- **What it is**: SQL-based transformation layer — turns raw data into analytics-ready models
- **Models**: SQL `SELECT` statements that dbt materializes as tables or views
- **Materializations**: `view`, `table`, `incremental`, `ephemeral`
- **Incremental models**: only process new/changed rows — critical for large tables
- **Refs and sources**: `{{ ref('model_name') }}` — dbt builds the DAG automatically
- **Tests**: `not_null`, `unique`, `accepted_values`, `relationships` — data quality built in
- **Documentation**: auto-generated data catalog from `description` fields
- **Macros**: Jinja templating for reusable SQL logic
- **Snapshots**: slowly changing dimension (SCD Type 2) handling
- **dbt Cloud vs. dbt Core**: managed vs. self-hosted

### Airflow (Orchestration)
- **What it is**: a workflow orchestrator — defines, schedules, and monitors DAGs (Directed Acyclic Graphs) of tasks
- **Core concepts**: DAG, Task, Operator, Sensor, XCom, Connection, Variable
- **Operators**: `PythonOperator`, `BashOperator`, `SQLOperator`, `S3Sensor`, `DbtOperator`
- **Scheduling**: cron syntax + dynamic scheduling
- **Backfill**: re-run historical DAG runs
- **Idempotency**: DAG runs must be safe to retry — design tasks so re-running doesn't corrupt data
- **TaskFlow API**: modern Python-native way to write DAGs
- **Alternatives**: **Prefect** (more Pythonic, easier local dev), **Dagster** (asset-centric, better for data engineering), **Mage**

### [PROJECT 6] End-to-End Modern Data Stack Pipeline
Build a complete pipeline:
1. Use **Fivetran** (free trial) to sync a source (e.g., Google Sheets or a Postgres DB) → Snowflake
2. Write **dbt models**: staging → intermediate → mart layers
3. Add dbt **tests** and **documentation**
4. Orchestrate the full pipeline with **Airflow** (run locally with Docker Compose):
   - Fivetran trigger → dbt run → dbt test → alert on failure
5. Query the mart layer from Snowflake and build a dashboard (Metabase, Streamlit, or Looker Studio)

**Skills locked in**: full modern data stack, dbt modeling patterns, Airflow DAGs, Snowflake

---

## Phase 9 — Distributed Computing & Scalable Pipelines (4–5 weeks)

When data doesn't fit in memory or a single machine, you need distributed systems.

### Why Distributed Computing?
- A single machine: ~terabytes of disk, ~hundreds of GB of RAM, ~hundreds of CPU cores
- A cluster: petabytes of storage, terabytes of RAM, thousands of cores
- Trade-off: network overhead, complexity, debugging difficulty

### Apache Spark
- **Architecture**: Driver + Executors; Spark distributes work across a cluster
- **RDD → DataFrame → Dataset**: evolution of the core abstractions; use DataFrames
- **Lazy evaluation**: transformations build a DAG, nothing runs until an action is called
- **Partitioning**: how data is split across executors — bad partitioning kills performance
- **Shuffle**: when Spark needs to redistribute data across partitions (e.g., `groupBy`, `join`) — most expensive operation
- **Catalyst optimizer**: Spark's query planner — rewrites your DataFrame code for efficiency
- **Tungsten**: memory management and code generation engine
- **PySpark**: Python API — what you'll use day-to-day
- **SparkSQL**: run SQL on DataFrames — familiar entry point
- **Delta Lake**: ACID transactions + versioning on top of Spark + Parquet
- **Where it runs**: EMR (AWS), Databricks, GCP Dataproc, local mode for dev

### Apache Beam
- **What it is**: a unified programming model for batch and streaming pipelines
- **Runners**: the same Beam pipeline can run on Dataflow (GCP), Flink, Spark, or locally
- **Key concepts**: `PCollection`, `PTransform`, `Pipeline`, windowing
- **When to use vs. Spark**: Beam is better for streaming-first, multi-runner portability; Spark for batch-heavy analytics

### Kafka & Streaming
- **What Kafka is**: distributed event log — producers write events, consumers read them
- **Topics, partitions, consumer groups**: the core abstractions
- **Retention**: Kafka retains messages for a configurable time (not just until consumed)
- **Kafka Connect**: ingests data from DBs/APIs into Kafka and out to destinations
- **Kafka Streams / ksqlDB**: stream processing on top of Kafka
- **When streaming matters**: real-time dashboards, fraud detection, event-driven architectures, CDC

### HPC Environments
- **What HPC is**: High-Performance Computing — clusters with fast interconnects (InfiniBand), shared filesystems (Lustre/GPFS), job schedulers
- **SLURM**: the dominant job scheduler — submit jobs, request resources (CPUs, GPUs, RAM), wait in queue
- **Batch jobs vs. interactive**: most HPC work is batch — submit a script, it runs when resources are available
- **MPI**: Message Passing Interface — low-level distributed computing for scientific simulations
- **Module system**: `module load python/3.10` — shared software environments on HPC clusters
- **When you'll use it**: large model training, genomics, physics simulations, research computing
- **Cloud HPC**: AWS ParallelCluster, Google Batch — bring HPC patterns to cloud

### [PROJECT 7] Distributed Data Pipeline with Spark
1. Spin up a local Spark cluster with Docker Compose (or use Databricks Community Edition — free)
2. Process a large dataset (>1GB) — NYC Taxi data works well (~30GB uncompressed)
3. Implement a pipeline: ingest raw CSV → clean → aggregate → write Delta Lake tables
4. Practice: repartitioning, caching, broadcasting small tables, reading Spark UI to find bottlenecks
5. Write the same pipeline in both Spark SQL and DataFrame API
6. Compare performance: local pandas vs. Spark (understand when Spark is NOT worth the overhead)

**Skills locked in**: Spark internals, PySpark, Delta Lake, cluster debugging, Spark UI

---

## Phase 10 — MLOps & Model Deployment (3–4 weeks)

Data scientists build models; data engineers productionize them. You need both sides.

### ML Experiment Tracking
- **MLflow**: log parameters, metrics, artifacts; compare runs; model registry
- **Weights & Biases**: richer UI, better for deep learning
- **Key concepts**: experiment, run, artifact, model version, stage (Staging → Production)

### Model Serving
- **Batch inference**: run predictions on a dataset, store results — use Spark or Airflow
- **Real-time inference**: low-latency API endpoint — FastAPI + model loaded in memory, or managed serving
- **Model serialization**: `pickle`, `joblib`, ONNX (cross-platform), TorchScript
- **Managed serving**: AWS SageMaker, GCP Vertex AI, Databricks Model Serving

### Feature Stores
- **What they solve**: training-serving skew (features computed differently at train vs. serve time)
- **Tools**: Feast (open-source), Tecton (managed), Hopsworks
- **Online vs. offline store**: offline for training (historical), online for low-latency serving

### Containerization & Kubernetes Basics
- **Docker**: build images, write Dockerfiles, multi-stage builds
- **Docker Compose**: multi-container local development
- **Kubernetes**: container orchestration at scale — Pods, Deployments, Services, Ingress
- **Helm**: Kubernetes package manager
- You don't need to be a K8s expert, but you need to read manifests and deploy workloads

### CI/CD for Data
- GitHub Actions for running dbt tests, Spark tests, model validation on every PR
- Automated data quality checks before promotion to production
- Blue-green deployments for models

### [PROJECT 8] End-to-End ML Pipeline
1. Train a simple ML model (scikit-learn or LightGBM) on your cleaned data
2. Track experiments with **MLflow** (local)
3. Register the best model in MLflow Model Registry
4. Serve it via a FastAPI endpoint with a health check
5. Containerize and deploy to your cloud setup from Project 5A
6. Build an Airflow DAG that retrains the model weekly, evaluates it, and promotes if better
7. Add a simple monitoring check: alert if prediction distribution shifts

**Skills locked in**: MLflow, model registry, automated retraining, model serving, monitoring

---

## Phase 11 — Advanced Topics (ongoing)

These are specializations to pick based on your role and interests.

### Data Contracts & Data Quality
- **Data contracts**: formal agreements between data producers and consumers on schema and SLAs
- **Great Expectations** / **Soda**: data quality frameworks — define expectations, test data
- **dbt tests + Airflow alerts**: lightweight quality gates in your existing stack

### Reverse ETL
- **What it is**: moving data from your warehouse back into operational tools (Salesforce, HubSpot)
- **Tools**: Census, Hightouch

### Real-Time Analytics
- **Pinot / Druid**: OLAP databases designed for sub-second queries on millions of rows with real-time ingestion
- **Flink**: powerful stateful stream processing — more complex than Beam but more capable

### LLM Infrastructure at Scale
- **vLLM**: high-throughput LLM inference server — uses PagedAttention for efficient GPU memory use
- **Triton Inference Server**: NVIDIA's serving framework — optimized for GPU inference
- **Quantization**: INT8/INT4 — reduce model size and memory at slight accuracy cost
- **LoRA / QLoRA**: parameter-efficient fine-tuning — fine-tune LLMs without updating all weights
- **Multi-GPU / multi-node training**: tensor parallelism, pipeline parallelism, data parallelism

### Infrastructure as Code
- **Terraform**: declare cloud infrastructure in code — reproducible, version-controlled infra
- **Pulumi**: IaC with real programming languages (Python, TypeScript)

---

## Suggested Project Portfolio Summary

| Project | Phase | Core Skills Demonstrated |
|---------|-------|--------------------------|
| [P0] Shell ETL script | 1 | Linux, scripting, scheduling |
| [P1] Python pipeline → Parquet | 2 | Python, pandas, pydantic, data formats |
| [P2A] FastAPI data access layer | 3 | REST API design, auth, pagination |
| [P2B] API ingestion pipeline | 3 | API client, retry logic, data ingestion |
| [P3] Local data warehouse + Redis | 4 | DuckDB, star schema, caching |
| [P4A] Semantic search engine | 5 | Embeddings, vector DB, ANN search |
| [P4B] Full RAG application | 6 | RAG, LLM APIs, hybrid retrieval |
| [P5A] Deploy API to AWS | 7 | Docker, ECS, ALB, Secrets Manager |
| [P5B] Cloud data lake | 7 | S3, Lambda, Glue, Athena |
| [P6] Full modern data stack | 8 | Fivetran, Snowflake, dbt, Airflow |
| [P7] Distributed Spark pipeline | 9 | PySpark, Delta Lake, cluster tuning |
| [P8] End-to-end ML pipeline | 10 | MLflow, model serving, automated retraining |

---

## Tool & Technology Map

```
DATA INGESTION          STORAGE               TRANSFORMATION
─────────────           ─────────             ──────────────
Fivetran                S3 / GCS              dbt
Custom Python APIs      Snowflake             Spark / PySpark
Kafka Connect           PostgreSQL / RDS      Apache Beam
AWS Glue                DuckDB (local)        Pandas / Polars
                        Redis (cache)         Delta Lake
                        Vector DBs (Chroma)

ORCHESTRATION           ML & AI               SERVING & INFRA
─────────────           ───────               ───────────────
Airflow                 MLflow                FastAPI
Prefect                 scikit-learn          Docker / ECS
Dagster                 LightGBM              Kubernetes
                        LLM APIs (OpenAI)     AWS Lambda
                        RAG (LangChain)       Terraform
                        vLLM (serving)        CloudWatch
```

---

## Rough Timeline (at 10 hrs/week)

| Phase | Topic | Duration |
|-------|-------|----------|
| 0 | CS Fundamentals (CPU, GPU, networking) | 2–3 weeks |
| 1 | Linux, shell, Git | 2 weeks |
| 2 | Python for data | 3–4 weeks |
| 3 | APIs | 3–4 weeks |
| 4 | Databases | 4–5 weeks |
| 5 | Tokenization & embeddings | 2–3 weeks |
| 6 | RAG | 3–4 weeks |
| 7 | Cloud | 4–5 weeks |
| 8 | Modern data stack | 4–5 weeks |
| 9 | Distributed computing | 4–5 weeks |
| 10 | MLOps | 3–4 weeks |
| 11 | Advanced (pick 2–3) | ongoing |

**Total to solid T-shape**: ~9–12 months at a steady pace.

---

## The Mental Models That Tie It All Together

1. **Data has gravity** — compute should move to data, not data to compute. That's why S3 + Athena exists.
2. **Scale the bottleneck, not everything** — find what's slow (I/O, CPU, memory, network) before adding complexity.
3. **Idempotency is a virtue** — every pipeline step should be safe to re-run. Design for failure.
4. **Schemas are contracts** — enforce them early (pydantic, dbt tests, Avro) or pay later.
5. **Tokens are money** — every LLM call has a cost proportional to tokens. Count them.
6. **The warehouse is the source of truth** — everything flows in, transformations happen inside, results flow out.
