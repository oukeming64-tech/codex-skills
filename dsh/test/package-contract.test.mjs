import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..', '..');
const manifestPath = path.join(root, 'package.json');
const patchPath = path.join(root, 'dsh', 'cordis.patch.yml');
const expectedSkills = ['docs-sync-guardian', 'handoff-auditor'];

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function readSkillName(skill) {
  const body = fs.readFileSync(path.join(root, 'skills', skill, 'SKILL.md'), 'utf8');
  const match = /^---\n[\s\S]*?^name:\s*([^\n]+)\n[\s\S]*?^---$/m.exec(body);
  assert.ok(match, `${skill} must have YAML frontmatter`);
  return match[1].trim();
}

test('package identity and attribution point to oukeming64-tech', () => {
  const pkg = readJson(manifestPath);
  assert.equal(pkg.name, '@oukeming64-tech/codex-skills');
  assert.equal(pkg.version, '0.1.0');
  assert.equal(pkg.license, 'MIT');
  assert.equal(pkg.author?.name, 'oukeming64-tech');
  assert.equal(pkg.author?.url, 'https://github.com/oukeming64-tech');
  assert.equal(pkg.repository?.url, 'git+https://github.com/oukeming64-tech/codex-skills.git');
  assert.equal(pkg.homepage, 'https://github.com/oukeming64-tech/codex-skills');
  assert.equal(pkg.bugs, 'https://github.com/oukeming64-tech/codex-skills/issues');
});

test('package is a dependency-free DSH bundle with no install hooks', () => {
  const pkg = readJson(manifestPath);
  assert.equal(pkg.dsh?.bundle?.patch, './dsh/cordis.patch.yml');
  assert.equal(fs.existsSync(patchPath), true);
  for (const field of [
    'dependencies',
    'devDependencies',
    'optionalDependencies',
    'peerDependencies',
    'bundledDependencies',
    'bundleDependencies',
  ]) {
    assert.equal(Object.hasOwn(pkg, field), false, field);
  }
  for (const hook of ['preinstall', 'install', 'postinstall', 'prepare']) {
    assert.equal(pkg.scripts?.[hook], undefined, hook);
  }
  for (const keyword of ['agent-skills', 'deepseek-harness', 'dsh-plugin']) {
    assert.ok(pkg.keywords?.includes(keyword), `missing keyword ${keyword}`);
  }
});

test('bundle inserts one isolated Skill provider for the packaged skills', () => {
  const patch = fs.readFileSync(patchPath, 'utf8');
  assert.match(patch, /^- insert:/m);
  assert.match(patch, /id:\s*oukeming64-tech-codex-skills/);
  assert.match(patch, /name:\s*'@deepseek-ai\/dsh-skill-filesystem'/);
  assert.match(patch, /providerName:\s*oukeming64-tech-codex-skills/);
  assert.match(patch, /includeDefaultRoots:\s*false/);
  assert.match(patch, /bundledSkillDir:\s*!!js/);
  assert.match(
    patch,
    /createRequire\(baseUrl\)\.resolve\('@oukeming64-tech\/codex-skills\/package\.json'\)/,
  );
  assert.doesNotMatch(patch, /^\s*(?:customSkillDirs|mcpServers|telemetry|credentials|hooks):/m);
  assert.equal([...patch.matchAll(/^- insert:/gm)].length, 1);
});

test('the public bundle contains only the selected first-wave skills', () => {
  const actual = fs.readdirSync(path.join(root, 'skills'), { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
    .sort();
  assert.deepEqual(actual, expectedSkills);
  for (const skill of expectedSkills) {
    assert.equal(readSkillName(skill), skill);
    assert.equal(fs.existsSync(path.join(root, 'skills', skill, 'agents', 'openai.yaml')), true);
  }
});

test('README documents exact install, uninstall, compatibility, and ownership', () => {
  const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
  assert.match(readme, /@deepseek-ai\/dsh@0\.1\.0-rc\.6/);
  assert.match(readme, /github:oukeming64-tech\/codex-skills#dsh-v0\.1\.0/);
  assert.match(readme, /remove @oukeming64-tech\/codex-skills/);
  assert.match(readme, /not an official DeepSeek product/i);
  assert.match(readme, /https:\/\/github\.com\/oukeming64-tech\/codex-skills/);
  assert.match(readme, /no MCP server, network client[\s\S]*credential handling[\s\S]*install hook/i);
});
