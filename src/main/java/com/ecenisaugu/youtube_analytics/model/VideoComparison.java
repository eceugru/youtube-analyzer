package com.ecenisaugu.youtube_analytics.model;

import java.util.Map;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Document(collection = "video-comparison")
public class VideoComparison {

    @Id
    private String Id;
    private String videoAId;
    private String videoBId;
    private  Map<String, String> llmResult;
     
}
