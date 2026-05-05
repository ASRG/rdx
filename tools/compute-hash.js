const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

function canonicalJson(obj) {
  if (obj === null || typeof obj !== 'object') return JSON.stringify(obj);
  if (Array.isArray(obj)) return '[' + obj.map(canonicalJson).join(',') + ']';
  const keys = Object.keys(obj).sort();
  return '{' + keys.map(k => JSON.stringify(k) + ':' + canonicalJson(obj[k])).join(',') + '}';
}

function computeIntegrity(profile) {
  const copy = JSON.parse(JSON.stringify(profile));
  copy.integrity = {};
  const canonical = canonicalJson(copy);
  return crypto.createHash('sha256').update(canonical, 'utf8').digest('hex');
}

const profilePath = process.argv[2];
if (!profilePath) {
  console.error('Usage: node tools/compute-hash.js <profile.json>');
  process.exit(1);
}

const profile = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const hash = computeIntegrity(profile);
console.log(hash);
