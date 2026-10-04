const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..', 'src');
const files = fs.readdirSync(root).filter(x=>x.endsWith('.ts')).sort();
const forbidden = [
  ['Math.random', /Math\.random\s*\(/],
  ['Date.now', /Date\.now\s*\(/],
  ['performance.now', /performance\.now\s*\(/],
  ['parseFloat', /parseFloat\s*\(/],
  ['Number constructor', /\bNumber\s*\(/],
  ['crypto randomness', /randomBytes|randomUUID|getRandomValues/],
  ['network I/O', /\bfetch\s*\(|https?\.request\s*\(/]
];
let failures = [];
let source = '';
for (const file of files) {
  const text = fs.readFileSync(path.join(root,file),'utf8');
  source += `\n/*FILE:${file}*/\n${text}`;
  for(const [label,re] of forbidden) if(re.test(text)) failures.push(`${file}: ${label}`);
}
const idsMatch = source.match(/"RHC", "FG", "MFP", "CNEP", "BCPP", "FIEP", "AKEP", "DES", "OTP", "EIYE",\s*\n\s*"SES", "CDM", "ESM", "DPG", "REP", "CVDE", "OPCC", "RCB", "EIA", "PEDC"/);
if(!idsMatch) failures.push('mechanism registry does not contain locked 20 IDs');
if(!source.includes('ADVISORY_ONLY')) failures.push('authority boundary token missing');
if(!source.includes('autoPromote:false')) failures.push('explicit no-auto-promotion path missing');
if(failures.length){ console.error('STATIC_VERIFY_FAIL'); for(const x of failures) console.error(x); process.exit(1); }
console.log(`STATIC_VERIFY_PASS files=${files.length} forbidden_patterns=0 mechanism_registry=20 authority_boundary=present`);
