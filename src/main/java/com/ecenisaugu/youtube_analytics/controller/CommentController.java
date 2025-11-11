package com.ecenisaugu.youtube_analytics.controller;

import com.ecenisaugu.youtube_analytics.dto.VideoDetailsDTO;
import com.ecenisaugu.youtube_analytics.repository.CommentsRepository;
import com.ecenisaugu.youtube_analytics.service.CommentService;
import com.ecenisaugu.youtube_analytics.service.VideoLinkProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/comments")
public class CommentController {
    private final CommentsRepository commentsRepository;

    @Autowired
    private VideoLinkProducer videoLinkProducer;
    private CommentService commentService;

    CommentController(CommentsRepository commentsRepository) {
        this.commentsRepository = commentsRepository;
    }

    @PostMapping("/sentimentAnalysis")
    public ResponseEntity<String> sentimentAnalysis(@RequestBody Map<String, String> videoUrl){
        // Burada link frontend 'den çekilir ✅
        //rabbitmq ile pythona job atanır.
        // --> Python linki alır ve işler.
        String url = videoUrl.get("url");
        System.out.println("Video linki : " + url);

        videoLinkProducer.sendVideoUrl(url);

        return ResponseEntity.ok("Video link RabbitMQ'ya gönderildi: " + url);
    };

    @GetMapping("/sentimentAnalysis")
    public VideoDetailsDTO getVideoDetailController(@RequestBody Map<String, String> videoUrl){
        return null;
    }



}
