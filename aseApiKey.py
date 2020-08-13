from aseLib import ASELib

ase = ASELib()

res = ase.post("/ase/api/account/apikey",json={})
apiKey = res.json()
print(apiKey)
