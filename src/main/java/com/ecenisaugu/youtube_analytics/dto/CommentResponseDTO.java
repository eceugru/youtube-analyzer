package com.ecenisaugu.youtube_analytics.dto;

import lombok.Getter;
import lombok.Setter;

// Tek bir yorum için 

@Getter
@Setter
public class CommentResponseDTO {
    // Gereksiz veri taşımamak için frontend'e burada videoId kullanılmadı
    private String author;
    private String text;
    private String sentiment;
    
}
