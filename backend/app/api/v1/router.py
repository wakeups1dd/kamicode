from fastapi import APIRouter
from app.api.v1 import auth, submissions, problems, admin, users, seasons, rush, achievements, websocket

router = APIRouter()

router.include_router(auth.router)
router.include_router(submissions.router)
router.include_router(problems.router)
router.include_router(admin.router)
router.include_router(users.router)
router.include_router(seasons.router)
router.include_router(rush.router)
router.include_router(achievements.router)
router.include_router(websocket.router)
