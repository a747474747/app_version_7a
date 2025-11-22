#!/usr/bin/env node

/**
 * Type Generation Script for Four-Engine Frontend
 *
 * This script fetches the OpenAPI specification from the FastAPI backend
 * and generates TypeScript types using openapi-typescript-codegen.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const OPENAPI_URL = `${BACKEND_URL}/openapi.json`;
const OUTPUT_DIR = path.join(__dirname, '..', 'src', 'types');
const TEMP_SPEC_FILE = path.join(__dirname, 'temp-openapi.json');

async function fetchOpenAPISpec() {
  console.log('🔄 Fetching OpenAPI specification from:', OPENAPI_URL);

  try {
    const response = await fetch(OPENAPI_URL);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const spec = await response.json();

    // Write to temp file for the codegen tool
    fs.writeFileSync(TEMP_SPEC_FILE, JSON.stringify(spec, null, 2));

    console.log('✅ OpenAPI specification fetched successfully');
    return spec;

  } catch (error) {
    console.error('❌ Failed to fetch OpenAPI specification:', error.message);

    // Check if backend is running
    if (error.code === 'ECONNREFUSED') {
      console.log('\n💡 Make sure the backend is running:');
      console.log('   cd backend && python -m uvicorn src.main:app --reload');
    }

    throw error;
  }
}

function generateTypes() {
  console.log('🔄 Generating TypeScript types...');

  try {
    // Ensure output directory exists
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    // Run openapi-typescript-codegen
    const command = `npx openapi-typescript-codegen --input ${TEMP_SPEC_FILE} --output ${OUTPUT_DIR} --client axios --useOptions`;

    execSync(command, {
      stdio: 'inherit',
      cwd: process.cwd()
    });

    console.log('✅ TypeScript types generated successfully');
    console.log(`📁 Types available in: ${OUTPUT_DIR}`);

  } catch (error) {
    console.error('❌ Failed to generate types:', error.message);
    throw error;
  }
}

function cleanup() {
  // Clean up temp file
  if (fs.existsSync(TEMP_SPEC_FILE)) {
    fs.unlinkSync(TEMP_SPEC_FILE);
    console.log('🧹 Cleaned up temporary files');
  }
}

async function main() {
  console.log('🚀 Starting TypeScript type generation for Four-Engine Frontend\n');

  try {
    await fetchOpenAPISpec();
    generateTypes();
    cleanup();

    console.log('\n🎉 Type generation completed successfully!');
    console.log('\n📝 Next steps:');
    console.log('   - Import types from src/types/index.ts');
    console.log('   - Use generated API client for backend communication');

  } catch (error) {
    cleanup();
    console.error('\n💥 Type generation failed');
    process.exit(1);
  }
}

// Handle script execution
if (require.main === module) {
  main();
}

module.exports = { fetchOpenAPISpec, generateTypes, cleanup };
