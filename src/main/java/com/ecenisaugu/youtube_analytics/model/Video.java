package com.ecenisaugu.youtube_analytics.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collation = "video")
@Getter
@Setter
@AllArgsConstructor
public class Video {
    private String videoId;
    private String title;
    private String channelTitle;
    private String likeCount;
    private String commentCount;
}
