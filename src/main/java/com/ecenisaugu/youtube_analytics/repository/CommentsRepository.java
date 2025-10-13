package com.ecenisaugu.youtube_analytics.repository;

import com.ecenisaugu.youtube_analytics.model.Comments;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface CommentsRepository extends MongoRepository<Comments, String> {
}
