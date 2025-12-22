package com.ecenisaugu.youtube_analytics.repository.eminOlmadıklarım;

import com.ecenisaugu.youtube_analytics.model.comment.Comments;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface CommentsRepository extends MongoRepository<Comments, String> {
    public List<Comments> findByVideoId(String videoId);
}
