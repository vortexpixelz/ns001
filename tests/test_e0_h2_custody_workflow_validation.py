import ast,copy,hashlib,io,json,os,pathlib,tempfile,urllib.error,urllib.request,unittest,textwrap
from unittest.mock import patch
WORKFLOW = pathlib.Path(__file__).resolve().parents[1] / '.github/workflows/ns001-h1-custody.yml'
workflow = WORKFLOW.read_text()
script = textwrap.dedent(workflow.split("          python3 - <<'PY'\n", 1)[1].split('          PY\n', 1)[0])
ast.parse(script)
# Synthetic bytes keep tests offline and independent of the retained private/local ZIP.
# Only the expected digest in the extracted test copy is substituted. Pin assertions
# below verify the production workflow still contains the exact frozen identity.
artifact = b'H' * 51103
FROZEN_DIGEST = 'a055e9817808fddc3de1c1be138e4ab6f7539b01a470a2455bee64a354db614f'
script = script.replace(FROZEN_DIGEST, hashlib.sha256(artifact).hexdigest())
f='NS001_H1_AUDIT_BUNDLE_20260903.zip';p='NS001_H1_PUBLICATION_PROVENANCE.json';commit='a'*40
base={'schema':'ns001.h1.publication-provenance.v1','repository_id':1354037143,'publisher_account_id':202687650,'artifact_name':f,'artifact_size':51103,'artifact_sha256':hashlib.sha256(artifact).hexdigest(),'h1_source_commit':'6e33cb9ca7019e50e2f247ade9ae8c9a7b40d3ff','mandate_adoption_commit':'cd6e3eb806fa5a5045daaf35904ea927cec68f55','publication_commit':commit,'release_tag':'review','historical_custody_established':False,'e0_status':'HOLD','h2a2_status':'UNSTARTED'}
class Response(io.BytesIO):
 def geturl(self):return 'https://release-assets.githubusercontent.com/mock'
def run(case):
 prov=copy.deepcopy(base)
 if case=='scope':prov['e0_status']='AUTHORIZED'
 if case=='type':prov['artifact_size']='51103'
 raw=json.dumps(prov).encode()
 if case=='duplicate-json':raw=b'{"historical_custody_established":true,'+raw[1:]
 if case=='duplicate-same':raw=b'{"e0_status":"HOLD",'+raw[1:]
 if case=='duplicate-nested':raw=b'{"extra":{"x":1,"x":2},'+raw[1:]
 if case=='duplicate-array':raw=b'{"extra":[{"x":1,"x":2}],'+raw[1:]
 if case=='duplicate-escaped':raw=b'{"e0_\\u0073tatus":"HOLD",'+raw[1:]
 if case=='unique-nested':raw=b'{"extra":[{"x":1},{"x":2}],'+raw[1:]
 blobs={f:artifact,p:raw}
 assets=[{'name':n,'id':i+1,'size':len(b),'state':'uploaded','uploader':{'id':202687650},'browser_download_url':'https://github.com/vortexpixelz/ns001/releases/download/review/'+n,'created_at':'2026-01-01T00:00:00Z'} for i,(n,b) in enumerate(blobs.items())]
 rel={'id':1,'tag_name':'review','immutable':True,'draft':False,'assets':assets,'published_at':'2026-01-01T00:00:00Z'}
 if case=='mutable':rel['immutable']=False
 if case=='draft':rel['draft']=True
 if case=='missing-asset':assets.pop(0)
 if case=='duplicate-asset':assets.append(copy.deepcopy(assets[0]))
 if case=='uploader':assets[0]['uploader']['id']=42
 if case=='wrong-size':assets[0]['size']=51102
 if case=='state':assets[0]['state']='starter'
 if case=='tag':rel['tag_name']='other'
 if case=='wrong-bytes':blobs[f]=b'X'+artifact[1:]
 if case=='locator':assets[0]['browser_download_url']='https://example.org/other'
 if case=='null-time':rel['published_at']=None
 if case.startswith('time:'):
  _,target,kind=case.split(':')
  obj,key=(rel,'published_at') if target=='release' else (assets[0],'created_at')
  values={'null':None,'empty':'','malformed':'yesterday','calendar':'2026-02-30T00:00:00Z',
          'timezone':'2026-01-01T00:00:00','offset':'2026-01-01T00:00:00+00:00',
          'fraction':'2026-01-01T00:00:00.123Z','space':' 2026-01-01T00:00:00Z',
          'numeric':123,'boolean':True,'leap':'2024-02-29T23:59:59Z'}
  if kind=='missing':del obj[key]
  else:obj[key]=values[kind]
 env={'RELEASE_TAG':'review','PUBLICATION_COMMIT':commit,'PROVENANCE_SHA256':hashlib.sha256(raw).hexdigest(),'GITHUB_WORKFLOW_REF':'review','GITHUB_WORKFLOW_SHA':commit,'GITHUB_ACTOR_ID':'202687650','GITHUB_RUN_ID':'1'}
 if case=='provenance-digest':env['PROVENANCE_SHA256']='0'*64
 if case=='invalid-commit':env['PUBLICATION_COMMIT']='main'
 def mock(req,timeout):
  url=req.full_url if hasattr(req,'full_url') else req
  if case=='network-error':raise OSError('mock offline error')
  if url.endswith('/ns001'):d={'id':1354037143,'private':False}
  elif '/releases/tags/' in url:
   if case=='missing-release':raise urllib.error.HTTPError(url,404,'mock missing',None,None)
   d=rel
  elif '/git/ref/tags/' in url:d={'object':{'type':'tree' if case=='bad-tag-type' else 'commit','sha':'b'*40 if case=='wrong-commit' else commit}}
  elif '/releases/download/' in url:return Response(blobs[url.rsplit('/',1)[1]])
  else:raise AssertionError(url)
  encoded=json.dumps(d).encode()
  if '/releases/tags/' in url and case=='duplicate-api':encoded=b'{"immutable":false,'+encoded[1:]
  if '/releases/tags/' in url and case=='duplicate-api-nested':encoded=b'{"extra":{"x":1,"x":2},'+encoded[1:]
  return Response(encoded)
 cwd=os.getcwd()
 with tempfile.TemporaryDirectory(prefix='ns001-review-') as temp:
  os.chdir(temp)
  try:
   with patch.dict(os.environ,env),patch.object(urllib.request,'urlopen',side_effect=mock):
    try:exec(compile(script,'review-guard','exec'),{})
    except (SystemExit, ValueError, KeyError, OSError):return 'REJECT'
    return 'ACCEPT'
  finally:os.chdir(cwd)
