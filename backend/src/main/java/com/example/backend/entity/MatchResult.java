package com.example.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "match_results")
@Data
public class MatchResult {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "resume_id", nullable = false)
    private Resume resume;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "job_id", nullable = false)
    private Job job;

    @Column(name = "similarity_score")
    private Double similarityScore;

    @Column(name = "unbiased_score")
    private Double unbiasedScore;

    @Column(name = "placement_probability")
    private Double placementProbability;

    @Column(name = "extracted_skills", columnDefinition = "TEXT")
    private String extractedSkills; // JSON array of matched skills

    @Column(name = "matched_at")
    private LocalDateTime matchedAt = LocalDateTime.now();
}
