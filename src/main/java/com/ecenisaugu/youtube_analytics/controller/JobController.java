package com.ecenisaugu.youtube_analytics.controller;


import com.ecenisaugu.youtube_analytics.dto.VideoResultResponseDTO;
import com.ecenisaugu.youtube_analytics.model.AnalysisJob;
import com.ecenisaugu.youtube_analytics.repository.AnalysisJobRepository;
import com.ecenisaugu.youtube_analytics.service.CommentService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/jobs")
public class JobController {

    private final AnalysisJobRepository analysisJobRepository;
    private final CommentService commentService;

    public JobController(AnalysisJobRepository analysisJobRepository, CommentService commentService) {
        this.analysisJobRepository = analysisJobRepository;
        this.commentService = commentService;
    }

    // Job status
    @GetMapping("/{jobId}")
    public ResponseEntity<AnalysisJob> getJobStatus(@PathVariable String jobId) {
        AnalysisJob job = analysisJobRepository.findById(jobId).orElseThrow();
        return ResponseEntity.ok(job);
    }

    // Yorum analizi ve özetleme sonuçları 
    @GetMapping("/results/{jobId}")
    public ResponseEntity<VideoResultResponseDTO> getJobResult(@PathVariable String jobId) {

        AnalysisJob job = analysisJobRepository.findById(jobId).orElseThrow();

        if (!"DONE".equals(job.getStatus())){
            return ResponseEntity.status(409).build();
        }

        // Burada sadece yorumları gönderiyor - özetleme
        // job içinde videoId içeriyor bu sayede job kullanılarak sonuçlara erişilebiliniyor
        // <-- Burada özetleme sonucuda yüklenmesi gerekiyor -->
        VideoResultResponseDTO videoResultResponseDTO = commentService.getVideoDetails(job.getVideoId());
        
        return ResponseEntity.ok(videoResultResponseDTO);
    }

}
