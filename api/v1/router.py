from fastapi import APIRouter

from api.v1.routes.entries import entries_router
from api.v1.routes.users import users_router
from api.v1.routes.insights import insight_router
from api.v1.routes.stats import stats_router
from api.v1.routes.analytics import analytics_router

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(entries_router)
router.include_router(users_router)
router.include_router(insight_router)
router.include_router(stats_router)
router.include_router(analytics_router)
