package com.ecenisaugu.youtube_analytics.model;

import java.util.List;
import java.util.Map;

public class CommentsSummary {
    private String summary;
    private List<String> selected_sentences;
    private Map<String, Double> scores;

    // Getters and Setters
    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public Map<String, Double> getScores() {
        return scores;
    }

    public void setScores(Map<String, Double> scores) {
        this.scores = scores;
    }

    public List<String> getSelected_sentences() {
        return selected_sentences;
    }

    public void setSelected_sentences(List<String> selected_sentences) {
        this.selected_sentences = selected_sentences;
    }
}
