package com.example.backend.service;

import com.example.backend.dto.ExtractionResponseDto;
import com.example.backend.dto.ScoreResponseDto;
import com.example.backend.entity.Job;
import com.example.backend.entity.MatchResult;
import com.example.backend.entity.Resume;
import com.example.backend.entity.User;
import com.example.backend.repository.JobRepository;
import com.example.backend.repository.MatchResultRepository;
import com.example.backend.repository.ResumeRepository;
import com.example.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ResumeOrchestratorService {

    @Autowired
    private MLServiceClient mlServiceClient;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ResumeRepository resumeRepository;

    @Autowired
    private JobRepository jobRepository;

    @Autowired
    private MatchResultRepository matchResultRepository;

    /**
     * This orchestrates the whole flow from the moment the user clicks "Upload"
     * And now it SAVES the results permanently to PostgreSQL!
     */
    public ScoreResponseDto processNewResume(MultipartFile pdfFile, String jobDescriptionText) throws Exception {

        // 1. Send the PDF to our Python brain to extract the text out of it
        ExtractionResponseDto extractionResponse = mlServiceClient.extractTextFromPdf(pdfFile);

        // Make sure it actually worked
        if ("success".equals(extractionResponse.getStatus())) {

            // We successfully pulled the text out.
            String rawText = extractionResponse.getText();

            // 2. Now, pass that raw text AND the job description to the Math part of the AI
            ScoreResponseDto scoreResponse = mlServiceClient.calculateScore(rawText, jobDescriptionText);

            // 🌟 3. NEW STEP: Save everything to our Postgres Database! 🌟

            // We need a dummy user for now since we haven't built out the login page
            User user = userRepository.findByEmail("test@example.com").orElseGet(() -> {
                User dummy = new User();
                dummy.setEmail("test@example.com");
                dummy.setPasswordHash("fakepassword");
                dummy.setRole("APPLICANT");
                return userRepository.save(dummy);
            });

            // Save the Job Requirements
            Job job = new Job();
            job.setTitle("Custom Job Analysis");
            job.setDescription(jobDescriptionText);
            job = jobRepository.save(job);

            // Save the Resume details
            Resume resume = new Resume();
            resume.setUser(user);
            resume.setFilePath("local://" + pdfFile.getOriginalFilename());
            resume.setExtractionStatus("SUCCESS");
            resume.setRawText(rawText);
            resume = resumeRepository.save(resume);

            // Finally, save the Mathematical Match Result!
            MatchResult match = new MatchResult();
            match.setResume(resume);
            match.setJob(job);
            match.setSimilarityScore(scoreResponse.getSimilarity_score_percentage());
            match.setUnbiasedScore(scoreResponse.getUnbiased_score_percentage());
            match.setPlacementProbability(scoreResponse.getPlacement_probability());

            // Try to pack the skills list into a single String (like a fake JSON string)
            // so we can fit it right into the database!
            if (scoreResponse.getMatched_skills() != null) {
                match.setExtractedSkills(String.join(",", scoreResponse.getMatched_skills()));
            }
            matchResultRepository.save(match);

            // 4. Return the final math package to the user!
            return scoreResponse;
        } else {
            throw new Exception("Could not read the PDF file!");
        }
    }
}
