package com.ecenisaugu.youtube_analytics.service;

import com.ecenisaugu.youtube_analytics.dto.CommentResponseDTO;
import com.ecenisaugu.youtube_analytics.dto.VideoResultResponseDTO;
import com.ecenisaugu.youtube_analytics.model.comment.Comments;
import com.ecenisaugu.youtube_analytics.model.comment.VideoCommentsSummary;
import com.ecenisaugu.youtube_analytics.repository.eminOlmadıklarım.CommentsRepository;
import com.ecenisaugu.youtube_analytics.repository.eminOlmadıklarım.VideoCommentsSummaryRepository;
import org.springframework.stereotype.Service;


import java.util.*;

@Service
public class CommentService {

    private final CommentsRepository commentsRepository;
    private final VideoCommentsSummaryRepository  videoCommentsSummaryRepository;

    public CommentService(CommentsRepository commentsRepository, VideoCommentsSummaryRepository videoCommentsSummaryRepository) {
        this.commentsRepository = commentsRepository;
        this.videoCommentsSummaryRepository = videoCommentsSummaryRepository;
    }


    public VideoResultResponseDTO getVideoDetails(String videoId) {
        // Yorum özeti
        VideoCommentsSummary summaryCollection = videoCommentsSummaryRepository.findByVideoId(videoId);
        String summaryText = summaryCollection != null ? summaryCollection.getSummary() : "Henüz özet oluşturulmadı";


        // Yorumları standartlaştırma 
        // Burada yorumlar "text - author - sentiment" alanları alınması istenir
        List<Comments> commentsColletion = commentsRepository.findByVideoId(videoId);
        List<CommentResponseDTO> commentDTOs = commentsColletion.stream()
        .map(comment ->{
                CommentResponseDTO dto = new CommentResponseDTO();
                dto.setText(comment.getText_tr());
                dto.setAuthor(comment.getAuthor());
                dto.setSentiment(comment.getSentiment());
                return dto;
            }).toList();

        // pozitif - negatif - notr yorum sayıları

        long pozitiveCount = commentsColletion.stream()
            .filter(c ->"Pozitif".equalsIgnoreCase(c.getSentiment()))
            .count();
        long negativeCount = commentsColletion.stream()
            .filter(c -> "Negatif".equalsIgnoreCase(c.getSentiment()))
            .count();
        long notrCount = commentsColletion.stream()
            .filter(c -> "Nötr".equalsIgnoreCase(c.getSentiment()))
            .count();

        // Birleşik veri yapısı
        VideoResultResponseDTO videoResultResponseDTO = new VideoResultResponseDTO();
        videoResultResponseDTO.setComments(commentDTOs);
        videoResultResponseDTO.setSummary(summaryText);
        videoResultResponseDTO.setVideoId(videoId);
        videoResultResponseDTO.setPositiveCount(pozitiveCount);
        videoResultResponseDTO.setNegativeCount(negativeCount);
        videoResultResponseDTO.setNeutralCount(notrCount);

        return videoResultResponseDTO;
    }



    // url'den video id çıkarma işlemleri
    public static String extractVideoId(String videoUrl) {
        // Boşlukları ve çift tırnakları temizle
        videoUrl = videoUrl.trim().replace("\"", "");

        if (videoUrl.contains("v=")) {
            return videoUrl.split("v=")[1].split("&")[0];
        } else if (videoUrl.contains("youtu.be/")) {
            return videoUrl.split("youtu.be/")[1].split("\\?")[0];
        } else {
            throw new IllegalArgumentException("Geçersiz YouTube video linki: " + videoUrl);
        }
    }
}
