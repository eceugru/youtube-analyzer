package com.ecenisaugu.youtube_analytics.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Getter
@Setter
@Document(collection = "analysis-job")
public class AnalysisJob {

    @Id
    private String jobId;
    private String videoId;
    private String videoAUrl;
    private String videoBUrl;
    private String status; // RUNNING, DONE, FAILED
}
