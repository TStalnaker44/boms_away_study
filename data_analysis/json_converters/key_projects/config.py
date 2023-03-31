
types = {"S":"['shared']",
         "FS":"['familiar']['shared']",
         "P":"['familiar']['producers']['shared']",
         "IP":"['familiar']['producers']['internal']",
         "EP":"['familiar']['producers']['external']",
         "C":"['familiar']['consumers']",
         "FN":"['familiar']['non_users']",
         "NU":"['non_users']",
         "O":"['oboms']",
         "Q":"['demographics']"}

shared = ["ResponseID"]

ranked = ["C7"]

multi = ["FS1","FS4","FS8","P2","P3","P4","P8","EP1","C1",
         "C2","C6","FN1","Q4","Q5","ID"]

single = ["S1","S2","S3","FS2","FS3","FS6","FS9","P1","P6","IP1","C3",
          "C4","FN2","O1","O2","Q1","Q2","Q3","Q6","Q8","Q9","Q10"]


ranked_answers = {
      "c7" : ["Stored with trusted third party",
      "Located in repositories along with source code",
      "Downloadable from project website",
      "Available from the project developers upon request",
      "Attached to software binaries",
      "Other"]
}

ids = {"consumer":"We use or analyze the SBOMs of other projects (including our dependencies)",
       "producer":"We create SBOMs for the software that we produce",
       "familiar_non_user":"I am familiar with SBOMs, but we do not use them in our projects",
       "unfamiliar":"I am unfamiliar with SBOMs",
       "other":"Other (please specify)"}