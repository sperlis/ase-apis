from aseLib import ASELib

ase = ASELib()

def printoutItems():
    # get current user information
    res = ase.get("/ase/api/currentuser")
    user = res.json()
    print(user)

    # get a list of all available templates (scant files)
    res = ase.get("/ase/api/templates")
    templates = res.json()
    print(templates)

    # get a list of all available test policies
    res = ase.get("/ase/api/testpolicies")
    policies = res.json()
    print(policies)


    # get a list of all available folders (according to permissions)
    res = ase.get("/ase/api/folders")
    folders = res.json()
    print(folders)

    # get a list of all available applications (according to permissions)
    res = ase.get("/ase/api/applications")
    applications = res.json()
    print(applications)


printoutItems()

