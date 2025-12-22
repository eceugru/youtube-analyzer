package com.ecenisaugu.youtube_analytics.model.comment;

import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Getter;
import lombok.Setter;

// Collection dan verileri çekip kullanmak için kullanılacak
// burası için bir dto yapmaya gerek yok çünkü tek bir alan var zaten

@Getter
@Setter
@Document(collection = "comments-summary")
public class VideoCommentsSummary {
    private String videoId;
    private String summary;
}
