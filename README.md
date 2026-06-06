# hpc-flow

> Launch scientific tools and scripts on remote HPC/cloud infrastructure with a single command. No Docker. No VM. No hassle.

![Status](https://img.shields.io/badge/status-early%20development-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Cloud](https://img.shields.io/badge/cloud-Akash%20Network-purple)
![CLI](https://img.shields.io/badge/interface-CLI-green)

---

## What is hpc-flow?

**hpc-flow** is an open source CLI tool that lets researchers run scientific tools and scripts on remote compute infrastructure (starting with [Akash Network](https://akash.network)) using a single command.

It handles everything automatically:

- uploading input files
- provisioning remote resources
- running the computation
- downloading results locally
- cleaning up remote deployments

The researcher only needs to prepare their files and type one command.

---

## Why hpc-flow?

Running scientific workloads on remote infrastructure typically requires:

- setting up Docker containers or VMs
- configuring remote environments manually
- transferring files by hand
- monitoring job execution
- cleaning up resources when done

Each team reinvents the wheel. hpc-flow solves this by providing a unified, tool-centric CLI designed specifically for scientific workflows.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/hpc-flow.git
cd hpc-flow

# Install (method to be defined based on implementation language)
# Example for Python-based CLI:
pip install -e .

# Run a bioinformatics tool on Akash
hpc run vsearch \
  --input reads.fasta \
  --id 0.97 \
  --output centroids.fasta \
  --cloud akash

# Run a custom script
hpc run-script analyse.py \
  --runtime python:3.11 \
  --input data.tsv \
  --output result.csv \
  --cloud akash
```

---

## Examples

### Bioinformatics — sequence analysis with vsearch

```bash
hpc run vsearch \
  --input reads.fasta \
  --id 0.97 \
  --threads 8 \
  --output centroids.fasta \
  --cloud akash
```

### Geospatial — slope calculation from a DEM raster

```bash
hpc run geoprocess \
  --input dem.tif \
  --operation slope \
  --output slope.tif \
  --cloud akash
```

### Custom script — Python analysis with dependencies

```bash
hpc run-script analyse.py \
  --runtime python:3.11 \
  --input data.tsv \
  --output result.csv \
  --cloud akash
```

---

## How It Works

```
Researcher's machine                Remote infrastructure (Akash)
─────────────────────               ──────────────────────────────

  hpc run vsearch ...
        │
        ▼
  ┌─────────────┐
  │   CLI       │  ── prepares JobSpec (tool, args, files, resources)
  └─────────────┘
        │
        ▼
  ┌─────────────┐
  │  JobRunner  │  ── submits job to backend
  │  (Akash)    │──────────────────────────────► [ Deploy container ]
  └─────────────┘                                [ Upload input files ]
        │                                        [ Run computation    ]
        │                                        [ Expose results     ]
        ▼
  ┌─────────────┐
  │  Results    │ ◄────────────────────────────── [ Download outputs  ]
  │  (local)    │                                 [ Cleanup deployment]
  └─────────────┘
```

**Step by step:**

1. The CLI parses the command and validates parameters
2. It builds a `JobSpec` (tool or script, arguments, input files, resource requirements)
3. The `JobRunner` provisions a deployment on Akash Network
4. Input files are uploaded to the remote environment
5. The computation runs remotely
6. Output files are automatically downloaded to the local machine
7. The remote deployment is destroyed

---

## Features

| Feature | Status |
|---|---|
| Unified CLI (`hpc run`, `hpc run-script`) | 🔄 In progress |
| Tool registry (vsearch, geoprocess, ...) | 🔄 In progress |
| Akash Network backend | 🔄 In progress |
| Automatic file transfer (input/output) | 🔄 In progress |
| Python script execution | 🔄 In progress |
| Bash script execution | 📋 Planned |
| R script execution | 📋 Planned |
| Local job history and logs | 📋 Planned |
| Web dashboard | 📋 Planned |
| Multi-cloud support | 📋 Planned |

---

## Architecture

### 1. CLI layer

The `hpc` binary installed on the researcher's machine. It parses commands, loads tool definitions, prepares the `JobSpec`, and communicates with the backend.

### 2. Tool registry

A collection of YAML/JSON definitions describing supported tools:

```yaml
name: vsearch
version: "2.28.1"
image: quay.io/biocontainers/vsearch:2.28.1--h6a68c12_0
parameters:
  - name: input
    flag: --fastx_uniques
  - name: id
    flag: --id
  - name: output
    flag: --centroids
resources:
  cpu: 4
  memory: 8Gi
```

### 3. JobRunner interface

A generic abstraction allowing multiple cloud/HPC backends:

```
submit(JobSpec)       → jobId
status(jobId)         → pending | running | succeeded | failed
fetch_results(jobId)  → local files
cleanup(jobId)
```

### 4. AkashJobRunner (POC backend)

The first implementation targets Akash Network:

- creates a deployment using the tool's container image
- handles input file transfer
- monitors job status via logs
- downloads output files when complete
- destroys the deployment automatically

### 5. Script execution

Two supported modes:

- **Inline script mode** — the CLI uploads the script (and optionally a `requirements.txt`), and runs it inside a base runtime image (e.g. `python:3.11`)
- **Custom container mode** *(planned)* — the researcher provides a pre-built image containing their full environment

---

## Supported Tools (Registry)

| Tool | Domain | Status |
|---|---|---|
| vsearch | Bioinformatics | 🔄 In progress |
| geoprocess (GDAL/rasterio) | Geospatial | 🔄 In progress |
| blast | Bioinformatics | 📋 Planned |
| samtools | Bioinformatics | 📋 Planned |
| Custom Python script | Any | 🔄 In progress |
| Custom Bash script | Any | 📋 Planned |
| Custom R script | Any | 📋 Planned |

---

## Roadmap

### Phase 1 — MVP / POC (open source CLI)

- [ ] Minimal CLI: `hpc run`, `hpc run-script`
- [ ] Generic `JobRunner` interface
- [ ] `AkashJobRunner` implementation
- [ ] Tool registry with vsearch and one geospatial tool
- [ ] Input/output file management
- [ ] Demonstrable POC: one bioinfo pipeline + one geospatial pipeline

### Phase 2 — Hardening & extension

- [ ] Additional tools in the registry
- [ ] Additional script runtimes (R, Bash, Julia)
- [ ] Local job history (metadata, duration, errors)
- [ ] Improved logging and monitoring

### Phase 3 — Managed layer (SaaS / dashboard)

- [ ] Web application connected to hpc-flow
- [ ] Job visualization (current and past)
- [ ] Resource usage and logs
- [ ] User and project management
- [ ] Multi-lab support with quotas
- [ ] Option to launch jobs from the UI

---

## Target Users

- Researchers and engineers in **bioinformatics**
- Researchers and engineers in **geomatics / spatial data**
- Any discipline running **CPU or GPU intensive scripts**
- Research institutes, universities, biotechs, and space agencies that need:
  - on-demand or large-scale compute
  - minimal infrastructure administration

---

## Positioning

| | hpc-flow | Classic cloud (AWS, GCP) | Traditional HPC (Slurm, PBS) |
|---|---|---|---|
| No Docker/VM knowledge needed | ✅ | ❌ | ❌ |
| Tool-centric interface | ✅ | ❌ | ❌ |
| Decentralized / multi-cloud | ✅ | ❌ | ❌ |
| Automatic file transfer | ✅ | Manual | Manual |
| Automatic cleanup | ✅ | Manual | Manual |
| Open source & extensible | ✅ | ❌ | Partial |

---

## Contributing

Contributions are welcome. You can:

- open an issue to report a bug or suggest a feature
- propose a new tool definition for the registry
- implement a new cloud/HPC backend adapter
- improve documentation

Please open an issue before submitting a large pull request so we can discuss the approach first.

---

## Prerequisites

- Linux, macOS, or Windows
- Network access
- An Akash Network wallet and access (for remote execution)
- Python 3.11+ (if using the Python-based CLI)

---

## Project Status

> **Early development.** The project is currently in the design and initial implementation phase.  
> The API, CLI interface, and internal architecture may change significantly before the first stable release.

---

## License

MIT License — see [LICENSE](./LICENSE) for details.

---

## Contact & Links

- Repository: [github.com/your-org/hpc-flow](https://github.com/your-org/hpc-flow)
- Issues: [github.com/your-org/hpc-flow/issues](https://github.com/your-org/hpc-flow/issues)
- Akash Network: [akash.network](https://akash.network)

---

## FAQ

**Can researchers run their own scripts?**  
Yes. hpc-flow supports both packaged tools (from the registry) and custom scripts provided by the researcher.

**Do users need to know Docker?**  
No. The goal is to hide all container and infrastructure complexity from the end user.

**Is hpc-flow locked to Akash?**  
No. The architecture is built around a generic `JobRunner` interface. New backends (AWS, GCP, Slurm, etc.) can be added as adapters.

**What file formats are supported?**  
Any file format. hpc-flow transfers files as-is. The tool or script running remotely determines what formats it accepts.

**Can I add my own tool to the registry?**  
Yes. Tools are described in simple YAML files. Contributions to the registry are welcome via pull request.
