class PostDetailsAggregations:
    @staticmethod
    def get_all_post(user_id: str):
        return [
            {
                "$lookup": {
                    "from": "post_like_details",
                    "localField": "post_id",
                    "foreignField": "post_id",
                    "as": "like_details",
                }
            },
            {"$unwind": {"path": "$like_details", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 0,
                    "caption": 1,
                    "description": 1,
                    "tags": 1,
                    "post_id": 1,
                    "user_id": 1,
                    "user_name": 1,
                    "user_profile": 1,
                    "object_url": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "likes": 1,
                    "liked": {"$in": [user_id, "$like_details.liked_by"]},
                }
            },
        ]
