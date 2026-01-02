#  Applied AI Engineer Challenge: Multi-Agent Content Generation System - Resubmission
A modular, agentic content generation system that autonomously converts structured product data into machine-readable JSON pages using multi-agent orchestration, reusable content logic blocks, and template-based automation.

## Problem Addressed
The core requirement of the task has not been met because it failed to demonstrate a true multi-agent system. The feedback specifically stated:
"Simply hard-coding multiple functions or sequential logic and labeling them as 'agents' does not satisfy this requirement. A valid solution requires: Clear separation of agent responsibilities, Dynamic agent interaction and coordination, An architecture that supports agent autonomy rather than static control flow"

A valid solution requires:
- Clear separation of agent responsibilities
- Dynamic agent interaction and coordination
- An architecture that supports agent autonomy rather than static control flow
  
## Solution Overview
This implementation now represents a genuine multi-agent system that:
- Eliminates static control flow
- Implements dynamic coordination
- Ensures agent autonomy
- Demonstrates emergent behavior
- Addresses all feedback requirements

## Solution Implemented
| Aspect                 | Previous Implementation                      | Current Implementation                         | Why the core requirement of the task has not been met                                                              | Changes Made                                                |
| ---------------------- | -------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Architecture Type**  | Static function calls labeled as “agents”    | True multi-agent system with message passing   | “Hard-coding multiple functions or sequential logic and labeling them as agents” | Introduced event-loop orchestrator with message queue       |
| **Agent Coordination** | Manual orchestration, hard-coded sequence    | Dynamic coordination via `PlannerAgent`        | “Manually wired logic without an underlying agentic architecture”                | `PlannerAgent` inspects blackboard and decides next actions |
| **Agent Interaction**  | Direct function calls between components     | Message passing via `AgentRegistry`            | No message-based communication                                                   | All communication routed through message queue              |
| **Control Flow**       | Fixed pipeline order                         | Adaptive order based on system state           | “Static control flow”                                                            | Dynamic re-planning after each artifact                     |
| **Agent Autonomy**     | Functions called in predetermined order      | Autonomous agents respond to specific messages | “Agents not independent, modular”                                                | Each agent decides how to handle incoming messages          |      |
| **System Behavior**    | Predictable execution                        | Emergent behavior from agent interactions      | “Not demonstrating intended outcomes”                                            | System adapts based on current state                       
| **Decision Making**    | Coded in orchestration logic                 | Runtime decisions by `PlannerAgent`            | “No dynamic coordination”                                                        | Planner re-plans after each step                            |

---

### Key Architecture Principles

### 1. Clear Agent Boundaries
Each agent has:
- **Single responsibility**: One specific task (parse, generate block, render page, etc.)
- **Defined input/output**: Messages with typed payloads
- **No hidden global state**: All state via blackboard
- **Message-driven**: Only acts when receiving messages it can handle

### 2. Dynamic Agent Interaction (Not Static Control Flow)
- **Event-loop orchestrator** processes message queue continuously
- **PlannerAgent re-plans** after every artifact creation
- **No hardcoded sequence**: Order emerges from message dependencies
- **Adaptive behavior**: System adjusts based on what's missing

### 3. Agent Autonomy
- **Independent decision making**: Each agent decides how to handle messages
- **No direct agent-to-agent calls**: All communication via message queue
- **Self-contained logic**: Agents don't know about other agents' internals
- **Stateless processing**: Agents read from blackboard, write results back

---

## Multi Agent Architecture 
The system follows an agentic architecture where autonomous agents operate over a shared blackboard, and execution order emerges dynamically based on system state rather than predefined control flow.

![System Architecture](docs/System%20Design/multi-agent-architecture-diagram.png)

## System Components

### Core Runtime
- **Message**: Dataclass for agent communication (type, payload, source, trace_id)
- **Blackboard**: Shared state with artifacts, goals, and event log
- **Agent**: Abstract base class with can_handle() and handle() methods
- **AgentRegistry**: Registers agents and routes messages to capable handlers
- **EventLoopOrchestrator**: Runs message queue until goals satisfied

### Autonomous Agents

#### - PlannerAgent (Coordinator)
  - **Responsibility**: Inspect blackboard, decide what's missing, emit task messages
  - **Dynamic Behavior**: Re-plans after every artifact creation

#### - ParserAgent (Data Ingestion)
  - **Responsibility**: Convert raw JSON to structured ProductData model
  - **Trigger**: "parse_product" message
  - **Output**: "product_data" artifact on blackboard

#### - Block Agents (Content Generation)
  - **BenefitsAgent, UsageAgent, IngredientsAgent, SafetyAgent, ComparisonAgent**
  - **Responsibility**: Generate specific content blocks from ProductData
  - **Trigger**: "generate_block:{type}" messages
  - **Output**: "block:{type}" artifacts

