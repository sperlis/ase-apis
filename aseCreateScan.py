from aseLib import ASELib

ase = ASELib()

# start a scan job, using a scant template as a base
jobDetails = {
  "testPolicyId": 2,  # policy ID - Application Only
  "folderId": 1,      # ASE folder ID
  #"applicationId": 0, # No application specified
  "name": "A Test Scan",
  "description": "",
  "contact": ""
}

                                                # 7 == template ID of demo.testfire.net - replace with ID of wanted template
res = ase.post("/ase/api/jobs/7/dastconfig/createjob",json=jobDetails)
jobInfo = res.json()
print(jobInfo)

# change new job configuration
    # set starting URL
configItem = {
  "scantNodeXpath": "StartingUrl",   # shortcut name
  "scantNodeNewValue": "https://demo.testfire.net",
  "encryptNodeValue": False
}
res = ase.post("/ase/api/jobs/" + str(jobInfo["id"]) + "/dastconfig/updatescant",json=configItem)
if (not res.status_code == 200) :
    error = res.json()
    print(error["errorMessage"])

    # set number of threads
configItem = {
  "scantNodeXpath": "//ScanConfiguration/Communication/NumberOfThreads", # fully qualified
  "scantNodeNewValue": 3,
  "encryptNodeValue": False
}
res = ase.post("/ase/api/jobs/" + str(jobInfo["id"]) + "/dastconfig/updatescant",json=configItem)
if (not res.status_code == 200) :
    error = res.json()
    print(error["errorMessage"])

    # run the job
        #obtain E-tag
res = ase.get("/ase/api/jobs/" + str(jobInfo["id"]))
action = { "type": "run"}
headers = {}
headers["If-Match"] = res.headers["Etag"]
res = ase.post("/ase/api/jobs/" + str(jobInfo["id"]) + "/actions",json=action,headers=headers)
if (not res.status_code == 200) :
    error = res.json()
    print(error["errorMessage"])
del headers["If-Match"]
