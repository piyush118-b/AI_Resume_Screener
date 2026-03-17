package com.example.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "resumes")
@Data
public class Resume {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(name = "file_path", nullable = false)
    private String filePath;

    @Column(name = "extraction_status")
    private String extractionStatus = "PENDING"; // PENDING, SUCCESS, FAILED

    @Column(name = "raw_text", columnDefinition = "TEXT")
    private String rawText;

    @Column(name = "uploaded_at")
    private LocalDateTime uploadedAt = LocalDateTime.now();
}
