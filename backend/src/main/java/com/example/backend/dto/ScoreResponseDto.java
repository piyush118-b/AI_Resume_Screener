package com.example.backend.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class ScoreResponseDto {
    private String status;
    private String candidate_name; // 🌟 NEW LLM Output
    private Double similarity_score_percentage;
    private Double unbiased_score_percentage;
    private Double placement_probability;
    private Double bias_gap;
    private Map<String, List<String>> redacted_items;
    private List<String> matched_skills;
    private List<String> missing_skills;
    private List<String> education;
    private List<ExperienceDto> experience; // 🌟 NEW LLM Structured Data

    @Data
    public static class ExperienceDto {
        private String role;
        private String company;
        private String years;
        private List<String> achievements;
    }
}
