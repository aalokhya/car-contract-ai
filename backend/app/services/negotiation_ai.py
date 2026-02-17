def generate_tips(contract_id: int, risks=None):

    tips = {
        "unfair_clauses": [],
        "negotiation_points": [],
        "message_to_dealer": ""
    }

    if risks:
        for risk in risks:
            if "Penalty" in risk:
                tips["unfair_clauses"].append("Penalty charges may increase overall cost")
                tips["negotiation_points"].append("Request reduction or cap on penalties")

            if "termination" in risk.lower():
                tips["unfair_clauses"].append("Termination terms may be strict")
                tips["negotiation_points"].append("Request flexible termination terms")

            if "liability" in risk.lower():
                tips["negotiation_points"].append("Clarify liability responsibilities")

    tips["message_to_dealer"] = (
        "I would like to review some terms in the contract, "
        "especially penalties and termination conditions. "
        "Can we discuss possible revisions?"
    )

    return tips
