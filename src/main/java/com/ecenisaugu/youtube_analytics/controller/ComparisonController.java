package com.ecenisaugu.youtube_analytics.controller;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ecenisaugu.youtube_analytics.model.AnalysisJob;
import com.ecenisaugu.youtube_analytics.model.VideoComparison;
import com.ecenisaugu.youtube_analytics.repository.AnalysisJobRepository;
import com.ecenisaugu.youtube_analytics.repository.VideoComparisonRepository;
import com.ecenisaugu.youtube_analytics.service.CommentService;
import com.ecenisaugu.youtube_analytics.service.VideoCompareProducer;

import jakarta.websocket.server.PathParam;

import java.util.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;



@RestController
@RequestMapping("/api/compare")
public class ComparisonController {

    private final AnalysisJobRepository analysisJobRepository;
    private final VideoCompareProducer videoCompareProducer;
    private final VideoComparisonRepository videoComparisonRepository;


    public ComparisonController(AnalysisJobRepository analysisJobRepository, VideoCompareProducer videoCompareProducer, VideoComparisonRepository videoComparisonRepository){
        this.analysisJobRepository = analysisJobRepository;
        this.videoCompareProducer = videoCompareProducer;
        this.videoComparisonRepository = videoComparisonRepository;
        
    }


    @PostMapping("/start")
    public ResponseEntity<Map<String, String>> postMethodName(@RequestBody Map<String, String> body) {
        // Burada linkler frontend' den çekilir
        // Rabbitmq ile pythona job atanır.
        // Python linkleri alır ve işler.
        // Burada sadece link gönderilmeli
        
        String urlA = body.get("urlA");
        String urlB = body.get("urlB");

        String jobId = UUID.randomUUID().toString();

        AnalysisJob analysisJob = new AnalysisJob();
        analysisJob.setJobId(jobId);
        analysisJob.setVideoId(null);
        analysisJob.setVideoAUrl(urlA);
        analysisJob.setVideoBUrl(urlB);
        analysisJob.setStatus("RUNNING");

        analysisJobRepository.save(analysisJob);

        Map<String, String> map = Map.of(
            "jobId", jobId,
            "videoAUrl", urlA,
            "videoBUrl", urlB
        );

        videoCompareProducer.sendVideoUrls(map);
        
        return ResponseEntity.ok(Map.of("jobId", jobId));
    }

    @GetMapping("/results/{jobId}")
    public ResponseEntity<?> getCompareResult(@PathVariable String jobId) {
        AnalysisJob job = analysisJobRepository.findById(jobId).orElseThrow();
         
        if(!"DONE".equalsIgnoreCase(job.getStatus())){
            return ResponseEntity.status(409).build();
        }

        String videoAId = CommentService.extractVideoId(job.getVideoAUrl());
        String videoBId = CommentService.extractVideoId(job.getVideoBUrl());

        VideoComparison videoComparison = videoComparisonRepository.findByVideoAIdAndVideoBId(videoAId, videoBId).orElseThrow();

        return ResponseEntity.ok(videoComparison.getLlmResult());
    }
    
    
    
}
