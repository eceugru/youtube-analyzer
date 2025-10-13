package com.ecenisaugu.youtube_analytics.repository;

import com.ecenisaugu.youtube_analytics.model.VideoAnalyses;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface VideoAnalysesRepository extends MongoRepository<VideoAnalyses, String> {
}
