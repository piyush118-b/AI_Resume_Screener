package com.example.backend.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class ScoreResponseDto {
    private String status;
    private Double similarity_score_percentage;
    private Double unbiased_score_percentage; // 🌟 NEW: The bias-free score
    private Double placement_probability; // 🌟 NEW: XGBoost Hiring Predictor
    private Double bias_gap; // 🌟 NEW: How much PII warped the result
    private Map<String, List<String>> redacted_items; // 🌟 NEW: What was scrubbed
    private List<String> matched_skills;
    private List<String> missing_skills; // 🌟 NEW: What the candidate is missing
    private List<String> education;
}
