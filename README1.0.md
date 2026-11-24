# env-doctor 🩺

A fast, lightweight, zero-dependency Python CLI tool that validates your `.env` file against `.env.example` to catch missing keys, empty values, and undocumented environment variables before they break production.

## Why env-doctor?

Misconfigured environment variables are one of the most common causes of deployment failures. `env-doctor` integrates seamlessly into local development workflows and CI/CD pipelines using only the Python standard library.

## Features

- **Zero Dependencies:** Runs out of the box with Python 3.7+.
- **Missing Key Detection:** Alerts you when required keys from `.env.example` are absent in `.env`.
- **Empty Value Warnings:** Flags keys that exist but have no assigned value.
- **Strict Mode:** Optionally fail builds if undocumented keys exist in `.env`.

## Quick Start

1. Clone the repository:
   ```bash
   git clone [https://github.com/MOTAWF/env-doctor.git](https://github.com/MOTAWF/env-doctor.git)
   cd env-doctor
