package com.ecenisaugu.youtube_analytics.repository;

import java.util.Optional;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.ecenisaugu.youtube_analytics.model.VideoComparison;

public interface VideoComparisonRepository extends MongoRepository<VideoComparison, String>{
    Optional<VideoComparison> findByVideoAIdAndVideoBId(String videoAId, String videoBId);
    
}
