def compute_match(resume_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str], int]:
    """Compute the match between resume and job skills."""
    common_skills = []
    missing_skills = []
    for skill in job_skills:
        if skill in resume_skills:
            common_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    match_score = int(len(common_skills) / len(job_skills) * 100)

    return [common_skills, missing_skills, match_score]