#### - QuestionAgent (Q&A Generation)
  - **Responsibility**: Generate 15+ categorized questions
  - **Trigger**: "generate_questions" message
  - **Output**: "questions" artifact with categories (Informational, Safety, Usage, Purchase, Comparison)

#### - PageRenderAgent (Template Rendering)
  - **Responsibility**: Render final pages using templates
  - **Trigger**: "render_page:{type}" messages
  - **Output**: JSON content for faq.json, product_page.json, comparison_page.json

#### - GraphAgent (System Visualization)
  - **Responsibility**: Build execution graph from message flow
  - **Trigger**: "build_graph" message
  - **Output**: graph.json showing agent interactions

### - Templates and Content Blocks
  - **TemplateEngine**: Custom template rendering system
  - **Page Templates**: FAQ, Product, Comparison with structured fields
  - **Content Blocks**: Reusable logic for transforming data into copy


### Message Flow Example

1. **User** sends "start" message with product data
2. **PlannerAgent** receives "start", stores data, emits "plan"
3. **PlannerAgent** receives "plan", sees missing product_data, emits "parse_product"
4. **ParserAgent** receives "parse_product", creates product_data artifact
5. **PlannerAgent** sees new artifact, emits "generate_block:benefits"
6. **BenefitsAgent** generates benefits block artifact
7. **PlannerAgent** continues until all goals satisfied

---

# System Design
The system is designed as a layered, agentic architecture with explicit data flow.

### 1. High-Level System Architecture
The system follows a modular, multi-agent architecture designed to generate structured content from product datasets in an automated, scalable, and extensible manner. The design separates responsibilities across specialized AI agents, coordinated through a central orchestrator and shared memory layer. At a high level, the system transforms structured user input (JSON) into multiple structured output artifacts using reusable content blocks and templates.

![System Architecture](docs/System%20Design/System%20Architecture.jpeg)


### 2. Orchestration Graph (DAG)
The system execution is governed by a Directed Acyclic Graph (DAG) that defines task dependencies, execution order, and parallelism across AI agents. The orchestrator uses this DAG to dynamically schedule agents based on data readiness and output availability.

![Orchestration Graph](docs/System%20Design/Orchestration%20Graph.jpeg)

- Agents are triggered only when required input data is ready, ensuring efficient and deterministic execution.
- Content Logic and Question Generator agents run in parallel after data parsing to maximize throughput.
- The Orchestrator dynamically decides which downstream tasks to execute (FAQ, product, comparison) based on data readiness and target output.
- Final nodes validate and generate schema-compliant JSON outputs for FAQs, product pages, comparisons, and graphs.

### 3. End-to-End Flow Chart
This flow chart explains the system behavior at a **conceptual level**. It transforms raw input data into structured, ready-to-use JSON outputs through coordinated orchestration and autonomous agents.

![Flowchart](docs/System%20Design/Flowchart.jpeg)


- The system ingests raw product data along with user requirements as structured inputs.
- A central orchestrator performs workflow orchestration and dynamic planning based on input data and target outputs.
- Autonomous AI agents process the data and generate modular, reusable content blocks.
- Generated content blocks are assembled using templates to compose complete pages and artifacts.
- The final result is delivered as validated, structured JSON files ready for downstream consumption.

### 4. Sequence Diagram
This sequence diagram illustrates how multiple AI agents interact over time to generate structured content. It highlights synchronous and asynchronous coordination managed by the orchestrator from input ingestion to final JSON output.

![Sequence Diagram](docs/System%20Design/Sequence%20Diagram.jpeg)

- The user submits a product dataset in JSON format to start the workflow.
- The orchestrator agent receives the input and dynamically plans task execution.
- The data parsing agent extracts and structures relevant product information.
- The question generator and content logic agents run in parallel to create categorized FAQs and content blocks.
- The template engine agent assembles generated content using predefined validation templates.
- Agents share progress and intermediate results through asynchronous state updates.
- The JSON output agent validates the final structure and saves the generated JSON files.
- The workflow completes once all required outputs are successfully generated and stored.

---

## Results
This produces:
- `outputs/faq.json` - Frequently Asked Questions page with 15+ categorized Q&As
- `outputs/product_page.json` - Product description page
- `outputs/comparison_page.json` - Comparison with fictional competitor
- `outputs/graph.json` - Dynamic execution graph

---

## Architecture Validation

This implementation addresses the feedback about requiring a "true multi-agent system" by:

1. **Eliminating static control flow**: No hardcoded sequence of operations
2. **Implementing dynamic coordination**: PlannerAgent adapts based on system state
3. **Ensuring agent autonomy**: Each agent operates independently
4. **Using message passing**: All communication via message queue
5. **Shared state management**: Blackboard for coordination without direct coupling

The system demonstrates genuine multi-agent architecture where emergent behavior arises from autonomous agent interactions, not predetermined orchestration.




