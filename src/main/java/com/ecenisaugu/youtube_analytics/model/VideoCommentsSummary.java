package com.ecenisaugu.youtube_analytics.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "comments-summary")
public class VideoCommentsSummary {
    @Id
    private String id;
    private String videoId;
    private CommentsSummary summary; // iç içe obje

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getVideoId() {
        return videoId;
    }

    public void setVideoId(String videoId) {
        this.videoId = videoId;
    }

    public CommentsSummary getSummary() {
        return summary;
    }

    public void setSummary(CommentsSummary summary) {
        this.summary = summary;
    }
}
