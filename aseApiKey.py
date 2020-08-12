from aseLib import ASELib

ase = ASELib()

res = ase.get("/ase/api/version")
version = res.json()
print(version)

