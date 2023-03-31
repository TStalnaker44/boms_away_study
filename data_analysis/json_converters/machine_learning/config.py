
types = {"B":"background",
         "AI":"aibom_fields",
         "D":"databom_fields",
         "C":"challenges",
         "Q":"demographics"}

shared = ["ResponseID"]

ranked = ["AI6","D6"]

multi = ["B2","AI2","D3","Q4"]

single = ["B1","AI1","AI3","D1","C4","C6","Q1","Q2",
          "Q3","Q5","Q6","Q8","Q9","Q10", "B3","AI5",
          "D2","D4","C3","C5"]

ranked_answers = {
      "ai6" : ["Stored with trusted third party",
            "Located in repositories along with source code",
            "Downloadable from project website",
            "Available from the project developers upon request",
            "Attached to software binaries",
            "Other"],

      "d6" : ["Stored with a trusted third party",
            "Located alongside the dataset",
            "Downloadable from maintainer or owner website",
            "Available from owner upon request",
            "Other"]
}

ids = {}