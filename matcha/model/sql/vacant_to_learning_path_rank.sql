--
-- 
with path_hard_skills as (
    select
        distinct
        p.code_path,
        p.name_path,
        p.type_path,
        chs.code_skill,
        hs.name_hskill 
    from path p
    left join path_competence pc 
        on (p.code_path = pc.code_path)
    left join competence_hard_skills chs 
        on (pc.code_competence = chs.code_competence)
    left join hard_skills hs
        on (chs.code_skill = hs.code_hskill)
),
-- 
-- 
skill_match as (
    select
        code_path,
        name_path,
        count(*) as n_skills,
        sum(if(lower(name_hskill)
                    in :values,
            1, 0)
            ) as `rank`,
		group_concat(if(lower(name_hskill)
						in :values,
						name_hskill, NULL)
					separator '$') as matched_skills_names,
		group_concat(if(lower(name_hskill)
						in :values,
						code_skill, NULL)
					separator '$') as matched_skills_codes,
		group_concat(if(lower(name_hskill)
						not in :values,
						name_hskill, NULL)
					separator '$') as unmatched_skills_names,
		group_concat(if(lower(name_hskill)
						not in :values,
						code_skill, NULL)
					separator '$') as unmatched_skills_codes
    from
        path_hard_skills
    where
        type_path = 'CORE'
    group by
        code_path,
        name_path
    order by
        `rank` desc,
        code_path desc
)
-- 
-- 
select
    *,
    if(`rank` is null, 0, `rank` / n_skills) as affinity
from skill_match
