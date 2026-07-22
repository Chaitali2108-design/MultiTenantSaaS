PLAN_LIMITS = {

    "FREE": {
        "max_users": 5,
        "max_projects": 5,
        "storage_limit_gb": 1,
    },

    "BASIC": {
        "max_users": 20,
        "max_projects": 25,
        "storage_limit_gb": 5,
    },

    "PRO": {
        "max_users": 100,
        "max_projects": 100,
        "storage_limit_gb": 25,
    },

    "ENTERPRISE": {
        "max_users": 1000,
        "max_projects": 1000,
        "storage_limit_gb": 100,
    },
}


def apply_plan_limits(organization):

    limits = PLAN_LIMITS.get(
        organization.plan
    )

    if limits:

        organization.max_users = limits["max_users"]

        organization.max_projects = limits["max_projects"]

        organization.storage_limit_gb = limits["storage_limit_gb"]

        organization.save()