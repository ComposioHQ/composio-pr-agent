# Composio PR Review

A Pull Request review automation system using Composio.

## Prerequisites

- Docker
- Make

## Environment Setup

Create a GITHUB_PULL_REQUEST_EVENT trigger in your Composio account. Follow the instructions [here](https://docs.composio.dev/introduction/intro/quickstart_3).

Create a `.env` file in the root directory with your required environment variables:
- COMPOSIO_API_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- GITHUB_ACCESS_TOKEN
- OPENAI_API_KEY

## Usage

### Quick Start

1. Pull the latest Docker image:
   ```bash
   docker pull composio/pr-review:latest
   ```

2. Start the container:
   ```bash
   make run
   ```


### Build and Run

1. Build the Docker image:
   ```bash
   make clean && make build
   ```

2. Start the container:
   ```bash
   make run
   ```