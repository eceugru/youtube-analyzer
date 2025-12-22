package com.ecenisaugu.youtube_analytics.repository.eminOlmadıklarım;

import com.ecenisaugu.youtube_analytics.model.comment.VideoCommentsSummary;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface VideoCommentsSummaryRepository extends MongoRepository<VideoCommentsSummary, String> {
    public VideoCommentsSummary findByVideoId(String videoId);
}
