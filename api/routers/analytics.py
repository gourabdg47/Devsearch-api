from fastapi import APIRouter, Depends
from api.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, desc
from api.models.user import User
from api.models.search_log import SearchLog
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/analytics")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    # Queries per Vertical
    queries_per_vertical = await db.execute(
        func.count(SearchLog.id).group_by(SearchLog.vertical)
    )
    queries_per_vertical = dict(queries_per_vertical.fetchall())

    # User Activity Over Time (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    user_activity = await db.execute(
        func.count(SearchLog.id).group_by(func.date(SearchLog.timestamp))
        .filter(SearchLog.timestamp >= thirty_days_ago)
        .order_by(func.date(SearchLog.timestamp))
    )
    user_activity = [{"date": date, "count": count} for date, count in user_activity.fetchall()]

    # Top Users
    top_users = await db.execute(
        db.query(User.username, func.count(SearchLog.id).label('query_count'))
        .join(SearchLog)
        .group_by(User.id)
        .order_by(desc('query_count'))
        .limit(5)
    )
    top_users = [{"username": username, "queryCount": count} for username, count in top_users.fetchall()]

    # Recent Activity
    recent_activity = await db.execute(
        db.query(User.username, SearchLog.vertical, SearchLog.query, SearchLog.timestamp)
        .join(User)
        .order_by(desc(SearchLog.timestamp))
        .limit(20)
    )
    recent_activity = [
        {
            "username": username,
            "vertical": vertical,
            "query": query,
            "timestamp": timestamp.isoformat()
        }
        for username, vertical, query, timestamp in recent_activity.fetchall()
    ]

    return {
        "queriesPerVertical": queries_per_vertical,
        "userActivityOverTime": user_activity,
        "topUsers": top_users,
        "recentActivity": recent_activity
    }