import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / 'backend'))
from main import app,MODEL_PATH
from fastapi.testclient import TestClient

casos=[
('C01','I need information about my life insurance','LIFE_INSURANCE'),
('C02','I need information about my auto insurance','AUTO_INSURANCE'),
('C03','I need information about my home insurance','HOME_INSURANCE'),
('C04','I need information about my health insurance','HEALTH_INSURANCE'),
('C05','I need information about my pet insurance','PET_INSURANCE'),
('C06','I need information about my travel insurance','TRAVEL_INSURANCE'),
('C07','I want to file an insurance claim','CLAIMS'),
('C08','How can I pay my insurance premium?','PAYMENT'),
('C09','I want to renew my insurance policy','RENEW'),
('C10','I would like to get an insurance quote','QUOTE'),
('C11','How can I contact customer service?','CONTACT'),
('C12','I want to make a complaint','COMPLAINTS'),
('E01','','RECHAZO'),('E02','   ','RECHAZO'),
('E03','zzzzqwerty123','RECHAZO'),('E04','!!! 🦄','RECHAZO'),
('E05','a'*2001,'RECHAZO'),
('E06','  I need information about my life insurance  ','LIFE_INSURANCE'),
('E07','I NEED INFORMATION ABOUT MY LIFE INSURANCE','LIFE_INSURANCE'),
('E08','I need informtion about my life insuranc','LIFE_INSURANCE'),
('D01','¿Qué cubre mi seguro de vida?','EXPLORATORIO'),
('D02','insurance','EXPLORATORIO'),
('D03','I need life insurance and auto insurance','EXPLORATORIO'),
('D04','I like pizza and life insurance','EXPLORATORIO'),
('D05','What does my insurance cover?','COVERAGE'),
]
results=[]
with TestClient(app) as c:
 for id,text,expected in casos:
  r=c.post('/predecir',json={'texto':text});data=r.json()
  observed=data.get('categoria','RECHAZO' if r.status_code==422 else 'ERROR')
  results.append(dict(id=id,texto=text,esperado=expected,http=r.status_code,observado=observed,probabilidad=data.get('probabilidad'),terminos=data.get('terminos_reconocidos'),coincide=None if expected=='EXPLORATORIO' else observed==expected,respuesta=data))
out=Path(__file__).resolve().parent / 'resultados_ampliados.json'
out.write_text(json.dumps({'fecha':'2026-11-01','metodo':'FastAPI TestClient local; sin conexión de red ni Docker','sha256_modelo':hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest(),'nota':'Expectativas manuales; conjunto ilustrativo, no estimación de accuracy general.','casos':results},ensure_ascii=False,indent=2))
for r in results: print(r['id'],r['esperado'],r['observado'],r['http'],round(r['probabilidad'] or 0,4),r['coincide'])