cases=['valid','missing-release','missing-asset','wrong-bytes','uploader','provenance-digest','scope','type','mutable','draft','duplicate-asset','wrong-size','state','tag','locator','invalid-commit','wrong-commit','bad-tag-type','network-error','duplicate-json','null-time']

cases += ['duplicate-same','duplicate-nested','duplicate-array','duplicate-escaped',
          'unique-nested','duplicate-api','duplicate-api-nested']
cases += ['time:'+target+':'+kind for target in ['release','asset'] for kind in
          ['null','missing','empty','malformed','calendar','timezone','offset','fraction','space','numeric','boolean','leap']]

class CustodyWorkflowGuardTests(unittest.TestCase):
    def test_boundary_pins(self):
        header = workflow.split('permissions:', 1)[0]
        self.assertIn('  workflow_dispatch:', header)
        for forbidden in ['  push:', '  pull_request:', '  release:', '  schedule:', '  workflow_call:']:
            self.assertNotIn(forbidden, header)
        self.assertIn('permissions: {}', workflow)
        self.assertIn('    permissions:\n      id-token: write\n      attestations: write\n    steps:', workflow)
        self.assertIn(FROZEN_DIGEST, workflow)
        self.assertIn("download(filename, digest, 51103)", workflow)
        self.assertIn("filename = 'NS001_H1_AUDIT_BUNDLE_20260903.zip'", workflow)
        self.assertIn('uses: actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6', workflow)
        self.assertIn('push-to-registry: false', workflow)
        self.assertIn('create-storage-record: false', workflow)

# One unittest per case makes totals and individual failures visible.
for case in cases:
    def check(self, case=case):
        valid = case in ['valid','unique-nested'] or case.endswith(':leap')
        self.assertEqual(run(case), 'ACCEPT' if valid else 'REJECT', case)
    setattr(CustodyWorkflowGuardTests, 'test_guard_'+case.replace(':','_').replace('-','_'), check)

if __name__ == '__main__':
    unittest.main()
