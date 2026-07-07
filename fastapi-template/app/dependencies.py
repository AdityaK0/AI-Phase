# DB session is now handled by DBSessionMiddleware + ContextVar in database.py.
# No get_db() needed anywhere.
#
# Put shared FastAPI Depends() here as the app grows — e.g.:
#
#   def get_current_user(token: str = Header(...)) -> UserResponse:
#       ...
#
#   def require_admin(user: UserResponse = Depends(get_current_user)) -> UserResponse:
#       if user.role != "admin":
#           raise HTTPException(403, "Admin only")
#       return user
