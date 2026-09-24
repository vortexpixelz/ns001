#!/usr/bin/env python3
"""Run exactly one positive and two negative checks in isolated network namespaces."""
import os, pathlib, subprocess, tempfile, json, hashlib
p = pathlib.Path(__file__).resolve().parent
gh = '/home/jacob/.local/opt/ns001-gh/2.101.0/gh'
assert hashlib.sha256(pathlib.Path(gh).read_bytes()).hexdigest() == 'ea857a3f0f7d4276cf5848b236542c5048e2eaa7bdd1b6ddec238f8793e74bff'
zipfile = p / 'NS001_H1_AUDIT_BUNDLE_20260903.zip'
assert hashlib.sha256(zipfile.read_bytes()).hexdigest() == 'a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f'
bundle = next(p.glob('sha256:*.jsonl'))
policy = ['--bundle', str(bundle), '--custom-trusted-root', str(p/'trusted_root.jsonl'), '--repo', 'vortexpixelz/ns001', '--cert-identity', 'https://github.com/vortexpixelz/ns001/.github/workflows/ns001-h1-custody.yml@refs/heads/main', '--cert-oidc-issuer', 'https://token.actions.githubusercontent.com', '--signer-digest', 'd9dcfbef1bea173b316bc968fd71421c982422c3', '--source-digest', 'd9dcfbef1bea173b316bc968fd71421c982422c3', '--source-ref', 'refs/heads/main', '--predicate-type', 'https://github.com/vortexpixelz/ns001/predicates/h1-custody/v1', '--deny-self-hosted-runners', '--format', 'json']
with tempfile.TemporaryDirectory(prefix='ns001-offline-') as t:
 env = {k:v for k,v in os.environ.items() if k not in ['GH_TOKEN','GITHUB_TOKEN','GH_ENTERPRISE_TOKEN','GITHUB_ENTERPRISE_TOKEN']}
 env.update(GH_CONFIG_DIR=t, GH_PROMPT_DISABLED='1', GH_NO_UPDATE_NOTIFIER='1')
 wrong = pathlib.Path(t)/'wrong.zip'; wrong.write_bytes(zipfile.read_bytes()+b'\nNS001 negative verification\n')
 copy = pathlib.Path(t)/'identity.zip'; copy.write_bytes(zipfile.read_bytes())
 cases = [('positive',zipfile,policy),('wrong-artifact',wrong,policy),('wrong-identity',copy,[('wrong/repository' if x=='vortexpixelz/ns001' else x) for x in policy])]
 results=[]
 for name,artifact,flags in cases:
  cmd=['unshare','-Urn',gh,'attestation','verify',str(artifact),*flags]
  r=subprocess.run(cmd,env=env,capture_output=True)
  (p/(name+'.stdout')).write_bytes(r.stdout); (p/(name+'.stderr')).write_bytes(r.stderr)
  results.append(dict(case=name,command=cmd,exit_code=r.returncode,artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest()))
 (p/'verification-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print([(r['case'],r['exit_code']) for r in results])
 assert [r['exit_code'] for r in results]==[0,1,1]
