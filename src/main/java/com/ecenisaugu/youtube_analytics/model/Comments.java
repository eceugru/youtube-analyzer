package com.ecenisaugu.youtube_analytics.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collation = "comments")
@Getter
@Setter
public class Comments {
    @Id
    private String commentId;
    private String videoId;
    private String text;
    private String author;
    private String likeCount;

    public Comments(String videoId, String text, String author, String likeCount) {
        this.videoId = videoId;
        this.text = text;
        this.author = author;
        this.likeCount = likeCount;
    }

}
