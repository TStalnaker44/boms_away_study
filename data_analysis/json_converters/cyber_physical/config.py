
types = {"G":"['general']", 
         "SB":"['background']['sbom']", 
         "HB":"['background']['hbom']",
         "L":"['likert']", 
         "O":"['open']", 
         "Q":"['demographics']"}

shared = ["ResponseID"]

ranked = ["O4"]

multi = ["HB3", "Q4"]

single = ["SB1", "HB1", "HB2", "L1", "L2", "L3", "L4", "L5", "L6",
          "Q1", "Q2", "Q3", "Q8", "Q9", "Q10"]

ranked_answers = {
      "o4" : ["Stored with trusted third party",
            "Published in associated repositories",
            "Downloadable from project website",
            "Available upon request",
            "Packaged/included with the associated system",
            "Other"]
}

ids = {}