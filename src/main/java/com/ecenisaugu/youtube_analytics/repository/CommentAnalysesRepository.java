package com.ecenisaugu.youtube_analytics.repository;

import com.ecenisaugu.youtube_analytics.model.CommentAnalyses;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface CommentAnalysesRepository extends MongoRepository<CommentAnalyses, String> {
}
