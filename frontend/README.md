# Four-Engine Frontend

Frontend for the Four-Engine System Architecture built with Next.js and TypeScript.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Generate TypeScript types from backend API:
   ```bash
   npm run generate-types
   ```

   This will fetch the OpenAPI specification from the backend and generate TypeScript types and API client code.

## Type Generation

The `generate-types` script:

- Fetches the OpenAPI JSON from `http://localhost:8000/openapi.json` (configurable via `BACKEND_URL` env var)
- Generates TypeScript types using `openapi-typescript-codegen`
- Outputs generated code to `src/types/`
- Creates an axios-based API client for backend communication

### Prerequisites

- Backend must be running and accessible
- Node.js and npm installed

### Environment Variables

- `BACKEND_URL`: Backend URL (default: `http://localhost:8000`)

## Development

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Generated Types

After running `npm run generate-types`, you'll have:

- `src/types/index.ts`: Main types export
- `src/types/models.ts`: API model definitions
- `src/types/services.ts`: API client services

Import and use these types throughout your React components for type-safe API communication.
