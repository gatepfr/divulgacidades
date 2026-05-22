const fs = require('fs');
const path = require('path');

// Mock window object for node execution
global.window = {};

// Load data.js
const dataJsContent = fs.readFileSync(path.join(__dirname, '..', 'data.js'), 'utf8');
eval(dataJsContent);

console.log("--- Testing JS Logic ---");

// Test 1: Slugs
const testCities = [
  { name: "São Paulo", expected: "sao_paulo" },
  { name: "Brasília", expected: "brasilia" },
  { name: "Adolfo", expected: "adolfo" },
  { name: "Rio de Janeiro", expected: "rio_de_janeiro" },
  { name: "Fernando de Noronha", expected: "fernando_de_noronha" }
];

console.log("1. Testing getCitySlug:");
for (const tc of testCities) {
  const result = window.getCitySlug(tc.name);
  console.log(`- "${tc.name}" => "${result}" (Expected: "${tc.expected}")`);
  if (result !== tc.expected) {
    console.error("FAIL: Slug mismatch!");
    process.exit(1);
  }
}

// Test 2: Checking mapped cities list is populated
const totalStates = Object.keys(window.ESTADOS_CIDADES).length;
console.log(`2. Total states mapped: ${totalStates}`);
if (totalStates !== 27) {
  console.error(`FAIL: Expected 27 states, got ${totalStates}`);
  process.exit(1);
}

// Test 3: getElectionData (procedural fallback generator)
console.log("3. Testing getElectionData for Fernando de Noronha:");
const fdnData = window.getElectionData("PE", "Fernando de Noronha");
console.log(`- Population: ${fdnData.populacao}`);
console.log(`- Prefeito: ${fdnData.prefeito ? fdnData.prefeito.nome : 'None'} (${fdnData.prefeito ? fdnData.prefeito.partido : ''})`);
console.log(`- Vereadores count: ${fdnData.vereadores.length}`);
console.log(`- Senadores count: ${fdnData.senadores.length}`);
if (!fdnData.prefeito || fdnData.vereadores.length === 0 || fdnData.senadores.length === 0) {
  console.error("FAIL: Procedural fallback data is incomplete!");
  process.exit(1);
}

// Test 4: Verification of physical JSON files matching the map
console.log("4. Verifying mapped cities have valid files or slugs:");
let missingCount = 0;
let fdnCorrectlyMissing = false;

for (const [uf, cities] of Object.entries(window.ESTADOS_CIDADES)) {
  for (const city of cities) {
    const slug = window.getCitySlug(city);
    const filePath = path.join(__dirname, '..', 'data', uf, `${slug}.json`);
    if (!fs.existsSync(filePath)) {
      if (uf === "PE" && slug === "fernando_de_noronha") {
        fdnCorrectlyMissing = true;
      } else {
        console.warn(`Missing file: data/${uf}/${slug}.json (${city})`);
        missingCount++;
      }
    }
  }
}

console.log(`- Missing files (excluding Fernando de Noronha): ${missingCount}`);
if (missingCount > 0) {
  console.error("FAIL: Real data files missing for mapped cities!");
  process.exit(1);
}

if (!fdnCorrectlyMissing) {
  console.error("FAIL: Expected Fernando de Noronha to be missing real data file!");
  process.exit(1);
}

console.log("All JS logic and file mapping tests PASSED successfully!");
