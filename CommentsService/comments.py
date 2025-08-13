# CRUD functions
from flask import jsonify
from config import call_proc
from datetime import datetime, timezone
from authorize import get_local_user

# for the CreatedOn column
def get_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# Read; gets all unarchived comment
def get_comments():
    rows = call_proc("CW2.GetActiveComments")
    return jsonify(rows), 200

# get comments by comment id
def get_comment_by_id(commentID):
    rows = call_proc("CW2.GetActiveComments")
    result = next((row for row in rows if row["Comment_ID"] == int(commentID)), None)
    if result:
        return jsonify(result), 200
    else:
        return {'message': 'Comment not found'}, 404

# get comment by user
def get_comments_by_user(userID):
    rows = call_proc("CW2.GetActiveComments")
    filter = [row for row in rows if row["User_ID"] == int(userID)]
    return jsonify(filter), 200

# Create
def post_comment(body, token_info): #added in the apikey auth, token_info
    print("DEBUG body:", body)
    print("DEBUG token_info:", token_info)

    if not token_info:
        return {'message': 'Unauthorized'}, 401
    
    # find user by email
    email = token_info.get("Email") or token_info.get("email")
    local_user = get_local_user(email)
    if not local_user:
        return {'message': 'User not found in SQL'}, 404
    
    user_id = local_user['User_ID']

    required_fields = ['Trail_ID', 'Content']
    for field in required_fields:
        val = body.get(field)
        if val is None or (isinstance(val, str) and val.strip() == ""):
            return {'message': f"{field} is required"}, 400
        
    # timestamp if timestamp isn't provided manually
    created_on = body.get('CreatedOn') or get_timestamp()

    params = (int(body['Trail_ID']), user_id, body['Content'], created_on, 0)
    try:
        call_proc("CW2.InsertComment", params)
        return {'message': 'Comment created'}, 201
    except Exception as e:
        return {'message': f"Error creating comment: {str(e)}"}, 500

# Update
def put_comment(commentID, body, token_info):
    if not token_info: #checks its the author editing
        return {'message': 'Unauthorized'}, 401
    
    email = token_info.get("Email") or token_info.get("email")
    local_user = get_local_user(email)
    if not local_user:
        return {'message': 'User not found in SQL'}, 404
    
    user_id = local_user['User_ID']

    params = (commentID, user_id, body.get('Content'), body.get('IsArchived', 0))
    try:
        call_proc("CW2.UpdateComment", params)
        return {'message': 'Comment updated'}, 200
    except Exception as e:
        return {'message': f"Error updating comment: {str(e)}"}, 500

# Delete
def delete_comment(commentID, token_info):
    if not token_info:
        return {'message': 'Unauthorized'}, 401
    
    email = token_info.get("Email") or token_info.get("email")
    if not email:
        return {'message': 'Unauthorized: missing email'}, 401

    local_user = get_local_user(email)
    if not local_user:
        return {'message': 'User not found'}, 404
    
    # admins only
    if local_user.get('Role', '').lower() != 'admin':
        return {'message': 'Forbidden: admin only!'}, 403
    
    try:
        call_proc("CW2.ArchiveComment", (commentID, local_user['User_ID']))
        return {'message': 'Comment archived'}, 200
    except Exception as e:
        return {'message': f"Error archiving comment: {str(e)}"}, 500