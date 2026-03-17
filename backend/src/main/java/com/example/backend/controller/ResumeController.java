package com.example.backend.controller;

import com.example.backend.dto.ScoreResponseDto;
import com.example.backend.service.ResumeOrchestratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController // This tells Spring Boot: "This file handles Internet Traffic!"
@RequestMapping("/api/v1/resume") // The starting URL for all matching endpoints
public class ResumeController {

    // Give this Controller a "Brain" (The Orchestrator Service we just built)
    @Autowired
    private ResumeOrchestratorService orchestratorService;

    /**
     * The Main internet door!
     * Someone knocks on this door with a PDF file and a Job Description string.
     */
    @PostMapping("/scan")
    public ResponseEntity<ScoreResponseDto> scanAndScoreResume(
            @RequestParam("file") MultipartFile file,
            @RequestParam("job_description") String jobDescription) {

        try {
            // Drop it off into the workflow we built!
            ScoreResponseDto result = orchestratorService.processNewResume(file, jobDescription);

            // Return status code 200 (OK) with the final math!
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            // Something broke (Maybe Python server is offline?)
            e.printStackTrace();
            return ResponseEntity.internalServerError().build(); // Give a 500 error code
        }
    }
}
