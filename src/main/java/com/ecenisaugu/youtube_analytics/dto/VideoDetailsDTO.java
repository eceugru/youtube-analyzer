package com.ecenisaugu.youtube_analytics.dto;

import com.ecenisaugu.youtube_analytics.model.Comments;
import com.ecenisaugu.youtube_analytics.model.CommentsSummary;

import java.util.List;

public class VideoDetailsDTO {
    // Birleştirilmiş veri modeli
    private String videoId;
    private List<Comments> comments;
    private CommentsSummary commentsSummary;

    // Getters and Setters
    public String getVideoId() {
        return videoId;
    }

    public void setVideoId(String videoId) {
        this.videoId = videoId;
    }

    public List<Comments> getComments() {
        return comments;
    }

    public void setComments(List<Comments> comments) {
        this.comments = comments;
    }

    public CommentsSummary getCommentsSummary() {
        return commentsSummary;
    }

    public void setCommentsSummary(CommentsSummary commentsSummary) {
        this.commentsSummary = commentsSummary;
    }
}
