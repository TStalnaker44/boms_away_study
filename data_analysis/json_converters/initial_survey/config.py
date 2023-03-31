
types = {"S":"shared", "P":"producers", "C":"consumers",
     "T":"developers", "SM":"standard_makers", "E":"educators",
     "Q":"demographics","SC":"security"}

shared = ["ResponseID"]

ranked = ["S9", "E5"]

multi = ["S2", "P2", "P3", "C2", "T2",  "T3",
         "T4", "SM2", "E4", "Q4", "Q5"]

single = ["S4", "S7", "P7", "C4", "C5", "T5", "E2", "E3",
          "SC1", "SC2", "SC3", "SC4", "SC5", "SC6", "Q1",
          "Q2", "Q3", "Q6", "Q8", "Q9", "Q10"]

ranked_answers = {
      "s9" : ["Stored with trusted third party",
            "Located in repositories along with source code",
            "Downloadable from project website",
            "Available from the project developers upon request",
            "Attached to software binaries",
            "Other"],

      "e5" : ["Official SBOM format documentation",
            "Specialized training courses or seminars",
            "Conference presentations",
            "Curated SBOM examples",
            "Requirements set by regulatory bodies",
            "Integration of SBOM functionality into existing tools",
            "Other"]
}

ids = {"consumer":"I use the SBOMs of software projects I am involved in or third-party software components/dependencies",
       "educator":"I develop, compile, and/or apply educational resources related to SBOMs",
       "standard_maker":"I am involved in defining standards / specifications for SBOMs",
       "producer":"I create SBOMs for the software projects I am involved in",
       "tool_developer":"I create tools that generate or process SBOMs",
       "other":"Other (please specify)"}