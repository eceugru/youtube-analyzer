package com.ecenisaugu.youtube_analytics.repository;

import com.ecenisaugu.youtube_analytics.model.VideoCommentsSummary;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface VideoCommentsSummaryRepository extends MongoRepository<VideoCommentsSummary, String> {
}
