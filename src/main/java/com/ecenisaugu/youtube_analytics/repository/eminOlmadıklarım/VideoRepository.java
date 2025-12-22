package com.ecenisaugu.youtube_analytics.repository.eminOlmadıklarım;

import com.ecenisaugu.youtube_analytics.model.video.Video;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface VideoRepository extends MongoRepository<Video, String> {
}
