package com.ecenisaugu.youtube_analytics.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "comments")
@Getter
@Setter
public class Comments {
    @Id
    private String commentId;
    private String videoId;
    private String text_tr;
    private String text_en;
    private String author;
    private int likeCount;
    private String sentiment;
    private float score;

    public Comments(String videoId, String text_tr, String author, int likeCount, String sentiment, int score,String text_en) {
        this.videoId = videoId;
        this.text_tr = text_tr;
        this.author = author;
        this.likeCount = likeCount;
        this.sentiment = sentiment;
        this.text_en = text_en;
        this.score = score;
    }

}
