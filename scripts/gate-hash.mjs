#!/usr/bin/env node
/**
 * Считает хэш кода доступа (FNV-1a, hex) — его подставляем в src/data/site.ts → gate.hash.
 * Использование: node scripts/gate-hash.mjs <код>
 */
const code = process.argv.slice(2).join(' ');

if (!code) {
  console.error('Использование: node scripts/gate-hash.mjs <код>');
  process.exit(1);
}

let h = 0x811c9dc5;
for (const b of new TextEncoder().encode(code)) {
  h ^= b;
  h = Math.imul(h, 0x01000193) >>> 0;
}

console.log(h.toString(16).padStart(8, '0'));
