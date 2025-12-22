package com.ecenisaugu.youtube_analytics.controller;

import com.ecenisaugu.youtube_analytics.model.AnalysisJob;
import com.ecenisaugu.youtube_analytics.repository.AnalysisJobRepository;
import com.ecenisaugu.youtube_analytics.service.CommentService;
import com.ecenisaugu.youtube_analytics.service.VideoLinkProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/comments")
public class CommentController {
    @Autowired
    private VideoLinkProducer videoLinkProducer;
    @Autowired
    private AnalysisJobRepository analysisJobRepository;

    @PostMapping("/sentimentAnalysis")
    public ResponseEntity<Map<String,String>> sentimentAnalysis(@RequestBody Map<String, String> body){
        // Burada link frontend 'den çekilir ✅
        //rabbitmq ile pythona job atanır.
        // --> Python linki alır ve işler.
        String url = body.get("url");

        String videoId = CommentService.extractVideoId(url);

        String jobId = UUID.randomUUID().toString();

        AnalysisJob analysisJob = new AnalysisJob();
        analysisJob.setJobId(jobId);
        analysisJob.setVideoId(videoId);
        analysisJob.setVideoAUrl(null);
        analysisJob.setVideoBUrl(null);
        analysisJob.setStatus("RUNNING");

        analysisJobRepository.save(analysisJob);

        // queue'ye bu gönderiliyor 
        Map<String,String> map = Map.of(
                "jobId", jobId,
                "videoUrl",url
        );

        videoLinkProducer.sendVideoUrl(map);


        return ResponseEntity.ok(Map.of("jobId", jobId));
    };

    // ----------------------------------------------
    // Verilerin gönderilmesi jobController ile yapılıyor
    // ----------------------------------------------

}
