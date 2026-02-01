# Method.AI Frontend

Minimal Next.js frontend for Method.AI.

## Overview

This is a lightweight frontend for testing the Method.AI API. It provides a simple form interface for generating draft procedures.

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Configuration

The frontend expects the backend API to be running at `http://localhost:8000`. This can be configured by modifying the API endpoint in the code.

## Features

- Target molecule input (SMILES format)
- Experience level selection
- Equipment checkboxes
- Submit to API and display results

## Notes

This is a minimal implementation for development and testing. A production frontend would include:

- Proper error handling and loading states
- Form validation
- Better styling and UX
- Authentication
- Result history
