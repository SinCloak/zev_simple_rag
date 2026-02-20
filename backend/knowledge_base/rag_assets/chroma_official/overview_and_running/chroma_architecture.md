> ## Documentation Index
> Fetch the complete documentation index at: https://docs.trychroma.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Architecture

> Chroma is designed with a modular architecture that prioritizes performance and ease of use. It scales seamlessly from local development to large-scale production, while exposing a consistent API across all deployment modes.

Chroma is designed with a modular architecture that prioritizes performance and ease of use. It scales seamlessly from local development to large-scale production, while exposing a consistent API across all deployment modes.

Chroma delegates, as much as possible, problems of data durability to trusted sub-systems such as SQLite and Cloud Object Storage, focusing the system design on core problems of data management and information retrieval.

## Deployment Modes

Chroma runs wherever you need it to, supporting you in everything from local experimentation, to large scale production workloads.

* **Local**: as an embedded library - great for prototyping and experimentation.
* **Single Node**: as a single-node server - great for small to medium scale workloads of \< 10M records in a handful of collections.
* **Distributed**: as a scalable distributed system - great for large scale production workloads, supporting millions of collections.

You can use [Chroma Cloud](https://www.trychroma.com/signup?utm_source=docs-architecture), which is a managed offering of distributed Chroma.

## Core Components

Regardless of deployment mode, Chroma is composed of five core components. Each plays a distinct role in the system and operates over the shared [Chroma data model](#chroma-data-model).

<img className="block dark:hidden" src="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=8230cb5c91cdfb4f17336accd059d2e7" alt="Chroma System architecture" data-og-width="1469" width="1469" data-og-height="684" height="684" data-path="images/system-diagram-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=280&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=273870ebb3f01768631ce728ba22c12f 280w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=560&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=f54cffaad0808d3355b29ecf21f8793d 560w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=840&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=bfd8f1cfa19aeaf6ff48ebbe3482e76f 840w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=1100&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=bb5d40e1aeb407cbbf5c5d8e4e17b3d3 1100w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=1650&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=e7864e779fb26b3fb32b4ea22a6f7d9b 1650w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-light.png?w=2500&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=7919fdac8e77d024b103c5f0d867bfeb 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=3b27d74ee4a3f1c58a6d0c38e41ab40b" alt="Chroma System architecture" data-og-width="1469" width="1469" data-og-height="684" height="684" data-path="images/system-diagram-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=280&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=3dfbb907de1945bc3b1ea0edff46059b 280w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=560&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=48686acf9cbaaffa7903bcbf9c4644d6 560w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=840&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=3af77c07313d60052c7882bc77c1779b 840w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=1100&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=6c5a57cd67595d1e681b61f9a51c1b5e 1100w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=1650&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=577bad16cd1c3cc32721019a3c59ff9c 1650w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/system-diagram-dark.png?w=2500&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=981368d8b44470e5ba3fb37ec92c9c2f 2500w" />

### The Gateway

The entrypoint for all client traffic.

* Exposes a consistent API across all modes.
* Handles authentication, rate-limiting, quota management, and request validation.
* Routes requests to downstream services.

### The Log

Chroma's write-ahead log.

* All writes are recorded here before acknowledgment to clients.
* Ensures atomicity across multi-record writes.
* Provides durability and replay in distributed deployments.

### The Query Executor

Responsible for **all read operations.**

* Vector similarity, full-text and metadata search.
* Maintains a combination of in-memory and on-disk indexes, and coordinates with the Log to serve consistent results.

### The Compactor

A service that periodically builds and maintains indexes.

* Reads from the Log and builds updated vector / full-text / metadata indexes.
* Writes materialized index data to shared storage.
* Updates the System Database with metadata about new index versions.

### The System Database

Chroma's internal catalog.

* Tracks tenants, collections, and their metadata.
* In distributed mode, also manages cluster state (e.g., query/compactor node membership).
* Backed by a SQL database.

## Storage & Runtime

These components operate differently depending on the deployment mode, particularly in how they use storage and the runtime they operate in.

* In Local and Single Node mode, all components share a process and use the local filesystem for durability.
* In **Distributed** mode, components are deployed as independent services.
  * The log and built indexes are stored in cloud object storage.
  * The system catalog is backed by a SQL database.
  * All services use local SSDs as caches to reduce object storage latency and cost.

## Request Sequences

### Read Path

<img className="block dark:hidden" src="https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=cac0a618b57dc23bc15ec2387d4bcac2" alt="Chroma System Read Path" data-og-width="984" width="984" data-og-height="678" height="678" data-path="images/read-path-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=280&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=4e563579b220130b9a5ccd1b63724a29 280w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=560&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=13fc7e416f3b4191f72475b4cb4fbc60 560w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=840&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=024cfd507c3a1b6a685de71120a47cc2 840w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=1100&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=3b0ad5a0b004a4c06358533b4386b281 1100w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=1650&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=bea4dcccf9223bd94a5b4623b886a28b 1650w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-light.png?w=2500&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=dd65daccb1a97cd028c226e0063a4e42 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=99899a7f7817339bd4e7a1e410b845cf" alt="Chroma System Read Path" data-og-width="984" width="984" data-og-height="678" height="678" data-path="images/read-path-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=280&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=89f8f449fd0b85001b79378ed0b9b578 280w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=560&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=bf23bc98df725f55581627d9fe8f4571 560w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=840&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=00d979c908ec519b8de6998c1a29ac7e 840w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=1100&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=13e7ee7f8dc955d79f0f4fc8ac5669c3 1100w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=1650&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=ec32b63aa328416079c0fff02685b5e9 1650w, https://mintcdn.com/chroma-8943dec5/OHTRZei6ss2glLVb/images/read-path-dark.png?w=2500&fit=max&auto=format&n=OHTRZei6ss2glLVb&q=85&s=fbd080da6e7d07fe40712cc6d84567ba 2500w" />

<Steps>
  <Step>
    Request arrives at the gateway, where it is authenticated, checked against quota limits, rate limited and transformed into a logical plan.
  </Step>

  <Step>
    This logical plan is routed to the relevant query executor. In distributed Chroma, a rendezvous hash on the collection id is used to route the query to the correct nodes and provide cache coherence.
  </Step>

  <Step>
    The query executor transforms the logical plan into a physical plan for execution, reads from its storage layer, and performs the query. The query executor pulls data from the log to ensure a consistent read.
  </Step>

  <Step>
    The request is returned to the gateway and subsequently to the client.
  </Step>
</Steps>

### Write Path

<img className="block dark:hidden" src="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=a791ab900059c0d1592050a45ea98578" alt="Chroma System Write Path" data-og-width="1260" width="1260" data-og-height="678" height="678" data-path="images/write-path-light.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=280&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=37564e3fb45c3eb011fd2a31c874f7f3 280w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=560&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=fac7a67823d0eca261255883a904dd2f 560w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=840&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=f0d5c3755e2f196aa4f377775a61c33a 840w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=1100&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=46d3d0d5ed34acc15b7d22bc763c3851 1100w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=1650&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=370de02de079491d0c47ccbe541ec2ae 1650w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-light.png?w=2500&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=609f418b526927d5448b11c71a6ea98d 2500w" />

<img className="hidden dark:block" src="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=f9dc0b3dd158e83e9f7d6d2f1cbc2e18" alt="Chroma System Write Path" data-og-width="1260" width="1260" data-og-height="678" height="678" data-path="images/write-path-dark.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=280&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=080adfb5085d87018ccd34ef0e7d5741 280w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=560&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=758bdab46797eb1dceb5c345486acc3f 560w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=840&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=35c97e08b27e87946217bc946dec7db3 840w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=1100&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=4844b8e433c16d6b947d860bebccb311 1100w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=1650&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=c6b1b4a42a45d270d3ceb51b2c840b30 1650w, https://mintcdn.com/chroma-8943dec5/2QFLJScSYa9JT1WU/images/write-path-dark.png?w=2500&fit=max&auto=format&n=2QFLJScSYa9JT1WU&q=85&s=c07ebf978b85e17fc44e6bbbce4a9e94 2500w" />

<Steps>
  <Step>
    Request arrives at the gateway, where it is authenticated, checked against quota limits, rate limited and then transformed into a log of operations.
  </Step>

  <Step>
    The log of operations is forwarded to the write-ahead-log for persistence.
  </Step>

  <Step>
    After being persisted by the write-ahead-log, the gateway acknowledges the write.
  </Step>

  <Step>
    The compactor periodically pulls from the write-ahead-log and builds new index versions from the accumulated writes. These indexes are optimized for read performance and include vector, full-text, and metadata indexes.
  </Step>

  <Step>
    Once new index versions are built, they are written to storage and registered in the system database.
  </Step>
</Steps>

## Tradeoffs

Distributed Chroma is built on object storage in order to ensure the durability of your data and to deliver low costs. Object storage has extremely high throughput, easily capable of saturating a single nodes network bandwidth, but this comes at the cost of a relatively high latency floor of \~10-20ms.

In order to reduce the overhead of this latency floor, Distributed Chroma aggressively leverage SSD caching. When you first query a collection, a subset of the data needed to answer the query will be read selectively from object storage, incurring a cold-start latency penalty. In the background, the SSD cache will be loaded with the data for the collection. After the collection is fully warm, queries will be served entirely from SSD.

## Chroma Data Model

Chroma's data model is designed to balance simplicity, flexibility, and scalability. It introduces a few core abstractions - **Tenants**, **Databases**, and **Collections** - that allow you to organize, retrieve, and manage data efficiently across environments and use cases.

### Collections

A **collection** is the fundamental unit of storage and querying in Chroma. Each collection contains a set of items, where each item consists of:

* An ID uniquely identifying the item
* An **embedding vector**
* Optional **metadata** (key-value pairs)
* A document that belongs to the provided embedding

Collections are independently indexed and are optimized for fast retrieval using **vector similarity**, **full-text search**, and **metadata filtering**. In distributed deployments, collections can be sharded or migrated across nodes as needed; the system transparently manages paging them in and out of memory based on access patterns.

### Databases

Collections are grouped into **databases**, which serve as a logical namespace. This is useful for organizing collections by purpose - for example, separating environments like "staging" and "production", or grouping applications under a common schema.

Each database contains multiple collections, and each collection name must be unique within a database.

### Tenants

At the top level of the model is the **tenant**, which represents a single user, team, or account. Tenants provide complete isolation. No data or metadata, is shared across tenants. All access control, quota enforcement, and billing are scoped to the tenant level.
