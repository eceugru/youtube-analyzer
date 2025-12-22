package com.ecenisaugu.youtube_analytics.repository;

import com.ecenisaugu.youtube_analytics.model.AnalysisJob;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface AnalysisJobRepository extends MongoRepository<AnalysisJob, String> {

}
