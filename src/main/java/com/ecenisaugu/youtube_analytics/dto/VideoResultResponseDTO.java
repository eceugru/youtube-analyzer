package com.ecenisaugu.youtube_analytics.dto;

import java.util.List;

import lombok.Getter;
import lombok.Setter;

// Birleşik veri yapısı (frontend'e göndermek için özetleme ve yorumların birleştirilmesi)

@Getter
@Setter
public class VideoResultResponseDTO {
    private String videoId;
    private String summary;
    private List<CommentResponseDTO> comments;

    private long positiveCount;
    private long negativeCount;
    private long neutralCount;
    
}
