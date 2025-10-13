package com.ecenisaugu.youtube_analytics.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collation = "commentAnalyses")
@AllArgsConstructor
@Getter
@Setter
public class CommentAnalyses {
    private String commentAnalysesId;
    private String videoId;
    private String sentiment;
    private int score;
    private String commentId;

    public String getCommentId() {
        return commentId;
    }

    public void setCommentId(String commentId) {
        this.commentId = commentId;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public String getSentiment() {
        return sentiment;
    }

    public void setSentiment(String sentiment) {
        this.sentiment = sentiment;
    }

    public String getVideoId() {
        return videoId;
    }

    public void setVideoId(String videoId) {
        this.videoId = videoId;
    }

    public String getCommentAnalysesId() {
        return commentAnalysesId;
    }

    public void setCommentAnalysesId(String commentAnalysesId) {
        this.commentAnalysesId = commentAnalysesId;
    }
}
