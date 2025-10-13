package com.ecenisaugu.youtube_analytics.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collation = "videoAnalyses")
@AllArgsConstructor
@Getter
@Setter
public class VideoAnalyses {
    private String id;
    private String videoId;
    private String summary;
    private int pozitiveRating;
    private int negativeRating;
    private int naturalRating;

}
