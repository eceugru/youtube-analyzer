package com.ecenisaugu.youtube_analytics.service;

import com.ecenisaugu.youtube_analytics.dto.VideoDetailsDTO;
import com.ecenisaugu.youtube_analytics.repository.CommentsRepository;
import com.ecenisaugu.youtube_analytics.repository.VideoCommentsSummaryRepository;

public class CommentService {
    private final CommentsRepository commentsRepository;
    private final VideoCommentsSummaryRepository  videoCommentsSummaryRepository;

    public CommentService(CommentsRepository commentsRepository, VideoCommentsSummaryRepository videoCommentsSummaryRepository) {
        this.commentsRepository = commentsRepository;
        this.videoCommentsSummaryRepository = videoCommentsSummaryRepository;
    }

    public VideoDetailsDTO getVideoDetails(String videoUrl) {
        // url'den video id çıkarma işlemleri
        videoUrl = videoUrl.strip().replace('"', '');



        return null;
    }
}
